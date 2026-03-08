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


def load_service_mapping(workspace_root: Path) -> list[dict]:
    """Load the public service catalog from service_api_mapping.json."""
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
        result.append(
            {
                "alias": svc.get("alias", ""),
                "title": svc.get("title", ""),
                "type": svc.get("type", ""),
                "unit": svc.get("unit", ""),
                "tags": svc.get("tags") or [],
                "rank": svc.get("rank", 0),
                "api_count": len(svc.get("apis", [])),
                "api_paths": [a.get("path", "") for a in svc.get("apis", [])[:5]],
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
        "max_tokens": 4096,
    }

    print(f"\n{'=' * 60}", file=sys.stderr)
    print("LLM REQUEST", file=sys.stderr)
    print(f"{'=' * 60}", file=sys.stderr)
    print(f"  URL:         {url}", file=sys.stderr)
    print(f"  Model:       {OPENAI_MODEL}", file=sys.stderr)
    print(f"  Temperature: {payload['temperature']}", file=sys.stderr)
    print(f"  Max tokens:  {payload['max_tokens']}", file=sys.stderr)
    print(f"\n  System prompt ({len(system_prompt)} chars):", file=sys.stderr)
    print(f"  {system_prompt[:500]}{'...' if len(system_prompt) > 500 else ''}", file=sys.stderr)
    print(f"\n  User prompt ({len(user_prompt)} chars):", file=sys.stderr)
    print(f"  {user_prompt[:2000]}{'...' if len(user_prompt) > 2000 else ''}", file=sys.stderr)
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
        print(f"  Prompt tokens:     {usage.get('prompt_tokens', 'N/A')}", file=sys.stderr)
        print(f"  Completion tokens: {usage.get('completion_tokens', 'N/A')}", file=sys.stderr)
        print(f"  Total tokens:      {usage.get('total_tokens', 'N/A')}", file=sys.stderr)
    print(f"  Response length:   {len(content)} chars", file=sys.stderr)
    print(f"\n  Full response:", file=sys.stderr)
    print(content, file=sys.stderr)
    print(f"{'=' * 60}\n", file=sys.stderr)

    return content


SYSTEM_PROMPT = """\
You are a technical writer generating a GitHub organization profile README for \
Ace Data Cloud (AceDataCloud). Output ONLY the raw Markdown, no ```markdown fences, \
no explanations, no preamble.

REQUIREMENTS:
1. Start with a centered header block (<div align="center">):
   - Logo: <img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />
   - Title: <h1>Ace Data Cloud</h1> (must be HTML h1 tag, not Markdown #, since it is inside a div)
   - Tagline: <b>bold one-liner about unified AI API platform</b> (HTML bold, not Markdown)
   - Badges: use HTML <a><img> tags (NOT Markdown ![]()), because Markdown images don't render inside <div>.
     Example: <a href="https://platform.acedata.cloud"><img src="https://img.shields.io/badge/Platform-blue?style=flat-square" /></a>
     Badges: Platform (blue, links platform.acedata.cloud), API Docs (green, links docs.acedata.cloud), Nexior (orange, links hub.acedata.cloud), Status (brightgreen, links status.acedata.cloud)
   - Close </div> with a blank line (NO --- horizontal rule)

2. Sections in order:
   a) "## \U0001f680 What We Do" - brief intro paragraph + Markdown TABLE of service categories.
      Categories: LLM Chat, Image Generation, Video Generation, Music & Audio, Web Search.
      Populate each category from the service catalog data I provide.
      SKIP services of type Dataset, Deployment, Proxy, Introduction, Agent.
      SKIP infrastructure services (captcha, proxy, URL shortener, localization, identity, exchange-rate).
      SKIP the service with alias "aichat" (it is an internal alias, NOT a brand).
      Use proper brand names (e.g. "DeepSeek" not "Deepseek", "Midjourney" not "midjourney").
      For the service with alias "openai", show as "GPT / DALL-E" in LLM Chat AND Image Gen categories.
      Do NOT duplicate services - each brand name should appear AT MOST ONCE across the ENTIRE table.
      If a service belongs to multiple categories (e.g. openai has tags aichat+aiimage), pick the primary category only.
      The "openai" service should appear ONLY in LLM Chat as "GPT / DALL-E".
      Tag mapping: "aichat" -> LLM Chat, "aiimage" -> Image Gen, "aivideo" -> Video Gen, "aiaudio" -> Music & Audio.
      The "serp" service goes in Web Search.
      Make sure to include ALL matching services; do not omit any from the provided data.
      Only list clean brand names, not aliases. Capitalize properly:
      "fish" -> "Fish Audio", "producer" -> "Producer", "hailuo" -> "Hailuo", "nano-banana" -> "NanoBanana",
      "seedream" -> "Seedream", "seedance" -> "Seedance", "serp" -> "Google SERP".

   b) "## \U0001f50c MCP Servers (Model Context Protocol)" - intro line + Markdown TABLE.
      Columns: Server | PyPI | Description.
      Server column: link to GitHub repo [DirName](https://github.com/AceDataCloud/{dir_name})
      PyPI column: badge [![PyPI](https://img.shields.io/pypi/v/{package_name}?style=flat-square)](https://pypi.org/project/{package_name}/)
      Description: clean short desc (remove "MCP Server for" and "via AceDataCloud API" prefixes/suffixes).
      After table: pip install command with all package names.

   c) "## \U0001f4da API Documentation Repos" - intro line + inline dot-separated links.
      Include ONLY repos whose name ends with "API" (e.g. "SunoAPI", "FluxAPI").
      Exclude repos like "Docs", "Nexior", "StatusPage", "Roadmap", ".github" - only *API suffix repos.
      Format: [Display Name](https://github.com/AceDataCloud/{name})
      Display name: split CamelCase, e.g. "MidjourneyAPI" -> "Midjourney API", "GPT4oImageAPI" -> "GPT4o Image API".

   d) "## \U0001f310 Live Services" - Markdown TABLE.
      Must include these rows exactly:
      Developer Platform | platform.acedata.cloud | API keys, docs, billing, analytics
      API Gateway | api.acedata.cloud | OpenAI-compatible REST API endpoint
      Nexior | hub.acedata.cloud | Consumer app - chat, generate images/video/music
      Documentation | docs.acedata.cloud | Quickstart guides and API references
      Dify AI | dify.acedata.cloud | Visual AI workflow builder
      Status | status.acedata.cloud | Real-time service health monitoring
      Roadmap | roadmap.acedata.cloud | Public feature roadmap

   e) "## \u26a1 Quick Start" - curl example to /v1/chat/completions with Bearer YOUR_API_KEY, model gpt-4o.
      Then "Get your API key at [platform.acedata.cloud](...) - free tier available."

   f) "## \U0001f4b0 $ACE Token" - brief paragraph.
      Link: https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump

   g) "## \U0001f4ec Connect" - bullet list:
      Website (platform.acedata.cloud), Documentation (docs.acedata.cloud),
      Twitter/X (x.com/AceDataCloud), Discord (discord.gg/aedatacloud)

CRITICAL RULES:
- Use ONLY data I provide. Do NOT invent model names or versions.
- For service names, derive correct branding from alias + title key + API paths.
- Keep it professional and concise.
- No trailing whitespace on lines.
- End with a single newline.
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
                stars = f" ★{r['stars']}" if r['stars'] else ""
                print(f"    - {r['name']}: {r['description'][:80]}{stars}", file=sys.stderr)
        except Exception as e:
            print(f"  Warning: GitHub API error: {e}", file=sys.stderr)
    else:
        print("  GITHUB_TOKEN not set, skipping repo discovery", file=sys.stderr)

    print("\n[2/3] Loading service catalog...", file=sys.stderr)
    services = load_service_mapping(workspace_root)
    print(f"  Found {len(services)} public services", file=sys.stderr)
    for svc in services:
        print(f"    - {svc['alias']} ({svc['type']}, unit={svc['unit']}, apis={svc['api_count']}, tags={svc.get('tags', [])})", file=sys.stderr)

    print("\n[3/3] Discovering MCP servers...", file=sys.stderr)
    mcp_servers = discover_mcp_servers(workspace_root)
    print(f"  Found {len(mcp_servers)} MCP servers", file=sys.stderr)
    for s in mcp_servers:
        print(f"    - {s['dir_name']}: {s['package_name']} — {s['description']}", file=sys.stderr)

    # Build user prompt with all collected data
    user_prompt = "Generate the organization profile README using this real data:\n\n"

    if repos:
        user_prompt += "## GitHub Repositories (public, non-archived, non-fork)\n"
        user_prompt += json.dumps(repos, indent=2) + "\n\n"

    if services:
        user_prompt += "## Service Catalog (from platform database, sorted by rank)\n"
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
