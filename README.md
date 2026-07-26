# ⚡ 哪吒闹海 — Nezha Conquers the Dragon King

> *析骨还父，析肉还母。从莲花与烈焰中，他重新站起。*
> *Return bone to father, flesh to mother. From lotus and flame, he rises again.*

A bilingual, illustrated web storybook adapting the classic Chinese folktale **《哪吒闹海》 (Nézhā Nào Hǎi / Nezha Conquers the Dragon King)** for high-school students — narrated in Mandarin and English with **gongbi heavy-colour (工笔重彩)** illustration, themed around the Shang dynasty world of the *Investiture of the Gods*.

[![Live Demo](https://img.shields.io/badge/Live-Demo-161616?style=flat-square&logo=githubpages)](https://pimplesonnose.github.io/nezha/)
[![License: MIT](https://img.shields.io/badge/License-MIT-inherit?style=flat-square)](LICENSE)
[![Audience](https://img.shields.io/badge/Audience-High%20School-cinnabar?style=flat-square)](https://github.com)

---

## 🌟 Features

| | |
|---|---|
| 🎨 **Gongbi heavy-colour illustrations** | 8 工笔重彩 scenes, AI-generated with mineral-pigment-on-silk aesthetic |
| 🔤 **Bilingual narration** | Toggle English ↔ Chinese at any moment |
| 📖 **Two-block Hanzi + pinyin** | Chinese and pinyin render as two adjacent text blocks (line-aligned) |
| 🇨🇳 **Mandarin audio** | Female voice (Xiaoxiao), slowed -8% for clarity |
| 🇺🇸 **English audio** | Male voice (Guy), natural pace |
| ▶️ **Auto-play** | Seamless chapter-to-chapter narration |
| 🔥 **Dark silk ground UI** | Unique dark theme — gongbi colours glow like museum-lit paintings |
| 🪷 **Rising embers + falling petals** | Cinnabar flame-embers rise, pink lotus-petals fall — fire and lotus duality |
| 🌊 **Tide-line progress** | Wave-crest fill bar tracks your journey through the story |
| 🥁 **Tidal drum audio console** | Dragon-scale textured bottom bar with cinnabar playhead |
| ⌨️ **Keyboard shortcuts** | `← →` navigate · `Space` play/pause · `A` autoplay |
| 📱 **Responsive** | Reads beautifully on phone, tablet, and desktop |

---

## 📖 The Story

In the Shang dynasty, the fortress of Chentang Pass stood guard over the eastern coast. Its commander, Li Jing, awaited the birth of his third child — a pregnancy that had lasted three years and six months. What emerged was not a baby but a glistening flesh ball. When Li Jing struck it with his sword, a boy leapt forth: **Nezha**, destined to shake the Dragon King's palace to its foundations.

Armed with the Universe Ring and the Red Armillary Sash, seven-year-old Nezha bathed in the sea — and accidentally sent tremors through the Crystal Palace. The Dragon King's Yaksha general came to punish him; Nezha fought back. Then came Ao Bing, the Third Prince, who was slain in turn. When all Four Dragon Kings gathered at the gates of Chentang Pass and demanded Li Jing surrender his son, Nezha made a choice that would echo through two thousand years of Chinese memory:

> *"析骨还父，析肉还母。"*
> *"I return my bones to my father, and my flesh to my mother."*

He fell. But death was not the end. His master, Taiyi Zhenren, rebuilt his body from lotus roots and petals. Nezha rose again — reborn, more powerful, wielding the Fire-Tipped Spear and Wind-Fire Wheels. He defeated the Four Dragon Kings and ended their reign of terror forever.

**Moral:** Justice sometimes requires extraordinary courage — the courage to face the consequences of one's own actions, to sacrifice for others, and to rise again with purpose. True strength is not power; it is moral responsibility.

### 8 Chapters · 8 Illustrations · 16 Narrations · 1 Eternal Legend

| # | English | Chinese | Scene |
|---|---------|---------|-------|
| 1 | The Flesh Ball | 肉球降世 | Li Jing's fortress: the luminous flesh ball splits open, a boy leaps forth |
| 2 | The Dragon King's Toll | 龙王的索求 | The Crystal Palace: Ao Guang demands child sacrifices from the human world |
| 3 | The Boy at the Sea | 海边的少年 | Chentang Pass shore: Nezha bathes, the Red Sash shakes the ocean |
| 4 | The Death of Ao Bing | 敖丙之死 | A violent sea battle: Nezha vs. the Dragon King's Third Prince |
| 5 | The Four Kings at the Gate | 四海龙王临关 | Thunder and rain: four Dragon Kings demand Li Jing surrender his son |
| 6 | Returning Flesh and Bone | 析骨还父 | The emotional climax: Nezha's ultimate sacrifice for his people |
| 7 | The Lotus Reborn | 莲花化身 | Kunlun Mountain: Taiyi Zhenren rebuilds Nezha from lotus |
| 8 | The Third Lotus Prince | 莲花三太子 | The triumphant finale: Three Heads, Six Arms, the Dragon Kings defeated |

---

## 🛠️ Tech Stack

- **Frontend** — Vanilla HTML, CSS, JavaScript (zero dependencies)
- **Illustrations** — Cloudflare Workers AI (FLUX-1-schnell) with gongbi heavy-colour prompts
- **Narration** — Edge TTS (`edge-tts` Python library)

### Generate Assets

```bash
# 1. Generate illustrations (requires Cloudflare API keys)
python3 generate-images.py

# 2. Generate audio narration
python3 generate-audio.py

# 3. Serve locally
python3 -m http.server 8000
# → http://localhost:8000
```

---

## 🎵 Audio Voices

| Language | Voice | Speed | Character |
|----------|-------|-------|-----------|
| Mandarin (中文) | `zh-CN-XiaoxiaoNeural` | -8% (slower, clearer for learners) | Female narrator |
| English | `en-US-GuyNeural` | +0% (natural pace) | Male narrator |

---

## 📁 Project Structure

```
nezha/
├── index.html              # Single-page app
├── PLAN.md                 # Full build plan & research
├── README.md               # This file
├── README_CN.md            # 中文版说明
├── LICENSE                 # MIT
├── .gitignore
├── .nojekyll
├── css/
│   └── style.css           # Dark silk ground, gongbi heavy-colour theme
├── js/
│   ├── story-data.js       # Bilingual story content (8 chapters)
│   └── app.js              # App logic · navigation · audio · particles
├── images/
│   ├── chapter-1.webp …    # Served illustrations
│   └── raw/                # Generated originals
├── audio/
│   ├── en/                 # English mp3 files
│   └── zh/                 # Mandarin mp3 files
├── generate-images.py      # Cloudflare FLUX image generation
└── generate-audio.py       # Edge TTS audio generation
```

---

## 🎨 Design Theme

The visual identity is inspired by **gongbi heavy-colour (工笔重彩) painting** — the meticulous, richly saturated technique of Tang and Ming dynasty court illustration. Unlike the ink-wash (水墨) aesthetic of sibling storybook apps, Nezha uses a **dark silk ground** that makes the jewel-like mineral pigments glow, the way gongbi paintings are dramatically lit in museum display cases.

**Five Sacred Colours (五色):** Cinnabar red (朱砂) · Azurite blue (石青) · Gold (金) · Jade green (石绿) · Ink black (墨)

The interface embodies the story's core duality: **fire + lotus** — destructive power and restorative purity. Rising cinnabar embers drift upward like the Wind-Fire Wheels' sparks; falling pink lotus petals drift downward like rebirth. The progress bar is a tide filling with azurite blue. The audio console is a dragon-scale drum. Chapter dividers are stamped with a single cinnabar lotus petal.

---

## 🌐 Deploy

GitHub Pages is enabled on the `main` branch for automatic deployment.

**Live demo:** [https://pimplesonnose.github.io/nezha/](https://pimplesonnose.github.io/nezha/)

---

## 📚 Story Source

Adapted from **《封神演义》** (*Fēngshén Yǎnyì / Investiture of the Gods*, Ming dynasty, 1567) and the 1979 Shanghai Animation Film Studio film **《哪吒闹海》** (*Nezha Conquers the Dragon King*) — the first Chinese animated film screened at the Cannes Film Festival.

---

*Built with ❤️ for high-school students exploring Chinese mythology and moral philosophy.*

Crafted with 🤖 [Pi](https://pi.dev) | [Mimo](https://mimo.mi.com/)
