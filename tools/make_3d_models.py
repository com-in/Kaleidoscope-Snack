"""
Convert all kaleidoscope_snack items from builtin "item/generated" models to
custom JSON 3D models (flat double-sided planes), so that high-resolution
textures (512x512) display correctly and MCreator recognizes the setup.

What this script writes (all 11 items):
  1. <workspace>/models/<registry>.json            custom model (MCreator model
                                                   resource, self-contained)
  2. <workspace>/models/<registry>.json.textures   MCreator texture mapping
                                                   sidecar (layer0 -> texture)
  3. assets/<modid>/models/custom/<registry>.json  copy WITHOUT "textures"
                                                   section (exactly what
                                                   MCreator's copy_models task
                                                   produces at generation)
  4. assets/<modid>/models/item/<registry>.json    item model referencing the
                                                   custom model (MCreator's
                                                   item_cmodel.json.ftl form).
                                                   NOTE: MCreator resolves
                                                   mapped textures as
                                                   "%s:block/%s", so layer0
                                                   points to block/<tex>.
  5. assets/<modid>/textures/block/<tex>.png       texture copy for the model
                                                   texture mapping (the item/
                                                   copy stays for particles
                                                   and the editor icon)
  6. elements/<Element>.mod.json                   renderType 0 -> 1,
                                                   customModelName -> registry

Usage:
  python make_3d_models.py --dry-run   # report only
  python make_3d_models.py             # write everything
"""

import argparse
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
ASSETS = PROJECT_ROOT / "src" / "main" / "resources" / "assets" / "kaleidoscope_snack"
ELEMENTS_DIR = PROJECT_ROOT / "elements"
MODID = "kaleidoscope_snack"

# element file stem -> (registry name, texture name)
ITEMS = {
    "Pancake": ("pancake", "pancake"),
    "Squid": ("raw_squid", "squid"),
    "GrilledSquid": ("grilled_squid", "grilled_squid"),
    "Potstickers": ("potstickers", "potstickers"),
    "GroundMeat": ("ground_meat", "ground_meat"),
    "Sausage": ("sausage", "sausage"),
    "SausageCasing": ("sausage_casing", "sausage_casing"),
    "CookedSausage": ("cooked_sausage", "cooked_sausage"),
    "PotatoChunks": ("potato_chunks", "potato_chunks"),
    "SpicyCrinkleCutFries": ("spicy_crinkle_cut_fries", "spicy_crinkle_cut_fries"),
    "CrispyPorkBelly": ("crispy_pork_belly", "crispy_pork_belly"),
}

# display transforms copied verbatim from the vanilla 1.21.1
# assets/minecraft/models/item/generated.json (extracted from the client jar)
VANILLA_DISPLAY = {
    "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    "head": {"rotation": [0, 180, 0], "translation": [0, 13, 7], "scale": [1, 1, 1]},
    "thirdperson_righthand": {"rotation": [0, 0, 0], "translation": [0, 3, 1], "scale": [0.55, 0.55, 0.55]},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "fixed": {"rotation": [0, 180, 0], "scale": [1, 1, 1]},
}


# extrusion / silhouette sampling settings
GRID = 16            # cells per axis (1 model unit each)
COVER = 0.40         # cell is solid when its mean alpha >= this
# total thickness is 0.5 model units: back quad 7.75-7.775, core 7.775-8.225,
# front quad 8.225-8.25 (edit the z values inside build_model to change;
# 1.0 = vanilla feel, 1.5 = chunky)


def cell_alpha_grid(texture: str) -> np.ndarray:
    """Mean alpha (0..1) of each GRID x GRID cell of the item texture."""
    im = Image.open(ASSETS / "textures" / "item" / f"{texture}.png").convert("RGBA")
    a = np.asarray(im, dtype=np.float32)[..., 3] / 255.0
    cell = a.shape[0] // GRID
    return a.reshape(GRID, cell, GRID, cell).mean(axis=(1, 3))


def _clamp(v: float) -> float:
    return max(0.0, min(16.0, v))


