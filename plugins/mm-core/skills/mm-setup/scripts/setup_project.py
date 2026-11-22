#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""MonkeyMode project setup: writes .monkeymode/config.json and wires the core
template plus one engine adapter into a game project.

Claude Code runs this from the mm-setup skill after the interview. Other agents
(or people) can run it directly; --interactive asks the same questions.

    uv run setup_project.py --target . --show
    uv run setup_project.py --target . --detect
    uv run setup_project.py --target . --interactive
    uv run setup_project.py --target . --set engine=unity --set coding_level=can-read-code ... --apply
    uv run setup_project.py --target . --apply --adapter-dir <path to an mm-<engine>/adapter folder>
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve()
CORE_PLUGIN = HERE.parents[3]
TEMPLATE = CORE_PLUGIN / "template"
PLUGINS_DIR = CORE_PLUGIN.parent
CONFIG_PATH = Path(".monkeymode") / "config.json"
ENGINES = ["godot", "unity", "unreal", "bevy", "other"]
STAGES = ["idea", "planning", "building", "polishing"]
LEVELS = ["strict", "standard", "relaxed"]
PLATFORMS = ["pc", "mobile", "web", "console"]
TEXT_SUFFIXES = {".md", ".json", ".toml", ".yaml", ".yml", ".txt", ".ps1", ".py", ".cs", ".mjs", ".html", ".cmd", ".csv", ".example", ""}
MARK_START = "<!-- monkeymode:start -->"
MARK_END = "<!-- monkeymode:end -->"

DEFAULTS = {
    "version": 1,
    "project_name": None,
    "coding_level": None,
    "engine": None,
    "uses_chatgpt": None,
    "team": None,
    "genre": None,
    "platforms": None,
    "multiplayer": None,
    "max_players": None,
    "stage": None,
    "guardrail_level": None,
    "docs_dir": "docs/",
    "doc_language": "English",
    "communication_language": "English",
}

NEXT_STEP = {
    "idea": ("mm-brainstorm-game", "then mm-create-game-brief"),
    "planning": ("mm-create-game-brief", "or mm-gdd if you already have a brief"),
    "building": ("mm-document-project", "then mm-dev-story; mm-quick-dev for small changes"),
    "polishing": ("mm-playtest-plan", "then mm-performance-test and mm-code-review"),
}

QUESTIONS = [
    ("coding_level", "Can you read code?", ["can-read-code", "cannot-read-code"]),
    ("engine", "Which engine?", ENGINES),
    ("uses_chatgpt", "Do you also use ChatGPT? (recommended for images)", ["yes", "no"]),
    ("team", "Solo or team?", ["solo", "team"]),
    ("genre", "Genre (free text, e.g. co-op puzzle, roguelike)", None),
    ("platforms", "Target platforms (comma-separated: pc, mobile, web, console)", None),
    ("multiplayer", "Multiplayer?", ["yes", "no"]),
    ("max_players", "Maximum players (number, multiplayer only)", None),
    ("stage", "Where are you now?", STAGES),
    ("guardrail_level", "Guardrail level?", LEVELS),
    ("docs_dir", "Docs folder", None),
    ("project_name", "Game name", None),
]


def load_config(target: Path) -> dict:
    path = target / CONFIG_PATH
    data = dict(DEFAULTS)
    if path.is_file():
        data.update(json.loads(path.read_text(encoding="utf-8")))
    return data


