# MonkeyMode

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · **简体中文** · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md)

> **I'm Monkey Game Developer 🐒**
>
> 就算不太聪明的智能体(或开发者),用上 MonkeyMode 也会变聪明。

MonkeyMode 是一个面向 AI 编程智能体的开源游戏开发工具包。它给智能体一套经过实践检验的工作方式:从设计到发布的完整工作流(简报 → GDD → 架构 → 用户故事 → 开发 → 评审 → 试玩),要求它在宣布成功之前先自行验证结果的规则,拦截智能体在游戏代码中反复犯下的错误的护栏,以及针对 **Godot、Unity、Unreal 和 Bevy** 的引擎专属知识。

它提取自一个真实的 Unity + Mirror 合作游戏项目并做了通用化处理。它以 Claude Code 插件市场的形式发布,也适用于读取 `AGENTS.md` 的智能体(如 Codex)。

## 包含什么

| 插件 | 内容 |
|---|---|
| **`mm-core`**(必需) | 42 个 `mm-` 工作流技能(游戏简报、GDD、叙事、UX、架构、史诗与故事、开发故事、代码评审、冲刺计划与状态、试玩计划、性能与测试设计、回顾、调研、快速开发、评审、帮助等)、`mm-setup` 引导设置、智能体运行文档(`docs/ai/`:执行策略、验证手册、网络权威、交接、提交前流程、护栏等)、带编辑后钩子的护栏检查器、密钥与个人路径检查配置、概念图库与选择页面 |
| **`mm-unity`** | C# 禁用 API、程序集引用方向规则、批处理模式测试与构建脚本、Mirror 与 Netcode 说明、资源导入清单。*已在实际项目中验证* |
| **`mm-godot`** | GDScript 节点路径与信号规则、无头测试命令、高级多人游戏说明。*已对照 Godot 4.7 官方文档核实* |
| **`mm-unreal`** | UObject/GC 规则、禁用的 C++ 写法、UBT 与自动化测试命令、复制(Replication)说明。*已对照 Unreal Engine 5.9 官方文档部分核实* |
| **`mm-bevy`** | 系统中禁止阻塞、系统执行顺序、Clippy 禁用列表、cargo 测试命令、lightyear/replicon/renet 说明。*已对照 Bevy 0.20 核实* |
| `mm-agents`(可选) | 角色智能体(游戏设计师、架构师、开发者、独立开发者、技术写作者、分析师、产品经理、UX 设计师)与派对模式 |
| `mm-art-tools`(可选) | `mm-concept-art`(ChatGPT 提示词、Codex CLI 或其他方案)以及 Blender、RenderDoc、Nsight Graphics 的命令行工具封装 |

### 通用 vs. 引擎专属

