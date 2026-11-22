# MonkeyMode

[English](README.md) · [한국어](README.ko.md) · **日本語** · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md)

> **I'm Monkey Game Developer 🐒**
>
> ちょっと賢くないエージェント(や開発者)も、MonkeyMode と一緒なら賢くなります。

MonkeyMode は AI コーディングエージェントのためのオープンソースのゲーム開発キットです。エージェントに実績のある作業手順を与えます。企画からリリースまでのワークフロー(ブリーフ → GDD → アーキテクチャ → ストーリー → 開発 → レビュー → プレイテスト)、成功を主張する前に自分で結果を確認させるルール、エージェントがゲームコードで繰り返しがちなミスを止めるガードレール、そして **Godot、Unity、Unreal、Bevy** のエンジン別の知識が入っています。

実際の Unity + Mirror の協力プレイゲームのプロジェクトから抽出し、汎用化しました。Claude Code のプラグインマーケットプレイスとして配布され、`AGENTS.md` を読むエージェント(Codex など)でも動作します。

## 中身

| プラグイン | 内容 |
|---|---|
| **`mm-core`** (必須) | `mm-` ワークフロースキル 42 個(ゲームブリーフ、GDD、ナラティブ、UX、アーキテクチャ、エピックとストーリー、開発ストーリー、コードレビュー、スプリント計画と状況、プレイテスト計画、パフォーマンス・テスト設計、レトロスペクティブ、リサーチ、クイック開発、レビュー、ヘルプなど)、`mm-setup` オンボーディング、エージェント運用ドキュメント(`docs/ai/`: 実行ポリシー、検証プレイブック、ネットワーク権威、引き継ぎ、コミット前手順、ガードレールなど)、編集後フック付きのガードレールチェッカー、シークレット・個人パスのプロファイル、コンセプトギャラリーと選択ページ |
| **`mm-unity`** | C# の禁止 API、アセンブリ参照方向ルール、バッチモードのテスト・ビルドスクリプト、Mirror と Netcode のノート、アセットインポートのチェックリスト。*実プロジェクトで検証済み* |
| **`mm-godot`** | GDScript のノードパスとシグナルのルール、ヘッドレスのテストコマンド、ハイレベルマルチプレイヤーのノート。*Godot 4.7 公式ドキュメントで確認* |
| **`mm-unreal`** | UObject/GC のルール、禁止 C++ パターン、UBT と自動テストのコマンド、レプリケーションのノート。*Unreal Engine 5.9 公式ドキュメントで一部確認* |
| **`mm-bevy`** | システム内でのブロック禁止、システムの実行順、Clippy の禁止リスト、cargo のテストコマンド、lightyear/replicon/renet のノート。*Bevy 0.20 で確認* |
| `mm-agents` (任意) | ペルソナエージェント(ゲームデザイナー、アーキテクト、開発者、ソロ開発者、テクニカルライター、アナリスト、PM、UX デザイナー)とパーティーモード |
| `mm-art-tools` (任意) | `mm-concept-art`(ChatGPT 用プロンプト、Codex CLI、またはその他の方法)と Blender、RenderDoc、Nsight Graphics の CLI ハーネス |

### 共通 vs. エンジン別

