# MonkeyMode

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · **Français** · [Deutsch](README.de.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md)

> **I'm Monkey Game Developer 🐒**
>
> Même un agent (ou un dev) pas très malin devient malin quand il travaille avec MonkeyMode.

MonkeyMode est un kit open source de développement de jeux pour les agents de programmation IA. Il donne à l'agent une méthode de travail éprouvée : un flux de travail de la conception à la sortie (brief → GDD → architecture → stories → développement → revue → playtest), des règles qui l'obligent à vérifier son propre travail au lieu de crier victoire, des garde-fous qui bloquent les erreurs que les agents répètent dans le code de jeu, et des connaissances propres à **Godot, Unity, Unreal et Bevy**.

Il a été extrait d'un vrai projet de jeu coopératif Unity + Mirror, puis généralisé. Il est distribué comme une marketplace de plugins Claude Code et fonctionne aussi avec les agents qui lisent `AGENTS.md` (Codex et d'autres).

## Contenu

| Plugin | Ce que vous obtenez |
|---|---|
| **`mm-core`** (obligatoire) | 42 skills de flux `mm-` (brief du jeu, GDD, narration, UX, architecture, épopées et stories, story de développement, revue de code, planification et suivi de sprint, plan de playtest, conception des tests et des tests de performance, rétrospective, recherche, développement rapide, relecture, aide, ...), la configuration initiale `mm-setup`, des documents de fonctionnement pour l'agent (`docs/ai/` : politique d'exécution, guide de vérification, autorité réseau, passation, procédure avant commit, garde-fous, ...), le vérificateur de garde-fous avec un hook après chaque modification, un profil secrets et chemins personnels, ainsi qu'une galerie de concepts avec page de choix |
| **`mm-unity`** | API C# interdites, règles de dépendances entre assemblies, scripts de tests et de build en mode batch, notes sur Mirror et Netcode, check-list d'import d'assets. *Éprouvé sur un vrai projet* |
| **`mm-godot`** | Règles sur les chemins de nœuds et les signaux en GDScript, commandes de tests sans interface, notes sur le multijoueur haut niveau. *Vérifié avec la documentation de Godot 4.7* |
| **`mm-unreal`** | Règles UObject/GC, motifs C++ interdits, commandes UBT et de tests automatisés, notes sur la réplication. *Vérifié en partie avec la documentation d'Unreal Engine 5.9* |
| **`mm-bevy`** | Aucun blocage dans les systèmes, ordre des systèmes, interdictions Clippy, commandes de test cargo, notes sur lightyear/replicon/renet. *Vérifié avec Bevy 0.20* |
| `mm-agents` (optionnel) | Agents à personnalité (game designer, architecte, développeur, développeur solo, rédacteur technique, analyste, PM, designer UX) et mode fête |
| `mm-art-tools` (optionnel) | `mm-concept-art` (prompts ChatGPT, Codex CLI ou autres options) et outils en ligne de commande pour Blender, RenderDoc et Nsight Graphics |

### Commun vs. par moteur

| Commun (mm-core) | Par moteur (mm-&lt;engine&gt;) |
|---|---|
| Modèles du flux : brief du jeu, GDD, narration, UX, PRD, architecture, épopées/stories, story, plan de playtest, plan de tests de performance, conception des tests, check-list de revue de code, rétrospective, journal des décisions, contexte du projet | Modèle de contexte du projet |
| Comportement de l'agent, vérification, passation, maîtrise du périmètre, hygiène Git, flux d'équipe | Annexe d'architecture (structure des scènes et assets ; GDScript/C#, C#, C++/Blueprint, Rust/ECS) |
| Vérificateur de garde-fous, hooks après modification et avant commit, profil secrets | Profil de garde-fous du moteur et motifs interdits |
| Outils d'autovérification (logs, captures d'écran, lancement de plusieurs instances) | Commandes de build et de test (Unity fournit aussi des scripts) |
| Règles d'autorité réseau et niveaux de test indépendants du moteur | Notes multijoueur (Mirror/NGO, réplication, multijoueur haut niveau, lightyear/renet) |
| Guides de production d'assets et de personnages | Conseils `.gitignore` / LFS, import d'assets (Unity) |

La liste complète de la provenance de chaque élément se trouve dans [`docs/INVENTORY.md`](docs/INVENTORY.md) (en anglais).

