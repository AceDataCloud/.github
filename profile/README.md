<div align="center">
<img src="https://cdn.acedata.cloud/logo.png/thumb_450x_" alt="Ace Data Cloud" width="120" />
<h1>Ace Data Cloud</h1>
<b>One unified API for dozens of AI models — images, video, music, chat, search & more</b><br/><br/>
<a href="https://platform.acedata.cloud"><img src="https://img.shields.io/badge/platform-blue?style=flat-square" alt="Platform"/></a>
<a href="https://docs.acedata.cloud"><img src="https://img.shields.io/badge/docs-green?style=flat-square" alt="Docs"/></a>
<a href="https://hub.acedata.cloud"><img src="https://img.shields.io/badge/nexior-orange?style=flat-square" alt="Nexior"/></a>
<a href="https://status.acedata.cloud"><img src="https://img.shields.io/badge/status-brightgreen?style=flat-square" alt="Status"/></a>
</div>

## 🚀 What We Do

Ace Data Cloud provides a unified API gateway to access a wide range of AI services including chat, image, video, music, and search models. Our platform simplifies integration and accelerates AI-powered application development.

**31 services · 92 API endpoints · 1 category**

## 📡 Service Catalog

### 💬 AI Chat

| Service | Endpoints | Stage |
|---------|-----------|-------|
| Gemini Chat Completion API | /gemini/chat/completions | 🟡 |
| Kimi Chat Completion API | /kimi/chat/completions | 🟡 |
| Claude Chat Completion API<br/>Claude Messages API<br/>Claude Messages Count Tokens API | /v1/chat/completions<br/>/v1/messages<br/>/v1/messages/count_tokens | 🟡🟡🟢 |
| DeepSeek Chat Completion API | /deepseek/chat/completions | 🟡 |
| Grok Chat Completion API | /grok/chat/completions | 🟡 |
| AI Chat API | /aichat/conversations | 🟢 |
| OpenAI Chat Completion API | /openai/chat/completions | 🟢 |

### 🖼️ AI Image

| Service | Endpoints | Stage |
|---------|-----------|-------|
| ByteDance Seedream Images API<br/>ByteDance Seedream Tasks API | /seedream/images<br/>/seedream/tasks | 🟡🟢 |
| Nano Banana Generation API<br/>Nano Banana Tasks API | /nano-banana/images<br/>/nano-banana/tasks | 🟡🟢 |
| Flux Images Generation API<br/>Flux Tasks API | /flux/images<br/>/flux/tasks | 🟢🟢 |
| Midjourney Imagine API<br/>Midjourney Seed API<br/>Midjourney Edits API<br/>Midjourney Videos API<br/>Midjourney Describe API<br/>Midjourney Tasks API<br/> | /midjourney/imagine<br/>/midjourney/seed<br/>/midjourney/edits<br/>/midjourney/videos<br/>/midjourney/describe<br/>/midjourney/tasks | 🟢🟢🟢🟢🟢🟢 |
| Midjourney Translate API | /midjourney/translate | 🟡 |
| OpenAI Images Generations API<br/>OpenAI Images Edits API | /openai/images/generations<br/>/openai/images/edits | 🟢🟡 |
| Artistic QR Generation API<br/>Artistic QR Tasks API | /qrart/generate<br/>/qrart/tasks | —🟢 |
| Nano Banana AI image generation and editing service | /nano-banana/images<br/>/nano-banana/tasks | 🟡🟢 |

### 🎥 AI Video

