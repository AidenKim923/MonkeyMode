# MonkeyMode

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Français](README.fr.md) · **Deutsch** · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md)

> **I'm Monkey Game Developer 🐒**
>
> Selbst ein nicht ganz so schlauer Agent (oder Entwickler) wird schlau, wenn er mit MonkeyMode arbeitet.

MonkeyMode ist ein Open-Source-Kit für die Spieleentwicklung mit KI-Coding-Agenten. Es gibt dem Agenten eine erprobte Arbeitsweise: einen Ablauf vom Entwurf bis zum Release (Brief → GDD → Architektur → Stories → Entwicklung → Review → Playtest), Regeln, die ihn seine eigene Arbeit prüfen lassen, statt Erfolg nur zu behaupten, Leitplanken, die die Fehler blockieren, die Agenten in Spielecode immer wieder machen, und Engine-Wissen für **Godot, Unity, Unreal und Bevy**.

Es wird als Claude-Code-Plugin-Marketplace ausgeliefert und funktioniert auch mit Agenten, die `AGENTS.md` lesen (Codex und andere).

## Was enthalten ist

| Plugin | Was du bekommst |
|---|---|
| **`mm-core`** (erforderlich) | 42 `mm-` Workflow-Skills (Game Brief, GDD, Narrative, UX, Architektur, Epics und Stories, Dev Story, Code-Review, Sprintplanung und -status, Playtest-Plan, Test- und Performance-Design, Retrospektive, Recherche, Quick Dev, Review, Hilfe, ...), das Onboarding `mm-setup`, Arbeitsdokumente für den Agenten (`docs/ai/`: Ausführungsrichtlinie, Verifikations-Playbook, Netzwerkautorität, Übergabe, Ablauf vor dem Commit, Leitplanken, ...), den Leitplanken-Prüfer mit Hook nach jeder Änderung, ein Profil für Geheimnisse und persönliche Pfade sowie eine Konzeptgalerie mit Auswahlseite |
| **`mm-unity`** | Verbotene C#-APIs, Regeln für die Abhängigkeitsrichtung zwischen Assemblies, Test- und Build-Skripte im Batch-Modus, Hinweise zu Mirror und Netcode, Checkliste für den Asset-Import. *In einem echten Projekt erprobt* |
| **`mm-godot`** | Regeln für Knotenpfade und Signale in GDScript, Befehle für Headless-Tests, Hinweise zum High-Level-Multiplayer. *Mit der Godot-4.7-Dokumentation abgeglichen* |
| **`mm-unreal`** | UObject/GC-Regeln, verbotene C++-Muster, Befehle für UBT und automatisierte Tests, Hinweise zur Replikation. *Teilweise mit der Unreal-Engine-5.9-Dokumentation abgeglichen* |
| **`mm-bevy`** | Kein Blockieren in Systemen, Reihenfolge der Systeme, Clippy-Verbote, cargo-Testbefehle, Hinweise zu lightyear/replicon/renet. *Mit Bevy 0.20 abgeglichen* |
| `mm-agents` (optional) | Persona-Agenten (Game Designer, Architekt, Entwickler, Solo-Entwickler, technischer Redakteur, Analyst, PM, UX-Designer) und Party-Modus |
| `mm-art-tools` (optional) | `mm-concept-art` (ChatGPT-Prompts, Codex CLI oder Alternativen) sowie Kommandozeilen-Werkzeuge für Blender, RenderDoc und Nsight Graphics |

### Gemeinsam vs. pro Engine

