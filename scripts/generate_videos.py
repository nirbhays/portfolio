#!/usr/bin/env python
"""Image-to-video generation via Veo, seeding first+last frame with the same
raw illustration (already produced by generate_images.py) for a seamless loop.
Crops Veo's forced 16:9/9:16 letterboxing back to the source aspect via ffmpeg,
then encodes lightweight MP4 + WebM loops.

Usage:
  python scripts/generate_videos.py --list
  python scripts/generate_videos.py --only proj-shieldiac
  python scripts/generate_videos.py
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = Path(__file__).resolve().parent / ".raw_output"
ASSETS_DIR = ROOT / "assets" / "generated"
FFMPEG = r"C:\Users\SIN3WZ\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"

MOTION_SUFFIX = (
    " Extremely subtle, slow ambient motion within the scene only -- gentle "
    "flicker of light or embers, soft drifting steam, dust, or mist, delicate "
    "sway of small details. Camera completely static, no zoom, no pan, no "
    "camera movement whatsoever. Seamless looping motion, claymorphism "
    "diorama lighting, warm terracotta and copper tones, no blue or cyan."
)

MANIFEST = [
    {
        "id": "about-hero",
        "raw": "about-hero.png",
        "out_dir": "about",
        "out_name": "about-hero-motion",
        "veo_aspect": "9:16",
        "target_w": 480, "target_h": 600,
        "motion": "The tiny kiln embers flicker warmly, the coral polyps pulse gently with soft bioluminescent light, the lighthouse beacon beam slowly sweeps.",
    },
    {
        "id": "proj-shieldiac",
        "raw": "proj-shieldiac.png",
        "out_dir": "projects",
        "out_name": "shieldiac-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "The small amber warning gear glows and flickers gently, faint dust motes drift in the spotlight beam.",
    },
    {
        "id": "proj-tokenmeter",
        "raw": "proj-tokenmeter.png",
        "out_dir": "projects",
        "out_name": "tokenmeter-motion",
        "veo_aspect": "9:16",
        "target_w": 480, "target_h": 640,
        "motion": "The molten glass droplets shimmer and pulse gently with warm inner light, the balance scale sways very slightly.",
    },
    {
        "id": "proj-infracents",
        "raw": "proj-infracents.png",
        "out_dir": "projects",
        "out_name": "infracents-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "Leaves rustle gently in a light breeze, water trickles softly through the irrigation channel into the reservoir.",
    },
    {
        "id": "proj-agentloom",
        "raw": "proj-agentloom.png",
        "out_dir": "projects",
        "out_name": "agentloom-motion",
        "veo_aspect": "16:9",
        "target_w": 560, "target_h": 560,
        "motion": "The lantern flames flicker and glow warmly as they pass hand to hand, soft mist drifts slowly across the bridge below.",
    },
    {
        "id": "proj-airlock",
        "raw": "proj-airlock.png",
        "out_dir": "projects",
        "out_name": "airlock-motion",
        "veo_aspect": "9:16",
        "target_w": 480, "target_h": 640,
        "motion": "Water flows gently through the stacked filtration basins, soft steam rises off the wet copper surfaces.",
    },
    {
        "id": "proj-datamint",
        "raw": "proj-datamint.png",
        "out_dir": "projects",
        "out_name": "datamint-motion",
        "veo_aspect": "16:9",
        "target_w": 560, "target_h": 560,
        "motion": "The stamping press gently taps up and down, freshly stamped coins shimmer softly as they settle into the tray.",
    },
    {
        "id": "proj-modelledger",
        "raw": "proj-modelledger.png",
        "out_dir": "projects",
        "out_name": "modelledger-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "The glowing lineage threads between the ledger books pulse gently, dust motes drift slowly in the light.",
    },
    {
        "id": "proj-tuneforge",
        "raw": "proj-tuneforge.png",
        "out_dir": "projects",
        "out_name": "tuneforge-motion",
        "veo_aspect": "9:16",
        "target_w": 480, "target_h": 640,
        "motion": "The forge embers glow and flicker, a soft plume of steam rises gently from the quenching trough.",
    },
    {
        "id": "skill-cloud",
        "raw": "skill-cloud.png",
        "out_dir": "skills",
        "out_name": "cloud-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "The dust storm swirls gently, soft rain falls steadily, a warm sunbeam flickers through the clouds.",
    },
    {
        "id": "skill-iac",
        "raw": "skill-iac.png",
        "out_dir": "skills",
        "out_name": "iac-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "The glowing blueprint lines shimmer gently as the miniature city subtly rises brick by brick, the lantern flame flickers.",
    },
    {
        "id": "skill-containers",
        "raw": "skill-containers.png",
        "out_dir": "skills",
        "out_name": "containers-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "The coral polyps pulse gently with bioluminescent light, one dims softly while another blooms elsewhere.",
    },
    {
        "id": "skill-cicd",
        "raw": "skill-cicd.png",
        "out_dir": "skills",
        "out_name": "cicd-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "Water ripples gently in the canal locks as the small boats sway, warm harbor lights flicker in the distance.",
    },
    {
        "id": "skill-aiml",
        "raw": "skill-aiml.png",
        "out_dir": "skills",
        "out_name": "aiml-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "The kiln embers glow and flicker warmly, soft steam rises gently from the finished ceramic vessels.",
    },
    {
        "id": "skill-security",
        "raw": "skill-security.png",
        "out_dir": "skills",
        "out_name": "security-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "The twin lighthouse beacon beams sweep slowly and stay in sync, soft mist drifts gently over the water.",
    },
    {
        "id": "skill-languages",
        "raw": "skill-languages.png",
        "out_dir": "skills",
        "out_name": "languages-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "The inked roller subtly presses down, fine dust motes drift gently in the workshop light.",
    },
    {
        "id": "skill-data",
        "raw": "skill-data.png",
        "out_dir": "skills",
        "out_name": "data-motion",
        "veo_aspect": "16:9",
        "target_w": 640, "target_h": 480,
        "motion": "The orrery's glowing nodes orbit slowly on their delicate arms, candlelight flickers gently on the desk.",
    },
]


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def cropdetect(path):
    out = subprocess.run(
        [FFMPEG, "-i", str(path), "-vf", "cropdetect=24:2:0", "-f", "null", "-"],
        capture_output=True, text=True
    )
    crops = [l for l in out.stderr.splitlines() if "crop=" in l]
    if not crops:
        return None
    last = crops[-1].split("crop=")[-1].split()[0]
    return last  # "w:h:x:y"


def process_entry(entry, force=False):
    out_dir = ASSETS_DIR / entry["out_dir"]
    out_mp4 = out_dir / f"{entry['out_name']}.mp4"
    if out_mp4.exists() and not force:
        print(f"  skip  {entry['id']} (exists)")
        return

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    raw_path = RAW_DIR / entry["raw"]
    img_bytes = raw_path.read_bytes()
    img = types.Image(image_bytes=img_bytes, mime_type="image/png")
    prompt = entry["motion"] + MOTION_SUFFIX

    print(f"  gen   {entry['id']} -> veo ({entry['veo_aspect']})")
    op = client.models.generate_videos(
        model="veo-3.1-fast-generate-preview",
        source=types.GenerateVideosSource(prompt=prompt, image=img),
        config=types.GenerateVideosConfig(
            last_frame=img,
            duration_seconds=8,
            aspect_ratio=entry["veo_aspect"],
            resolution="720p",
        ),
    )
    while not op.done:
        time.sleep(10)
        op = client.operations.get(op)

    if op.error:
        print(f"  FAIL  {entry['id']}: {op.error}", file=sys.stderr)
        return

    video = op.result.generated_videos[0].video
    client.files.download(file=video)
    raw_video_path = RAW_DIR / f"{entry['id']}-raw.mp4"
    raw_video_path.write_bytes(video.video_bytes)

    crop = cropdetect(raw_video_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    vf = f"crop={crop}," if crop else ""
    vf += f"scale={entry['target_w']}:{entry['target_h']}:force_original_aspect_ratio=increase,crop={entry['target_w']}:{entry['target_h']}"

    run([FFMPEG, "-y", "-i", str(raw_video_path), "-vf", vf, "-an",
         "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-crf", "27", "-preset", "slow", "-movflags", "+faststart", str(out_mp4)])
    out_webm = out_dir / f"{entry['out_name']}.webm"
    run([FFMPEG, "-y", "-i", str(raw_video_path), "-vf", vf, "-an",
         "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "36", "-row-mt", "1", str(out_webm)])

    print(f"  done  {entry['id']} -> {out_mp4.stat().st_size // 1024}KB mp4, {out_webm.stat().st_size // 1024}KB webm")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    manifest = MANIFEST
    if args.only:
        wanted = set(args.only.split(","))
        manifest = [e for e in manifest if e["id"] in wanted]

    if args.list:
        for e in manifest:
            print(e["id"], e["out_dir"], e["veo_aspect"])
        return

    for entry in manifest:
        try:
            process_entry(entry, args.force)
        except Exception as exc:
            print(f"  FAIL  {entry['id']}: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
