#!/usr/bin/env python3
"""
Generate gongbi heavy-colour (工笔重彩) painting illustrations for 哪吒闹海.
Uses Cloudflare Workers AI (FLUX) with Shang-dynasty / Ming-dynasty gongbi prompts.
"""
import os
import sys
import base64
import time
import requests
from pathlib import Path

# Load Cloudflare credentials
env_path = Path.home() / ".pi" / "agent" / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"')

ACCOUNT_ID = os.environ.get("CLOUDFLARE_ID", "")
API_KEY    = os.environ.get("CLOUDFLARE_API_KEY", "")

if not ACCOUNT_ID or not API_KEY:
    print("❌ Cloudflare credentials not found in ~/.pi/agent/.env", file=sys.stderr)
    sys.exit(1)

API_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"

# ─── Shared style prefix ────────────────────────────────
STYLE = (
    "Chinese gongbi heavy-colour painting (工笔重彩画), "
    "meticulous fine brushwork, layered mineral pigments on sized silk, "
    "rich saturated jewel-like colour, precise controlled outlines, "
    "Shang dynasty aesthetic, Ming dynasty illustration tradition, "
    "deep azurite blue, cinnabar red, jade green, gold accents on dark silk ground, "
    "dramatic narrative composition, masterpiece quality, "
    "balanced composition, clear focal point."
)

# ─── Per-chapter illustration prompts ────────────────────
SCENES = {
    1: (
        "A dimly lit bedchamber inside a Shang-dynasty fortress: "
        "a luminous flesh ball glowing with golden light at centre frame; "
        "a warrior-general (Li Jing) with drawn sword in mid-strike; "
        "a seated woman (Lady Yin) on a carved bed behind, face filled with awe; "
        "golden light erupting from the split flesh ball; "
        "a small radiant boy leaping from within; "
        "ornate bronze vessels, silk curtains, oracle-bone inscriptions on walls; "
        "dramatic chiaroscuro lighting, the moment of divine birth"
    ),
    2: (
        "Underwater: the vast Crystal Palace of the East Sea, "
        "every coral column and jade tile meticulously painted; "
        "Ao Guang seated on a dragon-scale throne of coral and gold, "
        "wearing imperial dragon robes, cold expression; "
        "rows of Yaksha soldiers escorting small children in red festival clothes; "
        "deep azurite blue and jade-green water fills every space; "
        "cold imperial power, oppression rendered in jewel-like colour"
    ),
    3: (
        "The shoreline of Chentang Pass at midsummer: "
        "a small but fierce-eyed seven-year-old boy (Nezha) standing knee-deep in green-blue water, "
        "a bright cinnabar-red silk sash trailing and glowing in the water; "
        "ocean tremors radiating outward in concentric rings; "
        "distant fortress walls on coastal hills; "
        "warm terracotta earth, green coastal hills, bright red sash cutting through blue-green sea; "
        "a sense of innocent but immense power, every wave crest meticulously outlined"
    ),
    4: (
        "A violent sea battle: Nezha in mid-air, seven years old, fierce and determined, "
        "the golden Universe Ring raised above his head; "
        "Ao Bing in ornate dragon-spirit armour with trident, lunging upward from crashing waves; "
        "spray and foam rendered in fine gongbi detail; "
        "dramatic diagonal composition, deep azurite sea, "
        "cinnabar fire effects where the weapons clash, gold ring gleaming; "
        "intricate armour and dragon-scale detail on every surface"
    ),
    5: (
        "Outside the gates of Chentang Pass fortress in a thunderstorm: "
        "four Dragon Kings in full imperial regalia standing in a line — "
        "Ao Guang in blue dragon robes, Ao Qin in white, Ao Run in black, Ao Shun in red — "
        "each rendered with meticulous gongbi detail in their distinctive colour; "
        "Li Jing kneeling before them in the rain; "
        "dark thunderclouds, rain, the fortress gate towering behind; "
        "four distinct colour identities against the dark sky, moral weight"
    ),
    6: (
        "Inside the fortress: a young boy (Nezha) alone before his parents, "
        "holding a blade, face calm and resolute; "
        "Li Jing and Lady Yin weeping; "
        "the scene rendered with restrained dignity — no gore, "
        "only the emotional weight visible in their postures and expressions; "
        "intimate interior, candlelight casting warm shadows; "
        "cinnabar and gold tones fading to muted greys; "
        "tears rendered as fine gongbi detail, quiet devastating power"
    ),
    7: (
        "A sacred cave on Kunlun Mountain: "
        "an elderly immortal (Taiyi Zhenren) in white Daoist robes "
        "arranging lotus roots and large green lotus leaves into a human shape; "
        "a soft golden light (Nezha's soul) descending into the lotus body; "
        "a young boy rising from the lotus — reborn, eyes opening, "
        "surrounded by blooming pink lotus flowers; "
        "jade green and pink lotus palette, sacred mountain setting; "
        "golden spiritual light, fire-tipped spear and wind-fire wheels glowing"
    ),
    8: (
        "The triumphant finale: Nezha in full Three Heads and Six Arms form, "
        "each head fierce and determined, each arm wielding a different weapon; "
        "flying on blazing Wind-Fire Wheels that leave trails of cinnabar fire; "
        "the Fire-Tipped Spear held high; "
        "soaring above a shattered Crystal Palace in the ocean below; "
        "the Four Dragon Kings in retreat; "
        "full panoramic gongbi composition — azurite sea, cinnabar fire-wheels, "
        "gold divine light, jade-green lotus motifs woven into Nezha's armour; "
        "a single great lotus bloom rises from the churning water"
    )
}

