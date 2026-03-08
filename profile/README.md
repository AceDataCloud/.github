<div align="center">
<img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />
<h1>Ace Data Cloud</h1>
<b>Unified AI API platform for chat, image, video, and audio generation</b><br/>
<a href="https://platform.acedata.cloud"><img src="https://img.shields.io/badge/Platform-blue?style=flat-square" /></a>
<a href="https://docs.acedata.cloud"><img src="https://img.shields.io/badge/API%20Docs-green?style=flat-square" /></a>
<a href="https://hub.acedata.cloud"><img src="https://img.shields.io/badge/Nexior-orange?style=flat-square" /></a>
<a href="https://status.acedata.cloud"><img src="https://img.shields.io/badge/Status-brightgreen?style=flat-square" /></a>
</div>

## 🚀 What We Do

Ace Data Cloud offers a comprehensive unified AI API platform enabling developers to integrate advanced AI capabilities including chat, image, video, and audio generation through a single, consistent interface.

## 📡 Service Catalog

### 💬 AI Chat

| Service                    | API Endpoints                                                                                  | Stage   |
|----------------------------|-----------------------------------------------------------------------------------------------|---------|
| OpenAI (GPT / DALL-E)      | `GET /openai/chat/completions`<br/>`GET /openai/embeddings`<br/>`GET /openai/responses`       | 🟢      |
|                            | `GET /openai/images/generations`<br/>`GET /openai/images/edits`                               | 🟡      |
| AI Chat API                | `GET /aichat/conversations`                                                                   | 🟢      |
| Claude                    | `GET /v1/chat/completions`<br/>`GET /v1/messages`<br/>`GET /v1/messages/count_tokens`          | 🟡<br/>🟡<br/>🟢 |
| Grok                      | `GET /grok/chat/completions`                                                                  | 🟡      |
| DeepSeek                  | `GET /deepseek/chat/completions`                                                              | 🟡      |

### 🖼 AI Image

| Service                    | API Endpoints                                                                                  | Stage   |
|----------------------------|-----------------------------------------------------------------------------------------------|---------|
| Midjourney                 | `GET /midjourney/imagine`<br/>`GET /midjourney/seed`<br/>`GET /midjourney/edits`<br/>`GET /midjourney/videos`<br/>`GET /midjourney/describe`<br/>`GET /midjourney/translate`<br/>`GET /midjourney/tasks` | 🟢<br/>🟢<br/>🟢<br/>🟢<br/>🟢<br/>🟡<br/>🟢 |
| Flux                      | `GET /flux/images`<br/>`GET /flux/tasks`                                                      | 🟢      |
| Nano Banana               | `GET /nano-banana/images`<br/>`GET /nano-banana/tasks`                                        | 🟡<br/>🟢 |
| Seedream                  | `GET /seedream/images`<br/>`GET /seedream/tasks`                                              | 🟡<br/>🟢 |
| Artistic QR               | `GET /qrart/generate`<br/>`GET /qrart/tasks`                                                 | <br/>🟢  |

### 🎬 AI Video

| Service                    | API Endpoints                                                                                  | Stage   |
|----------------------------|-----------------------------------------------------------------------------------------------|---------|
| Midjourney                 | `GET /midjourney/videos`                                                                      | 🟢      |
| Luma                      | `GET /luma/tasks`<br/>`GET /luma/videos`                                                     | 🟢<br/>🟡 |
| Sora                      | `GET /sora/tasks`<br/>`GET /sora/videos`                                                     | 🟢<br/>🟢 |
| Veo                       | `GET /veo/videos`<br/>`GET /veo/tasks`                                                       | 🟡<br/>🟢 |
| Kling                     | `GET /kling/motion`<br/>`GET /kling/tasks`<br/>`GET /kling/videos`                           | 🟢      |
| Wan                       | `GET /wan/tasks`<br/>`GET /wan/videos`                                                       | 🟢      |
| Seedance                  | `GET /seedance/videos`<br/>`GET /seedance/tasks`                                             | 🟡<br/>🟢 |
| Hailuo                    | `GET /hailuo/tasks`<br/>`GET /hailuo/videos`                                                 | 🟢<br/>🟡 |

### 🎵 AI Audio

| Service                    | API Endpoints                                                                                  | Stage   |
|----------------------------|-----------------------------------------------------------------------------------------------|---------|
| Suno                      | `GET /suno/audios`<br/>`GET /suno/persona`<br/>`GET /suno/mp4`<br/>`GET /suno/timing`<br/>`GET /suno/vox`<br/>`GET /suno/wav`<br/>`GET /suno/midi`<br/>`GET /suno/style`<br/>`GET /suno/lyrics`<br/>`GET /suno/mashup-lyrics`<br/>`GET /suno/tasks`<br/>`GET /suno/upload` | 🟢<br/>🟢<br/>🟢<br/>🟢<br/>🟢<br/>🟢<br/>🟡<br/>🟢<br/>🟢<br/>🟢<br/>🟢<br/>🟢 |
| Fish                      | `GET /fish/audios`<br/>`GET /fish/voices`<br/>`GET /fish/tasks`                              | 🟢      |
| Producer                  | `GET /producer/upload`<br/>`GET /producer/videos`<br/>`GET /producer/wav`<br/>`GET /producer/audios`<br/>`GET /producer/tasks`<br/>`GET /producer/lyrics` | 🟢      |

