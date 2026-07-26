# 哪吒闹海 — Nezha Conquers the Dragon King

> A bilingual web storybook adapting the classic Chinese folktale **《哪吒闹海》** for high-school students, illustrated in **gongbi heavy-colour (工笔重彩)** painting style.

**[🌐 Live Demo](https://pimplesonnose.github.io/nezha/)**

---

## ✨ Features

- **Bilingual narration** — English and Chinese with separate pinyin blocks
- **8 gongbi heavy-colour illustrations** — AI-generated via Cloudflare FLUX-1-schnell
- **Pre-recorded audio** — Edge TTS: male English (GuyNeural, normal speed), female Mandarin (XiaoxiaoNeural, -8%)
- **Dark silk ground UI** — unique among sibling storybook apps
- **Rising embers + falling lotus petals** — signature particle effect
- **Tide-line progress** — wave-crest fill bar
- **Tidal drum audio console** — dragon-scale textured bottom bar
- **Keyboard shortcuts** — `← →` navigate, `Space` play/pause, `A` toggle autoplay
- **Mobile responsive**

## 🚀 Run Locally

```bash
cd nezha
python3 -m http.server 8000
# Open http://localhost:8000
```

## 🎨 Generate Assets

```bash
# Audio (Edge TTS)
python3 generate-audio.py

# Images (Cloudflare FLUX)
python3 generate-images.py
```

## 📁 Project Structure

```
nezha/
├── index.html                 # Single-page app shell
├── css/style.css              # Dark silk ground, gongbi heavy-colour theme
├── js/
│   ├── story-data.js          # 8 chapters: EN + ZH + Pinyin
│   └── app.js                 # Navigation, audio, particles, language toggle
├── images/                    # 8 gongbi heavy-colour illustrations
├── audio/
│   ├── en/                    # English narration (male, +0%)
│   └── zh/                    # Mandarin narration (female, -8%)
├── generate-audio.py          # Edge TTS script
├── generate-images.py         # Cloudflare FLUX script
├── PLAN.md                    # Full specification
└── README.md
```

## 📖 Story Source

Adapted from **《封神演义》** (Investiture of the Gods) and the 1979 Shanghai Animation Film Studio film **《哪吒闹海》**.

## 🎭 Design Philosophy

This app uses **gongbi heavy-colour (工笔重彩)** painting style — distinct from the ink-wash (水墨) style used in sibling storybook apps. The dark silk ground makes the saturated gongbi colours glow like museum-lit paintings.

**Five Sacred Colours (五色):** Cinnabar red · Azurite blue · Gold · Jade green · Ink black

## 📝 License

MIT

---

Crafted with 🤖 [Pi](https://pi.dev) | [Mimo](https://mimo.mi.com/)