def normalize(key: str, value):
    if value is None:
        return None
    if key in ("uses_chatgpt", "multiplayer"):
        if isinstance(value, bool):
            return value
        v = str(value).strip().lower()
        if v in ("yes", "y", "true", "1"):
            return True
        if v in ("no", "n", "false", "0"):
            return False
        raise SystemExit(f"{key}: expected yes or no, got {value!r}")
    if key == "platforms":
        items = value if isinstance(value, list) else [p.strip().lower() for p in str(value).split(",") if p.strip()]
        bad = [p for p in items if p not in PLATFORMS]
        if bad:
            raise SystemExit(f"platforms: unknown {bad}; choose from {PLATFORMS}")
        return items
    if key == "max_players":
        return int(value) if str(value).strip() else None
    if key == "coding_level":
        v = str(value).strip().lower()
        mapping = {"i can read code": "can-read-code", "i can't read code": "cannot-read-code", "i cannot read code": "cannot-read-code"}
        v = mapping.get(v, v)
        if v not in ("can-read-code", "cannot-read-code"):
            raise SystemExit("coding_level: expected can-read-code or cannot-read-code")
        return v
    if key == "engine" and value not in ENGINES:
        raise SystemExit(f"engine: choose from {ENGINES}")
    if key == "stage" and value not in STAGES:
        raise SystemExit(f"stage: choose from {STAGES}")
    if key == "guardrail_level" and value not in LEVELS:
        raise SystemExit(f"guardrail_level: choose from {LEVELS}")
    if key == "docs_dir":
        v = str(value).strip().replace("\\", "/").strip("/")
        if not v or ".." in v.split("/") or Path(v).is_absolute():
            raise SystemExit("docs_dir: give a folder relative to the project root, e.g. docs/")
        return v + "/"
    return value


def detect_engine(target: Path) -> list[str]:
    found = []
    if (target / "ProjectSettings" / "ProjectVersion.txt").is_file() or any(target.glob("*/ProjectSettings/ProjectVersion.txt")):
        found.append("unity")
    if (target / "project.godot").is_file() or any(target.glob("*/project.godot")):
        found.append("godot")
    if any(target.glob("*.uproject")) or any(target.glob("*/*.uproject")):
        found.append("unreal")
    cargo = target / "Cargo.toml"
    if cargo.is_file() and "bevy" in cargo.read_text(encoding="utf-8", errors="replace"):
        found.append("bevy")
    return found


def effective_level(cfg: dict) -> str:
    if cfg.get("coding_level") == "cannot-read-code":
        return "strict"
    return cfg.get("guardrail_level") or "standard"


def missing_questions(cfg: dict) -> list[str]:
    missing = []
    for key, _, _ in QUESTIONS:
        if key == "guardrail_level" and cfg.get("coding_level") == "cannot-read-code":
            continue
        if key == "max_players" and cfg.get("multiplayer") is not True:
            continue
        if cfg.get(key) is None:
            missing.append(key)
    return missing


def interactive(cfg: dict, target: Path) -> dict:
    detected = detect_engine(target)
    for key, prompt, choices in QUESTIONS:
        if key == "guardrail_level" and cfg.get("coding_level") == "cannot-read-code":
            print("Guardrail level: strict (fixed because you said you do not read code).")
            continue
        if key == "max_players" and cfg.get("multiplayer") is not True:
            continue
        current = cfg.get(key)
        default = current
        if key == "engine" and current is None and len(detected) == 1:
            default = detected[0]
        if key == "project_name" and current is None:
            default = target.resolve().name
        shown = ", ".join(current) if isinstance(current, list) else ("yes" if current is True else "no" if current is False else current)
        hint = f" [{shown if current is not None else default}]" if (current is not None or default is not None) else ""
        opts = f" ({' / '.join(choices)})" if choices else ""
        answer = input(f"{prompt}{opts}{hint}: ").strip()
        if not answer:
            answer = default
        if answer is None:
            continue
        cfg[key] = normalize(key, answer)
    return cfg


def assembly_prefix(name: str) -> str:
    parts = re.findall(r"[A-Za-z0-9]+", name)
    ident = "".join(p[:1].upper() + p[1:] for p in parts) or "Game"
    if ident[0].isdigit():
        ident = "Game" + ident
    return ident + "."


def placeholders(cfg: dict) -> dict:
    name = cfg.get("project_name") or "MyGame"
    engine = cfg.get("engine") or "other"
    platform = engine if engine in ("unity", "unreal", "godot") else "other"
    return {
        "<YourGame>": name,
        "<YourName>": "Developer",
        "<CommunicationLanguage>": cfg.get("communication_language") or "English",
        "<DocumentLanguage>": cfg.get("doc_language") or "English",
        "<Experience>": "beginner" if cfg.get("coding_level") == "cannot-read-code" else "intermediate",
        "<PrimaryPlatform>": platform,
        "<Engine>": engine,
        "<AssemblyPrefix>": assembly_prefix(name),
    }


