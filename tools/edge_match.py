"""Match anti-aliased edge colors to the nearest solid sprite color.

For every PNG in textures/item:
  - "core" pixels  = alpha >= 240 (the solid body)
  - target pixels  = alpha < 240 that lie within 3 px of the core
                     (this covers the AA ring and the invisible outer halo)
  - if a target pixel's RGB differs from the nearest core pixel's RGB by
    more than --threshold, its RGB is replaced by that core color.
The alpha channel is never modified, shapes/soft shadows are preserved.

Use --dry-run to only report. Skips spicy_crinkle_cut_fries (already
same-color edges) and any texture without semi-transparent edges.

Usage:
  python edge_match.py --dry-run
  python edge_match.py
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEXTURES_ROOT = PROJECT_ROOT / "src" / "main" / "resources" / "assets" / "kaleidoscope_snack" / "textures"
DEFAULT_SKIP = {"spicy_crinkle_cut_fries.png"}
CORE_ALPHA = 240
BAND = 3
THRESHOLD = 30


def process(path: Path, dry_run: bool, threshold: int) -> tuple[int, int]:
    img = Image.open(path).convert("RGBA")
    a = np.asarray(img).astype(np.int16)

    alpha = a[..., 3]
    core = alpha >= CORE_ALPHA
    if not core.any() or (alpha == 0).all():
        return 0, 0

    # nearest core pixel for every pixel of the image
    _, indices = ndimage.distance_transform_edt(~core, return_indices=True)
    src_y, src_x = indices
    d_core = np.sqrt(((np.indices(core.shape)[0] - src_y) ** 2 +
                      (np.indices(core.shape)[1] - src_x) ** 2))

    target = (alpha < CORE_ALPHA) & (d_core <= BAND)
    if not target.any():
        return 0, 0

    rgb = a[..., :3]
    src_rgb = rgb[src_y, src_x]
    delta = np.sqrt(((rgb.astype(np.float32) - src_rgb.astype(np.float32)) ** 2).sum(axis=2))
    change = target & (delta > threshold)
    n_change = int(change.sum())
    max_delta = float(delta[target].max()) if target.any() else 0.0

    if not dry_run and n_change:
        out = a.copy()
        out[..., :3][change] = src_rgb[change]
        Image.fromarray(out.astype(np.uint8), "RGBA").save(path, format="PNG", optimize=True)

    return n_change, max_delta


def main() -> int:
    parser = argparse.ArgumentParser(description="Match edge colors to body color")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--threshold", type=int, default=THRESHOLD)
    args = parser.parse_args()

    total = 0
    for p in sorted(TEXTURES_ROOT.rglob("*.png")):
        if p.name in DEFAULT_SKIP:
            print(f"skip  (by request)            : {p.name}")
            continue
        n, mx = process(p, args.dry_run, args.threshold)
        total += n
        state = "unchanged" if n == 0 else f"{n:6d} px recolored (max delta {mx:.0f})"
        print(f"{'dry' if args.dry_run else 'fix'}: {p.name:32s} {state}")
    print(f"\ntotal recolored: {total}" + (" (dry run, nothing written)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
