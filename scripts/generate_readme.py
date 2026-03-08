"""Generate the organization profile README from live GitHub/PyPI data."""

from pathlib import Path

ORG = "AceDataCloud"

# MCP servers: (repo_name, pypi_package, short_description) — sorted alphabetically
MCP_SERVERS = [
    ("MCPLuma", "mcp-luma", "Luma AI Video Generation"),
    ("MCPMidjourney", "mcp-midjourney", "Midjourney AI Image Generation"),
    ("MCPNanoBanana", "mcp-nanobanana-pro", "NanoBanana AI Image Generation"),
    ("MCPSerp", "mcp-serp", "Google SERP Search"),
    ("MCPSora", "mcp-sora", "Sora AI Video Generation"),
    ("MCPSuno", "mcp-suno", "Suno AI Music Generation"),
    ("MCPVeo", "mcp-veo", "Veo AI Video Generation"),
]

# API documentation repos — sorted alphabetically
API_DOC_REPOS = [
    ("DeepSeekAPI", "DeepSeek API"),
    ("FluxAPI", "Flux API"),
    ("GPT4oImageAPI", "GPT4o Image API"),
    ("GoogleSerpAPI", "Google SERP API"),
    ("HailuoAPI", "Hailuo API"),
    ("KlingAPI", "Kling API"),
    ("LumaAPI", "Luma API"),
    ("MidjourneyAPI", "Midjourney API"),
    ("NanoBananaAPI", "NanoBanana API"),
    ("OpenAIAPI", "OpenAI API"),
    ("PikaAPI", "Pika API"),
    ("PixverseAPI", "Pixverse API"),
    ("SoraAPI", "Sora API"),
    ("SunoAPI", "Suno API"),
    ("VeoAPI", "Veo API"),
]


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

<img src="https://cdn.acedata.cloud/acedatacloud.png" alt="Ace Data Cloud" width="120" />

# Ace Data Cloud

**Unified AI API Platform — One Key, Hundreds of AI Models**

Access GPT, Claude, Gemini, Grok, DeepSeek, Midjourney, Suno, Luma, Sora, and 100+ more AI services through a single, OpenAI-compatible API.

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
| **LLM Chat** | Gemini 2.5 Pro / Flash, Kimi (Moonshot), Claude 4 / 3.5 Sonnet, DeepSeek R1 / V3, Grok 3, GPT-4o / o1 / o3 |
| **Image Generation** | Seedream, NanoBanana, Flux, Midjourney, QR Art |
| **Video Generation** | Seedance, Sora, Veo, Kling, Wan (Alibaba), Luma Dream Machine, Hailuo (MiniMax) |
| **Music & Audio** | Suno AI, Fish Audio (TTS), Producer |
| **Web Search** | Google SERP API |

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
