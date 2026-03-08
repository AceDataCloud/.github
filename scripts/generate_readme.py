"""Generate the organization profile README from live GitHub/PyPI data."""

import json
import urllib.request
from pathlib import Path

ORG = "AceDataCloud"

# MCP servers: (repo_name, pypi_package, short_description)
MCP_SERVERS = [
    ("MCPSuno", "mcp-suno", "AI music generation with Suno"),
    ("MCPMidjourney", "mcp-midjourney", "AI image generation with Midjourney"),
    ("MCPSerp", "mcp-serp", "Google search (web, images, news)"),
    ("MCPLuma", "mcp-luma", "AI video generation with Luma"),
    ("MCPSora", "mcp-sora", "AI video generation with Sora"),
    ("MCPVeo", "mcp-veo", "AI video generation with Veo"),
    ("MCPNanoBanana", "mcp-nanobanana-pro", "AI image generation & editing"),
]

# API documentation repos
API_DOC_REPOS = [
    ("MidjourneyAPI", "Midjourney API"),
    ("SunoAPI", "Suno API"),
    ("LumaAPI", "Luma API"),
    ("DeepSeekAPI", "DeepSeek API"),
    ("GoogleSerpAPI", "Google SERP API"),
    ("FluxAPI", "Flux API"),
    ("GPT4oImageAPI", "GPT4o Image API"),
    ("KlingAPI", "Kling API"),
    ("HailuoAPI", "Hailuo API"),
    ("PikaAPI", "Pika API"),
]


def fetch_json(url: str):
    """Fetch JSON from a URL, return None on error."""
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def get_pypi_version(package: str):
    """Get latest PyPI version for a package."""
    data = fetch_json(f"https://pypi.org/pypi/{package}/json")
    if data:
        return data.get("info", {}).get("version")
    return None


def get_github_stars(repo: str):
    """Get star count for a GitHub repo."""
    data = fetch_json(f"https://api.github.com/repos/{ORG}/{repo}")
    if data:
        return data.get("stargazers_count")
    return None


def generate_mcp_table() -> str:
    """Generate the MCP servers table with live PyPI badges."""
    rows = []
    for repo, pypi_pkg, desc in MCP_SERVERS:
        badge = (
            f"[![PyPI](https://img.shields.io/pypi/v/{pypi_pkg}?style=flat-square)]"
            f"(https://pypi.org/project/{pypi_pkg}/)"
        )
        row = f"| [{repo}](https://github.com/{ORG}/{repo}) | {badge} | {desc} |"
        rows.append(row)

    header = "| Server | PyPI | Description |\n|--------|------|-------------|"
    return header + "\n" + "\n".join(rows)


def generate_api_doc_links() -> str:
    """Generate API documentation repo links."""
    links = []
    for repo, name in API_DOC_REPOS:
        links.append(f"[{name}](https://github.com/{ORG}/{repo})")
    return " · ".join(links)


def generate_install_command() -> str:
    """Generate pip install command for all MCP servers."""
    packages = " ".join(pypi for _, pypi, _ in MCP_SERVERS)
    return f"pip install {packages}"


def generate_readme() -> str:
    """Generate the full profile README."""
    mcp_table = generate_mcp_table()
    api_doc_links = generate_api_doc_links()
    install_cmd = generate_install_command()

    return f"""<div align="center">

<img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />

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

| Category | Services |
|----------|----------|
| **LLM Chat** | GPT-4o, Claude 4, Gemini 2.5, Grok, DeepSeek, Kimi, Qwen, and more |
| **Image Generation** | Midjourney, Flux, Seedream, DALL·E, Stable Diffusion |
| **Video Generation** | Sora, Luma Dream Machine, Veo, Kling, Hailuo, Pika, Seedance |
| **Music Generation** | Suno AI (generate, extend, cover, remix) |
| **Web Search** | Google SERP API (web, images, news, shopping, scholar) |
| **More** | QR Art, AI Headshots, NanoBanana, and growing |

## 🔌 MCP Servers (Model Context Protocol)

We publish official MCP servers so AI assistants (Claude, Cursor, Windsurf, etc.) can use our APIs as tools:

{mcp_table}

Install any server with one command:

```bash
{install_cmd}
```

## 📚 API Documentation Repos

Detailed API references with request/response examples for each service:

{api_doc_links}

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

</div>
"""


def main():
    readme_path = Path(__file__).parent.parent / "profile" / "README.md"
    content = generate_readme()

    # Check if content changed
    if readme_path.exists():
        old_content = readme_path.read_text()
        if old_content.strip() == content.strip():
            print("No changes detected.")
            return

    readme_path.write_text(content)
    print(f"Updated {readme_path}")


if __name__ == "__main__":
    main()
