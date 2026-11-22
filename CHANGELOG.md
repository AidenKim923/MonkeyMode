# Changelog

All notable changes to MonkeyMode are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - Unreleased

First public release.

### Added

- `mm-core` plugin: 43 `mm-` workflow skills from idea to retrospective (brief, GDD, narrative, UX, architecture, epics and stories, dev, code review, tests, playtest and performance plans, retrospective) and the `/mm-setup` onboarding interview.
- Agent operating docs (`docs/ai/`), the guardrail checker with an after-edit hook and optional pre-commit hook, strict/standard/relaxed guardrail levels and a secrets/personal-path profile.
- Coding-level setting ("I can read code" / "I can't read code") that changes how agents verify and explain their work.
- Engine adapters: `mm-godot` (checked against the Godot 4.7 docs), `mm-unity` (targets Unity 6; needs community verification), `mm-unreal` (partly checked against the Unreal Engine 5.9 docs), `mm-bevy` (checked against Bevy 0.20).
- Optional packs: `mm-agents` (persona agents and party mode) and `mm-art-tools` (concept art, Blender, RenderDoc and Nsight Graphics CLI harnesses).
- Setup for agents without Claude Code through `setup_project.py --copy-skills agents`.
- README in 11 languages, user guide, onboarding and inventory docs, contributing guide, Code of Conduct, security and support policies, issue and discussion forms, CI.

[Unreleased]: https://github.com/<owner>/MonkeyMode/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/<owner>/MonkeyMode/releases/tag/v0.1.0
