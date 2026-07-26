#!/usr/bin/env python3
"""
Generate narration audio for 哪吒闹海 using MiMo TTS.
Chinese: 冰糖 (female, slowed 5%)
English: Chloe (female, normal speed)
"""
import json
import os
import re
import sys
import time
import base64
from pathlib import Path
from urllib.request import Request, urlopen

# Load API key
env_path = Path.home() / ".pi" / "agent" / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("MIMO_API_KEY="):
                os.environ["MIMO_API_KEY"] = line.split("=", 1)[1].strip().strip('"')

API_KEY = os.environ.get("MIMO_API_KEY", "")
API_URL = "https://token-plan-sgp.xiaomimimo.com/v1/chat/completions"

if not API_KEY:
    print("❌ MIMO_API_KEY not found in ~/.pi/agent/.env", file=sys.stderr)
    sys.exit(1)

# ═══════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════
ENGLISH_VOICE  = "Chloe"
MANDARIN_VOICE = "冰糖"
ENGLISH_SPEED  = 1.0    # normal
MANDARIN_SPEED = 0.95   # slowed 5%
ENGLISH_STYLE  = "Epic narrator voice, deep and dramatic, like telling an ancient Chinese legend. Slow measured pace, gravitas, authoritative."
MANDARIN_STYLE = "沉稳大气的女声旁白，语速稍慢，像在讲述一个古老的神话传说。语气庄重，带有敬畏感。"
# ═══════════════════════════════════════════

AUDIO_DIR_EN = Path("audio/en")
AUDIO_DIR_ZH = Path("audio/zh")


def call_tts(text, voice, style, speed=1.0):
    """Call MiMo TTS API and return audio bytes."""
    payload = {
        "model": "mimo-v2.5-tts",
        "messages": [
            {"role": "user", "content": style},
            {"role": "assistant", "content": text}
        ],
        "audio": {
            "format": "mp3",
            "voice": voice,
            "speed": speed
        }
    }
    req = Request(API_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        })
    with urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    if "error" in data:
        raise Exception(data["error"]["message"])
    return base64.b64decode(data["choices"][0]["message"]["audio"]["data"])


def get_chapters():
    """Parse js/story-data.js and extract chapter data."""
    js_path = Path("js/story-data.js")
    if not js_path.exists():
        print(f"❌ {js_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(js_path, "r", encoding="utf-8") as f:
        code = f.read()

    chapters = []
    chapter_pattern = re.compile(
        r'id:\s*(\d+).*?'
        r'title:\s*\{.*?'
        r'en:\s*"((?:[^"\\]|\\.)*)".*?'
        r'zh:\s*"((?:[^"\\]|\\.)*)".*?'
        r'pinyin:\s*"((?:[^"\\]|\\.)*)".*?'
        r'\}.*?'
        r'content:\s*\{.*?'
        r'en:\s*"((?:[^"\\]|\\.)*)".*?'
        r'zh:\s*"((?:[^"\\]|\\.)*)".*?'
        r'pinyin:\s*"((?:[^"\\]|\\.)*)"',
        re.DOTALL
    )

    for m in chapter_pattern.finditer(code):
        chapters.append({
            "id": int(m.group(1)),
            "title_en": m.group(2).replace('\\n', '\n').replace('\\"', '"'),
            "title_zh": m.group(3).replace('\\n', '\n').replace('\\"', '"'),
            "content_en": m.group(5).replace('\\n', '\n').replace('\\"', '"'),
            "content_zh": m.group(6).replace('\\n', '\n').replace('\\"', '"'),
        })

    return chapters


def generate_english(chapters):
    """Generate English narration (Chloe, normal speed)."""
    print("\n🗣️  ENGLISH — Chloe (female, normal)")
    print("-" * 40)
    AUDIO_DIR_EN.mkdir(parents=True, exist_ok=True)

    ok = 0
    for ch in chapters:
        filename = f"chapter-{ch['id']}.mp3"
        path = AUDIO_DIR_EN / filename

        if path.exists():
            print(f"  ⏭️  {filename} — already exists")
            ok += 1
            continue

        text = f"{ch['title_en']}. {ch['content_en']}"
        print(f"  🎙️  Chapter {ch['id']}: \"{ch['title_en']}\"")
        try:
            audio = call_tts(text, ENGLISH_VOICE, ENGLISH_STYLE, ENGLISH_SPEED)
            path.write_bytes(audio)
            print(f"      ✅ {filename} ({len(audio)//1024} KB)")
            ok += 1
        except Exception as e:
            print(f"      ❌ Error: {e}", file=sys.stderr)
        time.sleep(1)

    return ok


def generate_mandarin(chapters):
    """Generate Mandarin narration (冰糖, slowed 5%)."""
    print("\n🗣️  MANDARIN — 冰糖 (female, -5%)")
    print("-" * 40)
    AUDIO_DIR_ZH.mkdir(parents=True, exist_ok=True)

    ok = 0
    for ch in chapters:
        filename = f"chapter-{ch['id']}.mp3"
        path = AUDIO_DIR_ZH / filename

        if path.exists():
            print(f"  ⏭️  {filename} — already exists")
            ok += 1
            continue

        text = f"{ch['title_zh']}。{ch['content_zh']}"
        print(f"  🎙️  第{ch['id']}章: {ch['title_zh']}")
        try:
            audio = call_tts(text, MANDARIN_VOICE, MANDARIN_STYLE, MANDARIN_SPEED)
            path.write_bytes(audio)
            print(f"      ✅ {filename} ({len(audio)//1024} KB)")
            ok += 1
        except Exception as e:
            print(f"      ❌ Error: {e}", file=sys.stderr)
        time.sleep(1)

    return ok


def main():
    print("=" * 60)
    print("🎵 哪吒闹海 — Audio Generation (MiMo TTS)")
    print("=" * 60)

    chapters = get_chapters()
    if not chapters:
        print("❌ Could not parse story data from js/story-data.js", file=sys.stderr)
        sys.exit(1)

    print(f"📖 Found {len(chapters)} chapters")
    print(f"🔊 Output: audio/en/, audio/zh/")
    print()

    en_ok = generate_english(chapters)
    zh_ok = generate_mandarin(chapters)

    total = len(chapters) * 2
    done = en_ok + zh_ok

    print(f"\n{'='*60}")
    print(f"🎉 Done: {done}/{total} audio files generated")
    print(f"{'='*60}")

    return done == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
