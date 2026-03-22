#!/usr/bin/env python3
"""Auto-generate AceDataCloud organization profile README.

Collects metadata from multiple sources and renders a deterministic organization
profile README. An optional LLM path is kept for experimentation.

Data sources:
  - GitHub API               (all public repos: name, description, stars, topics)
  - service_api_mapping.json  (service catalog from PlatformBackend submodule)
  - MCP*/pyproject.toml       (MCP server package names and descriptions)

Environment variables:
    GITHUB_TOKEN             - GitHub token for listing org repos
    ACEDATACLOUD_OPENAI_KEY  - Optional API key for the legacy --use-llm mode
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import certifi
except ImportError:  # pragma: no cover - optional runtime dependency
    certifi = None

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = SCRIPT_DIR / "profile" / "README.md"

OPENAI_BASE_URL = "https://api.acedata.cloud/v1"
OPENAI_MODEL = "gpt-4.1-mini"


def build_ssl_context() -> ssl.SSLContext:
    """Create an SSL context that works reliably on local macOS Python installs."""
    if certifi is not None:
        return ssl.create_default_context(cafile=certifi.where())
    return ssl.create_default_context()


SSL_CONTEXT = build_ssl_context()


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
        with urllib.request.urlopen(req, timeout=30, context=SSL_CONTEXT) as resp:
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
    with urllib.request.urlopen(req, timeout=120, context=SSL_CONTEXT) as resp:
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
    print("\n  Full response:", file=sys.stderr)
    print(content, file=sys.stderr)
    print(f"{'=' * 60}\n", file=sys.stderr)

    return content


SERVICE_CATEGORY_ORDER = [
    "AI Chat",
    "AI Image",
    "AI Video",
    "AI Audio",
    "Web & Data",
]

SERVICE_CATEGORY_LABELS = {
    "AI Chat": "LLM Chat",
    "AI Image": "Image Generation",
    "AI Video": "Video Generation",
    "AI Audio": "Music & Audio",
    "Web & Data": "Web Search",
}

FEATURED_REPO_ORDER = [
    ".github",
    "Docs",
    "VSCodeMCP",
    "Skills",
    "Nexior",
    "Dify",
    "FacilitatorX402",
]

FEATURED_REPO_PURPOSE = {
    ".github": "Organization profile and GitHub entry point for Ace Data Cloud's AI API and MCP ecosystem",
    "Docs": "Global API documentation, quickstart guides, and OpenAPI references for Ace Data Cloud services",
    "Skills": "Agent Skills repository for Claude Code, GitHub Copilot, Gemini CLI, OpenHands, Roo Code, and other coding agents",
    "VSCodeMCP": "VS Code extension that bundles Ace Data Cloud MCP servers for developer workflows",
    "PlatformBackend": "Core backend for service catalog, billing, applications, credentials, orders, and platform APIs",
    "PlatformFrontend": "Developer portal for API docs, pricing, credentials, and service management",
    "Nexior": "Consumer AI application for chat, image generation, video generation, and music creation",
    "Dify": "Ace Data Cloud fork of Dify with OAuth login, model auto-provisioning, and plugin integration",
    "FacilitatorX402": "X402 payment facilitator for AI API billing with Solana USDC and Base USDC support",
}

LIVE_SERVICES = [
    ("Developer Platform", "https://platform.acedata.cloud", "API keys, docs, billing, analytics"),
    ("API Gateway", "https://api.acedata.cloud", "OpenAI-compatible REST API endpoint"),
    ("Nexior", "https://hub.acedata.cloud", "Consumer app - chat, generate images, video, music"),
    ("Documentation", "https://docs.acedata.cloud", "Quickstart guides and API references"),
    ("Dify AI", "https://dify.acedata.cloud", "Visual AI workflow builder"),
    ("Status", "https://status.acedata.cloud", "Real-time service health monitoring"),
    ("Roadmap", "https://roadmap.acedata.cloud", "Public feature roadmap"),
]

AGENT_SURFACES = [
    (
        "Agent Skills",
        "https://github.com/AceDataCloud/Skills",
        "18 reusable skills for 15+ coding agents including Claude Code, GitHub Copilot, Gemini CLI, OpenHands, Roo Code, and TRAE",
    ),
    (
        "VS Code MCP Extension",
        "https://github.com/AceDataCloud/VSCodeMCP",
        "Marketplace-ready VS Code extension bundling 11 hosted and local MCP server integrations for Copilot Chat",
    ),
]

def clean_brand_name(display_name: str) -> str:
    """Normalize service names for the public category table."""
    replacements = {
        "OpenAI generation": "GPT / DALL·E / Sora",
        "Gemini AI": "Gemini",
        "Claude AI": "Claude",
        "DeepSeek AI": "DeepSeek",
        "ByteDance Seedream Image Generation": "Seedream",
        "ByteDance Seedance Video Generation": "Seedance",
        "Nano Banana Image Generation": "NanoBanana",
        "Flux Image Generation": "Flux",
        "Midjourney generation": "Midjourney",
        "Art QR Code Generation": "QR Art",
        "Face Transformation": "Face Transform",
        "Sora Video Generation": "Sora",
        "Veo Video Generation": "Veo",
        "Kling video generation": "Kling",
        "Tongyi Wansiang Video Generation": "Wan (Alibaba)",
        "Luma Video Generation": "Luma",
        "Hailuo Video Generation": "Hailuo",
        "Pixverse AI video generation": "Pixverse",
        "Suno Music Generation": "Suno",
        "Fish music generation": "Fish Audio",
        "Producer Music Generation": "Producer",
        "Search Engine": "Google SERP",
    }
    if display_name in replacements:
        return replacements[display_name]

    name = display_name.replace("Generation", "").replace("generation", "")
    name = name.replace("AI", "").replace("  ", " ").strip(" -")
    return name.strip()


def build_service_rows(services: list[dict]) -> list[tuple[str, str]]:
    """Build service category rows in a stable order."""
    grouped: dict[str, list[str]] = {key: [] for key in SERVICE_CATEGORY_ORDER}
    for service in services:
        category = service.get("category", "Web & Data")
        if category not in grouped:
            continue
        brand = clean_brand_name(service.get("display_name", service.get("alias", "")))
        if brand and brand not in grouped[category]:
            grouped[category].append(brand)

    rows = []
    for category in SERVICE_CATEGORY_ORDER:
        labels = grouped[category]
        if not labels:
            continue
        rows.append((SERVICE_CATEGORY_LABELS[category], ", ".join(labels)))
    return rows


def split_camel_case(name: str) -> str:
    """Convert CamelCase repo names to spaced labels."""
    special_cases = {
        "OpenAIAPI": "OpenAI API",
    }
    if name in special_cases:
        return special_cases[name]

    chars: list[str] = []
    for index, char in enumerate(name):
        if index > 0 and char.isupper() and not name[index - 1].isupper():
            chars.append(" ")
        chars.append(char)
    return "".join(chars)


def build_featured_repos(repos: list[dict]) -> list[dict]:
    """Select a stable set of public featured repositories."""
    repo_map = {repo["name"]: repo for repo in repos}
    featured = []
    for repo_name in FEATURED_REPO_ORDER:
        repo = repo_map.get(repo_name)
        if not repo:
            continue
        featured.append(
            {
                "name": repo_name,
                "url": repo["html_url"],
                "purpose": FEATURED_REPO_PURPOSE[repo_name],
            }
        )
    return featured


def build_api_doc_links(repos: list[dict]) -> list[str]:
    """Build inline documentation links from public API repos."""
    api_repos = sorted(
        (repo for repo in repos if repo["name"].endswith("API")),
        key=lambda repo: repo["name"],
    )
    links = []
    for repo in api_repos:
        label = split_camel_case(repo["name"])
        links.append(f"[{label}]({repo['html_url']})")
    return links


def render_readme(repos: list[dict], services: list[dict], mcp_servers: list[dict]) -> str:
    """Render the organization profile README deterministically."""
    lines = [
        "# Ace Data Cloud",
        "",
        "![Ace Data Cloud](https://cdn.acedata.cloud/logo.png/thumb_450x_)",
        "",
        "[![Platform](https://img.shields.io/badge/platform-blue?style=flat-square)](https://platform.acedata.cloud) [![API Docs](https://img.shields.io/badge/API%20Docs-green?style=flat-square)](https://docs.acedata.cloud) [![Nexior App](https://img.shields.io/badge/Nexior%20App-orange?style=flat-square)](https://hub.acedata.cloud) [![Status](https://img.shields.io/badge/Status-brightgreen?style=flat-square)](https://status.acedata.cloud)",
        "",
        "**Unified AI API Platform for Developers, AI Agents, and MCP Tools.**",
        "",
        "Ship chat, image, video, music, search, and automation workflows globally through one API key, one billing system, and one developer platform.",
        "",
        "---",
        "",
        "## What We Do",
        "",
        "Ace Data Cloud is a developer-first AI infrastructure platform. We make it practical to integrate leading AI APIs, MCP servers, and open workflows without juggling separate vendors, fragmented billing, or per-service auth.",
        "",
        "## Why Developers Use Ace Data Cloud",
        "",
        "- One API key for multiple AI providers and model families",
        "- OpenAI-compatible API gateway for fast integration",
        "- Production-ready APIs for image generation, video generation, music generation, chat, search, and automation",
        "- 18-language documentation and global-ready developer onboarding",
        "- MCP servers for Copilot, Claude, Cursor, VS Code, and other AI assistants",
        "- Billing, usage tracking, and developer tooling in one place",
        "",
        "| Category | Services |",
        "| --- | --- |",
    ]

    for category, service_names in build_service_rows(services):
        lines.append(f"| {category} | {service_names} |")

    lines.extend(
        [
            "",
            "**Browse all services →** [platform.acedata.cloud](https://platform.acedata.cloud)",
            "",
            "## Featured Repositories",
            "",
            "| Repository | Purpose |",
            "| --- | --- |",
        ]
    )

    for repo in build_featured_repos(repos):
        lines.append(f"| [{repo['name']}]({repo['url']}) | {repo['purpose']} |")

    lines.extend(
        [
            "",
            "## Agent Surfaces",
            "",
            "Ace Data Cloud ships both reusable agent knowledge and executable MCP tooling for modern coding assistants.",
            "",
            "| Surface | Purpose |",
            "| --- | --- |",
        ]
    )

    for name, url, purpose in AGENT_SURFACES:
        lines.append(f"| [{name}]({url}) | {purpose} |")

    lines.extend(
        [
            "",
            "## MCP Servers",
            "",
            "Our MCP (Model Context Protocol) servers let AI assistants use these APIs as powerful tools.",
            "",
            "| Server | PyPI | Description |",
            "| --- | --- | --- |",
        ]
    )

    for server in mcp_servers:
        package_name = server["package_name"]
        lines.append(
            "| "
            f"[{server['dir_name']}](https://github.com/AceDataCloud/{server['dir_name']}) | "
            f"[![PyPI](https://img.shields.io/pypi/v/{package_name}?style=flat-square)](https://pypi.org/project/{package_name}/) | "
            f"{server['description']} |"
        )

    install_packages = " ".join(server["package_name"] for server in mcp_servers)
    lines.extend(
        [
            "",
            "```bash",
            f"pip install {install_packages}",
            "```",
            "",
            "Use our MCP servers with GitHub Copilot, Claude Desktop, Cursor, Windsurf, and other MCP-compatible clients.",
            "",
            "## API Documentation",
            "",
        ]
    )

    api_links = build_api_doc_links(repos)
    api_links.append("[Full Documentation](https://docs.acedata.cloud)")
    lines.append("Explore detailed API references for our services:")
    lines.append("")
    lines.append(" · ".join(api_links))
    lines.extend(
        [
            "",
            "## Live Services",
            "",
            "| Service | Description |",
            "| --- | --- |",
        ]
    )

    for name, url, description in LIVE_SERVICES:
        lines.append(f"| [{name}]({url}) | {description} |")

    lines.extend(
        [
            "",
            "## Build Globally",
            "",
            "- Public docs and guides for global developers",
            "- MCP ecosystem distribution across registries and community directories",
            "- API docs repositories for search discovery and long-tail developer traffic",
            "- Automation infrastructure for multi-platform technical content distribution",
            "",
            "## Quick Start",
            "",
            "```bash",
            "curl https://api.acedata.cloud/v1/chat/completions \\",
            "  -H 'Authorization: Bearer YOUR_API_KEY' \\",
            "  -H 'Content-Type: application/json' \\",
            "  -d '{",
            '    "model": "gpt-4o",',
            '    "messages": [{"role": "user", "content": "Hello from Ace Data Cloud"}]',
            "  }'",
            "```",
            "",
            "Get your API key at [platform.acedata.cloud](https://platform.acedata.cloud) - free tier available.",
            "",
            "## $ACE Token",
            "",
            "The [$ACE token](https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump) connects the Ace Data Cloud ecosystem with community growth, incentives, and broader developer discovery.",
            "",
            "## Connect",
            "",
            "- Website: [platform.acedata.cloud](https://platform.acedata.cloud)",
            "- Documentation: [docs.acedata.cloud](https://docs.acedata.cloud)",
            "- Twitter / X: [x.com/AceDataCloud](https://x.com/AceDataCloud)",
            "- Discord: [discord.gg/aedatacloud](https://discord.gg/aedatacloud)",
        ]
    )

    return "\n".join(lines) + "\n"


SYSTEM_PROMPT = """\
You are a designer generating a GitHub organization profile README for \
Ace Data Cloud (AceDataCloud). Output ONLY raw Markdown — no ```markdown fences, \
no explanations, no preamble.

GOAL: A clean, impressive landing page with strong GitHub SEO. Think "startup homepage" \
for developers, AI agents, and MCP users. Show what the platform can do at a glance, \
surface important repos, and make the README discoverable for API, MCP, and AI workflow queries.

STRUCTURE (keep this exact order):

1. **Header**:
    - `# Ace Data Cloud`
    - `![Ace Data Cloud](https://cdn.acedata.cloud/logo.png/thumb_450x_)`
    - Badge links for Platform, API Docs, Nexior App, Status using shields.io `style=flat-square`
    - One bold line: `Unified AI API Platform for Developers, AI Agents, and MCP Tools.`
    - One short paragraph about shipping chat, image, video, music, search, and automation workflows globally through one API key, one billing system, and one developer platform.
    - Then `---`