def rewrite_docs_dir(text: str, docs_dir: str) -> str:
    if docs_dir == "docs/":
        return text
    return re.sub(r"(?<![\w./-])docs/(?=(ai|engine|project|work|guides|licenses)(/|\b))", docs_dir, text)


class Installer:
    def __init__(self, target: Path, cfg: dict, force: bool, dry_run: bool):
        self.target = target
        self.cfg = cfg
        self.force = force
        self.dry = dry_run
        self.written: list[str] = []
        self.skipped: list[str] = []
        self.subs = placeholders(cfg)
        self.docs_dir = cfg.get("docs_dir") or "docs/"

    def map_path(self, rel: str) -> str:
        if rel.startswith("docs/"):
            return self.docs_dir + rel[len("docs/"):]
        return rel

    def render(self, text: str) -> str:
        for k, v in self.subs.items():
            text = text.replace(k, v)
        return rewrite_docs_dir(text, self.docs_dir)

    def write(self, rel: str, data: bytes | str, overwrite: bool | None = None):
        dest = self.target / rel
        overwrite = self.force if overwrite is None else overwrite
        if dest.exists() and not overwrite:
            self.skipped.append(rel)
            return
        self.written.append(rel)
        if self.dry:
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, str):
            dest.write_text(data, encoding="utf-8", newline="\n")
        else:
            dest.write_bytes(data)

    def copy_tree(self, src: Path, dest_prefix: str = "", exclude: tuple[str, ...] = ()):
        for f in sorted(src.rglob("*")):
            if not f.is_file() or "__pycache__" in f.parts:
                continue
            rel = f.relative_to(src).as_posix()
            if any(fnmatch.fnmatch(rel, pat) for pat in exclude):
                continue
            out = self.map_path(dest_prefix + rel)
            if f.suffix in TEXT_SUFFIXES:
                self.write(out, self.render(f.read_text(encoding="utf-8")))
            else:
                self.write(out, f.read_bytes())

    def append_lines(self, rel: str, block: str):
        dest = self.target / rel
        existing = dest.read_text(encoding="utf-8") if dest.is_file() else ""
        have = set(existing.splitlines())
        lines = block.strip().splitlines()
        header = lines[0] if lines and lines[0].startswith("#") else "# Added by MonkeyMode mm-setup"
        if header in have:
            add = [l for l in lines if l.strip() and not l.startswith("#") and l not in have]
        else:
            add = [header] + [l for l in lines if l != header and (l.startswith("#") or l not in have)]
        if not [l for l in add if not l.startswith("#")] and header in have:
            return
        nl = chr(10)
        sep = "" if not existing or existing.endswith(nl) else nl
        text = existing + sep + (nl if existing else "") + nl.join(add) + nl
        self.write(rel, text, overwrite=True)


def find_adapter(engine: str, adapter_dir: str | None) -> Path | None:
    if engine == "other":
        return None
    if adapter_dir:
        p = Path(adapter_dir).resolve()
        if not (p / "adapter.json").is_file():
            raise SystemExit(f"--adapter-dir {p} has no adapter.json")
        return p
    sibling = PLUGINS_DIR / f"mm-{engine}" / "adapter"
    if (sibling / "adapter.json").is_file():
        return sibling
    raise SystemExit(
        f"Adapter for {engine} not found. Install the mm-{engine} plugin and pass its adapter folder with "
        f"--adapter-dir (the mm-{engine} skill prints the path), or run this script from a full MonkeyMode checkout."
    )


