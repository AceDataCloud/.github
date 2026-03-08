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

| Server | PyPI | Description |
|--------|------|-------------|
| [MCPSuno](https://github.com/AceDataCloud/MCPSuno) | [![PyPI](https://img.shields.io/pypi/v/mcp-suno?style=flat-square)](https://pypi.org/project/mcp-suno/) | AI music generation with Suno |
| [MCPMidjourney](https://github.com/AceDataCloud/MCPMidjourney) | [![PyPI](https://img.shields.io/pypi/v/mcp-midjourney?style=flat-square)](https://pypi.org/project/mcp-midjourney/) | AI image generation with Midjourney |
| [MCPSerp](https://github.com/AceDataCloud/MCPSerp) | [![PyPI](https://img.shields.io/pypi/v/mcp-serp?style=flat-square)](https://pypi.org/project/mcp-serp/) | Google search (web, images, news) |
| [MCPLuma](https://github.com/AceDataCloud/MCPLuma) | [![PyPI](https://img.shields.io/pypi/v/mcp-luma?style=flat-square)](https://pypi.org/project/mcp-luma/) | AI video generation with Luma |
| [MCPSora](https://github.com/AceDataCloud/MCPSora) | [![PyPI](https://img.shields.io/pypi/v/mcp-sora?style=flat-square)](https://pypi.org/project/mcp-sora/) | AI video generation with Sora |
| [MCPVeo](https://github.com/AceDataCloud/MCPVeo) | [![PyPI](https://img.shields.io/pypi/v/mcp-veo?style=flat-square)](https://pypi.org/project/mcp-veo/) | AI video generation with Veo |
| [MCPNanoBanana](https://github.com/AceDataCloud/MCPNanoBanana) | [![PyPI](https://img.shields.io/pypi/v/mcp-nanobanana-pro?style=flat-square)](https://pypi.org/project/mcp-nanobanana-pro/) | AI image generation & editing |

Install any server with one command:

```bash
pip install mcp-suno mcp-midjourney mcp-serp mcp-luma mcp-sora mcp-veo mcp-nanobanana-pro
```

## 📚 API Documentation Repos

Detailed API references with request/response examples for each service:

[Midjourney API](https://github.com/AceDataCloud/MidjourneyAPI) · [Suno API](https://github.com/AceDataCloud/SunoAPI) · [Luma API](https://github.com/AceDataCloud/LumaAPI) · [DeepSeek API](https://github.com/AceDataCloud/DeepSeekAPI) · [Google SERP API](https://github.com/AceDataCloud/GoogleSerpAPI) · [Flux API](https://github.com/AceDataCloud/FluxAPI) · [GPT4o Image API](https://github.com/AceDataCloud/GPT4oImageAPI) · [Kling API](https://github.com/AceDataCloud/KlingAPI) · [Hailuo API](https://github.com/AceDataCloud/HailuoAPI) · [Pika API](https://github.com/AceDataCloud/PikaAPI)

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
curl https://api.acedata.cloud/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello!"}]}'
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
