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
        apis = []
        for a in svc.get("apis", []):
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
                "unit": svc.get("unit", ""),
                "tags": svc.get("tags") or [],
                "category": svc.get("category", ""),
                "category_icon": svc.get("category_icon", ""),
                "rank": svc.get("rank", 0),
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

GOAL: Make the profile informative, data-rich, and visually engaging — like a \
landing page that helps developers quickly understand what Ace Data Cloud offers \
and how to start using it.  Show off the breadth of services with real data.

STRUCTURE (keep this order, but write naturally — not like a rigid template):

1. **Header** (<div align="center">):
   - Logo: <img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />
   - <h1>Ace Data Cloud</h1> (HTML h1, not Markdown #, since it is inside a div)
   - <b>Catchy one-liner about the unified AI API platform</b> (HTML bold)
   - Badges as HTML <a><img> (Markdown images don't render inside div):
     Platform (blue, platform.acedata.cloud), API Docs (green, docs.acedata.cloud),
     Nexior (orange, hub.acedata.cloud), Status (brightgreen, status.acedata.cloud)
   - Close </div>, blank line, NO --- rule

2. **## \U0001f680 What We Do** — Engaging intro paragraph (2-3 sentences), then a summary
   stat line like "**X AI services \u00b7 Y API endpoints \u00b7 Z categories**" derived from
   the real data counts I provide.

3. **## \U0001f4e1 Service Catalog** — THIS IS THE MAIN SHOWCASE.  Group by the `category`
   field from the data.  For each category use a sub-heading (### with a fitting emoji)
   and a Markdown table with columns:
   - **Service** — use `display_name` from the data; keep proper brand casing.
   - **API Endpoints** — list each API's `path`. Use `<br/>` for multiple paths in one cell.
   - **Stage** — map: Production \u2192 \U0001f7e2, Beta \u2192 \U0001f7e1, Alpha \u2192 \U0001f534, empty \u2192 \u2014.
     Show one dot per endpoint, matching order.

   Category order: AI Chat \u2192 AI Image \u2192 AI Video \u2192 AI Audio \u2192 Web & Data.
   SKIP categories: CAPTCHA, Proxy, Identity.
   SKIP services of type Dataset, Deployment, Proxy, Introduction, Agent.
   SKIP the service with alias "aichat" (internal, not a product).
   Include ALL other non-private services from the data.

4. **## \U0001f50c MCP Servers (Model Context Protocol)** — Short intro, then table:
   Server (GitHub link) | PyPI badge | Description (clean, no boilerplate prefix).
   After table: `pip install` one-liner with all packages.

5. **## \U0001f4da API Documentation Repos** — Intro line + dot-separated inline links.
   Include ONLY repos whose name ends with "API".
   Display name: split CamelCase \u2192 "Midjourney API".

6. **## \U0001f310 Live Services** — Table of live URLs:
   Developer Platform \u2192 platform.acedata.cloud, API Gateway \u2192 api.acedata.cloud,
   Nexior \u2192 hub.acedata.cloud, Documentation \u2192 docs.acedata.cloud,
   Dify AI \u2192 dify.acedata.cloud, Status \u2192 status.acedata.cloud,
   Roadmap \u2192 roadmap.acedata.cloud.

7. **## \u26a1 Quick Start** — curl example to `/v1/chat/completions`, Bearer YOUR_API_KEY, model gpt-4o.
   Then: "Get your API key at platform.acedata.cloud \u2014 free tier available."

8. **## \U0001f4b0 $ACE Token** — Brief paragraph.
   Link: https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump

9. **## \U0001f4ec Connect** — Bullet list: Website, Documentation, Twitter/X, Discord.

CRITICAL RULES:
- Use ONLY data I provide. Do NOT invent services, endpoints, or model names.
- Service names: use `display_name` from the data; capitalize properly.
- Keep it professional but NOT bland. Show real numbers, real endpoints.
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