def build_agents_section(cfg: dict, adapter: Path | None, docs_dir: str) -> str:
    base = (TEMPLATE / "AGENTS.base.md").read_text(encoding="utf-8")
    engine_snippet = (adapter / "AGENTS.snippet.md").read_text(encoding="utf-8") if adapter else (
        "## Engine: other\n\nNo engine adapter is installed. Describe your engine's structure, banned patterns, "
        f"build and test commands in [`{docs_dir}engine/`]({docs_dir}engine/README.md).\n"
    )
    if cfg.get("coding_level") == "cannot-read-code":
        user = (
            "The user does **not** read code.\n\n"
            "- Verify your own work before saying done: run the tests, the build, or the game, and look at the result.\n"
            "- Explain in plain words and with screenshots, never with code listings.\n"
            "- Always ask before risky actions: deleting or moving files, large refactors, installing packages, committing or pushing.\n"
            "- Guardrails run at **strict** level."
        )
    else:
        user = (
            "The user reads code.\n\n"
            "- Report in reviewable form: a diff summary and why each change was made.\n"
            f"- Guardrails run at **{effective_level(cfg)}** level."
        )
    if cfg.get("team") == "team":
        team = f"Team project. Follow [{docs_dir}ai/15_TEAM_GIT_WORKFLOW.md]({docs_dir}ai/15_TEAM_GIT_WORKFLOW.md): branch per task, pull requests, review checklist."
    else:
        team = "Solo project: no CODEOWNERS or ownership scheme. Work on a branch per task when the user asks for commits."
    if cfg.get("multiplayer"):
        players = f" for up to {cfg['max_players']} players" if cfg.get("max_players") else ""
        mp = (
            f"Multiplayer{players}. The server/host decides game state ([{docs_dir}ai/04]({docs_dir}ai/04_NETWORK_AUTHORITY_AND_TESTING.md), "
            f"[{docs_dir}engine/multiplayer.md]({docs_dir}engine/multiplayer.md)). Networked changes are not done without a multi-client check (M2)."
        )
    else:
        mp = "Single-player. Skip the networking rules and multiplayer grades; the verification levels L1-L3 still apply."
    images = (
        "Images: the user also uses ChatGPT. `mm-concept-art` writes ready-to-paste ChatGPT prompts plus an import checklist."
        if cfg.get("uses_chatgpt") else
        "Images: no ChatGPT. `mm-concept-art` uses the Codex CLI if available, otherwise Blender blockouts, free asset libraries or other generators."
    )
    platforms = ", ".join(cfg.get("platforms") or []) or "undecided"
    text = base
    for k, v in {
        "{{USER_SECTION}}": user, "{{TEAM_SECTION}}": team, "{{MULTIPLAYER_SECTION}}": mp, "{{IMAGES_SECTION}}": images,
        "{{ENGINE_SECTION}}": engine_snippet.strip(), "{{GENRE}}": cfg.get("genre") or "undecided",
        "{{PLATFORMS}}": platforms, "{{STAGE}}": cfg.get("stage") or "undecided",
    }.items():
        text = text.replace(k, v)
    return text


