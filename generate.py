#!/usr/bin/env python3
"""Auto-generate AceDataCloud organization profile README.

Data sources:
  - PlatformBackend/cost/service_api_mapping.json  (service catalog)
  - MCP*/pyproject.toml                            (MCP server packages)
  - GitHub API                                     (API documentation repos)

Usage:
  python generate.py              # local run (fallback list for API doc repos)
  GITHUB_TOKEN=xxx python generate.py   # with GitHub API discovery
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore[no-redefine]

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent
OUTPUT_PATH = SCRIPT_DIR / "profile" / "README.md"

# ── Display name overrides  (alias OR title_key → human-friendly name) ──────
DISPLAY_NAMES: dict[str, str] = {
    "openai": "GPT-4o / o1 / o3",
    "claude": "Claude 4 / 3.5 Sonnet",
    "gemini": "Gemini 2.5 Pro / Flash",
    "grok": "Grok 3",
    "deepseek": "DeepSeek R1 / V3",
    "kimi": "Kimi (Moonshot)",
    "nanobanana": "NanoBanana",
    "nano-banana": "NanoBanana",
    "midjourney": "Midjourney",
    "flux": "Flux",
    "seedream": "Seedream",
    "sora": "Sora",
    "luma": "Luma Dream Machine",
    "veo": "Veo",
    "kling": "Kling",
    "hailuo": "Hailuo (MiniMax)",
    "seedance": "Seedance",
    "wan": "Wan (Alibaba)",
    "suno": "Suno AI",
    "serp": "Google SERP API",
    "fish": "Fish Audio (TTS)",
    "producer": "Producer",
    "qrart": "QR Art",
    "face-change": "Face Swap",
}

# ── Category configuration ──────────────────────────────────────────────────
CATEGORY_ORDER = ["aichat", "aiimage", "aivideo", "aiaudio", "websearch"]
CATEGORY_LABELS: dict[str, str] = {
    "aichat": "**LLM Chat**",
    "aiimage": "**Image Generation**",
    "aivideo": "**Video Generation**",
    "aiaudio": "**Music & Audio**",
    "websearch": "**Web Search**",
}

# Force a service into a specific category (overrides tag-based detection)
CATEGORY_OVERRIDES: dict[str, str] = {
    "serp": "websearch",
}

# Service types to skip entirely
SKIP_TYPES = {"Introduction", "Deployment", "Dataset", "Proxy"}

# Aliases / title keys to skip (internal, infrastructure, or redundant services)
SKIP_ALIASES = {
    "aichat",             # redundant with the LLM Chat services
    "identity",           # internal identity verification
    "shorturl",           # internal URL shortener
    "image2text",         # internal
    "recaptcha",          # captcha service
    "hcaptcha",           # captcha service
    "localization",       # internal
    "face-change",        # niche service
    "adsl",               # proxy infrastructure
    "adsl-http-proxy",    # proxy infrastructure
}
SKIP_TITLE_KEYS = {"identity", "drawai", "aichat"}

# ── GitHub API doc repo display-name overrides ──────────────────────────────
REPO_DISPLAY: dict[str, str] = {
    "GPT4oImageAPI": "GPT4o Image API",
    "GoogleSerpAPI": "Google SERP API",
    "NanoBananaAPI": "NanoBanana API",
}

# Fallback list when GitHub API is unavailable
FALLBACK_API_DOC_REPOS = [
    ("DeepSeek API", "DeepSeekAPI"),
    ("Flux API", "FluxAPI"),
    ("GPT4o Image API", "GPT4oImageAPI"),
    ("Google SERP API", "GoogleSerpAPI"),
    ("Hailuo API", "HailuoAPI"),
    ("Kling API", "KlingAPI"),
    ("Luma API", "LumaAPI"),
    ("Midjourney API", "MidjourneyAPI"),
    ("NanoBanana API", "NanoBananaAPI"),
    ("OpenAI API", "OpenAIAPI"),
    ("Pika API", "PikaAPI"),
    ("Pixverse API", "PixverseAPI"),
    ("Sora API", "SoraAPI"),
    ("Suno API", "SunoAPI"),
    ("Veo API", "VeoAPI"),
]


# ── Helpers ─────────────────────────────────────────────────────────────────

def _title_key(title: str) -> str | None:
    """Extract the key from a $t(service_title_xxx) string."""
    m = re.match(r"\$t\(service_title_(\w+)\)", title)
    return m.group(1) if m else None


def _display_name(alias: str, title: str) -> str:
    """Resolve a human-friendly display name for a service."""
    # Try alias
    if alias and alias in DISPLAY_NAMES:
        return DISPLAY_NAMES[alias]
    # Try title key
    key = _title_key(title)
    if key and key in DISPLAY_NAMES:
        return DISPLAY_NAMES[key]
    # Auto-format from key or alias
    base = key or alias or "Unknown"
    return base.replace("_", " ").replace("-", " ").title()


def _repo_display_name(repo_name: str) -> str:
    """Convert a GitHub repo name like 'MidjourneyAPI' to 'Midjourney API'."""
    if repo_name in REPO_DISPLAY:
        return REPO_DISPLAY[repo_name]
    if repo_name.endswith("API"):
        return repo_name[:-3] + " API"
    return repo_name


# ── Data loaders ────────────────────────────────────────────────────────────

def load_services() -> tuple[dict[str, list[str]], list[str]]:
    """Load services from service_api_mapping.json, grouped by category."""
    mapping_path = WORKSPACE_ROOT / "PlatformBackend" / "cost" / "service_api_mapping.json"
    if not mapping_path.exists():
        print(f"Warning: {mapping_path} not found", file=sys.stderr)
        return {cat: [] for cat in CATEGORY_ORDER}, []

    with open(mapping_path) as f:
        services = json.load(f)

    categories: dict[str, list[str]] = {cat: [] for cat in CATEGORY_ORDER}
    other: list[str] = []

    for svc in sorted(services, key=lambda s: s.get("rank", 0)):
        if svc.get("private"):
            continue
        if svc.get("type", "") in SKIP_TYPES:
            continue

        alias = svc.get("alias", "")
        title = svc.get("title", "")
        tags = svc.get("tags") or []

        # Skip internal / infrastructure services
        if alias in SKIP_ALIASES:
            continue
        key = _title_key(title)
        if key and key in SKIP_TITLE_KEYS:
            continue

        name = _display_name(alias, title)

        # Category override?
        override_key = alias or key or ""
        if override_key in CATEGORY_OVERRIDES:
            cat = CATEGORY_OVERRIDES[override_key]
            if cat in categories and name not in categories[cat]:
                categories[cat].append(name)
            continue

        # Assign to first matching tag-based category
        placed = False
        for tag in tags:
            if tag in categories:
                if name not in categories[tag]:
                    categories[tag].append(name)
                placed = True
                break

        if not placed and svc.get("type") in ("Api", "Proxy"):
            if name not in other:
                other.append(name)

    return categories, other


def discover_mcp_servers() -> list[dict[str, str]]:
    """Discover MCP servers from MCP*/pyproject.toml in the workspace."""
    servers = []
    for mcp_dir in sorted(WORKSPACE_ROOT.glob("MCP*")):
        pyproject = mcp_dir / "pyproject.toml"
        if not pyproject.exists():
            continue
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)
        project = data.get("project", {})
        pkg_name = project.get("name", "")
        desc = project.get("description", "")
        if not pkg_name:
            continue
        # Clean up description for table display
        short_desc = (
            desc.replace("MCP Server for ", "")
            .replace(" via AceDataCloud API", "")
        )
        servers.append(
            {"dir_name": mcp_dir.name, "package_name": pkg_name, "description": short_desc}
        )
    return servers


def discover_api_doc_repos() -> list[tuple[str, str]]:
    """Discover *API repos from GitHub API, falling back to hardcoded list."""
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("GITHUB_TOKEN not set — using fallback API doc repos list", file=sys.stderr)
        return FALLBACK_API_DOC_REPOS

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "AceDataCloud-Profile-Generator",
    }
    repos: list[tuple[str, str]] = []
    page = 1
    try:
        while True:
            url = (
                f"https://api.github.com/orgs/AceDataCloud/repos"
                f"?per_page=100&page={page}&type=public"
            )
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
            for repo in data:
                name = repo["name"]
                if name.endswith("API") and not repo.get("archived") and not repo.get("fork"):
                    repos.append((_repo_display_name(name), name))
            if len(data) < 100:
                break
            page += 1
    except (urllib.error.URLError, OSError) as exc:
        print(f"Warning: GitHub API error ({exc}), using fallback list", file=sys.stderr)
        return FALLBACK_API_DOC_REPOS

    return sorted(repos) if repos else FALLBACK_API_DOC_REPOS


# ── README generation ───────────────────────────────────────────────────────

def generate_readme() -> str:
    categories, other_services = load_services()
    mcp_servers = discover_mcp_servers()
    api_doc_repos = discover_api_doc_repos()

    # Services table
    svc_rows = []
    for cat in CATEGORY_ORDER:
        names = categories.get(cat, [])
        if names:
            svc_rows.append(f"| {CATEGORY_LABELS[cat]} | {', '.join(names)} |")
    if other_services:
        svc_rows.append(f"| **More** | {', '.join(other_services)} |")
    services_table = (
        "| Category | Services |\n|----------|----------|\n" + "\n".join(svc_rows)
    )

    # MCP table
    mcp_rows = []
    pkg_names = []
    for srv in mcp_servers:
        dn, pn, desc = srv["dir_name"], srv["package_name"], srv["description"]
        mcp_rows.append(
            f"| [{dn}](https://github.com/AceDataCloud/{dn}) "
            f"| [![PyPI](https://img.shields.io/pypi/v/{pn}?style=flat-square)]"
            f"(https://pypi.org/project/{pn}/) "
            f"| {desc} |"
        )
        pkg_names.append(pn)
    mcp_table = (
        "| Server | PyPI | Description |\n|--------|------|-------------|\n"
        + "\n".join(mcp_rows)
    )
    pip_cmd = " ".join(pkg_names)

    # API docs links
    doc_links = " · ".join(
        f"[{display}](https://github.com/AceDataCloud/{repo})"
        for display, repo in api_doc_repos
    )

    # Assemble final README
    return f"""\
