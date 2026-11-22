"""Export Dragon Rider tracks and their optional class index from the production phase recipes."""
import argparse
import csv
import io
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from PIL import Image

SIDES = {"Player_Left": "player", "Enemy_Right": "enemy"}
LABELS = {
    0: "Idle", 5: "Advance", 11: "Return-to-formation", 17: "Hit-recoil", 18: "Recover-from-hit",
    21: "Guard", 22: "Recover-from-guard", 23: "Dodge", 24: "Recover-from-dodge", 29: "Death",
    32: "Paralysis", 33: "Recover-from-paralysis", 34: "Sleep", 35: "Wake-up",
    38: "Petrification", 39: "Recover-from-petrification", 42: "T2-Breath",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def require(condition, message):
    if not condition:
        raise ValueError(str(message))


def add_member(archive, name, data):
    info = zipfile.ZipInfo(name)
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, data)


def item_groups(native, catalog):
    names = catalog["ITEM_NAMES"]
    groups = {style: [] for style in native["style_order"]}
    lo, hi = catalog["ITEM_CATEGORIES"]["Spears & Lances"]
    ids = {names[str(i)]: i for i in range(lo, hi + 1)}
    slots = native["item_ordinals"]
    require([s["ordinal"] for s in slots] == list(range(11)), "Incomplete spear appearance slots")
    for slot in slots:
        groups[slot["style"]].extend(ids[name] for name in slot["retail_items"])
    expected = {"Leaf_Spear": [73, 74, *range(77, 88)], "Bronze_Partisan": [75], "Tide_Trident": [76]}
    for values in groups.values():
        values.sort()
    require(groups == expected, "Retail item or artwork assignment differs from the approved recipe")
    return groups


def export_track(source, timing, phase, ticks, target):
    start, end = phase["first_frame"], phase["last_frame"]
    require(timing["ticks_per_second"] == 60 and timing["frame_ticks"][start-1:end] == ticks, source)
    require(timing["canvas"] == [104, 96] and timing["anchor"] == [50, 75], source)
    archive = source / (phase["name"] + ".zip")
    if not archive.exists():
        require((start, end) == (1, timing["frames"]), source)
        archive = source / "Frame_Sequence.zip"
    target.mkdir(parents=True)
    path = target / "Timed.zip"
    with zipfile.ZipFile(archive) as original, zipfile.ZipFile(path, "w") as packaged:
        meta = json.loads(original.read("animation.json"))
        require(meta["format"] == "lordly-frame-sequence" and meta["version"] == 1, archive)
        require((meta["width"], meta["height"], meta["framesPerSecond"]) == (104, 96, 60), archive)
        require(meta["origin"] == {"x": 50, "y": 75} and meta["totalTicks"] == sum(ticks), archive)
        require([f["durationTicks"] for f in meta["frames"]] == ticks, archive)
        manifest = {k: meta[k] for k in ("format", "version", "width", "height", "origin", "framesPerSecond", "totalTicks")}
        frames = []
        elapsed = 0
        for i, frame in enumerate(meta["frames"]):
            duration = ticks[i]
            require(type(duration) is int and duration > 0 and frame["startTick"] == elapsed, archive)
            raw = original.read(frame["file"])
            require(raw == (source / f"frame_{start+i:02}.png").read_bytes(), archive)
            with Image.open(io.BytesIO(raw)) as image:
                require(image.mode == "RGBA" and image.size == (104, 96), archive)
                require(not any(image.getchannel("A").histogram()[1:255]), archive)
                pixels = Image.frombytes("RGBA", image.size, image.tobytes())
            name = f"{i+1:03}.png"
            pixels.save(target / name, optimize=True)
            add_member(packaged, name, (target / name).read_bytes())
            frames.append(dict(file=name, startTick=elapsed, durationTicks=duration))
            elapsed += duration
        manifest["frames"] = frames
        add_member(packaged, "animation.json", json.dumps(manifest, separators=(",", ":")).encode())
    with zipfile.ZipFile(path) as check:
        require(check.testzip() is None and json.loads(check.read("animation.json")) == manifest, path)
        for frame in frames:
            name = frame["file"]
            require(check.read(name) == (target / name).read_bytes(), path)
    return path