def apply(target: Path, cfg: dict, adapter_dir: str | None, force: bool, dry: bool, git_hooks: bool) -> dict:
    if not TEMPLATE.is_dir():
        raise SystemExit(f"Template not found at {TEMPLATE}.")
    engine = cfg.get("engine") or "other"
    adapter = find_adapter(engine, adapter_dir)
    inst = Installer(target, cfg, force, dry)
    docs_dir = inst.docs_dir
    level = effective_level(cfg)
    multiplayer = bool(cfg.get("multiplayer"))

    exclude = ["AGENTS.base.md", "CLAUDE.md", "gitignore.fragment", "engine-other/*"]
    if not multiplayer:
        exclude.append("docs/ai/04_NETWORK_AUTHORITY_AND_TESTING.md")
    if cfg.get("team") != "team":
        exclude.append("docs/ai/15_TEAM_GIT_WORKFLOW.md")
    inst.copy_tree(TEMPLATE, exclude=tuple(exclude))

    if adapter:
        meta = json.loads((adapter / "adapter.json").read_text(encoding="utf-8"))
        doc_exclude = () if multiplayer else ("multiplayer.md",)
        inst.copy_tree(adapter / "docs", "docs/engine/", exclude=doc_exclude)
        if (adapter / "tools").is_dir():
            inst.copy_tree(adapter / "tools", "tools/")
        for extra in sorted(adapter.glob("*.example")):
            inst.write(extra.name, inst.render(extra.read_text(encoding="utf-8")))
        mp_only = set(meta.get("multiplayerOnlyRules", []))
        for g in sorted((adapter / "guardrails").glob("*.json")):
            preset = json.loads(inst.render(g.read_text(encoding="utf-8")))
            dest = target / "guardrails" / g.name
            if "rules" not in preset:
                inst.write(f"guardrails/{g.name}", json.dumps(preset, indent=2) + "\n")
                continue
            if dest.is_file() and not force:
                data = json.loads(dest.read_text(encoding="utf-8"))
            else:
                data = preset
            data["noComments"] = bool(preset.get("noComments")) and level == "strict"
            ids = {r["id"] for r in data["rules"]}
            if multiplayer:
                data["rules"] += [r for r in preset["rules"] if r["id"] in mp_only and r["id"] not in ids]
            else:
                data["rules"] = [r for r in data["rules"] if r["id"] not in mp_only]
            new_text = json.dumps(data, indent=2) + "\n"
            if not dest.is_file() or dest.read_text(encoding="utf-8") != new_text:
                inst.write(f"guardrails/{g.name}", new_text, overwrite=True)
        for name in ("gitignore", "gitattributes"):
            if (adapter / name).is_file():
                inst.append_lines("." + name, (adapter / name).read_text(encoding="utf-8"))
    else:
        inst.copy_tree(TEMPLATE / "engine-other", "docs/engine/")
    inst.append_lines(".gitignore", (TEMPLATE / "gitignore.fragment").read_text(encoding="utf-8"))

    section = MARK_START + "\n" + inst.render(build_agents_section(cfg, adapter, docs_dir)).strip() + "\n" + MARK_END + "\n"
    agents = target / "AGENTS.md"
    if agents.is_file():
        old = agents.read_text(encoding="utf-8")
        if MARK_START in old and MARK_END in old:
            new = old[: old.index(MARK_START)] + section + old[old.index(MARK_END) + len(MARK_END):].lstrip("\n")
        else:
            new = old.rstrip() + "\n\n" + section
        inst.write("AGENTS.md", new, overwrite=True)
    else:
        inst.write("AGENTS.md", f"# AGENTS.md: {cfg.get('project_name') or 'MyGame'}\n\n" + section, overwrite=True)
    claude = target / "CLAUDE.md"
    if not claude.is_file():
        inst.write("CLAUDE.md", "@AGENTS.md\n")
    elif "@AGENTS.md" not in claude.read_text(encoding="utf-8"):
        inst.write("CLAUDE.md", claude.read_text(encoding="utf-8").rstrip() + "\n\n@AGENTS.md\n", overwrite=True)

    cfg_out = {k: cfg.get(k) for k in DEFAULTS}
    cfg_out["guardrail_level"] = level
    inst.write(CONFIG_PATH.as_posix(), json.dumps(cfg_out, indent=2) + "\n", overwrite=True)

    hooks_installed = False
    if git_hooks and not dry and (target / ".git").exists():
        subprocess.run(["git", "-C", str(target), "config", "core.hooksPath", ".githooks"], check=False)
        hooks_installed = True
    return {"written": inst.written, "skipped": inst.skipped, "adapter": str(adapter) if adapter else None,
            "guardrail_level": level, "git_hooks": hooks_installed}


def copy_skills(target: Path, where: str, packs: list[str], engine: str):
    roots = [CORE_PLUGIN] + [PLUGINS_DIR / p for p in packs]
    if engine and engine != "other":
        roots.append(PLUGINS_DIR / f"mm-{engine}")
    dests = {"agents": [".agents/skills"], "claude": [".claude/skills"], "both": [".agents/skills", ".claude/skills"]}[where]
    count = 0
    for root in roots:
        skills = root / "skills"
        if not skills.is_dir():
            raise SystemExit(f"{skills} not found: copying skills needs a full MonkeyMode checkout.")
        for skill in sorted(skills.iterdir()):
            if skill.is_dir():
                for d in dests:
                    out = target / d / skill.name
                    if out.exists():
                        shutil.rmtree(out)
                    shutil.copytree(skill, out, ignore=shutil.ignore_patterns("__pycache__"))
                count += 1
    return count


