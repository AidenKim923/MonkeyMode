#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""[Unity] Check assembly definition (.asmdef) references against guardrails/module-rules.json.

Every assembly named <assemblyPrefix><Module> may reference only the modules
listed in that module's "mayReference". Test assemblies (*.Tests) are skipped.
Exits 1 on violations.

    uv run tools/guardrails/asmdef_rules.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

SKIP_DIRS = {"Library", "Temp", "ThirdParty"}


def find_assets_dir(root: Path) -> Path | None:
    if (root / "ProjectSettings" / "ProjectVersion.txt").is_file():
        return root / "Assets"
    candidates = [d for d in root.iterdir() if d.is_dir() and (d / "ProjectSettings" / "ProjectVersion.txt").is_file()]
    if len(candidates) == 1:
        return candidates[0] / "Assets"
    if len(candidates) > 1:
        raise SystemExit(f"More than one Unity project under {root}: {', '.join(d.name for d in candidates)}. Pass --assets.")
    return root / "Assets" if (root / "Assets").is_dir() else None


def read_guid(meta: Path) -> str | None:
    if not meta.is_file():
        return None
    for line in meta.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^guid:\s*(\S+)", line)
        if m:
            return m.group(1)
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="project root")
    parser.add_argument("--assets", help="Unity Assets folder (default: auto-detect)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    rules = json.loads((root / "guardrails" / "module-rules.json").read_text(encoding="utf-8"))
    prefix = rules["assemblyPrefix"]
    modules = rules["modules"]
    blocked = rules.get("mustNotBeReferencedBy", {})

    assets = Path(args.assets).resolve() if args.assets else find_assets_dir(root)
    if not assets or not assets.is_dir():
        print("asmdef rules passed: no Assets folder yet, 0 assemblies checked.")
        return 0

    defs: dict[str, dict] = {}
    guid_to_name: dict[str, str] = {}
    for f in assets.rglob("*.asmdef"):
        if SKIP_DIRS.intersection(f.relative_to(assets).parts):
            continue
        data = json.loads(f.read_text(encoding="utf-8-sig"))
        defs[data["name"]] = data
        guid = read_guid(f.with_name(f.name + ".meta"))
        if guid:
            guid_to_name[guid] = data["name"]

    def module_of(assembly: str) -> str | None:
        if not assembly.startswith(prefix):
            return None
        rest = assembly[len(prefix):]
        return None if rest.endswith(".Tests") else rest

    violations: list[str] = []
    for name, data in sorted(defs.items()):
        module = module_of(name)
        if not module:
            continue
        if module not in modules:
            violations.append(
                f"ASMDEF:UNKNOWN_MODULE {name}  Module '{module}' is not in guardrails/module-rules.json. "
                "If it is a new module, define its allowed dependency direction in the rules file first (user approval)."
            )
            continue
        allowed = set(modules[module].get("mayReference", []))
        for ref in data.get("references", []):
            ref_name = guid_to_name.get(ref[5:]) if ref.startswith("GUID:") else ref
            ref_module = module_of(ref_name) if ref_name else None
            if ref_module and ref_module not in allowed:
                reason = f" {blocked[ref_module]}" if ref_module in blocked else ""
                violations.append(
                    f"ASMDEF:FORBIDDEN_REFERENCE {name} -> {ref_name}  {module} may not reference {ref_module}.{reason} "
                    "Invert the dependency or move the shared type into Core."
                )
        platforms = data.get("includePlatforms", [])
        if module != "Editor" and platforms == ["Editor"]:
            violations.append(
                f"ASMDEF:EDITOR_ONLY_RUNTIME {name}  A runtime module is set to the Editor-only platform. "
                f"Move editor code into {prefix}Editor."
            )

    if violations:
        for v in violations:
            print(v, file=sys.stderr)
        print(f"{len(violations)} asmdef rule violation(s). Fix the dependency direction instead of working around the reference.", file=sys.stderr)
        return 1
    print(f"asmdef rules passed: {len(defs)} assembl{'y' if len(defs) == 1 else 'ies'} checked, 0 violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
