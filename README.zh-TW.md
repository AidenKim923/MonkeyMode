# MonkeyMode

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · **繁體中文** · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md)

> **I'm Monkey Game Developer 🐒**
>
> 就算是不太聰明的代理(或開發者),用了 MonkeyMode 也會變聰明。

MonkeyMode 是一套給 AI 程式設計代理使用的開源遊戲開發工具組。它讓代理用一套經過實戰驗證的方式工作:從企劃到發行的完整工作流程(簡報 → GDD → 架構 → 使用者故事 → 開發 → 審查 → 試玩)、要求它在宣稱成功前先自行驗證結果的規則、攔下代理在遊戲程式碼中一再犯下的錯誤的護欄,以及針對 **Godot、Unity、Unreal 與 Bevy** 的引擎專屬知識。

它擷取自一個真實的 Unity + Mirror 合作遊戲專案,並經過通用化。它以 Claude Code 外掛市集的形式發布,也適用於會讀取 `AGENTS.md` 的代理(例如 Codex)。

## 內容

| 外掛 | 內容 |
|---|---|
| **`mm-core`**(必要) | 42 個 `mm-` 工作流程技能(遊戲簡報、GDD、敘事、UX、架構、史詩與故事、開發故事、程式碼審查、衝刺規劃與狀態、試玩計畫、效能與測試設計、回顧、研究、快速開發、審查、說明等)、`mm-setup` 初始設定、代理作業文件(`docs/ai/`:執行政策、驗證手冊、網路權威、交接、提交前流程、護欄等)、附編輯後掛鉤的護欄檢查器、機密與個人路徑檢查設定、概念圖庫與選擇頁面 |
| **`mm-unity`** | C# 禁用 API、組件參照方向規則、批次模式測試與建置腳本、Mirror 與 Netcode 說明、資產匯入清單。*已在實際專案中驗證* |
| **`mm-godot`** | GDScript 節點路徑與訊號規則、無頭測試指令、高階多人連線說明。*已對照 Godot 4.7 官方文件確認* |
| **`mm-unreal`** | UObject/GC 規則、禁用的 C++ 寫法、UBT 與自動化測試指令、複寫(Replication)說明。*已對照 Unreal Engine 5.9 官方文件部分確認* |
| **`mm-bevy`** | 系統內禁止阻塞、系統執行順序、Clippy 禁用清單、cargo 測試指令、lightyear/replicon/renet 說明。*已對照 Bevy 0.20 確認* |
| `mm-agents`(選用) | 角色代理(遊戲設計師、架構師、開發者、獨立開發者、技術寫作者、分析師、產品經理、UX 設計師)與派對模式 |
| `mm-art-tools`(選用) | `mm-concept-art`(ChatGPT 提示詞、Codex CLI 或其他方案)以及 Blender、RenderDoc、Nsight Graphics 的命令列工具封裝 |

### 共用 vs. 引擎專屬

