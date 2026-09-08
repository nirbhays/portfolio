#!/usr/bin/env python
"""Generate the portfolio's illustration set via Gemini image generation, then
post-process into optimized AVIF/WebP/JPG triples.

Usage:
  python scripts/generate_images.py --list
  python scripts/generate_images.py --dry-run --only hero-bg,about-hero
  python scripts/generate_images.py --only hero-bg,about-hero
  python scripts/generate_images.py --section skills
  python scripts/generate_images.py --force
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = Path(__file__).resolve().parent / "image_manifest.json"
RAW_DIR = Path(__file__).resolve().parent / ".raw_output"
LOG_PATH = Path(__file__).resolve().parent / "generation_log.json"
ASSETS_DIR = ROOT / "assets" / "generated"

MODEL_ID = "models/gemini-3.1-flash-image"

STYLE_SUFFIX = {
    "clay": (
        " Claymorphism-style isometric miniature diorama, soft matte physically-lit "
        "clay and wood surfaces, tilt-shift macro lens shallow depth of field, "
        "three-point warm studio lighting, fine paper-grain texture, palette of warm "
        "terracotta, brushed copper, bone white, and deep umber, no blue or cyan "
        "tones, generous negative space, single cohesive scene."
    ),
    "painterly": (
        " Painterly cinematic matte-painting, atmospheric volumetric light, wide "
        "vista composition, palette of warm terracotta, brushed copper, bone white, "
        "and deep umber with glowing amber accents, no blue or cyan tones, fine "
        "grain texture like a risograph print."
    ),
}


def load_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_log():
    if LOG_PATH.exists():
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_log(log):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def build_prompt(entry):
    return entry["prompt"] + STYLE_SUFFIX[entry["style"]]


def center_crop_resize(im, target_w, target_h):
    src_w, src_h = im.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        im = im.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        im = im.crop((0, top, src_w, top + new_h))
    return im.resize((target_w, target_h), Image.LANCZOS)


def save_optimized(im, out_dir, basename):
    out_dir.mkdir(parents=True, exist_ok=True)
    im = im.convert("RGB")
    paths = {}
    avif_path = out_dir / f"{basename}.avif"
    webp_path = out_dir / f"{basename}.webp"
    jpg_path = out_dir / f"{basename}.jpg"
    im.save(avif_path, "AVIF", quality=55)
    im.save(webp_path, "WEBP", quality=80)
    im.save(jpg_path, "JPEG", quality=82, optimize=True)
    for p in (avif_path, webp_path, jpg_path):
        paths[p.suffix[1:]] = {"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size}
    return paths


def call_gemini(prompt, aspect_ratio):
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set in environment.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt],
        config=types.GenerateContentConfig(
            image_config=types.ImageConfig(aspect_ratio=aspect_ratio)
        ),
    )
    for part in resp.candidates[0].content.parts:
        if getattr(part, "inline_data", None):
            return part.inline_data.data
    raise RuntimeError("No inline image data returned by the model")


def process_entry(entry, log, force):
    entry_id = entry["id"]
    out_dir = ASSETS_DIR / entry["output_dir"]
    basename = entry["output_basename"]
    final_jpg = out_dir / f"{basename}.jpg"

    if final_jpg.exists() and not force:
        print(f"  skip  {entry_id} (already exists, use --force to regenerate)")
        return

    raw_path = RAW_DIR / f"{entry_id}.png"

    if "source_id" in entry:
        source_raw = RAW_DIR / f"{entry['source_id']}.png"
        if not source_raw.exists():
            print(f"  MISS  {entry_id}: source raw {source_raw} not found, generate the source first")
            return
        im = Image.open(source_raw)
        im = center_crop_resize(im, entry["target_width"], entry["target_height"])
        paths = save_optimized(im, out_dir, basename)
        log[entry_id] = {"derived_from": entry["source_id"], "outputs": paths}
        print(f"  done  {entry_id} (derived crop from {entry['source_id']})")
        return

    prompt = build_prompt(entry)
    print(f"  gen   {entry_id} -> {MODEL_ID} ({entry['aspect_ratio']})")
    raw_bytes = call_gemini(prompt, entry["aspect_ratio"])
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_path.write_bytes(raw_bytes)

    im = Image.open(raw_path)
    im = center_crop_resize(im, entry["target_width"], entry["target_height"])
    paths = save_optimized(im, out_dir, basename)
    log[entry_id] = {"prompt": prompt, "outputs": paths}
    print(f"  done  {entry_id}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="list manifest entries and exit")
    ap.add_argument("--dry-run", action="store_true", help="print final prompts, no API calls")
    ap.add_argument("--only", help="comma-separated list of ids to process")
    ap.add_argument("--section", help="only process entries in this section")
    ap.add_argument("--force", action="store_true", help="regenerate even if output exists")
    args = ap.parse_args()

    manifest = load_manifest()

    if args.only:
        wanted = set(args.only.split(","))
        manifest = [e for e in manifest if e["id"] in wanted]
    if args.section:
        manifest = [e for e in manifest if e["section"] == args.section]

    if args.list:
        for e in manifest:
            src = f"(derived from {e['source_id']})" if "source_id" in e else e.get("aspect_ratio", "")
            print(f"{e['id']:24s} {e['section']:12s} {src}")
        return

    if args.dry_run:
        for e in manifest:
            if "source_id" in e:
                print(f"--- {e['id']} --- (derived crop, no prompt)")
            else:
                print(f"--- {e['id']} ---\n{build_prompt(e)}\n")
        return

    log = load_log()
    for entry in manifest:
        try:
            process_entry(entry, log, args.force)
        except Exception as exc:
            print(f"  FAIL  {entry['id']}: {exc}", file=sys.stderr)
        save_log(log)
        time.sleep(1)


if __name__ == "__main__":
    main()
