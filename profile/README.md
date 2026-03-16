<div align="center">
<img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />
<h1>Ace Data Cloud</h1>
<b>Unified AI API Platform — One Key, Hundreds of AI Models</b>
<p>Access a broad ecosystem of AI models for chat, image, video, music, and search through a single API platform.</p>
<a href="https://platform.acedata.cloud"><img src="https://img.shields.io/badge/platform-blue?style=flat-square" alt="Platform"/></a>
<a href="https://docs.acedata.cloud"><img src="https://img.shields.io/badge/API%20Docs-green?style=flat-square" alt="API Docs"/></a>
<a href="https://hub.acedata.cloud"><img src="https://img.shields.io/badge/Nexior%20App-orange?style=flat-square" alt="Nexior App"/></a>
<a href="https://status.acedata.cloud"><img src="https://img.shields.io/badge/Status-brightgreen?style=flat-square" alt="Status"/></a>
</div>

---

## What We Do

Ace Data Cloud offers a unified API platform connecting you to hundreds of AI models across multiple categories. Quickly integrate chatbots, image and video generation, music creation, and web search into your applications with one API key.

| Category    | Services                                      |
|-------------|-----------------------------------------------|
| LLM Chat    | Gemini, Kimi, Claude, DeepSeek, Grok, GPT / DALL·E / Sora |
| Image Generation | Seedream, NanoBanana, Flux, Midjourney, QR Art, Face Transform |
| Video Generation | Seedance, Sora, Veo, Kling, Wan (Alibaba), Luma, Hailuo, Pixverse |
| Music & Audio | Suno, Fish Audio, Producer                     |
| Web Search  | Google SERP                                   |

**Browse all services →** [platform.acedata.cloud](https://platform.acedata.cloud)

## MCP Servers

Our MCP (Model Context Protocol) servers enable AI assistants to use these APIs as powerful tools.

| Server | PyPI | Description |
|--------|------|-------------|
| [MCPFlux](https://github.com/AceDataCloud/MCPFlux) | [![PyPI](https://img.shields.io/pypi/v/mcp-flux-pro?style=flat-square)](https://pypi.org/project/mcp-flux-pro/) | Flux AI Image Generation |
| [MCPLuma](https://github.com/AceDataCloud/MCPLuma) | [![PyPI](https://img.shields.io/pypi/v/mcp-luma?style=flat-square)](https://pypi.org/project/mcp-luma/) | Luma AI Video Generation |
| [MCPMidjourney](https://github.com/AceDataCloud/MCPMidjourney) | [![PyPI](https://img.shields.io/pypi/v/mcp-midjourney?style=flat-square)](https://pypi.org/project/mcp-midjourney/) | Midjourney AI Image Generation |
| [MCPNanoBanana](https://github.com/AceDataCloud/MCPNanoBanana) | [![PyPI](https://img.shields.io/pypi/v/mcp-nanobanana-pro?style=flat-square)](https://pypi.org/project/mcp-nanobanana-pro/) | NanoBanana AI Image Generation |
| [MCPSeedance](https://github.com/AceDataCloud/MCPSeedance) | [![PyPI](https://img.shields.io/pypi/v/mcp-seedance?style=flat-square)](https://pypi.org/project/mcp-seedance/) | ByteDance Seedance AI Video Generation |
| [MCPSeedream](https://github.com/AceDataCloud/MCPSeedream) | [![PyPI](https://img.shields.io/pypi/v/mcp-seedream-pro?style=flat-square)](https://pypi.org/project/mcp-seedream-pro/) | ByteDance Seedream AI Image Generation |
| [MCPSerp](https://github.com/AceDataCloud/MCPSerp) | [![PyPI](https://img.shields.io/pypi/v/mcp-serp?style=flat-square)](https://pypi.org/project/mcp-serp/) | Google SERP Search |
| [MCPShortURL](https://github.com/AceDataCloud/MCPShortURL) | [![PyPI](https://img.shields.io/pypi/v/mcp-shorturl?style=flat-square)](https://pypi.org/project/mcp-shorturl/) | URL Shortening |
| [MCPSora](https://github.com/AceDataCloud/MCPSora) | [![PyPI](https://img.shields.io/pypi/v/mcp-sora?style=flat-square)](https://pypi.org/project/mcp-sora/) | Sora AI Video Generation |
| [MCPSuno](https://github.com/AceDataCloud/MCPSuno) | [![PyPI](https://img.shields.io/pypi/v/mcp-suno?style=flat-square)](https://pypi.org/project/mcp-suno/) | Suno AI Music Generation |
| [MCPVeo](https://github.com/AceDataCloud/MCPVeo) | [![PyPI](https://img.shields.io/pypi/v/mcp-veo?style=flat-square)](https://pypi.org/project/mcp-veo/) | Veo AI Video Generation |

```bash
pip install mcp-flux-pro mcp-luma mcp-midjourney mcp-nanobanana-pro mcp-seedance mcp-seedream-pro mcp-serp mcp-shorturl mcp-sora mcp-suno mcp-veo
```

## API Documentation

Explore detailed API references for our services:

[Flux API](https://github.com/AceDataCloud/FluxAPI) · [Luma API](https://github.com/AceDataCloud/LumaAPI) · [Midjourney API](https://github.com/AceDataCloud/MidjourneyAPI) · [Nano Banana API](https://github.com/AceDataCloud/NanoBananaAPI) · [OpenAI API](https://github.com/AceDataCloud/OpenAIAPI) · [Pixverse API](https://github.com/AceDataCloud/PixverseAPI) · [Serp API](https://github.com/AceDataCloud/SerpAPI) · [Sora API](https://github.com/AceDataCloud/SoraAPI) · [Suno API](https://github.com/AceDataCloud/SunoAPI) · [Veo API](https://github.com/AceDataCloud/VeoAPI) · [Full Documentation](https://docs.acedata.cloud)

## Live Services

| Service | Description |
|---------|-------------|
| [Developer Platform](https://platform.acedata.cloud) | API keys, docs, billing, analytics |
| [API Gateway](https://api.acedata.cloud) | OpenAI-compatible REST API endpoint |
| [Nexior](https://hub.acedata.cloud) | Consumer app — chat, generate images, video, music |
| [Documentation](https://docs.acedata.cloud) | Quickstart guides and API references |
| [Dify AI](https://dify.acedata.cloud) | Visual AI workflow builder |
| [Status](https://status.acedata.cloud) | Real-time service health monitoring |
| [Roadmap](https://roadmap.acedata.cloud) | Public feature roadmap |

## Quick Start

```bash
curl https://api.acedata.cloud/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello, world!"}]}'
```

Get your API key at [platform.acedata.cloud](https://platform.acedata.cloud) — free tier available.

## $ACE Token

The $ACE token powers the Ace Data Cloud ecosystem. Learn more and trade at [pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump](https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump).

## Connect

- Website: [platform.acedata.cloud](https://platform.acedata.cloud)
- Documentation: [docs.acedata.cloud](https://docs.acedata.cloud)
- Twitter / X: [x.com/AceDataCloud](https://x.com/AceDataCloud)
- Discord: [discord.gg/aedatacloud](https://discord.gg/aedatacloud)
