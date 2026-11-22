# MonkeyMode

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · **Tiếng Việt**

> **I'm Monkey Game Developer 🐒**
>
> Ngay cả một agent (hay một dev) không mấy thông minh cũng trở nên thông minh khi làm việc cùng MonkeyMode.

MonkeyMode là bộ công cụ phát triển game mã nguồn mở dành cho các AI agent viết code. Nó cho agent một cách làm việc đã được kiểm chứng: quy trình từ thiết kế đến phát hành (brief → GDD → kiến trúc → story → phát triển → review → playtest), các quy tắc buộc agent tự kiểm tra kết quả thay vì chỉ tuyên bố đã xong, các guardrail chặn những lỗi mà agent hay lặp lại trong code game, và kiến thức riêng cho từng engine **Godot, Unity, Unreal và Bevy**.

Nó được phát hành dưới dạng marketplace plugin của Claude Code và cũng hoạt động với các agent đọc `AGENTS.md` (Codex và các agent khác).

## Bên trong có gì

| Plugin | Bạn nhận được |
|---|---|
| **`mm-core`** (bắt buộc) | 42 skill quy trình `mm-` (brief game, GDD, cốt truyện, UX, kiến trúc, epic và story, dev story, review code, lập kế hoạch và theo dõi sprint, kế hoạch playtest, thiết kế kiểm thử và kiểm thử hiệu năng, retrospective, nghiên cứu, quick dev, review, trợ giúp, ...), phần thiết lập ban đầu `mm-setup`, tài liệu vận hành cho agent (`docs/ai/`: chính sách thực thi, sổ tay kiểm chứng, quyền quyết định mạng, bàn giao, quy trình trước khi commit, guardrail, ...), bộ kiểm tra guardrail kèm hook sau mỗi lần sửa, hồ sơ kiểm tra bí mật và đường dẫn cá nhân, cùng thư viện concept với trang lựa chọn |
| **`mm-unity`** | Các API C# bị cấm, quy tắc hướng phụ thuộc giữa các assembly, script test và build ở chế độ batch, ghi chú về Mirror và Netcode, checklist nhập asset. *Đã kiểm chứng trong dự án thật* |
| **`mm-godot`** | Quy tắc về đường dẫn node và signal trong GDScript, lệnh chạy test không giao diện, ghi chú về multiplayer cấp cao. *Đã đối chiếu với tài liệu Godot 4.7* |
| **`mm-unreal`** | Quy tắc UObject/GC, các mẫu C++ bị cấm, lệnh UBT và kiểm thử tự động, ghi chú về replication. *Đã đối chiếu một phần với tài liệu Unreal Engine 5.9* |
| **`mm-bevy`** | Không chặn (block) trong system, thứ tự chạy system, danh sách cấm của Clippy, lệnh test bằng cargo, ghi chú về lightyear/replicon/renet. *Đã đối chiếu với Bevy 0.20* |
| `mm-agents` (tùy chọn) | Các agent nhập vai (game designer, kiến trúc sư, lập trình viên, dev độc lập, người viết tài liệu kỹ thuật, chuyên viên phân tích, PM, nhà thiết kế UX) và chế độ party |
| `mm-art-tools` (tùy chọn) | `mm-concept-art` (prompt cho ChatGPT, Codex CLI hoặc phương án khác) và công cụ dòng lệnh cho Blender, RenderDoc, Nsight Graphics |

### Dùng chung và riêng cho từng engine