def build_model(registry: str, texture: str) -> dict:
    """Extruded model: full-sprite front/back quads (texture never clipped)
    plus an extruded silhouette core (GRID x GRID) that gives real thickness
    (z 7.75 -> 8.25, 0.5 units total). Side faces sample a 1-texel sliver
    of the sprite's edge so the rim color matches."""
    g = cell_alpha_grid(texture)
    solid = g >= COVER
    z0, z1 = 7.775, 8.225     # extruded core depth (quads add 0.025 on both sides)
    texel = 1.0 / (GRID * 2) * 0.9     # ~1 texel in 0-16 uv units
    pad = 0.01

    quad_faces = {
        "south": {"uv": [0, 0, 16, 16], "texture": "#layer0"},
        "north": {"uv": [16, 0, 0, 16], "texture": "#layer0"},
    }
    elements = [
        {"from": [0.0, 0.0, 7.75], "to": [16.0, 16.0, 7.775], "faces": dict(quad_faces)},
    ]

    for i in range(GRID):
        j = 0
        while j < GRID:
            if not solid[j, i]:
                j += 1
                continue
            j0 = j
            lf = (i > 0) and solid[j0, i - 1]
            rf = (i < GRID - 1) and solid[j0, i + 1]
            while j < GRID and solid[j, i] and \
                    ((i > 0) and solid[j, i - 1]) == lf and \
                    ((i < GRID - 1) and solid[j, i + 1]) == rf:
                j += 1
            j1 = j - 1

            faces = {
                "south": {"uv": [i, j0, i + 1, j1 + 1], "texture": "#layer0"},
                "north": {"uv": [i + 1, j0, i, j1 + 1], "texture": "#layer0"},
            }
            if not lf:   # left rim -> west face, sliver of the cell's left edge
                u = i + pad
                faces["west"] = {"uv": [u, j0, u + texel, j1 + 1], "texture": "#layer0"}
            if not rf:   # right rim -> east face
                u = i + 1 - pad - texel
                faces["east"] = {"uv": [u, j0, u + texel, j1 + 1], "texture": "#layer0"}
            if j0 == 0 or not solid[j0 - 1, i]:      # top rim -> up face
                v = j0 + pad
                faces["up"] = {"uv": [i, v, i + 1, v + texel], "texture": "#layer0"}
            if j1 == GRID - 1 or not solid[j1 + 1, i]:  # bottom rim -> down face
                v = j1 + 1 - pad - texel
                faces["down"] = {"uv": [i, v, i + 1, v + texel], "texture": "#layer0"}

            elements.append({
                "from": [float(i), float(GRID - 1 - j1), z0],
                "to": [float(i + 1), float(GRID - j0), z1],
                "faces": faces,
            })

    elements.append(
        {"from": [0.0, 0.0, 8.225], "to": [16.0, 16.0, 8.25], "faces": dict(quad_faces)},
    )

    return {
        "credit": f"kaleidoscope_snack extruded HD item model ({registry})",
        "gui_light": "front",
        "textures": {
            "layer0": f"{MODID}:item/{texture}",
            "particle": f"{MODID}:item/{texture}",
        },
        "elements": elements,
        "display": VANILLA_DISPLAY,
    }


def build_sidecar(texture: str) -> dict:
    """MCreator texture mapping sidecar (.json.textures)."""
    return {"mappings": {"default": {"name": "default", "map": {"layer0": texture}}}}


def build_item_model(registry: str, texture: str) -> dict:
    """Item model in the exact form of MCreator's item_cmodel.json.ftl output."""
    return {
        "parent": f"{MODID}:custom/{registry}",
        "textures": {
            "layer0": f"{MODID}:block/{texture}",
            "particle": f"{MODID}:item/{texture}",
        },
    }


def write_json(path: Path, data, dry: bool, counter: list):
    counter[0] += 1
    if dry:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    dry = args.dry_run

    written = [0]
    print(f"{'item':24s} {'model':34s} notes")
    for stem, (registry, texture) in sorted(ITEMS.items()):
        # 1-2: workspace model + sidecar
        model = build_model(registry, texture)
        write_json(MODELS_DIR / f"{registry}.json", model, dry, written)
        write_json(MODELS_DIR / f"{registry}.json.textures", build_sidecar(texture), dry, written)

        # 3: resource copy without textures section (mimics MCreator's copy_models)
        stripped = {k: v for k, v in model.items() if k != "textures"}
        write_json(ASSETS / "models" / "custom" / f"{registry}.json", stripped, dry, written)

        # 4: item model referencing the custom model
        write_json(ASSETS / "models" / "item" / f"{registry}.json",
                   build_item_model(registry, texture), dry, written)

        # 5: block texture copy for the texture mapping
        src_tex = ASSETS / "textures" / "item" / f"{texture}.png"
        dst_tex = ASSETS / "textures" / "block" / f"{texture}.png"
        if not dry:
            dst_tex.parent.mkdir(parents=True, exist_ok=True)
            if not dst_tex.exists() or src_tex.read_bytes() != dst_tex.read_bytes():
                shutil.copy2(src_tex, dst_tex)
        written[0] += 1

        # 6: element patch
        elem_path = ELEMENTS_DIR / f"{stem}.mod.json"
        data = json.loads(elem_path.read_text(encoding="utf-8"))
        defn = data["definition"]
        old = (defn["renderType"], defn["customModelName"])
        defn["renderType"] = 1          # Model.Type.JSON
        defn["customModelName"] = registry
        if not dry:
            elem_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written[0] += 1
        print(f"{stem:24s} models/{registry}.json  elements={len(model['elements']):3d}"
              f"  renderType {old[0]}->1, model {old[1]}->{registry}")

    print(f"\ntotal files {'to write' if dry else 'written'}: {written[0]}")
    if dry:
        print("(dry run, nothing written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