### 🔍 Web & Data

| Service                    | API Endpoints                                                                                  | Stage   |
|----------------------------|-----------------------------------------------------------------------------------------------|---------|
| Google SERP                | `GET /serp/google`                                                                            | 🟢      |

## 🔌 MCP Servers (Model Context Protocol)

| Server           | PyPI                                                                                                          | Description                       |
|------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------|
| [MCPLuma](https://github.com/AceDataCloud/MCPLuma)           | [![PyPI](https://img.shields.io/pypi/v/mcp-luma?style=flat-square)](https://pypi.org/project/mcp-luma/)           | Luma AI Video Generation        |
| [MCPMidjourney](https://github.com/AceDataCloud/MCPMidjourney) | [![PyPI](https://img.shields.io/pypi/v/mcp-midjourney?style=flat-square)](https://pypi.org/project/mcp-midjourney/) | Midjourney AI Image Generation  |
| [MCPNanoBanana](https://github.com/AceDataCloud/MCPNanoBanana) | [![PyPI](https://img.shields.io/pypi/v/mcp-nanobanana-pro?style=flat-square)](https://pypi.org/project/mcp-nanobanana-pro/) | NanoBanana AI Image Generation  |
| [MCPSerp](https://github.com/AceDataCloud/MCPSerp)           | [![PyPI](https://img.shields.io/pypi/v/mcp-serp?style=flat-square)](https://pypi.org/project/mcp-serp/)           | Google SERP Search              |
| [MCPSora](https://github.com/AceDataCloud/MCPSora)           | [![PyPI](https://img.shields.io/pypi/v/mcp-sora?style=flat-square)](https://pypi.org/project/mcp-sora/)           | Sora AI Video Generation        |
| [MCPSuno](https://github.com/AceDataCloud/MCPSuno)           | [![PyPI](https://img.shields.io/pypi/v/mcp-suno?style=flat-square)](https://pypi.org/project/mcp-suno/)           | Suno AI Music Generation        |
| [MCPVeo](https://github.com/AceDataCloud/MCPVeo)             | [![PyPI](https://img.shields.io/pypi/v/mcp-veo?style=flat-square)](https://pypi.org/project/mcp-veo/)             | Veo AI Video Generation         |

```bash
pip install mcp-luma mcp-midjourney mcp-nanobanana-pro mcp-serp mcp-sora mcp-suno mcp-veo
```

## 📚 API Documentation Repos

Explore detailed API references and guides for our AI services:

[Flux API](https://github.com/AceDataCloud/FluxAPI) · [Luma API](https://github.com/AceDataCloud/LumaAPI) · [Midjourney API](https://github.com/AceDataCloud/MidjourneyAPI) · [Nano Banana API](https://github.com/AceDataCloud/NanoBananaAPI) · [OpenAI API](https://github.com/AceDataCloud/OpenAIAPI) · [Pixverse API](https://github.com/AceDataCloud/PixverseAPI) · [Serp API](https://github.com/AceDataCloud/SerpAPI) · [Sora API](https://github.com/AceDataCloud/SoraAPI) · [Suno API](https://github.com/AceDataCloud/SunoAPI) · [Veo API](https://github.com/AceDataCloud/VeoAPI)

## 🌐 Live Services

| Service             | URL                      | Description                                |
|---------------------|--------------------------|--------------------------------------------|
| Developer Platform  | platform.acedata.cloud   | API keys, docs, billing, analytics         |
| API Gateway         | api.acedata.cloud        | OpenAI-compatible REST API endpoint        |
| Nexior              | hub.acedata.cloud        | Consumer app - chat, generate images/video/music |
| Documentation       | docs.acedata.cloud       | Quickstart guides and API references       |
| Dify AI             | dify.acedata.cloud       | Visual AI workflow builder                  |
| Status              | status.acedata.cloud     | Real-time service health monitoring        |
| Roadmap             | roadmap.acedata.cloud    | Public feature roadmap                      |

## ⚡ Quick Start

```bash
curl -X POST "https://api.acedata.cloud/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello, world!"}]}'
```

Get your API key at [platform.acedata.cloud](https://platform.acedata.cloud) - free tier available.

## 💰 $ACE Token

$ACE is the native utility token powering the Ace Data Cloud ecosystem, enabling seamless transactions and rewards across our AI API platform. Learn more at [https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump](https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump).

## 📬 Connect

- Website: [platform.acedata.cloud](https://platform.acedata.cloud)  
- Documentation: [docs.acedata.cloud](https://docs.acedata.cloud)  
- Twitter/X: [x.com/AceDataCloud](https://x.com/AceDataCloud)  
- Discord: [discord.gg/aedatacloud](https://discord.gg/aedatacloud)