| 共通 (mm-core) | エンジン別 (mm-&lt;engine&gt;) |
|---|---|
| ワークフローのテンプレート: ゲームブリーフ、GDD、ナラティブ、UX、PRD、アーキテクチャ、エピック/ストーリー、ストーリー、プレイテスト計画、パフォーマンステスト計画、テスト設計、コードレビューのチェックリスト、レトロスペクティブ、決定ログ、プロジェクトコンテキスト | プロジェクトコンテキストのテンプレート |
| エージェントの振る舞い、検証、引き継ぎ、スコープ管理、Git の衛生、チームのワークフロー | アーキテクチャ補足(シーン・アセット構成; GDScript/C#、C#、C++/Blueprint、Rust/ECS) |
| ガードレールチェッカー、編集後・コミット前フック、シークレットプロファイル | エンジンのガードレールプロファイルと禁止パターン |
| 自己検証ツール(ログ、スクリーンショット、複数インスタンス起動) | ビルドとテストのコマンド(Unity はスクリプトも同梱) |
| エンジン非依存のネットワーク権威ルールとテスト等級 | マルチプレイヤーのノート(Mirror/NGO、レプリケーション、ハイレベルマルチプレイヤー、lightyear/renet) |
| アセット・キャラクターのパイプラインガイド | `.gitignore` / LFS のヒント、アセットインポート(Unity) |

どの部分がどこから来たかの一覧は [`docs/INVENTORY.md`](docs/INVENTORY.md)(英語)にあります。

## インストール (Claude Code)

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # pick your engine: mm-godot, mm-unity, mm-unreal, mm-bevy
```

任意パック: `/plugin install mm-agents@monkeymode`、`/plugin install mm-art-tools@monkeymode`。

必要なもの: Claude Code v2.1.271 以降(選択肢が固定されたプラグイン設定)、Python 3.11+ と [`uv`](https://docs.astral.sh/uv/)(ワークフロースクリプトとガードレール)、`.ps1` ツール用の PowerShell 7、ローカルのコンセプト・選択ページ用の Node.js 18+。

`mm-core` にはあなた自身についての設定が 2 つあり、`/plugin` → MonkeyMode core → configure(または `claude plugin configure mm-core@monkeymode`)で設定します。未設定のままなら `/mm-setup` が代わりに質問します。

| 設定 | 選択肢 |
|---|---|
| `coding_level` | I can read code / I can't read code(コードを読める / 読めない) |
| `uses_chatgpt` | yes / no(「画像には ChatGPT をおすすめします」) |

## クイックスタート

1. Claude Code でゲームプロジェクトを開き、**`/mm-setup`** を実行します。エンジン、ソロかチームか、ジャンルとプラットフォーム、マルチプレイヤーの有無、プロジェクトの段階、ガードレールの強さ(コードを読める場合のみ)、ドキュメントフォルダーを聞いたあと、すべてをインストールして次の一歩を教えてくれます。分岐を含む全体の流れは [`docs/ONBOARDING.md`](docs/ONBOARDING.md) にあります。
2. 勧められたスキルを実行します。新しいアイデアなら `/mm-brainstorm-game`、既存のコードベースなら `/mm-document-project` です。
3. 次に何をすべきか迷ったら、いつでも `/mm-help` に聞いてください。

プロジェクトに追加されるもの:

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

## Claude Code なしで (AGENTS.md を読むエージェント)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

同じ質問をして同じファイルをインストールし、スキルを `.agents/skills/` にコピーします。詳しくは [`docs/ONBOARDING.md`](docs/ONBOARDING.md#without-claude-code-codex-and-other-agentsmd-agents) を参照してください。

## ドキュメント

- [ユーザーガイド](docs/GUIDE.md): インストール、セットアップの質問、各ステップのスキルと出力ファイルを含むワークフロー全体、ガードレール、画像、エンジン別ノート、FAQ(英語)
- [オンボーディング](docs/ONBOARDING.md): セットアップのフローチャートと各回答で変わること(英語)
- [インベントリ](docs/INVENTORY.md): 出典、共通とエンジン別の区分、スキル名の対応表(英語)
- [コントリビューション](CONTRIBUTING.md): スキル・エンジンアダプター・ガードレールルールの追加、テスト、PR チェックリスト(英語)

## カスタマイズ

- プロジェクトのルール: プロジェクト内の `AGENTS.md`(MonkeyMode のマーカーの外)、`docs/ai/`、`docs/engine/` を編集します。これらはスキルの指示より優先されます。
- スキルの動作: `_mm/custom/<skill-name>.toml`(チーム)または `<skill-name>.user.toml`(個人)に上書き設定を置きます。`persistent_facts` などの配列はスキルの既定値に追加されます。`/mm-customize` が案内します。
- ガードレール: `guardrails/<engine>.json` にルールを足すか、新しい `guardrails/<name>.json` プロファイルを作ります(形式は `docs/ai/12`)。変更は意図したときだけにしてください。エージェントは自分でルールを緩めないよう指示されています。

## インストールのテスト

```
claude plugin validate .                      # marketplace
claude plugin validate plugins/mm-core       # each plugin
claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity
```

最後のコマンドは、マーケットプレイスを追加せず、そのセッションの間だけプラグインを読み込んで Claude Code を起動します。コントリビューターはスクリプトのテストと `uv run tools/scrub.py` も実行します([CONTRIBUTING.md](CONTRIBUTING.md) 参照)。

## クレジットとライセンス

MonkeyMode は MIT ライセンスです([LICENSE](LICENSE))。ワークフロースキルは [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) と BMad Game Dev Studio モジュール(MIT)を、グラフィックツールのスキルは [CLI-Anything](https://github.com/HKUDS/CLI-Anything)(Apache-2.0)をもとにしています。MonkeyMode は独立したプロジェクトであり、元の作者の承認を受けたものではありません。詳細とすべての変更点: [NOTICE](NOTICE)、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

コントリビューションを歓迎します。[CONTRIBUTING.md](CONTRIBUTING.md) と[行動規範](CODE_OF_CONDUCT.md)をご覧ください。特に Godot、Unreal、Bevy のアダプターの修正を歓迎します。公式ドキュメントで確認済みですが、まだ実際のプロジェクトでは使われておらず、確認できなかった項目は各アダプターで *needs verification* と記されています。
