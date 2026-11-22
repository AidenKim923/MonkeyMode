# MonkeyMode

[English](README.md) · **한국어** · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md)

> **I'm Monkey Game Developer 🐒**
>
> 조금 덜 똑똑한 에이전트(또는 개발자)도 MonkeyMode와 함께라면 똑똑해집니다.

MonkeyMode는 AI 코딩 에이전트를 위한 오픈소스 게임 개발 키트입니다. 에이전트에게 검증된 작업 방식을 줍니다. 기획부터 출시까지 이어지는 워크플로(브리프 → GDD → 아키텍처 → 스토리 → 개발 → 리뷰 → 플레이테스트), 성공했다고 말하기 전에 스스로 결과를 확인하게 하는 규칙, 에이전트가 게임 코드에서 자주 저지르는 실수를 막는 가드레일, 그리고 **Godot, Unity, Unreal, Bevy** 엔진별 지식이 들어 있습니다.

실제 Unity + Mirror 협동 게임 프로젝트에서 추출해 일반화했습니다. Claude Code 플러그인 마켓플레이스로 배포되며, `AGENTS.md`를 읽는 에이전트(Codex 등)에서도 동작합니다.

## 구성

| 플러그인 | 내용 |
|---|---|
| **`mm-core`** (필수) | `mm-` 워크플로 스킬 42개(게임 브리프, GDD, 서사, UX, 아키텍처, 에픽과 스토리, 개발 스토리, 코드 리뷰, 스프린트 계획과 현황, 플레이테스트 계획, 성능·테스트 설계, 회고, 리서치, 빠른 개발, 리뷰, 도움말 등), `mm-setup` 온보딩, 에이전트 운영 문서(`docs/ai/`: 실행 정책, 검증 플레이북, 네트워크 권위, 인수인계, 커밋 전 절차, 가드레일 등), 편집 후 훅이 달린 가드레일 검사기, 비밀값·개인 경로 프로필, 콘셉트 갤러리와 선택 페이지 |
| **`mm-unity`** | C# 금지 API, 어셈블리 참조 방향 규칙, 배치 모드 테스트·빌드 스크립트, Mirror와 Netcode 노트, 에셋 임포트 체크리스트. *실전 검증됨* |
| **`mm-godot`** | GDScript 노드 경로·시그널 규칙, 헤드리스 테스트 명령, 고수준 멀티플레이 노트. *Godot 4.7 공식 문서로 확인* |
| **`mm-unreal`** | UObject/GC 규칙, 금지 C++ 패턴, UBT·자동화 테스트 명령, 리플리케이션 노트. *Unreal Engine 5.9 공식 문서로 일부 확인* |
| **`mm-bevy`** | 시스템 안에서 블로킹 금지, 시스템 순서, Clippy 금지 목록, cargo 테스트 명령, lightyear/replicon/renet 노트. *Bevy 0.20 기준으로 확인* |
| `mm-agents` (선택) | 페르소나 에이전트(게임 디자이너, 아키텍트, 개발자, 1인 개발자, 테크니컬 라이터, 분석가, PM, UX 디자이너)와 파티 모드 |
| `mm-art-tools` (선택) | `mm-concept-art`(ChatGPT 프롬프트, Codex CLI 또는 대안)와 Blender, RenderDoc, Nsight Graphics용 CLI 하네스 |

### 공통 vs. 엔진별