def summary(cfg: dict, result: dict | None, target: Path) -> str:
    level = effective_level(cfg)
    stage = cfg.get("stage") or "idea"
    first, then = NEXT_STEP[stage]
    lines = [
        f"MonkeyMode is set up for {cfg.get('project_name') or target.name}.",
        f"- Engine: {cfg.get('engine') or 'other'}" + (" (adapter installed)" if result and result.get("adapter") else ""),
        f"- You {'do not read' if cfg.get('coding_level') == 'cannot-read-code' else 'read'} code, so guardrails run at {level} level"
        + (" and agents check their own work, explain in plain words, and ask before risky steps." if cfg.get("coding_level") == "cannot-read-code" else " and reports come as diff summaries."),
        f"- {'Team' if cfg.get('team') == 'team' else 'Solo'} project; {'multiplayer' if cfg.get('multiplayer') else 'single-player'}; platforms: {', '.join(cfg.get('platforms') or []) or 'undecided'}",
        f"- Images: {'ChatGPT prompts' if cfg.get('uses_chatgpt') else 'Codex CLI or alternatives'}",
        f"- Docs live in {cfg.get('docs_dir') or 'docs/'}; settings in {CONFIG_PATH.as_posix()}",
    ]
    if result:
        lines.append(f"- Files written: {len(result['written'])}; kept as they were: {len(result['skipped'])}")
        if not result.get("git_hooks"):
            lines.append("- Optional: run `git config core.hooksPath .githooks` to check guardrails before every commit.")
    lines.append(f"Next step: run {first} ({then}).")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", default=".", help="game project root")
    ap.add_argument("--show", action="store_true", help="print the current config and the questions still open (JSON)")
    ap.add_argument("--detect", action="store_true", help="print engines detected in the target (JSON)")
    ap.add_argument("--interactive", action="store_true", help="ask the setup questions on the terminal")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE", help="set an answer (repeatable)")
    ap.add_argument("--apply", action="store_true", help="write config and install core + engine adapter")
    ap.add_argument("--adapter-dir", help="engine adapter folder (the mm-<engine> plugin's adapter/)")
    ap.add_argument("--force", action="store_true", help="overwrite existing template files (AGENTS.md section and config are always updated)")
    ap.add_argument("--dry-run", action="store_true", help="show what would be written")
    ap.add_argument("--git-hooks", action="store_true", help="set core.hooksPath to .githooks")
    ap.add_argument("--copy-skills", choices=["none", "agents", "claude", "both"], default="none",
                    help="copy skills into the project for agents without the Claude Code plugin (agents = .agents/skills)")
    ap.add_argument("--packs", default="", help="optional packs to copy with --copy-skills, e.g. mm-agents,mm-art-tools")
    args = ap.parse_args(argv)

    target = Path(args.target).resolve()
    cfg = load_config(target)

    if args.detect:
        print(json.dumps({"detected": detect_engine(target)}))
        return 0
    for item in args.set:
        if "=" not in item:
            raise SystemExit(f"--set expects KEY=VALUE, got {item!r}")
        key, value = item.split("=", 1)
        if key not in DEFAULTS:
            raise SystemExit(f"unknown key {key!r}; known: {sorted(DEFAULTS)}")
        cfg[key] = normalize(key, value)
    if args.interactive:
        cfg = interactive(cfg, target)
    if args.show:
        print(json.dumps({"config": cfg, "configFile": str(target / CONFIG_PATH), "exists": (target / CONFIG_PATH).is_file(),
                          "missing": missing_questions(cfg), "detected": detect_engine(target)}, indent=2))
        if not args.apply:
            return 0
    if not args.apply and not args.interactive:
        ap.print_help()
        return 0

    if cfg.get("project_name") is None:
        cfg["project_name"] = target.name
    if cfg.get("engine") is None:
        found = detect_engine(target)
        if len(found) != 1:
            raise SystemExit(f"engine is not set and detection found {found or 'nothing'}; pass --set engine=<{'|'.join(ENGINES)}>")
        cfg["engine"] = found[0]
    still = [k for k in missing_questions(cfg) if k not in ("genre", "platforms", "max_players")]
    if still:
        raise SystemExit(f"answers missing: {still}. Use --set or --interactive.")

    result = apply(target, cfg, args.adapter_dir, args.force, args.dry_run, args.git_hooks)
    if args.copy_skills != "none":
        packs = [p.strip() for p in args.packs.split(",") if p.strip()]
        n = copy_skills(target, args.copy_skills, packs, cfg["engine"])
        print(f"Copied {n} skills.")
    if args.dry_run:
        print(json.dumps(result, indent=2))
    print(summary(cfg, result, target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