| 通用 (mm-core) | 引擎专属 (mm-&lt;engine&gt;) |
|---|---|
| 工作流模板:游戏简报、GDD、叙事、UX、PRD、架构、史诗/故事、故事、试玩计划、性能测试计划、测试设计、代码评审清单、回顾、决策日志、项目上下文 | 项目上下文模板 |
| 智能体行为、验证、交接、范围控制、Git 规范、团队工作流 | 架构补充(场景与资源结构;GDScript/C#、C#、C++/Blueprint、Rust/ECS) |
| 护栏检查器、编辑后与提交前钩子、密钥检查配置 | 引擎护栏配置与禁用写法 |
| 自我验证工具(日志、截图、多实例启动) | 构建与测试命令(Unity 还附带脚本) |
| 与引擎无关的网络权威规则与测试等级 | 多人游戏说明(Mirror/NGO、复制、高级多人游戏、lightyear/renet) |
| 资源与角色制作流程指南 | `.gitignore` / LFS 提示、资源导入(Unity) |

每个部分的来源清单见 [`docs/INVENTORY.md`](docs/INVENTORY.md)(英文)。

## 安装 (Claude Code)

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # pick your engine: mm-godot, mm-unity, mm-unreal, mm-bevy
```

可选扩展包:`/plugin install mm-agents@monkeymode`、`/plugin install mm-art-tools@monkeymode`。

环境要求:Claude Code v2.1.271 或更高版本(支持固定选项的插件设置)、Python 3.11+ 与 [`uv`](https://docs.astral.sh/uv/)(工作流脚本与护栏)、用于 `.ps1` 工具的 PowerShell 7、用于本地概念与选择页面的 Node.js 18+。

`mm-core` 有两项关于你本人的设置,可在 `/plugin` → MonkeyMode core → configure(或 `claude plugin configure mm-core@monkeymode`)中设置。如果不设置,`/mm-setup` 会改为直接询问你。

| 设置 | 选项 |
|---|---|
| `coding_level` | I can read code / I can't read code(能读代码 / 不能读代码) |
| `uses_chatgpt` | yes / no("图像推荐使用 ChatGPT") |

## 快速开始

1. 在 Claude Code 中打开你的游戏项目,运行 **`/mm-setup`**。它会询问引擎、单人还是团队、类型与平台、是否多人、项目阶段、护栏强度(仅在你能读代码时询问)以及文档文件夹,然后安装所有内容并告诉你下一步。完整的分支流程见 [`docs/ONBOARDING.md`](docs/ONBOARDING.md)。
2. 运行它推荐的技能:新点子用 `/mm-brainstorm-game`,已有代码库用 `/mm-document-project`。
3. 不确定下一步做什么时,随时问 `/mm-help`。

项目中会新增:

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

## 不使用 Claude Code(读取 AGENTS.md 的智能体)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

它会问同样的问题、安装同样的文件,并把技能复制到 `.agents/skills/`。详见 [`docs/ONBOARDING.md`](docs/ONBOARDING.md#without-claude-code-codex-and-other-agentsmd-agents)。

## 文档

- [用户指南](docs/GUIDE.md):安装、设置问答、包含每一步技能与产出文件的完整工作流、护栏、图像、引擎说明、常见问题(英文)
- [引导设置](docs/ONBOARDING.md):设置流程图以及每个回答会改变什么(英文)
- [清单](docs/INVENTORY.md):来源、通用与引擎专属的划分、技能名称对照表(英文)
- [贡献指南](CONTRIBUTING.md):添加技能、引擎适配器与护栏规则,测试,PR 清单(英文)

## 自定义

- 项目规则:编辑项目中的 `AGENTS.md`(MonkeyMode 标记区域之外)、`docs/ai/` 和 `docs/engine/`。它们优先于技能中的指令。
- 技能行为:把覆盖配置放在 `_mm/custom/<skill-name>.toml`(团队)或 `<skill-name>.user.toml`(个人)。`persistent_facts` 等数组会追加到技能默认值之后。`/mm-customize` 会一步步引导你。
- 护栏:在 `guardrails/<engine>.json` 中添加规则,或新建 `guardrails/<name>.json` 配置(格式见 `docs/ai/12`)。只在有意为之时修改;智能体被要求绝不自行放宽规则。

## 测试安装

```
claude plugin validate .                      # marketplace
claude plugin validate plugins/mm-core       # each plugin
claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity
```

最后一条命令会在不添加插件市场的情况下,仅在本次会话中加载插件并启动 Claude Code。贡献者还需要运行脚本测试和 `uv run tools/scrub.py`(见 [CONTRIBUTING.md](CONTRIBUTING.md))。

## 致谢与许可证

MonkeyMode 采用 MIT 许可证([LICENSE](LICENSE))。工作流技能基于 [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) 与 BMad Game Dev Studio 模块(MIT),图形工具技能基于 [CLI-Anything](https://github.com/HKUDS/CLI-Anything)(Apache-2.0)。MonkeyMode 是独立项目,未获得原作者的背书。详细信息与全部修改:[NOTICE](NOTICE)、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

欢迎贡献:请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 和[行为准则](CODE_OF_CONDUCT.md)。尤其欢迎对 Godot、Unreal 和 Bevy 适配器的修正:它们已对照官方文档核实,但尚未在真实项目中使用,未能确认的条目在各适配器中标注为 *needs verification*。