| 공통 (mm-core) | 엔진별 (mm-&lt;engine&gt;) |
|---|---|
| 워크플로 템플릿: 게임 브리프, GDD, 서사, UX, PRD, 아키텍처, 에픽/스토리, 스토리, 플레이테스트 계획, 성능 테스트 계획, 테스트 설계, 코드 리뷰 체크리스트, 회고, 결정 로그, 프로젝트 컨텍스트 | 프로젝트 컨텍스트 템플릿 |
| 에이전트 행동, 검증, 인수인계, 범위 통제, Git 위생, 팀 워크플로 | 아키텍처 보충 문서(씬·에셋 구조; GDScript/C#, C#, C++/Blueprint, Rust/ECS) |
| 가드레일 검사기, 편집 후·커밋 전 훅, 비밀값 프로필 | 엔진 가드레일 프로필과 금지 패턴 |
| 자가 검증 도구(로그, 스크린샷, 다중 인스턴스 실행) | 빌드·테스트 명령(Unity는 스크립트도 포함) |
| 엔진 중립 네트워크 권위 규칙과 테스트 등급 | 멀티플레이 노트(Mirror/NGO, 리플리케이션, 고수준 멀티플레이, lightyear/renet) |
| 에셋·캐릭터 파이프라인 가이드 | `.gitignore` / LFS 힌트, 에셋 임포트(Unity) |

무엇이 어디서 왔는지는 [`docs/INVENTORY.md`](docs/INVENTORY.md)에 정리되어 있습니다(영문).

## 설치 (Claude Code)

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # pick your engine: mm-godot, mm-unity, mm-unreal, mm-bevy
```

선택 팩: `/plugin install mm-agents@monkeymode`, `/plugin install mm-art-tools@monkeymode`.

요구 사항: Claude Code v2.1.271 이상(선택지가 고정된 플러그인 설정), Python 3.11+와 [`uv`](https://docs.astral.sh/uv/)(워크플로 스크립트와 가드레일), `.ps1` 도구용 PowerShell 7, 로컬 콘셉트·선택 페이지용 Node.js 18+.

`mm-core`에는 사용자에 관한 설정이 두 개 있습니다. `/plugin` → MonkeyMode core → configure(또는 `claude plugin configure mm-core@monkeymode`)에서 설정합니다. 비워 두면 `/mm-setup`이 대신 물어봅니다.

| 설정 | 선택지 |
|---|---|
| `coding_level` | I can read code / I can't read code (코드를 읽을 수 있음 / 없음) |
| `uses_chatgpt` | yes / no ("이미지는 ChatGPT를 권장합니다") |

## 빠른 시작

1. Claude Code에서 게임 프로젝트를 열고 **`/mm-setup`**을 실행합니다. 엔진, 1인/팀, 장르와 플랫폼, 멀티플레이 여부, 프로젝트 단계, 가드레일 수준(코드를 읽는 경우에만), 문서 폴더를 물은 뒤 모든 것을 설치하고 다음 단계를 알려 줍니다. 분기 흐름 전체는 [`docs/ONBOARDING.md`](docs/ONBOARDING.md)에 있습니다.
2. 추천받은 스킬을 실행합니다. 새 아이디어라면 `/mm-brainstorm-game`, 이미 있는 코드베이스라면 `/mm-document-project`입니다.
3. 다음에 뭘 할지 모르겠으면 언제든 `/mm-help`에 물어보세요.

프로젝트에 생기는 것:

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

## Claude Code 없이 (AGENTS.md를 읽는 에이전트)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

같은 질문을 하고 같은 파일을 설치하며, 스킬을 `.agents/skills/`로 복사합니다. 자세한 내용은 [`docs/ONBOARDING.md`](docs/ONBOARDING.md#without-claude-code-codex-and-other-agentsmd-agents)를 보세요.

## 문서

- [사용자 가이드](docs/GUIDE.md): 설치, 설정 인터뷰, 단계별 스킬과 산출 파일이 포함된 전체 워크플로, 가드레일, 이미지, 엔진별 노트, FAQ (영문)
- [온보딩](docs/ONBOARDING.md): 설정 흐름도와 각 답이 바꾸는 것 (영문)
- [인벤토리](docs/INVENTORY.md): 출처, 공통/엔진별 구분, 스킬 이름 대응표 (영문)
- [기여 가이드](CONTRIBUTING.md): 스킬·엔진 어댑터·가드레일 규칙 추가, 테스트, PR 체크리스트 (영문)

## 커스터마이징

- 프로젝트 규칙: 프로젝트의 `AGENTS.md`(MonkeyMode 표시 구간 밖), `docs/ai/`, `docs/engine/`을 고칩니다. 이 문서들이 스킬 지시보다 우선합니다.
- 스킬 동작: `_mm/custom/<skill-name>.toml`(팀) 또는 `<skill-name>.user.toml`(개인)에 덮어쓸 값을 둡니다. `persistent_facts` 같은 배열은 스킬 기본값 뒤에 추가됩니다. `/mm-customize`가 안내합니다.
- 가드레일: `guardrails/<engine>.json`에 규칙을 추가하거나 새 `guardrails/<name>.json` 프로필을 만듭니다(형식은 `docs/ai/12`). 의도할 때만 바꾸세요. 에이전트는 스스로 규칙을 완화하지 않도록 되어 있습니다.

## 설치 테스트

```
claude plugin validate .                      # marketplace
claude plugin validate plugins/mm-core       # each plugin
claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity
```

마지막 명령은 마켓플레이스를 추가하지 않고 한 세션 동안만 플러그인을 불러와 Claude Code를 시작합니다. 기여자는 스크립트 테스트와 `uv run tools/scrub.py`도 실행합니다([CONTRIBUTING.md](CONTRIBUTING.md) 참고).

## 크레딧과 라이선스

MonkeyMode는 MIT 라이선스입니다([LICENSE](LICENSE)). 워크플로 스킬은 [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD)와 BMad Game Dev Studio 모듈(MIT)을, 그래픽 도구 스킬은 [CLI-Anything](https://github.com/HKUDS/CLI-Anything)(Apache-2.0)을 바탕으로 합니다. MonkeyMode는 독립 프로젝트이며 원저작자의 보증을 받지 않았습니다. 자세한 내용과 모든 수정 사항: [NOTICE](NOTICE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

기여를 환영합니다. [CONTRIBUTING.md](CONTRIBUTING.md)와 [행동 강령](CODE_OF_CONDUCT.md)을 보세요. 특히 Godot, Unreal, Bevy 어댑터에 대한 수정을 환영합니다. 공식 문서로 확인했지만 아직 실제 프로젝트에서 쓰이지 않았고, 확인하지 못한 항목은 각 어댑터에 *needs verification*으로 표시되어 있습니다.
