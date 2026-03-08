<div align="center">
<img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />
<h1>Ace Data Cloud</h1>
<b>One unified API for dozens of AI models — images, video, music, chat, search & more</b><br/><br/>
<a href="https://platform.acedata.cloud"><img src="https://img.shields.io/badge/platform-blue?style=flat-square&logo=cloudflare" alt="Platform" /></a>
<a href="https://docs.acedata.cloud"><img src="https://img.shields.io/badge/docs-green?style=flat-square&logo=read-the-docs" alt="Docs" /></a>
<a href="https://hub.acedata.cloud"><img src="https://img.shields.io/badge/nexior-orange?style=flat-square&logo=vue.js" alt="Nexior" /></a>
<a href="https://status.acedata.cloud"><img src="https://img.shields.io/badge/status-brightgreen?style=flat-square&logo=uptimerobot" alt="Status" /></a>
</div>

## 🚀 What We Do

Ace Data Cloud provides a unified API platform that integrates dozens of AI models across multiple domains including chat, image, video, audio, and web data services. Developers can access a broad range of AI capabilities through a single, consistent interface.

**23 services · 71 API endpoints · 5 categories**

## 📡 Service Catalog

### 💬 AI Chat

| Service      | Endpoints                                                                                     | Stage        |
|--------------|-----------------------------------------------------------------------------------------------|--------------|
| Gemini AI    | /gemini/chat/completions                                                                      | 🟡           |
| Kimi         | /kimi/chat/completions                                                                        | 🟡           |
| Claude AI    | /v1/chat/completions<br/>/v1/messages<br/>/v1/messages/count_tokens                            | 🟡🟡🟢       |
| DeepSeek AI  | /deepseek/chat/completions                                                                    | 🟡           |
| Grok         | /grok/chat/completions                                                                        | 🟡           |
| OpenAI generation | /openai/chat/completions<br/>/openai/embeddings<br/>/openai/images/generations<br/>/openai/responses<br/>/openai/images/edits | 🟢🟢🟢🟢🟡 |

### 🖼️ AI Image

| Service                 | Endpoints                                                                                         | Stage        |
|-------------------------|-------------------------------------------------------------------------------------------------|--------------|
| ByteDance Seedream Image Generation | /seedream/images<br/>/seedream/tasks                                                        | 🟡🟢       |
| Nano Banana Image Generation | /nano-banana/images<br/>/nano-banana/tasks                                                    | 🟡🟢       |
| Flux Image Generation    | /flux/images<br/>/flux/tasks                                                                     | 🟢🟢       |
| Midjourney generation    | /midjourney/imagine<br/>/midjourney/seed<br/>/midjourney/edits<br/>/midjourney/videos<br/>/midjourney/describe<br/>/midjourney/translate<br/>/midjourney/tasks | 🟢🟢🟢🟢🟢🟡🟢 |
| Face Transformation     | /face/analyze<br/>/face/beautify<br/>/face/change-age<br/>/face/change-gender<br/>/face/detect-live<br/>/face/swap<br/>/face/cartoon | 🔴🔴🔴🔴🔴🔴🔴 |
| Art QR Code Generation  | /qrart/generate<br/>/qrart/tasks                                                                 | —🟢       |

### 🎥 AI Video

| Service                     | Endpoints                                                                                     | Stage        |
|-----------------------------|-----------------------------------------------------------------------------------------------|--------------|
| ByteDance Seedance Video Generation | /seedance/videos<br/>/seedance/tasks                                                    | 🟡🟢       |
| Sora Video Generation       | /sora/tasks<br/>/sora/videos                                                                  | 🟢🟢       |
| Veo Video Generation        | /veo/videos<br/>/veo/tasks                                                                    | 🟡🟢       |
| Kling video generation      | /kling/motion<br/>/kling/tasks<br/>/kling/videos                                              | 🟢🟢🟢     |
| Tongyi Wansiang Video Generation | /wan/tasks<br/>/wan/videos                                                                | 🟢🟢       |
| Luma Video Generation       | /luma/tasks<br/>/luma/videos                                                                  | 🟢🟡       |
| Hailuo Video Generation     | /hailuo/tasks<br/>/hailuo/videos                                                              | 🟢🟡       |

### 🎵 AI Audio

