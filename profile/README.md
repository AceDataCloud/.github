<div align="center">
<img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />
<h1>Ace Data Cloud</h1>
<b>Your unified AI API platform for next-gen image, video, audio, and chat services</b><br/><br/>
<a href="https://platform.acedata.cloud"><img src="https://img.shields.io/badge/platform-blue?logo=cloudflare" alt="Platform"/></a>
<a href="https://docs.acedata.cloud"><img src="https://img.shields.io/badge/API%20Docs-green?logo=read-the-docs" alt="API Docs"/></a>
<a href="https://hub.acedata.cloud"><img src="https://img.shields.io/badge/Nexior-orange?logo=vue.js" alt="Nexior"/></a>
<a href="https://status.acedata.cloud"><img src="https://img.shields.io/badge/status-brightgreen?logo=uptimerobot" alt="Status"/></a>
</div>

## 🚀 What We Do

Ace Data Cloud offers a comprehensive suite of AI services spanning chat, image, video, and audio generation, all accessible through a unified API platform. Developers can integrate cutting-edge AI capabilities with ease and scale.

**7 AI services · 74 API endpoints · 5 categories**

## 📡 Service Catalog

### 💬 AI Chat

| Service      | API Endpoints                                                                                      | Stage                      |
|--------------|--------------------------------------------------------------------------------------------------|----------------------------|
| Gemini       | /gemini/chat/completions                                                                          | 🟡                         |
| Kimi         | /kimi/chat/completions                                                                            | 🟡                         |
| Claude       | /v1/chat/completions<br/>/v1/messages<br/>/v1/messages/count_tokens                               | 🟡🟡🟢                      |
| DeepSeek     | /deepseek/chat/completions                                                                        | 🟡                         |
| Grok         | /grok/chat/completions                                                                            | 🟡                         |
| OpenAI       | /openai/chat/completions<br/>/openai/embeddings<br/>/openai/responses                             | 🟢🟢🟢                      |

### 🖼️ AI Image

| Service      | API Endpoints                                                                                      | Stage                      |
|--------------|--------------------------------------------------------------------------------------------------|----------------------------|
| Nano Banana  | /nano-banana/images<br/>/nano-banana/tasks                                                       | 🟡🟢                      |
| Flux         | /flux/images<br/>/flux/tasks                                                                      | 🟢🟢                      |
| Midjourney   | /midjourney/imagine<br/>/midjourney/seed<br/>/midjourney/edits<br/>/midjourney/videos<br/>/midjourney/describe<br/>/midjourney/translate<br/>/midjourney/tasks | 🟢🟢🟢🟢🟢🟡🟢 |
| OpenAI       | /openai/images/generations<br/>/openai/images/edits                                              | 🟢🟡                      |

### 🎥 AI Video

| Service      | API Endpoints                                                                                      | Stage                      |
|--------------|--------------------------------------------------------------------------------------------------|----------------------------|
| Seedance     | /seedance/videos<br/>/seedance/tasks                                                             | 🟡🟢                      |
| Sora         | /sora/tasks<br/>/sora/videos                                                                     | 🟢🟢                      |
| Veo          | /veo/videos<br/>/veo/tasks                                                                        | 🟡🟢                      |
| Kling        | /kling/motion<br/>/kling/tasks<br/>/kling/videos                                                 | 🟢🟢🟢                      |
| Wan          | /wan/tasks<br/>/wan/videos                                                                        | 🟢🟢                      |
| Luma         | /luma/tasks<br/>/luma/videos                                                                      | 🟢🟡                      |
| Hailuo       | /hailuo/tasks<br/>/hailuo/videos                                                                  | 🟢🟡                      |
| Pixverse     | /pixverse (not listed in APIs, skip)                                                             | —                          |

### 🎵 AI Audio

| Service      | API Endpoints                                                                                      | Stage                      |
|--------------|--------------------------------------------------------------------------------------------------|----------------------------|
| Suno         | /suno/audios<br/>/suno/persona<br/>/suno/mp4<br/>/suno/timing<br/>/suno/vox<br/>/suno/wav<br/>/suno/midi<br/>/suno/style<br/>/suno/lyrics<br/>/suno/mashup-lyrics<br/>/suno/tasks<br/>/suno/upload | 🟢🟢🟢🟢🟢🟢🟡🟢🟢🟢🟢🟢 |
| Fish         | /fish/audios<br/>/fish/voices<br/>/fish/tasks                                                    | 🟢🟢🟢                      |
| Producer     | /producer/upload<br/>/producer/videos<br/>/producer/wav<br/>/producer/audios<br/>/producer/tasks<br/>/producer/lyrics | 🟢🟢🟢🟢🟢🟢 |

