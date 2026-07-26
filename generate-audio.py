#!/usr/bin/env python3
"""
Generate narration audio for 哪吒闹海 (Nezha Conquers the Dragon King) using Edge TTS.
Chinese: zh-CN-XiaoxiaoNeural (female, slowed -8%)
English: en-US-GuyNeural (male, normal speed)
"""
import os
import sys
import re
import asyncio
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("Installing edge-tts…")
    os.system("pip install edge-tts")
    import edge_tts

# ═══════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════
ENGLISH_VOICE  = "en-US-GuyNeural"
MANDARIN_VOICE = "zh-CN-XiaoxiaoNeural"
ENGLISH_SPEED  = "+0%"
MANDARIN_SPEED = "-8%"
# ═══════════════════════════════════════════

AUDIO_DIR_EN = Path("audio/en")
AUDIO_DIR_ZH = Path("audio/zh")


def get_chapters():
    """Parse js/story-data.js and extract chapter data."""
    js_path = Path("js/story-data.js")
    if not js_path.exists():
        print(f"❌ {js_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(js_path, "r", encoding="utf-8") as f:
        code = f.read()

    chapters = []

    # Extract each chapter block
    chapter_pattern = re.compile(
        r'id:\s*(\d+).*?'
        r'title:\s*\{.*?'
        r'en:\s*"([^"]+)".*?'
        r'zh:\s*"([^"]+)".*?'
        r'pinyin:\s*"([^"]+)"'
        r'.*?\}.*?'
        r'content:\s*\{.*?'
        r'en:\s*"((?:[^"\\]|\\.)*)".*?'
        r'zh:\s*"((?:[^"\\]|\\.)*)".*?'
        r'pinyin:\s*"((?:[^"\\]|\\.)*)"',
        re.DOTALL
    )

    matches = chapter_pattern.findall(code)

    if matches:
        for m in matches:
            # Unescape JS string escapes
            en_content = m[4].replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'")
            zh_content = m[5].replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'")
            # Strip any remaining backslash artifacts
            en_content = en_content.replace('\\', '')
            zh_content = zh_content.replace('\\', '')

            chapters.append({
                "id":      int(m[0]),
                "title":   {"en": m[1], "zh": m[2], "pinyin": m[3]},
                "content": {"en": en_content, "zh": zh_content}
            })

    return chapters


async def generate_audio(text, voice, speed, output_path):
    """Generate a single audio file using Edge TTS."""
    try:
        communicate = edge_tts.Communicate(text, voice, rate=speed)
        await communicate.save(str(output_path))
        size_kb = output_path.stat().st_size // 1024
        print(f"  ✅ {output_path.name} ({size_kb} KB)")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}", file=sys.stderr)
        return False


async def generate_english(chapters):
    """Generate English narration (male voice, normal speed)."""
    print("\n🗣️  ENGLISH — Guy (male, +0%)")
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

        text = f"{ch['title']['en']}. {ch['content']['en']}"
        print(f"  🎙️  Chapter {ch['id']}: \"{ch['title']['en']}\"")
        if await generate_audio(text, ENGLISH_VOICE, ENGLISH_SPEED, path):
            ok += 1

    return ok


async def generate_mandarin(chapters):
    """Generate Mandarin narration (female voice, slowed -8%)."""
    print("\n🗣️  MANDARIN — Xiaoxiao (female, -8%)")
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

        text = f"{ch['title']['zh']}。{ch['content']['zh']}"
        print(f"  🎙️  第{ch['id']}章: {ch['title']['zh']}")
        if await generate_audio(text, MANDARIN_VOICE, MANDARIN_SPEED, path):
            ok += 1

    return ok


async def main():
    print("=" * 60)
    print("🎵 哪吒闹海 — Audio Generation (Edge TTS)")
    print("=" * 60)

    chapters = get_chapters()
    if not chapters:
        print("❌ Could not parse story data from js/story-data.js", file=sys.stderr)
        sys.exit(1)

    print(f"📖 Found {len(chapters)} chapters")
    print(f"🔊 Output: audio/en/, audio/zh/")
    print()

    en_ok = await generate_english(chapters)
    zh_ok = await generate_mandarin(chapters)

    total = len(chapters) * 2
    done  = en_ok + zh_ok

    print(f"\n{'='*60}")
    print(f"🎉 Done: {done}/{total} audio files generated")
    print(f"{'='*60}")

    return done == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