def build(stage, catalog, art, routes, donor_class):
    jobs = read(art / "Actions.json")
    native = read(art / "Native/Frames.json")
    groups = item_groups(native, catalog)
    entries = []
    keys = set()
    intended_attack = catalog["ACTION_NAMES"]["40"]
    with routes.open(encoding="utf-8-sig", newline="") as file:
        breath_routes = {int(r["action_id"]) for r in csv.DictReader(file)
                         if r["class"] == donor_class and r["selector_dec"] == "42"
                         and r["attack_lane"] == "Normal" and r["action"] == intended_attack}
    require(breath_routes == {40}, "Unconfirmed breath action")
    for action, job in jobs.items():
        for phase in native["selector_phases"][action]:
            selector = phase["selector"]
            key, action_id = "motion", selector
            if action == "11_Breath_Attack":
                require((phase["name"], selector) == (intended_attack.replace(" ", "_"), 42), "Reconfirm the authored attack")
                key, action_id = "attack", 40
            ticks = job["ticks"][phase["first_frame"]-1:phase["last_frame"]]
            folder = f"{selector:02}-{LABELS[selector]}"
            for view, side in SIDES.items():
                identity = (key, action_id, side)
                require(identity not in keys, identity)
                keys.add(identity)
                entry = {key: action_id, "side": side, "loop": job["loop"], "behind": False}
                require(type(job["loop"]) is bool and job["loop"] == (selector in (0, 5)), identity)
                weapons = []
                for role in ["Body", *groups]:
                    source = art / role / action / view
                    timing = read(source / "Timing.json")
                    require(phase in timing["phases"] and timing["loop"] == job["loop"], source)
                    path = export_track(source, timing, phase, ticks, stage / folder / view / role)
                    relative = path.relative_to(stage).as_posix()
                    if role == "Body":
                        entry["body"] = relative
                    else:
                        weapons.append({"path": relative, "items": groups[role]})
                entry["weapons"] = weapons
                entries.append(entry)
    expected = {(("attack", 40) if s == 42 else ("motion", s)) + (side,)
                for s in LABELS for side in SIDES.values()}
    require(keys == expected, "Missing or unexpected action/side")
    index = {"format": "lordly-class-animations", "version": 1, "sequences": entries}
    (stage / "class-animations.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--art", type=Path, required=True)
    parser.add_argument("--routes", type=Path, required=True)
    parser.add_argument("--donor-class", required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--class-dir", type=Path, required=True)
    parser.add_argument("--download", type=Path, required=True)
    args = parser.parse_args()
    dest = args.class_dir.resolve()
    with tempfile.TemporaryDirectory(dir=dest.parent) as tmp:
        stage = Path(tmp) / dest.name
        build(stage, read(args.catalog), args.art, args.routes, args.donor_class)
        shutil.copyfile(dest / "README.md", stage / "README.md")
        files = sorted(f.relative_to(stage) for f in stage.rglob("*") if f.is_file())
        stale = {f.relative_to(dest) for f in dest.rglob("*") if f.is_file()} - set(files)
        require(not stale, f"Review stale files before publishing: {stale}")
        bundle = Path(tmp) / "download.zip"
        with zipfile.ZipFile(bundle, "w") as archive:
            for file in files:
                add_member(archive, (Path(dest.name) / file).as_posix(), (stage / file).read_bytes())
        with zipfile.ZipFile(bundle) as archive:
            require(archive.testzip() is None and len(archive.namelist()) == len(files), bundle)
            for file in files:
                require(archive.read((Path(dest.name) / file).as_posix()) == (stage / file).read_bytes(), file)
        for file in files:
            out = dest / file
            if not out.exists() or out.read_bytes() != (stage / file).read_bytes():
                out.parent.mkdir(parents=True, exist_ok=True)
                (stage / file).replace(out)
        args.download.parent.mkdir(parents=True, exist_ok=True)
        bundle.replace(args.download)
    print(f"Validated and exported {dest.name} to {args.download}")


if __name__ == "__main__":
    main()
