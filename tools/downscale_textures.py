"""
Downscale oversized item/block textures to 16x16 for MCreator / Minecraft.

Why: models using "item/generated" (and MCreator's texture editor) expect
16x16 textures. Larger textures (e.g. 512x512) make the item render as a
giant stretched mesh in game, and MCreator cannot handle them properly.

Modes:
  sharp (default)   - premultiplied LANCZOS average + binary alpha + color
                      lift (saturation/contrast). Keeps the silhouette,
                      crisp hard edges, no washed-out look.
  nearest           - hard nearest-neighbor sampling + binary alpha.
                      Heavy aliasing/noise on 32:1 sources; rarely useful.
  smooth            - premultiplied-alpha BOX average only. Soft, no fringe.

What it does:
  1. Copies every oversized texture into a backup folder (outside resources/,
     so the backup is never shipped inside the built jar).
  2. Resizes the texture to 16x16 with the selected mode.
  3. Overwrites the original file in place.

Usage:
  python downscale_textures.py                     # sharp mode (default)
  python downscale_textures.py --mode nearest      # hard sampling
  python downscale_textures.py --mode smooth       # soft averaged mode
  python downscale_textures.py --dry-run           # report only, no changes
"""

import argparse
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEXTURES_ROOT = PROJECT_ROOT / "src" / "main" / "resources" / "assets" / "kaleidoscope_snack" / "textures"
BACKUP_ROOT = PROJECT_ROOT / "hd_texture_backup"
TARGET_SIZE = (16, 16)
ALPHA_CUTOFF = 128
SATURATION = 1.35
CONTRAST = 1.10


def resize_nearest(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Hard nearest-neighbor sampling, then binary alpha for MC-style pixels."""
    rgba = im.convert("RGBA")
    small = rgba.resize(size, Image.NEAREST)

    arr = np.asarray(small).copy()
    arr[..., 3] = np.where(arr[..., 3] >= ALPHA_CUTOFF, 255, 0)
    return Image.fromarray(arr, mode="RGBA")


def premultiplied_resize(im: Image.Image, size: tuple[int, int], resample) -> np.ndarray:
    """Resize RGBA without halo artifacts, return float array (h,w,4), 0-255.

    Transparent pixels can carry arbitrary RGB values; a naive resize blends
    those colors into the visible edge. Work in premultiplied alpha space:
    RGB *= A, resize, then divide RGB back by the resized A.
    """
    rgba = im.convert("RGBA")
    arr = np.asarray(rgba, dtype=np.float32)

    alpha = arr[..., 3:4] / 255.0
    premult = np.empty_like(arr)
    premult[..., :3] = arr[..., :3] * alpha
    premult[..., 3:4] = arr[..., 3:4]

    small = Image.fromarray(premult.astype(np.uint8), mode="RGBA").resize(size, resample)
    out = np.asarray(small, dtype=np.float32)

    a = out[..., 3:4] / 255.0
    safe = a > (1.0 / 255.0)
    rgb = np.zeros_like(out[..., :3])
    np.divide(out[..., :3], np.where(safe, a, 1.0), out=rgb, where=safe)

    result = np.concatenate([rgb, out[..., 3:4]], axis=-1)
    return np.clip(result, 0, 255).astype(np.uint8)


def resize_smooth(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Premultiplied-alpha BOX average. Soft look, no fringe."""
    return Image.fromarray(premultiplied_resize(im, size, Image.BOX), mode="RGBA")


def resize_sharp(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Silhouette-preserving average + binary alpha + saturation/contrast lift."""
    arr = premultiplied_resize(im, size, Image.LANCZOS).copy()
    arr[..., 3] = np.where(arr[..., 3] >= ALPHA_CUTOFF, 255, 0)
    arr[arr[..., 3] == 0, :3] = 0

    img = Image.fromarray(arr, mode="RGBA")
    rgb = img.convert("RGB")
    rgb = ImageEnhance.Color(rgb).enhance(SATURATION)
    rgb = ImageEnhance.Contrast(rgb).enhance(CONTRAST)

    out = np.dstack([np.asarray(rgb), arr[..., 3]])
    return Image.fromarray(out, mode="RGBA")


MODES = {
    "nearest": resize_nearest,
    "smooth": resize_smooth,
    "sharp": resize_sharp,
}


def iter_pngs(root: Path):
    if not root.is_dir():
        return
    for p in sorted(root.rglob("*.png")):
        yield p


def main() -> int:
    parser = argparse.ArgumentParser(description="Downscale textures to 16x16")
    parser.add_argument("--mode", choices=sorted(MODES), default="sharp",
                        help="resize algorithm (default: sharp)")
    parser.add_argument("--dry-run", action="store_true", help="report only, no changes")
    args = parser.parse_args()

    resize_fn = MODES[args.mode]
    converted = 0
    skipped = 0
    failed = 0

    for src in iter_pngs(TEXTURES_ROOT):
        try:
            with Image.open(src) as im:
                size = im.size
                if size == TARGET_SIZE:
                    skipped += 1
                    continue

                print(f"[{size[0]}x{size[1]}] -> {TARGET_SIZE[0]}x{TARGET_SIZE[1]} ({args.mode}) : {src.relative_to(PROJECT_ROOT)}")
                if args.dry_run:
                    converted += 1
                    continue

                # backup original, preserving relative folder structure
                rel = src.relative_to(TEXTURES_ROOT)
                dst_backup = BACKUP_ROOT / rel
                dst_backup.parent.mkdir(parents=True, exist_ok=True)
                if not dst_backup.exists():
                    shutil.copy2(src, dst_backup)

                small = resize_fn(im, TARGET_SIZE)
                small.save(src, format="PNG", optimize=True)
                converted += 1
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"[FAIL] {src}: {exc}", file=sys.stderr)

    print(f"\nconverted={converted} skipped(16x16)={skipped} failed={failed}")
    if not args.dry_run and converted:
        print(f"backup of originals: {BACKUP_ROOT}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