| Dùng chung (mm-core) | Riêng cho từng engine (mm-&lt;engine&gt;) |
|---|---|
| Mẫu quy trình: brief game, GDD, cốt truyện, UX, PRD, kiến trúc, epic/story, story, kế hoạch playtest, kế hoạch kiểm thử hiệu năng, thiết kế kiểm thử, checklist review code, retrospective, nhật ký quyết định, bối cảnh dự án | Mẫu bối cảnh dự án |
| Hành vi của agent, kiểm chứng, bàn giao, kiểm soát phạm vi, giữ Git gọn gàng, quy trình nhóm | Phần bổ sung kiến trúc (cấu trúc scene và asset; GDScript/C#, C#, C++/Blueprint, Rust/ECS) |
| Bộ kiểm tra guardrail, hook sau khi sửa và trước khi commit, hồ sơ kiểm tra bí mật | Hồ sơ guardrail của engine và các mẫu bị cấm |
| Công cụ tự kiểm chứng (log, ảnh chụp màn hình, chạy nhiều phiên bản) | Lệnh build và test (Unity còn kèm script) |
| Quy tắc quyền quyết định mạng và cấp độ kiểm thử không phụ thuộc engine | Ghi chú multiplayer (Mirror/NGO, replication, multiplayer cấp cao, lightyear/renet) |
| Hướng dẫn quy trình sản xuất asset và nhân vật | Gợi ý `.gitignore` / LFS, nhập asset (Unity) |

## Cài đặt (Claude Code)

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # pick your engine: mm-godot, mm-unity, mm-unreal, mm-bevy
```

Gói tùy chọn: `/plugin install mm-agents@monkeymode`, `/plugin install mm-art-tools@monkeymode`.

Yêu cầu: Claude Code v2.1.271 trở lên (cài đặt plugin với lựa chọn cố định), Python 3.11+ và [`uv`](https://docs.astral.sh/uv/) (script quy trình và guardrail), PowerShell 7 cho các công cụ `.ps1`, Node.js 18+ cho trang concept và lựa chọn chạy cục bộ.

`mm-core` có hai cài đặt về bạn, đặt trong `/plugin` → MonkeyMode core → configure (hoặc bằng `claude plugin configure mm-core@monkeymode`). Nếu để trống, `/mm-setup` sẽ hỏi bạn.

| Cài đặt | Lựa chọn |
|---|---|
| `coding_level` | I can read code / I can't read code (tôi đọc được code / không) |
| `uses_chatgpt` | yes / no ("Với hình ảnh, chúng tôi khuyên dùng ChatGPT") |

## Bắt đầu nhanh

1. Mở dự án game của bạn trong Claude Code và chạy **`/mm-setup`**. Nó sẽ hỏi về engine, bạn làm một mình hay theo nhóm, thể loại và nền tảng, có multiplayer hay không, giai đoạn của dự án, mức guardrail (chỉ khi bạn đọc được code) và thư mục tài liệu, sau đó cài đặt mọi thứ và cho bạn biết bước tiếp theo. Toàn bộ luồng có rẽ nhánh nằm trong [`docs/ONBOARDING.md`](docs/ONBOARDING.md).
2. Chạy skill được đề xuất, ví dụ `/mm-brainstorm-game` cho một ý tưởng mới hoặc `/mm-document-project` cho codebase có sẵn.
3. Hỏi `/mm-help` bất cứ khi nào bạn không chắc bước tiếp theo là gì.

Những gì được thêm vào dự án:

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

## Không dùng Claude Code (agent đọc AGENTS.md)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

Script đặt cùng những câu hỏi, cài cùng những tệp và sao chép skill vào `.agents/skills/`. Xem [`docs/ONBOARDING.md`](docs/ONBOARDING.md#without-claude-code-codex-and-other-agentsmd-agents).

## Tài liệu

- [Hướng dẫn sử dụng](docs/GUIDE.md): cài đặt, phần hỏi đáp thiết lập, toàn bộ quy trình kèm skill và tệp kết quả của từng bước, guardrail, hình ảnh, ghi chú theo engine, câu hỏi thường gặp (tiếng Anh)
- [Thiết lập ban đầu](docs/ONBOARDING.md): sơ đồ thiết lập và mỗi câu trả lời thay đổi điều gì (tiếng Anh)
- [Danh mục](docs/INVENTORY.md): dùng chung và riêng cho engine, bảng tên skill (tiếng Anh)
- [Đóng góp](CONTRIBUTING.md): thêm skill, adapter engine và quy tắc guardrail; kiểm thử; checklist PR (tiếng Anh)

## Tùy chỉnh

- Quy tắc dự án: sửa `AGENTS.md` (bên ngoài phần đánh dấu của MonkeyMode), `docs/ai/` và `docs/engine/` trong dự án. Chúng được ưu tiên hơn chỉ dẫn của skill.
- Hành vi của skill: đặt phần ghi đè vào `_mm/custom/<skill-name>.toml` (nhóm) hoặc `<skill-name>.user.toml` (cá nhân). Các mảng như `persistent_facts` được nối thêm vào giá trị mặc định của skill. `/mm-customize` sẽ hướng dẫn bạn.
- Guardrail: thêm quy tắc vào `guardrails/<engine>.json` hoặc tạo hồ sơ mới `guardrails/<name>.json` (định dạng trong `docs/ai/12`). Chỉ thay đổi khi bạn thực sự muốn; agent được dặn không bao giờ tự nới lỏng chúng.

## Kiểm tra cài đặt

```
claude plugin validate .                      # marketplace
claude plugin validate plugins/mm-core       # each plugin
claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity
```

Lệnh cuối khởi động Claude Code với các plugin được nạp trong một phiên, không cần thêm marketplace. Người đóng góp cũng chạy test của các script và `uv run tools/scrub.py` (xem [CONTRIBUTING.md](CONTRIBUTING.md)).

## Ghi công và giấy phép

MonkeyMode dùng giấy phép MIT ([LICENSE](LICENSE)). Các skill quy trình dựa trên [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) và mô-đun BMad Game Dev Studio (MIT), còn các skill công cụ đồ họa dựa trên [CLI-Anything](https://github.com/HKUDS/CLI-Anything) (Apache-2.0). MonkeyMode là dự án độc lập và không được các tác giả đó bảo trợ. Chi tiết và mọi thay đổi: [NOTICE](NOTICE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Chúng tôi hoan nghênh mọi đóng góp: xem [CONTRIBUTING.md](CONTRIBUTING.md) và [Bộ quy tắc ứng xử](CODE_OF_CONDUCT.md). Đặc biệt hoan nghênh các chỉnh sửa cho adapter Godot, Unreal và Bevy: chúng đã được đối chiếu với tài liệu chính thức nhưng chưa được dùng trong dự án thật, và những điểm chưa xác nhận được đánh dấu *needs verification* trong từng adapter.