2. **## What We Do** — 2-3 sentences, confident and concise. Position Ace Data Cloud as \
    developer-first AI infrastructure. Mention leading AI APIs, MCP servers, and open workflows. \
    Then add `## Why Developers Use Ace Data Cloud` with exactly 5-6 bullet points covering:
    - one API key for multiple AI providers
    - OpenAI-compatible API gateway
    - production-ready APIs for chat, image, video, music, search, automation
    - global or multilingual docs / onboarding
    - MCP servers for Copilot, Claude, Cursor, VS Code, and similar tools
    - billing / usage / developer tooling in one place
    After that, add a single Markdown TABLE with 2 columns: Category | Services. \
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

3. **## Featured Repositories** — Add a 2-column table `Repository | Purpose` using real repos \
    from the provided GitHub data. Include these when present: Docs, PlatformBackend, PlatformFrontend, \
    Nexior, VSCodeMCP, Dify, FacilitatorX402. Purpose text must be concise, keyword-rich, and based on real \
    descriptions or obvious repo roles from names. No inventions.

4. **## MCP Servers** — One intro sentence about MCP (Model Context Protocol) \
   letting AI assistants use these APIs as tools. Then a table:
   | Server | PyPI | Description |
   - Server: link to `github.com/AceDataCloud/{dir_name}`
   - PyPI: badge [![PyPI](https://img.shields.io/pypi/v/{package_name}?style=flat-square)](https://pypi.org/project/{package_name}/)
   - Description: from the data as-is
   After table: ```pip install {all package names}```
    Then one short sentence: use these MCP servers with GitHub Copilot, Claude Desktop, Cursor, Windsurf, and other MCP-compatible clients.

5. **## API Documentation** — One intro sentence, then inline dot-separated links. \
   Include ONLY GitHub repos whose name ends with "API" \
   (e.g. FluxAPI, SunoAPI). Display: split CamelCase → "Flux API". \
   Also link to [Full Documentation](https://docs.acedata.cloud) at the end.

6. **## Live Services** — Table with columns: Service | Description. \
   The Service column MUST be a Markdown link: [Name](https://url). Rows:
   - [Developer Platform](https://platform.acedata.cloud) | API keys, docs, billing, analytics
   - [API Gateway](https://api.acedata.cloud) | OpenAI-compatible REST API endpoint
   - [Nexior](https://hub.acedata.cloud) | Consumer app — chat, generate images, video, music
   - [Documentation](https://docs.acedata.cloud) | Quickstart guides and API references
   - [Dify AI](https://dify.acedata.cloud) | Visual AI workflow builder
   - [Status](https://status.acedata.cloud) | Real-time service health monitoring
   - [Roadmap](https://roadmap.acedata.cloud) | Public feature roadmap

7. **## Build Globally** — exactly 4 bullets covering:
    - public docs and guides for global developers
    - MCP registry / community directory presence
    - API docs repositories for search discovery and long-tail traffic
    - automation infrastructure for multi-platform technical content distribution

8. **## Quick Start** — curl to `/v1/chat/completions`, Bearer YOUR_API_KEY, \
   model gpt-4o. Then: \
   "Get your API key at [platform.acedata.cloud](https://platform.acedata.cloud) — free tier available."

9. **## $ACE Token** — 1-2 sentences with link: \
   https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump

10. **## Connect** — Bullet list:
   - Website: [platform.acedata.cloud](https://platform.acedata.cloud)
   - Documentation: [docs.acedata.cloud](https://docs.acedata.cloud)
   - Twitter / X: [x.com/AceDataCloud](https://x.com/AceDataCloud)
   - Discord: [discord.gg/aedatacloud](https://discord.gg/aedatacloud)

STYLE RULES:
- Section headers: ## only, NO emojis in headers. Clean and professional.
- Prefer Markdown over raw HTML unless a badge image requires it.
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
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Use the legacy LLM generation path instead of deterministic rendering",
    )
    args = parser.parse_args()
    workspace_root = args.workspace.resolve()

    api_key = os.environ.get("ACEDATACLOUD_OPENAI_KEY", "")
    github_token = os.environ.get("GITHUB_TOKEN", "")

    if args.use_llm and not api_key:
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

    if args.use_llm:
        print("Calling LLM to generate README...", file=sys.stderr)
        readme = call_llm(SYSTEM_PROMPT, user_prompt, api_key)

        if readme.startswith("```"):
            lines = readme.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            readme = "\n".join(lines)

        if not readme.endswith("\n"):
            readme += "\n"
    else:
        print("Rendering README with deterministic template...", file=sys.stderr)
        readme = render_readme(repos, services, mcp_servers)

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(readme)
    print(f"Updated: {OUTPUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