| Service | Endpoints | Stage |
|---------|-----------|-------|
| ByteDance Seedance Videos API<br/>ByteDance Seedance Tasks API | /seedance/videos<br/>/seedance/tasks | 🟡🟢 |
| Sora Tasks API<br/>Sora Videos Generation API | /sora/tasks<br/>/sora/videos | 🟢🟢 |
| Veo Videos Generation API<br/>Veo Tasks API | /veo/videos<br/>/veo/tasks | 🟡🟢 |
| Kling Motion Generation API<br/>Kling Tasks API<br/>Kling Videos Generation API | /kling/motion<br/>/kling/tasks<br/>/kling/videos | 🟢🟢🟢 |
| Wan Tasks API<br/>Wan Videos Generation API | /wan/tasks<br/>/wan/videos | 🟢🟢 |
| Luma Tasks API<br/>Luma Videos Generation API | /luma/tasks<br/>/luma/videos | 🟢🟡 |
| Hailuo Tasks API<br/>Hailuo Videos Generation API | /hailuo/tasks<br/>/hailuo/videos | 🟢🟡 |

### 🎵 AI Audio

| Service | Endpoints | Stage |
|---------|-----------|-------|
| Suno Audios Generation API<br/>Suno Persona API<br/>Suno MP4 API<br/>Suno Timing API<br/>Suno Vox API<br/>Suno Wav API<br/>Suno Style API<br/>Suno Lyrics Generation API<br/>Suno MashupLyrics Generation API<br/>Suno Tasks API<br/>Suno Upload API<br/>Suno MIDI Generation API | /suno/audios<br/>/suno/persona<br/>/suno/mp4<br/>/suno/timing<br/>/suno/vox<br/>/suno/wav<br/>/suno/style<br/>/suno/lyrics<br/>/suno/mashup-lyrics<br/>/suno/tasks<br/>/suno/upload<br/>/suno/midi | 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟡 |
| Fish Audios Generation API<br/>Fish Voices Generation API<br/>Fish Tasks API | /fish/audios<br/>/fish/voices<br/>/fish/tasks | 🟢🟢🟢 |
| Producer Upload API<br/>Producer Videos API<br/>Producer Wav API<br/>Producer Audios Generation API<br/>Producer Tasks API<br/>Producer Lyrics Generation API | /producer/upload<br/>/producer/videos<br/>/producer/wav<br/>/producer/audios<br/>/producer/tasks<br/>/producer/lyrics | 🟢🟢🟢🟢🟢🟢 |

### 🌐 Web & Data

| Service | Endpoints | Stage |
|---------|-----------|-------|
| Google SERP API | /serp/google | 🟢 |
| Recognition Image2Text API | /captcha/recognition/image2text | 🟡 |
| Recognition Recaptcha2 API<br/>Token Recaptcha2 API<br/>Captcha Token Recaptcha3 API | /captcha/recognition/recaptcha2<br/>/captcha/token/recaptcha2<br/>/captcha/token/recaptcha3 | 🟡🟡🟡 |
| Recognition hCaptcha API<br/>Token hCaptcha API | /captcha/recognition/hcaptcha<br/>/captcha/token/hcaptcha | 🟡🟡 |
| ADSL Proxy Extract API<br/>ADSL Proxy Whitelist API | /adsl/extract<br/>/adsl/whitelist | 🟡🟢 |
| Localization Translate API | /localization/translate | 🟡 |
| Short URL API | /shorturl | 🟢 |
| Face Analyze API<br/>Face Beautify API<br/>Face ChangeAge API<br/>人脸性别转换 API<br/>Face DetectLive API<br/>Face Swap API<br/>人像动漫化 API | /face/analyze<br/>/face/beautify<br/>/face/change-age<br/>/face/change-gender<br/>/face/detect-live<br/>/face/swap<br/>/face/cartoon | 🔴🔴🔴🔴🔴🔴🔴 |
| 银行卡基础信息查询 API<br/>银行卡二要素核验 API<br/>银行卡三要素核验 API<br/>银行卡四要素核验 API<br/>身份证人像照片验证 API<br/>身份信息及有效期核验 API<br/>身份证识别及信息核验 API<br/>Identity Phone Check-1e API<br/>Identity Phone Check-2e API<br/>Identity Phone Check-3e API | /identity/bankcard/check-1e<br/>/identity/bankcard/check-2e<br/>/identity/bankcard/check-3e<br/>/identity/bankcard/check-4e<br/>/identity/idcard/check-1e<br/>/identity/idcard/check-2e<br/>/identity/idcard/ocr<br/>/identity/phone/check-1e<br/>/identity/phone/check-2e<br/>/identity/phone/check-3e | 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 |