### 🌐 Web & Data

| Service      | API Endpoints                                                                                      | Stage                      |
|--------------|--------------------------------------------------------------------------------------------------|----------------------------|
| Serp         | /serp/google                                                                                    | 🟢                         |
| QRArt        | /qrart/generate<br/>/qrart/tasks                                                                | —🟢                      |
| ShortURL     | /shorturl                                                                                       | 🟢                         |

## 🔌 MCP Servers (Model Context Protocol)

Ace Data Cloud provides MCP servers that enable seamless AI model context integration for image, video, music, and search services.

| Server         | PyPI Badge                                                                                          | Description                                         |
|----------------|---------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| [MCPLuma](https://github.com/AceDataCloud/MCPLuma)           | [![PyPI](https://img.shields.io/pypi/v/mcp-luma.svg)](https://pypi.org/project/mcp-luma/)           | MCP Server for Luma AI Video Generation via AceDataCloud API |
| [MCPMidjourney](https://github.com/AceDataCloud/MCPMidjourney) | [![PyPI](https://img.shields.io/pypi/v/mcp-midjourney.svg)](https://pypi.org/project/mcp-midjourney/) | MCP Server for Midjourney AI Image Generation via AceDataCloud API |
| [MCPNanoBanana](https://github.com/AceDataCloud/MCPNanoBanana) | [![PyPI](https://img.shields.io/pypi/v/mcp-nanobanana-pro.svg)](https://pypi.org/project/mcp-nanobanana-pro/) | MCP Server for NanoBanana AI Image Generation via AceDataCloud API |
| [MCPSerp](https://github.com/AceDataCloud/MCPSerp)             | [![PyPI](https://img.shields.io/pypi/v/mcp-serp.svg)](https://pypi.org/project/mcp-serp/)             | MCP Server for Google SERP Search via AceDataCloud API |
| [MCPSora](https://github.com/AceDataCloud/MCPSora)             | [![PyPI](https://img.shields.io/pypi/v/mcp-sora.svg)](https://pypi.org/project/mcp-sora/)             | MCP Server for Sora AI Video Generation via AceDataCloud API |
| [MCPSuno](https://github.com/AceDataCloud/MCPSuno)             | [![PyPI](https://img.shields.io/pypi/v/mcp-suno.svg)](https://pypi.org/project/mcp-suno/)             | MCP Server for Suno AI Music Generation via AceDataCloud API |
| [MCPVeo](https://github.com/AceDataCloud/MCPVeo)               | [![PyPI](https://img.shields.io/pypi/v/mcp-veo.svg)](https://pypi.org/project/mcp-veo/)               | MCP Server for Veo AI Video Generation via AceDataCloud API |

```bash
pip install mcp-luma mcp-midjourney mcp-nanobanana-pro mcp-serp mcp-sora mcp-suno mcp-veo
```

## 📚 API Documentation Repos

Explore detailed API references and guides for Ace Data Cloud services:

[Docs API](https://github.com/AceDataCloud/Docs)

## 🌐 Live Services

| Service             | URL                        |
|---------------------|----------------------------|
| Developer Platform  | [platform.acedata.cloud](https://platform.acedata.cloud) |
| API Gateway        | [api.acedata.cloud](https://api.acedata.cloud)           |
| Nexior             | [hub.acedata.cloud](https://hub.acedata.cloud)           |
| Documentation      | [docs.acedata.cloud](https://docs.acedata.cloud)         |
| Dify AI            | [dify.acedata.cloud](https://dify.acedata.cloud)         |
| Status             | [status.acedata.cloud](https://status.acedata.cloud)     |
| Roadmap            | [roadmap.acedata.cloud](https://roadmap.acedata.cloud)   |

## ⚡ Quick Start

```bash
curl -X POST https://api.acedata.cloud/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello, Ace Data Cloud!"}]}'
```

Get your API key at [platform.acedata.cloud](https://platform.acedata.cloud) — free tier available.

## 💰 $ACE Token

The $ACE token powers the Ace Data Cloud ecosystem, enabling seamless transactions and rewards within our AI platform. Join the community and explore token utilities.

[View $ACE Token on Pump.fun](https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump)

## 📬 Connect

- Website: [https://acedata.cloud](https://acedata.cloud)
- Documentation: [https://docs.acedata.cloud](https://docs.acedata.cloud)
- Twitter/X: [https://twitter.com/AceDataCloud](https://twitter.com/AceDataCloud)
- Discord: [https://discord.gg/acedatacloud](https://discord.gg/acedatacloud)
