#!/usr/bin/env python3
"""Regenerate tools/apps.json from the suite registry.

apps.json is what the index generator reads. It is NOT hand-edited any more:
it is derived from nijatva-suite/docs/APP-REGISTRY.json, which is verified
against the repositories.

Usage:
    python3 tools/gen_apps_json.py [path/to/APP-REGISTRY.json]
    python3 tools/gen_apps_json.py --check     # exit 1 if apps.json is stale
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_REGISTRY = HERE.parent.parent / "nijatva-suite" / "docs" / "APP-REGISTRY.json"
TARGET = HERE / "apps.json"


def slug(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())


def build(registry_path: Path) -> dict:
    reg = json.loads(registry_path.read_text())
    apps = []
    for a in reg["apps"]:
        apps.append({
            "code": a["code"],
            "name": a["name"],
            "site": slug(a["name"]),
            "repo": a["repo"],
            "package": a["package"],
            "phase": a["phase"],
            "status": a["status"],
            "ui": a["ui"],
            "indexed": a["indexed"],
        })
    apps.sort(key=lambda a: a["name"].lower())
    return {
        "owner": reg["owner"],
        "generated_from": "nijatva-suite/docs/APP-REGISTRY.json",
        "generated": reg["generated"],
        "counts": reg["counts"],
        "apps": apps,
    }


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    registry = Path(args[0]) if args else DEFAULT_REGISTRY
    if not registry.exists():
        print(f"registry not found: {registry}", file=sys.stderr)
        return 2
    body = json.dumps(build(registry), indent=2) + "\n"
    if "--check" in sys.argv:
        if not TARGET.exists() or TARGET.read_text() != body:
            print("apps.json is stale, run tools/gen_apps_json.py", file=sys.stderr)
            return 1
        print("apps.json up to date")
        return 0
    TARGET.write_text(body)
    data = json.loads(body)
    print(f"wrote {TARGET.relative_to(HERE.parent)}: {len(data['apps'])} apps, "
          f"{sum(1 for a in data['apps'] if a['repo'])} with a repo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