<div align="center">

<img src="https://cdn.acedata.cloud/acedatacloud.png" alt="Ace Data Cloud" width="120" />

# Ace Data Cloud

**Unified AI API Platform — One Key, Hundreds of AI Models**

Access GPT-4o, Claude, Gemini, Grok, DeepSeek, Midjourney, Suno, Luma, Sora, and 100+ more AI services through a single, OpenAI-compatible API.

[![Platform](https://img.shields.io/badge/Platform-platform.acedata.cloud-blue?style=flat-square)](https://platform.acedata.cloud)
[![API Docs](https://img.shields.io/badge/API_Docs-docs.acedata.cloud-green?style=flat-square)](https://docs.acedata.cloud)
[![Nexior](https://img.shields.io/badge/Nexior_App-hub.acedata.cloud-orange?style=flat-square)](https://hub.acedata.cloud)
[![Status](https://img.shields.io/badge/Status-status.acedata.cloud-brightgreen?style=flat-square)](https://status.acedata.cloud)

</div>

---

## 🚀 What We Do

Ace Data Cloud provides a **unified API gateway** to access the world's leading AI models and services. Instead of managing multiple API keys, rate limits, and SDKs, developers use **one API key** to access everything:

{services_table}

## 🔌 MCP Servers (Model Context Protocol)

We publish official MCP servers so AI assistants (Claude, Cursor, Windsurf, etc.) can use our APIs as tools:

{mcp_table}

Install any server with one command:

```bash
pip install {pip_cmd}
```

## 📚 API Documentation Repos

Detailed API references with request/response examples for each service:

{doc_links}

## 🌐 Live Services

| Service | URL | Description |
|---------|-----|-------------|
| **Developer Platform** | [platform.acedata.cloud](https://platform.acedata.cloud) | API keys, docs, billing, analytics |
| **API Gateway** | [api.acedata.cloud](https://api.acedata.cloud) | OpenAI-compatible REST API endpoint |
| **Nexior** | [hub.acedata.cloud](https://hub.acedata.cloud) | Consumer app — chat, generate images/video/music |
| **Documentation** | [docs.acedata.cloud](https://docs.acedata.cloud) | Quickstart guides and API references |
| **Dify AI** | [dify.acedata.cloud](https://dify.acedata.cloud) | Visual AI workflow builder |
| **Status** | [status.acedata.cloud](https://status.acedata.cloud) | Real-time service health monitoring |
| **Roadmap** | [roadmap.acedata.cloud](https://roadmap.acedata.cloud) | Public feature roadmap |

## ⚡ Quick Start

```bash
# Chat with any LLM — OpenAI-compatible
curl https://api.acedata.cloud/v1/chat/completions \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{{"model": "gpt-4o", "messages": [{{"role": "user", "content": "Hello!"}}]}}'
```

Get your API key at [platform.acedata.cloud](https://platform.acedata.cloud) — free tier available.

## 💰 $ACE Token

The [$ACE token](https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump) on Solana powers our ecosystem. Stake $ACE to unlock API call discounts.

## 📬 Connect

- 🌐 [Website](https://platform.acedata.cloud)
- 📖 [Documentation](https://docs.acedata.cloud)
- 🐦 [Twitter / X](https://x.com/AceDataCloud)
- 💬 [Discord](https://discord.gg/aedatacloud)
"""


def main():
    readme = generate_readme()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if OUTPUT_PATH.exists() and OUTPUT_PATH.read_text() == readme:
        print("Profile README is already up to date.")
        return

    OUTPUT_PATH.write_text(readme)
    print(f"Updated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