| Gemeinsam (mm-core) | Pro Engine (mm-&lt;engine&gt;) |
|---|---|
| Workflow-Vorlagen: Game Brief, GDD, Narrative, UX, PRD, Architektur, Epics/Stories, Story, Playtest-Plan, Performance-Testplan, Testdesign, Code-Review-Checkliste, Retrospektive, Entscheidungsprotokoll, Projektkontext | Vorlage für den Projektkontext |
| Verhalten des Agenten, Verifikation, Übergabe, Umfangskontrolle, Git-Hygiene, Team-Workflow | Architektur-Ergänzung (Szenen- und Asset-Struktur; GDScript/C#, C#, C++/Blueprint, Rust/ECS) |
| Leitplanken-Prüfer, Hooks nach Änderungen und vor Commits, Profil für Geheimnisse | Leitplanken-Profil der Engine und verbotene Muster |
| Werkzeuge zur Selbstprüfung (Logs, Screenshots, Start mehrerer Instanzen) | Build- und Testbefehle (Unity bringt zusätzlich Skripte mit) |
| Engine-neutrale Regeln zur Netzwerkautorität und Teststufen | Multiplayer-Hinweise (Mirror/NGO, Replikation, High-Level-Multiplayer, lightyear/renet) |
| Leitfäden für Asset- und Charakterproduktion | Hinweise zu `.gitignore` / LFS, Asset-Import (Unity) |

## Installation (Claude Code)

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # pick your engine: mm-godot, mm-unity, mm-unreal, mm-bevy
```

Optionale Pakete: `/plugin install mm-agents@monkeymode`, `/plugin install mm-art-tools@monkeymode`.

Voraussetzungen: Claude Code v2.1.271 oder neuer (Plugin-Einstellungen mit festen Auswahlmöglichkeiten), Python 3.11+ und [`uv`](https://docs.astral.sh/uv/) (Workflow-Skripte und Leitplanken), PowerShell 7 für die `.ps1`-Werkzeuge, Node.js 18+ für die lokale Konzept- und Auswahlseite.

`mm-core` hat zwei Einstellungen zu dir, die du unter `/plugin` → MonkeyMode core → configure (oder mit `claude plugin configure mm-core@monkeymode`) setzt. Lässt du sie leer, fragt `/mm-setup` stattdessen nach.

| Einstellung | Auswahl |
|---|---|
| `coding_level` | I can read code / I can't read code (ich kann Code lesen / nicht) |
| `uses_chatgpt` | yes / no („Für Bilder empfehlen wir ChatGPT“) |

## Schnellstart

1. Öffne dein Spielprojekt in Claude Code und führe **`/mm-setup`** aus. Es fragt nach der Engine, ob du allein oder im Team arbeitest, nach Genre und Plattformen, Multiplayer, der Projektphase, der Stärke der Leitplanken (nur wenn du Code liest) und dem Dokumentationsordner, installiert dann alles und nennt dir den nächsten Schritt. Der vollständige Ablauf mit allen Verzweigungen steht in [`docs/ONBOARDING.md`](docs/ONBOARDING.md).
2. Führe den empfohlenen Skill aus, zum Beispiel `/mm-brainstorm-game` für eine neue Idee oder `/mm-document-project` für eine bestehende Codebasis.
3. Frag `/mm-help`, wann immer du nicht weißt, was als Nächstes kommt.

Was in dein Projekt kommt:

```
AGENTS.md            MonkeyMode section (rules, your answers, engine snippet)
CLAUDE.md            @AGENTS.md
.monkeymode/         config.json (your project answers)
_mm/                 workflow runtime: config, catalog, scripts, custom/ overrides
docs/ai/             agent operating docs
docs/engine/         engine adapter docs
docs/project/        your approved design (filled over time)
docs/work/           work records and handoffs
guardrails/          secrets.json + <engine>.json
tools/               guardrail checker, verification tools
.githooks/           optional pre-commit guardrails
```

## Ohne Claude Code (Agenten, die AGENTS.md lesen)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

Das stellt dieselben Fragen, installiert dieselben Dateien und kopiert die Skills nach `.agents/skills/`. Siehe [`docs/ONBOARDING.md`](docs/ONBOARDING.md#without-claude-code-codex-and-other-agentsmd-agents).

## Dokumentation

- [Benutzerhandbuch](docs/GUIDE.md): Installation, das Einrichtungsgespräch, der komplette Ablauf mit Skill und Ergebnisdatei für jeden Schritt, Leitplanken, Bilder, Engine-Hinweise, FAQ (auf Englisch)
- [Onboarding](docs/ONBOARDING.md): das Ablaufdiagramm der Einrichtung und was jede Antwort ändert (auf Englisch)
- [Inventar](docs/INVENTORY.md): gemeinsam vs. pro Engine, Tabelle der Skill-Namen (auf Englisch)
- [Mitwirken](CONTRIBUTING.md): Skills, Engine-Adapter und Leitplanken-Regeln hinzufügen; Tests; PR-Checkliste (auf Englisch)

## Anpassen

- Projektregeln: Bearbeite `AGENTS.md` (außerhalb der MonkeyMode-Markierungen), `docs/ai/` und `docs/engine/` in deinem Projekt. Sie haben Vorrang vor den Anweisungen der Skills.
- Verhalten der Skills: Lege Überschreibungen in `_mm/custom/<skill-name>.toml` (Team) oder `<skill-name>.user.toml` (persönlich) ab. Arrays wie `persistent_facts` werden an die Standardwerte des Skills angehängt. `/mm-customize` führt dich durch.
- Leitplanken: Füge Regeln zu `guardrails/<engine>.json` hinzu oder lege ein neues Profil `guardrails/<name>.json` an (Format in `docs/ai/12`). Ändere sie nur bewusst; Agenten sind angewiesen, sie nie eigenmächtig zu lockern.

## Installation testen

```
claude plugin validate .                      # marketplace
claude plugin validate plugins/mm-core       # each plugin
claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity
```

Der letzte Befehl startet Claude Code für eine Sitzung mit geladenen Plugins, ohne den Marketplace hinzuzufügen. Wer mitwirkt, führt außerdem die Skript-Tests und `uv run tools/scrub.py` aus (siehe [CONTRIBUTING.md](CONTRIBUTING.md)).

## Danksagung und Lizenz

MonkeyMode steht unter der MIT-Lizenz ([LICENSE](LICENSE)). Die Workflow-Skills basieren auf [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) und dem Modul BMad Game Dev Studio (MIT), die Skills für Grafikwerkzeuge auf [CLI-Anything](https://github.com/HKUDS/CLI-Anything) (Apache-2.0). MonkeyMode ist unabhängig und wird von diesen Autoren nicht unterstützt. Details und alle Änderungen: [NOTICE](NOTICE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Beiträge sind willkommen: siehe [CONTRIBUTING.md](CONTRIBUTING.md) und den [Verhaltenskodex](CODE_OF_CONDUCT.md). Besonders willkommen sind Korrekturen an den Adaptern für Godot, Unreal und Bevy: Sie wurden mit der offiziellen Dokumentation abgeglichen, aber noch nicht in einem echten Projekt eingesetzt, und offene Punkte sind in jedem Adapter mit *needs verification* markiert.