MAX_RETRIES = 3
RETRY_DELAY = 8


def generate_image(prompt, output_path):
    """Generate an image using Cloudflare AI FLUX model with retries."""
    payload = {
        "prompt":     STYLE + ", " + prompt,
        "width":      1024,
        "height":     768,
        "num_steps":  4,
        "guidance":   7.5
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json"
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"  🎨 Attempt {attempt}/{MAX_RETRIES} — requesting image…")
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
            data = resp.json()

            if "result" in data and "image" in data["result"]:
                img_bytes = base64.b64decode(data["result"]["image"])
                with open(output_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  ✅ Saved {output_path.name} ({len(img_bytes)//1024} KB)")
                return True
            else:
                print(f"  ⚠️  Unexpected response: {str(data)[:200]}")

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else 0
            if status == 429:
                wait = RETRY_DELAY * attempt
                print(f"  ⏳ Rate-limited (429). Waiting {wait}s…")
                time.sleep(wait)
                continue
            print(f"  ❌ HTTP {status}: {e}")
        except requests.exceptions.Timeout:
            print(f"  ⏰ Timeout on attempt {attempt}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

        if attempt < MAX_RETRIES:
            print(f"  ⏳ Retrying in {RETRY_DELAY}s…")
            time.sleep(RETRY_DELAY)

    return False


def main():
    output_dir = Path("images/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("🎨 哪吒闹海 — Image Generation (FLUX-1-schnell)")
    print("=" * 60)
    print(f"📁 Output: {output_dir.absolute()}")
    print(f"🎯 Model:  @cf/black-forest-labs/flux-1-schnell")
    print(f"🖌️  Style:  Gongbi heavy-colour (工笔重彩)")
    print()

    success = 0
    total = len(SCENES)

    for ch_num in sorted(SCENES):
        prompt = SCENES[ch_num]
        out = output_dir / f"chapter-{ch_num}.webp"

        if out.exists():
            sz = out.stat().st_size // 1024
            print(f"⏭️  Chapter {ch_num} — already exists ({sz} KB)")
            success += 1
            continue

        print(f"\n📖 Chapter {ch_num}/{total}: Generating…")
        if generate_image(prompt, out):
            success += 1
        else:
            print(f"  ❌ FAILED for chapter {ch_num}")

    print(f"\n{'='*60}")
    print(f"✅ Done: {success}/{total} images generated")
    print(f"{'='*60}")

    # Copy raw → images/ (final serving dir)
    final_dir = Path("images")
    for webp in output_dir.glob("chapter-*.webp"):
        dest = final_dir / webp.name
        if not dest.exists():
            import shutil
            shutil.copy2(webp, dest)
            print(f"📋 Copied {webp.name} → images/")

    return success == total


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
