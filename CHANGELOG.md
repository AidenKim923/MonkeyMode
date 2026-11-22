# Changelog

All notable changes to MonkeyMode are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-11-23

First public release.

### Added

- `mm-core` plugin: 43 `mm-` workflow skills from idea to retrospective (brief, GDD, narrative, UX, architecture, epics and stories, dev, code review, tests, playtest and performance plans, retrospective) and the `/mm-setup` onboarding interview.
- Agent operating docs (`docs/ai/`), the guardrail checker with an after-edit hook and optional pre-commit hook, strict/standard/relaxed guardrail levels and a secrets/personal-path profile.
- Coding-level setting ("I can read code" / "I can't read code") that changes how agents verify and explain their work.
- Engine adapters: `mm-godot` (checked against the Godot 4.7 docs), `mm-unity` (targets Unity 6; needs community verification), `mm-unreal` (partly checked against the Unreal Engine 5.9 docs), `mm-bevy` (checked against Bevy 0.20).
- Optional packs: `mm-agents` (persona agents and party mode) and `mm-art-tools` (concept art, Blender, RenderDoc and Nsight Graphics CLI harnesses).
- Setup for agents without Claude Code through `setup_project.py --copy-skills agents`.
- README in 11 languages, user guide, onboarding and inventory docs, contributing guide, Code of Conduct, security and support policies, issue and discussion forms, CI.
- Claude Code subagents: 16 in `mm-agents` (`mm-game-designer`, `mm-level-designer`, `mm-gameplay-programmer`, `mm-code-reviewer`, `mm-qa-tester`, `mm-performance-profiler`, `mm-network-engineer`, `mm-technical-artist`, `mm-ui-ux-designer`, `mm-narrative-writer`, `mm-audio-designer`, `mm-economy-balancer`, `mm-build-release-engineer`, `mm-localization`, `mm-guardrail-auditor`, `mm-docs-writer`) and one engine expert per engine plugin (`mm-godot-expert`, `mm-unity-expert`, `mm-unreal-expert`, `mm-bevy-expert`). Each reads the project config and docs, keeps the guardrails, verifies its own work and reports in plain language for non-coders. The code reviewer and guardrail auditor are read-only.
- `mm-help` lists the subagents and explains how to call them; the user guide has a new "Agents" section.
- `tools/check_manifests.py` checks agent frontmatter (name, `mm-` prefix, description, tools).
- GitHub Sponsors: `.github/FUNDING.yml`, a sponsor badge and section in every README, and a note in `SUPPORT.md`.

[Unreleased]: https://github.com/AidenKim923/MonkeyMode/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AidenKim923/MonkeyMode/releases/tag/v0.1.0