## Installation (Claude Code)

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # pick your engine: mm-godot, mm-unity, mm-unreal, mm-bevy
```

Packs optionnels : `/plugin install mm-agents@monkeymode`, `/plugin install mm-art-tools@monkeymode`.

Prérequis : Claude Code v2.1.271 ou plus récent (réglages de plugin à choix fixes), Python 3.11+ et [`uv`](https://docs.astral.sh/uv/) (scripts du flux et garde-fous), PowerShell 7 pour les outils `.ps1`, Node.js 18+ pour la page locale de concepts et de choix.

`mm-core` a deux réglages qui vous concernent, à définir dans `/plugin` → MonkeyMode core → configure (ou avec `claude plugin configure mm-core@monkeymode`). Si vous les laissez vides, `/mm-setup` vous pose la question.

| Réglage | Choix |
|---|---|
| `coding_level` | I can read code / I can't read code (je sais lire du code / non) |
| `uses_chatgpt` | yes / no (« Pour les images, nous recommandons ChatGPT ») |

## Démarrage rapide

1. Ouvrez votre projet de jeu dans Claude Code et lancez **`/mm-setup`**. Il vous demande le moteur, si vous travaillez seul ou en équipe, le genre et les plateformes, le multijoueur, l'étape du projet, le niveau des garde-fous (seulement si vous lisez du code) et le dossier de documentation, puis installe tout et vous indique l'étape suivante. Le déroulé complet avec ses embranchements est dans [`docs/ONBOARDING.md`](docs/ONBOARDING.md).
2. Lancez la skill recommandée, par exemple `/mm-brainstorm-game` pour une nouvelle idée ou `/mm-document-project` pour une base de code existante.
3. Demandez à `/mm-help` dès que vous ne savez pas quoi faire ensuite.

Ce qui est ajouté à votre projet :

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

## Sans Claude Code (agents qui lisent AGENTS.md)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

Il pose les mêmes questions, installe les mêmes fichiers et copie les skills dans `.agents/skills/`. Voir [`docs/ONBOARDING.md`](docs/ONBOARDING.md#without-claude-code-codex-and-other-agentsmd-agents).

## Documentation

- [Guide de l'utilisateur](docs/GUIDE.md) : installation, l'entretien de configuration, le flux complet avec la skill et le fichier produit à chaque étape, garde-fous, images, notes par moteur, FAQ (en anglais)
- [Prise en main](docs/ONBOARDING.md) : le schéma de configuration et ce que change chaque réponse (en anglais)
- [Inventaire](docs/INVENTORY.md) : provenance de chaque élément, commun vs. par moteur, table des noms de skills (en anglais)
- [Contribuer](CONTRIBUTING.md) : ajouter des skills, des adaptateurs de moteur et des règles de garde-fous ; tests ; check-list de PR (en anglais)

## Personnalisation

- Règles du projet : modifiez `AGENTS.md` (hors des marqueurs MonkeyMode), `docs/ai/` et `docs/engine/` dans votre projet. Ils priment sur les instructions des skills.
- Comportement des skills : placez vos surcharges dans `_mm/custom/<skill-name>.toml` (équipe) ou `<skill-name>.user.toml` (personnel). Les tableaux comme `persistent_facts` s'ajoutent aux valeurs par défaut de la skill. `/mm-customize` vous guide.
- Garde-fous : ajoutez des règles à `guardrails/<engine>.json` ou créez un nouveau profil `guardrails/<name>.json` (format dans `docs/ai/12`). Ne les modifiez que volontairement ; les agents ont pour consigne de ne jamais les assouplir d'eux-mêmes.

## Tester l'installation

```
claude plugin validate .                      # marketplace
claude plugin validate plugins/mm-core       # each plugin
claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity
```

La dernière commande lance Claude Code avec les plugins chargés pour une seule session, sans ajouter la marketplace. Les contributeurs lancent aussi les tests des scripts et `uv run tools/scrub.py` (voir [CONTRIBUTING.md](CONTRIBUTING.md)).

## Crédits et licence

MonkeyMode est sous licence MIT ([LICENSE](LICENSE)). Ses skills de flux s'appuient sur [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) et le module BMad Game Dev Studio (MIT), et ses skills d'outils graphiques sur [CLI-Anything](https://github.com/HKUDS/CLI-Anything) (Apache-2.0). MonkeyMode est indépendant et n'est pas approuvé par leurs auteurs. Détails et liste de toutes les modifications : [NOTICE](NOTICE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Les contributions sont les bienvenues : voir [CONTRIBUTING.md](CONTRIBUTING.md) et le [Code de conduite](CODE_OF_CONDUCT.md). Les corrections des adaptateurs Godot, Unreal et Bevy sont particulièrement appréciées : ils ont été vérifiés avec la documentation officielle mais n'ont pas encore servi sur un vrai projet, et les points encore ouverts sont marqués *needs verification* dans chaque adaptateur.
