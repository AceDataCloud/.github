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


SKIP_ALIASES = {"aichat"}
SKIP_CATEGORIES = {"CAPTCHA", "Proxy", "Identity"}
SKIP_TYPES = {"Dataset", "Deployment", "Proxy", "Introduction", "Agent"}


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
        if svc.get("alias", "") in SKIP_ALIASES:
            continue
        category = svc.get("category", "")
        if category in SKIP_CATEGORIES:
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
                "alias": svc.get("alias", ""),
                "display_name": svc.get("display_name", ""),
                "type": svc.get("type", ""),
                "tags": svc.get("tags") or [],
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
                desc = desc[len(prefix):]
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
You are a technical writer generating a GitHub organization profile README for \
Ace Data Cloud (AceDataCloud). Output ONLY the raw Markdown — no ```markdown fences, \
no explanations, no preamble.

GOAL: Informative, data-rich, visually engaging landing page that helps \
developers quickly see what Ace Data Cloud offers.

STRUCTURE (keep this exact order):

1. **Header** (<div align="center">):
   - <img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />
   - <h1>Ace Data Cloud</h1>
   - <b>One unified API for dozens of AI models — images, video, music, chat, search & more</b>
   - Badges (HTML <a><img>, shields.io style=flat-square):
     Platform (blue → platform.acedata.cloud), Docs (green → docs.acedata.cloud),
     Nexior (orange → hub.acedata.cloud), Status (brightgreen → status.acedata.cloud)
   - Close </div> then a blank line. NO --- horizontal rule.

2. **## 🚀 What We Do** — 2-3 sentence intro, then a bold stat line using the \
   EXACT numbers I provide in `summary_stats` (services, endpoints, categories). \
   Do NOT re-count yourself — just use my numbers.

3. **## 📡 Service Catalog** — THE MAIN SHOWCASE. \
   Group by `category` from the data. For each category: ### with emoji, then a \
   Markdown table:
   | Service | Endpoints | Stage |
   - **Service**: `display_name` from data — keep original casing.
   - **Endpoints**: each API's `path`, use `<br/>` for multiple.
   - **Stage**: Production→🟢, Beta→🟡, Alpha→🔴, empty→—. One dot per endpoint.

   Category display order: AI Chat → AI Image → AI Video → AI Audio → Web & Data.
   Include ALL services in the data — I have already pre-filtered.

   IMPORTANT: If a service appears in the data once, show it ONCE under its \
   listed category. Do NOT duplicate a service across categories.

4. **## 🔌 MCP Servers** — Short intro, then table:
   | Server | Install | Description |
   - Server: link to `github.com/AceDataCloud/{dir_name}`
   - Install: `pip install {package_name}` in inline code
   - Description: use `description` from the data as is (already cleaned)

5. **## 📚 API Documentation Repos** — Inline dot-separated links. \
   Include ONLY repos whose name literally ends with the 3 letters "API" \
   (e.g. FluxAPI, SunoAPI, MidjourneyAPI). \
   Do NOT include repos like "Docs" or "Dify". \
   Display: split CamelCase → "Flux API".

6. **## 🌐 Live Services** — Table with columns: Service | URL | Description.
   Rows (use these EXACT URLs):
   - Developer Platform | platform.acedata.cloud | API keys, billing, service management
   - API Gateway | api.acedata.cloud | Unified endpoint for all services
   - Nexior | hub.acedata.cloud | Consumer AI app (chat, images, video, music)
   - Documentation | docs.acedata.cloud | API reference & guides
   - Dify AI | dify.acedata.cloud | AI workflow builder
   - Status | status.acedata.cloud | Uptime monitoring
   - Roadmap | roadmap.acedata.cloud | Public product roadmap

7. **## ⚡ Quick Start** — curl to `/v1/chat/completions`, Bearer YOUR_API_KEY, \
   model gpt-4o. Then: "Get your free API key → [platform.acedata.cloud](https://platform.acedata.cloud)"

8. **## 💰 $ACE Token** — Brief paragraph with link: \
   https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump

9. **## 📬 Connect** — Bullet list with EXACTLY these URLs:
   - 🌐 Website: [platform.acedata.cloud](https://platform.acedata.cloud)
   - 📖 Documentation: [docs.acedata.cloud](https://docs.acedata.cloud)
   - 🐦 Twitter / X: [x.com/AceDataCloud](https://x.com/AceDataCloud)
   - 💬 Discord: [discord.gg/aedatacloud](https://discord.gg/aedatacloud)

RULES:
- Use ONLY data I provide. NEVER invent services, endpoints, or descriptions.
- No trailing whitespace. End with a single newline.
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
            f"    - {svc['alias']} ({svc['type']}, display_name={svc.get('display_name','')}, category={svc.get('category','')}, apis={len(svc.get('apis', []))}, tags={svc.get('tags', [])})",
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