| 共用 (mm-core) | 引擎專屬 (mm-&lt;engine&gt;) |
|---|---|
| 工作流程範本:遊戲簡報、GDD、敘事、UX、PRD、架構、史詩/故事、故事、試玩計畫、效能測試計畫、測試設計、程式碼審查清單、回顧、決策紀錄、專案脈絡 | 專案脈絡範本 |
| 代理行為、驗證、交接、範圍控管、Git 規範、團隊工作流程 | 架構補充(場景與資產結構;GDScript/C#、C#、C++/Blueprint、Rust/ECS) |
| 護欄檢查器、編輯後與提交前掛鉤、機密檢查設定 | 引擎護欄設定與禁用寫法 |
| 自我驗證工具(日誌、截圖、多實例啟動) | 建置與測試指令(Unity 另附腳本) |
| 與引擎無關的網路權威規則與測試等級 | 多人連線說明(Mirror/NGO、複寫、高階多人連線、lightyear/renet) |
| 資產與角色製作流程指南 | `.gitignore` / LFS 提示、資產匯入(Unity) |

各部分的來源清單請見 [`docs/INVENTORY.md`](docs/INVENTORY.md)(英文)。

## 安裝 (Claude Code)

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # pick your engine: mm-godot, mm-unity, mm-unreal, mm-bevy
```

選用套件:`/plugin install mm-agents@monkeymode`、`/plugin install mm-art-tools@monkeymode`。

需求:Claude Code v2.1.271 或更新版本(支援固定選項的外掛設定)、Python 3.11+ 與 [`uv`](https://docs.astral.sh/uv/)(工作流程腳本與護欄)、執行 `.ps1` 工具用的 PowerShell 7、本機概念與選擇頁面用的 Node.js 18+。

`mm-core` 有兩項關於你本人的設定,可在 `/plugin` → MonkeyMode core → configure(或 `claude plugin configure mm-core@monkeymode`)中設定。若不設定,`/mm-setup` 會改為直接詢問你。

| 設定 | 選項 |
|---|---|
| `coding_level` | I can read code / I can't read code(看得懂程式碼 / 看不懂) |
| `uses_chatgpt` | yes / no(「圖片建議使用 ChatGPT」) |

## 快速開始

1. 在 Claude Code 中開啟你的遊戲專案,執行 **`/mm-setup`**。它會詢問引擎、單人或團隊、類型與平台、是否多人、專案階段、護欄強度(只在你看得懂程式碼時詢問)與文件資料夾,接著安裝所有內容並告訴你下一步。完整的分支流程請見 [`docs/ONBOARDING.md`](docs/ONBOARDING.md)。
2. 執行它推薦的技能:新點子用 `/mm-brainstorm-game`,既有的程式碼庫用 `/mm-document-project`。
3. 不確定下一步時,隨時問 `/mm-help`。

專案中會新增:

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

## 不使用 Claude Code(讀取 AGENTS.md 的代理)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

它會問同樣的問題、安裝同樣的檔案,並把技能複製到 `.agents/skills/`。詳見 [`docs/ONBOARDING.md`](docs/ONBOARDING.md#without-claude-code-codex-and-other-agentsmd-agents)。

## 文件

- [使用者指南](docs/GUIDE.md):安裝、設定問答、包含每一步技能與產出檔案的完整工作流程、護欄、圖片、引擎說明、常見問題(英文)
- [初始設定](docs/ONBOARDING.md):設定流程圖與每個回答會改變什麼(英文)
- [清單](docs/INVENTORY.md):來源、共用與引擎專屬的區分、技能名稱對照表(英文)
- [貢獻指南](CONTRIBUTING.md):新增技能、引擎轉接器與護欄規則,測試,PR 檢查清單(英文)

## 自訂

- 專案規則:編輯專案中的 `AGENTS.md`(MonkeyMode 標記區段之外)、`docs/ai/` 與 `docs/engine/`。這些文件優先於技能中的指示。
- 技能行為:把覆寫設定放在 `_mm/custom/<skill-name>.toml`(團隊)或 `<skill-name>.user.toml`(個人)。`persistent_facts` 等陣列會附加在技能預設值之後。`/mm-customize` 會一步步引導你。
- 護欄:在 `guardrails/<engine>.json` 加入規則,或建立新的 `guardrails/<name>.json` 設定(格式見 `docs/ai/12`)。只在有意為之時修改;代理被要求絕不自行放寬規則。

## 測試安裝

```
claude plugin validate .                      # marketplace
claude plugin validate plugins/mm-core       # each plugin
claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity
```

最後一條指令會在不新增外掛市集的情況下,只在這次工作階段載入外掛並啟動 Claude Code。貢獻者也要執行腳本測試與 `uv run tools/scrub.py`(見 [CONTRIBUTING.md](CONTRIBUTING.md))。

## 致謝與授權

MonkeyMode 採用 MIT 授權([LICENSE](LICENSE))。工作流程技能以 [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) 與 BMad Game Dev Studio 模組(MIT)為基礎,圖形工具技能以 [CLI-Anything](https://github.com/HKUDS/CLI-Anything)(Apache-2.0)為基礎。MonkeyMode 是獨立專案,未獲原作者背書。詳細資訊與所有修改:[NOTICE](NOTICE)、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

歡迎貢獻:請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 與[行為準則](CODE_OF_CONDUCT.md)。特別歡迎修正 Godot、Unreal 與 Bevy 轉接器:它們已對照官方文件確認,但尚未在真實專案中使用,無法確認的項目在各轉接器中標示為 *needs verification*。
