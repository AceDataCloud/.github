#!/usr/bin/env python3
"""Auto-generate AceDataCloud organization profile README using LLM.

Collects metadata from multiple sources, feeds it to an LLM, and generates
a comprehensive, accurate organization profile README.

Data sources:
  - GitHub API               (all public repos: name, description, stars, topics)
  - service_api_mapping.json  (service catalog from PlatformBackend submodule)
  - MCP*/pyproject.toml       (MCP server package names and descriptions)

Environment variables:
  ACEDATACLOUD_OPENAI_KEY  - API key for api.acedata.cloud (OpenAI-compatible)
  GITHUB_TOKEN             - GitHub token for listing org repos
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = SCRIPT_DIR / "profile" / "README.md"

OPENAI_BASE_URL = "https://api.acedata.cloud/v1"
OPENAI_MODEL = "gpt-4.1-mini"


def fetch_github_repos(token: str) -> list[dict]:
    """Fetch all public non-archived non-fork repos from AceDataCloud org."""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "AceDataCloud-Profile-Generator",
    }
    all_repos: list[dict] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/orgs/AceDataCloud/repos"
            f"?per_page=100&page={page}&type=public"
        )
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        for repo in data:
            if repo.get("archived") or repo.get("fork"):
                continue
            all_repos.append(
                {
                    "name": repo["name"],
                    "description": repo.get("description") or "",
                    "html_url": repo["html_url"],
                    "homepage": repo.get("homepage") or "",
                    "stars": repo.get("stargazers_count", 0),
                    "topics": repo.get("topics", []),
                    "language": repo.get("language") or "",
                }
            )
        if len(data) < 100:
            break
        page += 1
    return sorted(all_repos, key=lambda r: r["name"])


SKIP_ALIASES = {"aichat", "shorturl", "localization"}
SKIP_CATEGORIES = {"CAPTCHA", "Proxy", "Identity"}
SKIP_TYPES = {"Dataset", "Deployment", "Proxy", "Introduction", "Agent"}
SKIP_TAGS = {"captcha", "proxy", "identity"}

# Map tag values to canonical category names
TAG_TO_CATEGORY = {
    "aichat": "AI Chat",
    "aiimage": "AI Image",
    "aivideo": "AI Video",
    "aiaudio": "AI Audio",
}


def _derive_category(svc: dict) -> str:
    """Derive category from explicit field or tags."""
    cat = svc.get("category", "")
    if cat:
        return cat
    for tag in svc.get("tags", []):
        if tag in TAG_TO_CATEGORY:
            return TAG_TO_CATEGORY[tag]
    return "Web & Data"


def _derive_display_name(svc: dict) -> str:
    """Derive display name from explicit field or alias."""
    name = svc.get("display_name", "")
    if name:
        return name
    alias = svc.get("alias", "")
    return alias.replace("-", " ").title()


def load_service_mapping(workspace_root: Path) -> list[dict]:
    """Load the public service catalog from service_api_mapping.json.

    Pre-filters to only include user-facing AI/data services with APIs.
    """
    mapping_path = (
        workspace_root / "PlatformBackend" / "cost" / "service_api_mapping.json"
    )
    if not mapping_path.exists():
        print(f"Warning: {mapping_path} not found", file=sys.stderr)
        return []
    with open(mapping_path) as f:
        services = json.load(f)
    result = []
    for svc in services:
        if svc.get("private"):
            continue
        if svc.get("type", "") in SKIP_TYPES:
            continue
        alias = svc.get("alias", "")
        if alias in SKIP_ALIASES:
            continue
        category = _derive_category(svc)
        if category in SKIP_CATEGORIES:
            continue
        tags = set(svc.get("tags") or [])
        if tags & SKIP_TAGS:
            continue
        raw_apis = svc.get("apis", [])
        if not raw_apis:
            continue
        apis = []
        for a in raw_apis:
            apis.append(
                {
                    "name": a.get("name", ""),
                    "path": a.get("path", ""),
                    "stage": a.get("stage", ""),
                }
            )
        result.append(
            {
                "alias": alias,
                "display_name": _derive_display_name(svc),
                "type": svc.get("type", ""),
                "tags": list(tags),
                "category": category,
                "apis": apis,
            }
        )
    return sorted(result, key=lambda s: s.get("rank", 0))


def discover_mcp_servers(workspace_root: Path) -> list[dict]:
    """Discover MCP servers from MCP*/pyproject.toml files."""
    try:
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            try:
                import tomllib  # type: ignore[import]
            except ImportError:
                import tomli as tomllib  # type: ignore[import,no-redef]
    except ImportError:
        print("Warning: tomllib/tomli not available", file=sys.stderr)
        return []

    servers = []
    for mcp_dir in sorted(workspace_root.glob("MCP*")):
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
        # Strip common boilerplate from descriptions
        for prefix in ("MCP Server for ", "MCP Server of "):
            if desc.startswith(prefix):
                desc = desc[len(prefix) :]
                break
        for suffix in (" via AceDataCloud API", " via Ace Data Cloud API"):
            if desc.endswith(suffix):
                desc = desc[: -len(suffix)]
                break
        servers.append(
            {
                "dir_name": mcp_dir.name,
                "package_name": pkg_name,
                "description": desc,
            }
        )
    return servers


def call_llm(system_prompt: str, user_prompt: str, api_key: str) -> str:
    """Call the OpenAI-compatible API at api.acedata.cloud."""
    url = f"{OPENAI_BASE_URL}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 8192,
    }

    print(f"\n{'=' * 60}", file=sys.stderr)
    print("LLM REQUEST", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)
    print(f"  URL:         {url}", file=sys.stderr)
    print(f"  Model:       {OPENAI_MODEL}", file=sys.stderr)
    print(f"  Temperature: {payload['temperature']}", file=sys.stderr)
    print(f"  Max tokens:  {payload['max_tokens']}", file=sys.stderr)
    print(f"\n  System prompt ({len(system_prompt)} chars):", file=sys.stderr)
    print(
        f"  {system_prompt[:500]}{'...' if len(system_prompt) > 500 else ''}",
        file=sys.stderr,
    )
    print(f"\n  User prompt ({len(user_prompt)} chars):", file=sys.stderr)
    print(
        f"  {user_prompt[:2000]}{'...' if len(user_prompt) > 2000 else ''}",
        file=sys.stderr,
    )
    print(f"{'=' * 60}", file=sys.stderr)

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())

    content = data["choices"][0]["message"]["content"].strip()
    usage = data.get("usage", {})

    print(f"\n{'=' * 60}", file=sys.stderr)
    print("LLM RESPONSE", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)
    if usage:
        print(
            f"  Prompt tokens:     {usage.get('prompt_tokens', 'N/A')}", file=sys.stderr
        )
        print(
            f"  Completion tokens: {usage.get('completion_tokens', 'N/A')}",
            file=sys.stderr,
        )
        print(
            f"  Total tokens:      {usage.get('total_tokens', 'N/A')}", file=sys.stderr
        )
    print(f"  Response length:   {len(content)} chars", file=sys.stderr)
    print(f"\n  Full response:", file=sys.stderr)
    print(content, file=sys.stderr)
    print(f"{'=' * 60}\n", file=sys.stderr)

    return content


SYSTEM_PROMPT = """\
You are a designer generating a GitHub organization profile README for \
Ace Data Cloud (AceDataCloud). Output ONLY raw Markdown — no ```markdown fences, \
no explanations, no preamble.

GOAL: A clean, impressive landing page. Think "startup homepage", not a data dump. \
Show what the platform can do at a glance, with links to learn more.

STRUCTURE (keep this exact order):

1. **Header** (<div align="center">):
   - <img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />
   - <h1>Ace Data Cloud</h1>
   - <b>Unified AI API Platform — One Key, Hundreds of AI Models</b>
   - A short tagline paragraph (1 sentence, normal text, describing what the platform does)
   - Badges (HTML <a><img>, shields.io style=flat-square):
     Platform (blue → platform.acedata.cloud), API Docs (green → docs.acedata.cloud),
     Nexior App (orange → hub.acedata.cloud), Status (brightgreen → status.acedata.cloud)
   - Close </div> then --- horizontal rule.

2. **## What We Do** — 2-3 sentences, confident and concise. \
   Then a single Markdown TABLE with 2 columns: Category | Services. \
   Rows: LLM Chat, Image Generation, Video Generation, Music & Audio, Web Search. \
   In the "Services" column, list CLEAN BRAND NAMES separated by commas. \
   MANDATORY brand name cleanup (apply these rules to display_name from data):
   - "OpenAI generation" → "GPT / DALL·E / Sora"
   - "Gemini AI" → "Gemini"
   - "Claude AI" → "Claude"
   - "DeepSeek AI" → "DeepSeek"
   - "ByteDance Seedream Image Generation" → "Seedream"
   - "ByteDance Seedance Video Generation" → "Seedance"
   - "Nano Banana Image Generation" → "NanoBanana"
   - "Flux Image Generation" → "Flux"
   - "Midjourney generation" → "Midjourney"
   - "Art QR Code Generation" → "QR Art"
   - "Face Transformation" → "Face Transform"
   - "Sora Video Generation" → "Sora"
   - "Veo Video Generation" → "Veo"
   - "Kling video generation" → "Kling"
   - "Tongyi Wansiang Video Generation" → "Wan (Alibaba)"
   - "Luma Video Generation" → "Luma"
   - "Hailuo Video Generation" → "Hailuo"
   - "Pixverse AI video generation" → "Pixverse"
   - "Suno Music Generation" → "Suno"
   - "Fish music generation" → "Fish Audio"
   - "Producer Music Generation" → "Producer"
   - "Search Engine" → "Google SERP"
   - For anything else, strip "Generation", "AI", trailing noise — keep just the brand.
   Keep it clean — just brand names, no endpoints, no stages, no emojis in cells. \
   After the table: "**Browse all services →** [platform.acedata.cloud](https://platform.acedata.cloud)"

3. **## MCP Servers** — One intro sentence about MCP (Model Context Protocol) \
   letting AI assistants use these APIs as tools. Then a table:
   | Server | PyPI | Description |
   - Server: link to `github.com/AceDataCloud/{dir_name}`
   - PyPI: badge [![PyPI](https://img.shields.io/pypi/v/{package_name}?style=flat-square)](https://pypi.org/project/{package_name}/)
   - Description: from the data as-is
   After table: ```pip install {all package names}```

4. **## API Documentation** — One intro sentence, then inline dot-separated links. \
   Include ONLY GitHub repos whose name ends with "API" \
   (e.g. FluxAPI, SunoAPI). Display: split CamelCase → "Flux API". \
   Also link to [Full Documentation](https://docs.acedata.cloud) at the end.

5. **## Live Services** — Table with columns: Service | Description. \
   The Service column MUST be a Markdown link: [Name](https://url). Rows:
   - [Developer Platform](https://platform.acedata.cloud) | API keys, docs, billing, analytics
   - [API Gateway](https://api.acedata.cloud) | OpenAI-compatible REST API endpoint
   - [Nexior](https://hub.acedata.cloud) | Consumer app — chat, generate images, video, music
   - [Documentation](https://docs.acedata.cloud) | Quickstart guides and API references
   - [Dify AI](https://dify.acedata.cloud) | Visual AI workflow builder
   - [Status](https://status.acedata.cloud) | Real-time service health monitoring
   - [Roadmap](https://roadmap.acedata.cloud) | Public feature roadmap

6. **## Quick Start** — curl to `/v1/chat/completions`, Bearer YOUR_API_KEY, \
   model gpt-4o. Then: \
   "Get your API key at [platform.acedata.cloud](https://platform.acedata.cloud) — free tier available."

7. **## $ACE Token** — 1-2 sentences with link: \
   https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump

8. **## Connect** — Bullet list:
   - Website: [platform.acedata.cloud](https://platform.acedata.cloud)
   - Documentation: [docs.acedata.cloud](https://docs.acedata.cloud)
   - Twitter / X: [x.com/AceDataCloud](https://x.com/AceDataCloud)
   - Discord: [discord.gg/aedatacloud](https://discord.gg/aedatacloud)

STYLE RULES:
- Section headers: ## only, NO emojis in headers. Clean and professional.
- Use ONLY data I provide. NEVER invent services or descriptions.
- No trailing whitespace. End file with a single newline.
- Keep the whole README under 120 lines. Brevity is elegance.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate organization profile README")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=SCRIPT_DIR.parent,
        help="Root of the Index workspace containing PlatformBackend/ and MCP*/ submodules",
    )
    args = parser.parse_args()
    workspace_root = args.workspace.resolve()

    api_key = os.environ.get("ACEDATACLOUD_OPENAI_KEY", "")
    github_token = os.environ.get("GITHUB_TOKEN", "")

    if not api_key:
        print("Error: ACEDATACLOUD_OPENAI_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Collect data from all sources
    print(f"\nWorkspace root: {workspace_root}", file=sys.stderr)
    print(f"Output path:    {OUTPUT_PATH}", file=sys.stderr)

    print("\n[1/3] Collecting GitHub repos...", file=sys.stderr)
    repos: list[dict] = []
    if github_token:
        try:
            repos = fetch_github_repos(github_token)
            print(f"  Found {len(repos)} public repos", file=sys.stderr)
            for r in repos:
                stars = f" ★{r['stars']}" if r["stars"] else ""
                print(
                    f"    - {r['name']}: {r['description'][:80]}{stars}",
                    file=sys.stderr,
                )
        except Exception as e:
            print(f"  Warning: GitHub API error: {e}", file=sys.stderr)
    else:
        print("  GITHUB_TOKEN not set, skipping repo discovery", file=sys.stderr)

    print("\n[2/3] Loading service catalog...", file=sys.stderr)
    services = load_service_mapping(workspace_root)
    print(f"  Found {len(services)} public services", file=sys.stderr)
    for svc in services:
        print(
            f"    - {svc['alias']} ({svc['type']}, display_name={svc.get('display_name', '')}, category={svc.get('category', '')}, apis={len(svc.get('apis', []))}, tags={svc.get('tags', [])})",
            file=sys.stderr,
        )

    print("\n[3/3] Discovering MCP servers...", file=sys.stderr)
    mcp_servers = discover_mcp_servers(workspace_root)
    print(f"  Found {len(mcp_servers)} MCP servers", file=sys.stderr)
    for s in mcp_servers:
        print(
            f"    - {s['dir_name']}: {s['package_name']} — {s['description']}",
            file=sys.stderr,
        )

    # Build user prompt with all collected data
    user_prompt = "Generate the organization profile README using this real data:\n\n"

    # Pre-compute summary stats for the LLM
    if services:
        total_endpoints = sum(len(s.get("apis", [])) for s in services)
        categories = sorted(set(s.get("category", "Other") for s in services))
        user_prompt += "## Summary Stats (use these exact numbers)\n"
        user_prompt += f"- Total services: {len(services)}\n"
        user_prompt += f"- Total API endpoints: {total_endpoints}\n"
        user_prompt += f"- Categories ({len(categories)}): {', '.join(categories)}\n\n"

    if repos:
        user_prompt += "## GitHub Repositories (public, non-archived, non-fork)\n"
        user_prompt += json.dumps(repos, indent=2) + "\n\n"

    if services:
        user_prompt += "## Service Catalog (pre-filtered, sorted by rank)\n"
        user_prompt += json.dumps(services, indent=2) + "\n\n"

    if mcp_servers:
        user_prompt += "## MCP Servers (from pyproject.toml files)\n"
        user_prompt += json.dumps(mcp_servers, indent=2) + "\n\n"

    # Call LLM to generate the README
    print("Calling LLM to generate README...", file=sys.stderr)
    readme = call_llm(SYSTEM_PROMPT, user_prompt, api_key)

    # Strip markdown fences if the LLM wraps output despite instructions
    if readme.startswith("```"):
        lines = readme.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        readme = "\n".join(lines)

    if not readme.endswith("\n"):
        readme += "\n"

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(readme)
    print(f"Updated: {OUTPUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
