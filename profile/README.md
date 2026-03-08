<div align="center">

<img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />

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

| Category             | Services                                                                                                   |
| -------------------- | ---------------------------------------------------------------------------------------------------------- |
| **LLM Chat**         | Gemini 2.5 Pro / Flash, Kimi (Moonshot), Claude 4 / 3.5 Sonnet, DeepSeek R1 / V3, Grok 3, GPT-4o / o1 / o3 |
| **Image Generation** | Seedream, NanoBanana, Flux, Midjourney, QR Art                                                             |
| **Video Generation** | Seedance, Sora, Veo, Kling, Wan (Alibaba), Luma Dream Machine, Hailuo (MiniMax)                            |
| **Music & Audio**    | Suno AI, Fish Audio (TTS), Producer                                                                        |
| **Web Search**       | Google SERP API                                                                                            |

## 🔌 MCP Servers (Model Context Protocol)

We publish official MCP servers so AI assistants (Claude, Cursor, Windsurf, etc.) can use our APIs as tools:

| Server                                                         | PyPI                                                                                                                        | Description                    |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| [MCPLuma](https://github.com/AceDataCloud/MCPLuma)             | [![PyPI](https://img.shields.io/pypi/v/mcp-luma?style=flat-square)](https://pypi.org/project/mcp-luma/)                     | Luma AI Video Generation       |
| [MCPMidjourney](https://github.com/AceDataCloud/MCPMidjourney) | [![PyPI](https://img.shields.io/pypi/v/mcp-midjourney?style=flat-square)](https://pypi.org/project/mcp-midjourney/)         | Midjourney AI Image Generation |
| [MCPNanoBanana](https://github.com/AceDataCloud/MCPNanoBanana) | [![PyPI](https://img.shields.io/pypi/v/mcp-nanobanana-pro?style=flat-square)](https://pypi.org/project/mcp-nanobanana-pro/) | NanoBanana AI Image Generation |
| [MCPSerp](https://github.com/AceDataCloud/MCPSerp)             | [![PyPI](https://img.shields.io/pypi/v/mcp-serp?style=flat-square)](https://pypi.org/project/mcp-serp/)                     | Google SERP Search             |
| [MCPSora](https://github.com/AceDataCloud/MCPSora)             | [![PyPI](https://img.shields.io/pypi/v/mcp-sora?style=flat-square)](https://pypi.org/project/mcp-sora/)                     | Sora AI Video Generation       |
| [MCPSuno](https://github.com/AceDataCloud/MCPSuno)             | [![PyPI](https://img.shields.io/pypi/v/mcp-suno?style=flat-square)](https://pypi.org/project/mcp-suno/)                     | Suno AI Music Generation       |
| [MCPVeo](https://github.com/AceDataCloud/MCPVeo)               | [![PyPI](https://img.shields.io/pypi/v/mcp-veo?style=flat-square)](https://pypi.org/project/mcp-veo/)                       | Veo AI Video Generation        |

Install any server with one command:

```bash
pip install mcp-luma mcp-midjourney mcp-nanobanana-pro mcp-serp mcp-sora mcp-suno mcp-veo
```

## 📚 API Documentation Repos

Detailed API references with request/response examples for each service:

[DeepSeek API](https://github.com/AceDataCloud/DeepSeekAPI) · [Flux API](https://github.com/AceDataCloud/FluxAPI) · [GPT4o Image API](https://github.com/AceDataCloud/GPT4oImageAPI) · [Google SERP API](https://github.com/AceDataCloud/GoogleSerpAPI) · [Hailuo API](https://github.com/AceDataCloud/HailuoAPI) · [Kling API](https://github.com/AceDataCloud/KlingAPI) · [Luma API](https://github.com/AceDataCloud/LumaAPI) · [Midjourney API](https://github.com/AceDataCloud/MidjourneyAPI) · [NanoBanana API](https://github.com/AceDataCloud/NanoBananaAPI) · [OpenAI API](https://github.com/AceDataCloud/OpenAIAPI) · [Pika API](https://github.com/AceDataCloud/PikaAPI) · [Pixverse API](https://github.com/AceDataCloud/PixverseAPI) · [Sora API](https://github.com/AceDataCloud/SoraAPI) · [Suno API](https://github.com/AceDataCloud/SunoAPI) · [Veo API](https://github.com/AceDataCloud/VeoAPI)

## 🌐 Live Services

| Service                | URL                                                      | Description                                      |
| ---------------------- | -------------------------------------------------------- | ------------------------------------------------ |
| **Developer Platform** | [platform.acedata.cloud](https://platform.acedata.cloud) | API keys, docs, billing, analytics               |
| **API Gateway**        | [api.acedata.cloud](https://api.acedata.cloud)           | OpenAI-compatible REST API endpoint              |
| **Nexior**             | [hub.acedata.cloud](https://hub.acedata.cloud)           | Consumer app — chat, generate images/video/music |
| **Documentation**      | [docs.acedata.cloud](https://docs.acedata.cloud)         | Quickstart guides and API references             |
| **Dify AI**            | [dify.acedata.cloud](https://dify.acedata.cloud)         | Visual AI workflow builder                       |
| **Status**             | [status.acedata.cloud](https://status.acedata.cloud)     | Real-time service health monitoring              |
| **Roadmap**            | [roadmap.acedata.cloud](https://roadmap.acedata.cloud)   | Public feature roadmap                           |

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
