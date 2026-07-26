# 哪吒闹海 — Nezha Conquers the Dragon King

> 一个双语网页故事书，改编自中国传统民间传说**《哪吒闹海》**，面向高中生，配以**工笔重彩**风格插图。

**[🌐 在线演示](https://pimplesonnose.github.io/nezha/)**

---

## ✨ 特色功能

- **双语朗读** — 中文（汉字 + 拼音）与英文一键切换
- **8幅工笔重彩插图** — 通过 Cloudflare FLUX-1-schnell AI 生成
- **逐章音频** — Edge TTS：英文男声（GuyNeural，正常速度）+ 中文女声（XiaoxiaoNeural，-8%减速）
- **暗色丝绸底色** — 区别于其他故事书应用的独特设计
- **上升火星 + 飘落莲花瓣** — 标志性粒子效果
- **潮汐进度条** — 波浪填充动画
- **潮鼓音频控制台** — 龙鳞纹理底栏
- **键盘快捷键** — `← →` 切换章节，`空格键` 播放/暂停，`A` 切换自动播放
- **移动端自适应**

## 🚀 本地运行

```bash
cd nezha
python3 -m http.server 8000
# 打开 http://localhost:8000
```

## 🎨 生成素材

```bash
# 音频（Edge TTS）
python3 generate-audio.py

# 插图（Cloudflare FLUX）
python3 generate-images.py
```

## 📁 项目结构

```
nezha/
├── index.html                 # 单页应用外壳
├── css/style.css              # 暗色丝绸底色，工笔重彩主题
├── js/
│   ├── story-data.js          # 8章：英文 + 中文 + 拼音
│   └── app.js                 # 导航、音频、粒子、语言切换
├── images/                    # 8幅工笔重彩插图
├── audio/
│   ├── en/                    # 英文朗读（男声，正常速度）
│   └── zh/                    # 中文朗读（女声，-8%减速）
├── generate-audio.py          # Edge TTS 脚本
├── generate-images.py         # Cloudflare FLUX 脚本
├── PLAN.md                    # 完整设计文档
└── README.md
```

## 📖 故事来源

改编自**《封神演义》**与1979年上海美术电影制片厂动画电影**《哪吒闹海》**。

## 🎭 设计理念

本应用采用**工笔重彩**绘画风格——与姊妹故事书应用的水墨风格截然不同。暗色丝绸底色使饱和的工笔色彩如同博物馆灯光下的画作般熠熠生辉。

**五色（五色）：** 朱砂红 · 石青蓝 · 金色 · 石绿 · 墨黑

## 📝 许可证

MIT

---

Crafted with 🤖 [Pi](https://pi.dev) | [Mimo](https://mimo.mi.com/)