## 🔌 MCP Servers

Ace Data Cloud offers MCP Servers to enable local deployment and integration of AI services using the Model Context Protocol.

| Server | Install | Description |
|--------|---------|-------------|
| [MCPLuma](https://github.com/AceDataCloud/MCPLuma) | `pip install mcp-luma` | Luma AI Video Generation |
| [MCPMidjourney](https://github.com/AceDataCloud/MCPMidjourney) | `pip install mcp-midjourney` | Midjourney AI Image Generation |
| [MCPNanoBanana](https://github.com/AceDataCloud/MCPNanoBanana) | `pip install mcp-nanobanana-pro` | NanoBanana AI Image Generation |
| [MCPSerp](https://github.com/AceDataCloud/MCPSerp) | `pip install mcp-serp` | Google SERP Search |
| [MCPSora](https://github.com/AceDataCloud/MCPSora) | `pip install mcp-sora` | Sora AI Video Generation |
| [MCPSuno](https://github.com/AceDataCloud/MCPSuno) | `pip install mcp-suno` | Suno AI Music Generation |
| [MCPVeo](https://github.com/AceDataCloud/MCPVeo) | `pip install mcp-veo` | Veo AI Video Generation |

## 📚 API Documentation Repos

[Flux API](https://github.com/AceDataCloud/FluxAPI) · [Luma API](https://github.com/AceDataCloud/LumaAPI) · [Midjourney API](https://github.com/AceDataCloud/MidjourneyAPI) · [Nano Banana API](https://github.com/AceDataCloud/NanoBananaAPI) · [Open AI API](https://github.com/AceDataCloud/OpenAIAPI) · [Pixverse API](https://github.com/AceDataCloud/PixverseAPI) · [Serp API](https://github.com/AceDataCloud/SerpAPI) · [Sora API](https://github.com/AceDataCloud/SoraAPI) · [Suno API](https://github.com/AceDataCloud/SunoAPI) · [Veo API](https://github.com/AceDataCloud/VeoAPI)

## 🌐 Live Services

| Service | URL | Description |
|---------|-----|-------------|
| Developer Platform | platform.acedata.cloud | API keys, billing, service management |
| API Gateway | api.acedata.cloud | Unified endpoint for all services |
| Nexior | hub.acedata.cloud | Consumer AI app (chat, images, video, music) |
| Documentation | docs.acedata.cloud | API reference & guides |
| Dify AI | dify.acedata.cloud | AI workflow builder |
| Status | status.acedata.cloud | Uptime monitoring |
| Roadmap | roadmap.acedata.cloud | Public product roadmap |

## ⚡ Quick Start

```bash
curl https://api.acedata.cloud/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello, Ace Data Cloud!"}]}'
```

Get your free API key → [platform.acedata.cloud](https://platform.acedata.cloud)

## 💰 $ACE Token

The $ACE token powers the Ace Data Cloud ecosystem, enabling decentralized governance and rewards. Learn more at [https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump](https://pump.fun/coin/GnHpRsrcyfHSMZNzmpjAzTFQA26vnbRMzbKQ11ZKpump)

## 📬 Connect

- 🌐 Website: [platform.acedata.cloud](https://platform.acedata.cloud)
- 📖 Documentation: [docs.acedata.cloud](https://docs.acedata.cloud)
- 🐦 Twitter / X: [x.com/AceDataCloud](https://x.com/AceDataCloud)
- 💬 Discord: [discord.gg/aedatacloud](https://discord.gg/aedatacloud)