| Service                  | Endpoints                                                                                       | Stage        |
|--------------------------|-------------------------------------------------------------------------------------------------|--------------|
| Suno Music Generation    | /suno/audios<br/>/suno/persona<br/>/suno/mp4<br/>/suno/timing<br/>/suno/vox<br/>/suno/wav<br/>/suno/midi<br/>/suno/style<br/>/suno/lyrics<br/>/suno/mashup-lyrics<br/>/suno/tasks<br/>/suno/upload | 🟢🟢🟢🟢🟢🟢🟡🟢🟢🟢🟢🟢 |
| Fish music generation    | /fish/audios<br/>/fish/voices<br/>/fish/tasks                                                   | 🟢🟢🟢     |
| Producer Music Generation | /producer/upload<br/>/producer/videos<br/>/producer/wav<br/>/producer/audios<br/>/producer/tasks<br/>/producer/lyrics | 🟢🟢🟢🟢🟢🟢 |

### 🌐 Web & Data

| Service       | Endpoints         | Stage  |
|---------------|-------------------|--------|
| Search Engine | /serp/google      | 🟢     |

## 🔌 MCP Servers

Ace Data Cloud offers MCP Servers to enable local or private deployments of AI services, providing scalable and flexible AI model hosting.

| Server          | Install                | Description               |
|-----------------|------------------------|---------------------------|
| [MCPLuma](https://github.com/AceDataCloud/MCPLuma)           | `pip install mcp-luma`           | Luma AI Video Generation       |
| [MCPMidjourney](https://github.com/AceDataCloud/MCPMidjourney) | `pip install mcp-midjourney`     | Midjourney AI Image Generation  |
| [MCPNanoBanana](https://github.com/AceDataCloud/MCPNanoBanana) | `pip install mcp-nanobanana-pro` | NanoBanana AI Image Generation  |
| [MCPSerp](https://github.com/AceDataCloud/MCPSerp)             | `pip install mcp-serp`            | Google SERP Search              |
| [MCPSora](https://github.com/AceDataCloud/MCPSora)             | `pip install mcp-sora`            | Sora AI Video Generation        |
| [MCPSuno](https://github.com/AceDataCloud/MCPSuno)             | `pip install mcp-suno`            | Suno AI Music Generation        |
| [MCPVeo](https://github.com/AceDataCloud/MCPVeo)               | `pip install mcp-veo`             | Veo AI Video Generation         |

## 📚 API Documentation Repos

[Flux API](https://github.com/AceDataCloud/FluxAPI) · [Luma API](https://github.com/AceDataCloud/LumaAPI) · [Midjourney API](https://github.com/AceDataCloud/MidjourneyAPI) · [Nano Banana API](https://github.com/AceDataCloud/NanoBananaAPI) · [OpenAI API](https://github.com/AceDataCloud/OpenAIAPI) · [Pixverse API](https://github.com/AceDataCloud/PixverseAPI) · [Serp API](https://github.com/AceDataCloud/SerpAPI) · [Sora API](https://github.com/AceDataCloud/SoraAPI) · [Suno API](https://github.com/AceDataCloud/SunoAPI) · [Veo API](https://github.com/AceDataCloud/VeoAPI)

## 🌐 Live Services

| Service             | URL                      | Description                                  |
|---------------------|--------------------------|----------------------------------------------|
| Developer Platform  | platform.acedata.cloud   | API keys, billing, service management        |
| API Gateway        | api.acedata.cloud        | Unified endpoint for all services             |
| Nexior             | hub.acedata.cloud        | Consumer AI app (chat, images, video, music) |
| Documentation      | docs.acedata.cloud       | API reference & guides                         |
| Dify AI            | dify.acedata.cloud       | AI workflow builder                            |
| Status             | status.acedata.cloud     | Uptime monitoring                              |
| Roadmap            | roadmap.acedata.cloud    | Public product roadmap                         |

## ⚡ Quick Start

```bash
curl https://api.acedata.cloud/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello, world!"}]}'
```

Get your free API key → [platform.acedata.cloud](https://platform.acedata.cloud)

## 💰 $ACE Token

The $ACE token powers the Ace Data Cloud ecosystem, enabling decentralized governance and incentives. Learn more and track it at [https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump](https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump)

## 📬 Connect

- 🌐 Website: [platform.acedata.cloud](https://platform.acedata.cloud)
- 📖 Documentation: [docs.acedata.cloud](https://docs.acedata.cloud)
- 🐦 Twitter / X: [x.com/AceDataCloud](https://x.com/AceDataCloud)
- 💬 Discord: [discord.gg/aedatacloud](https://discord.gg/aedatacloud)
