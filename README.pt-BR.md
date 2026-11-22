# MonkeyMode

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · **Português (Brasil)** · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md)

> **I'm Monkey Game Developer 🐒**
>
> Até um agente (ou dev) não tão esperto fica esperto quando trabalha com o MonkeyMode.

O MonkeyMode é um kit de desenvolvimento de jogos de código aberto para agentes de programação com IA. Ele dá ao agente um jeito comprovado de trabalhar em um jogo: um fluxo de trabalho do design ao lançamento (brief → GDD → arquitetura → histórias → desenvolvimento → revisão → playtest), regras que fazem o agente verificar o próprio trabalho em vez de simplesmente declarar sucesso, guardrails que bloqueiam os erros que agentes vivem cometendo em código de jogos e conhecimento específico para **Godot, Unity, Unreal e Bevy**.

Ele foi extraído de um projeto real de jogo cooperativo em Unity + Mirror e generalizado. É distribuído como um marketplace de plugins do Claude Code e também funciona com agentes que leem `AGENTS.md` (Codex e outros).

## O que vem incluído

| Plugin | O que você recebe |
|---|---|
| **`mm-core`** (obrigatório) | 42 skills de fluxo `mm-` (brief do jogo, GDD, narrativa, UX, arquitetura, épicos e histórias, história de desenvolvimento, revisão de código, planejamento e status de sprint, plano de playtest, design de testes e de desempenho, retrospectiva, pesquisa, desenvolvimento rápido, revisão, ajuda, ...), a configuração inicial `mm-setup`, documentos operacionais para o agente (`docs/ai/`: política de execução, manual de verificação, autoridade de rede, passagem de bastão, procedimento antes do commit, guardrails, ...), o verificador de guardrails com hook após cada edição, um perfil de segredos e caminhos pessoais, e uma galeria de conceitos com página de escolha |
| **`mm-unity`** | APIs de C# proibidas, regras de direção entre assemblies, scripts de teste e build em modo batch, notas de Mirror e Netcode, checklist de importação de assets. *Testado em projeto real* |
| **`mm-godot`** | Regras de caminhos de nós e sinais em GDScript, comandos de teste headless, notas de multiplayer de alto nível. *Conferido com a documentação do Godot 4.7* |
| **`mm-unreal`** | Regras de UObject/GC, padrões de C++ proibidos, comandos de UBT e de testes automatizados, notas de replicação. *Conferido em parte com a documentação do Unreal Engine 5.9* |
| **`mm-bevy`** | Nada de bloqueio dentro dos sistemas, ordem dos sistemas, proibições do Clippy, comandos de teste com cargo, notas de lightyear/replicon/renet. *Conferido com o Bevy 0.20* |
| `mm-agents` (opcional) | Agentes com persona (game designer, arquiteto, desenvolvedor, dev solo, redator técnico, analista, PM, designer de UX) e modo festa |
| `mm-art-tools` (opcional) | `mm-concept-art` (prompts para o ChatGPT, Codex CLI ou alternativas) e ferramentas de linha de comando para Blender, RenderDoc e Nsight Graphics |

### Comum vs. por engine

| Comum (mm-core) | Por engine (mm-&lt;engine&gt;) |
|---|---|
| Templates do fluxo: brief do jogo, GDD, narrativa, UX, PRD, arquitetura, épicos/histórias, história, plano de playtest, plano de teste de desempenho, design de testes, checklist de revisão de código, retrospectiva, registro de decisões, contexto do projeto | Template de contexto do projeto |
| Comportamento do agente, verificação, passagem de bastão, controle de escopo, higiene de Git, fluxo de equipe | Anexo de arquitetura (estrutura de cenas e assets; GDScript/C#, C#, C++/Blueprint, Rust/ECS) |
| Verificador de guardrails, hooks após editar e antes do commit, perfil de segredos | Perfil de guardrails da engine e padrões proibidos |
| Ferramentas de autoverificação (logs, capturas de tela, várias instâncias) | Comandos de build e teste (a Unity também traz scripts) |
| Regras de autoridade de rede e níveis de teste independentes da engine | Notas de multiplayer (Mirror/NGO, replicação, multiplayer de alto nível, lightyear/renet) |
| Guias de produção de assets e personagens | Dicas de `.gitignore` / LFS, importação de assets (Unity) |

A lista completa do que veio de onde está em [`docs/INVENTORY.md`](docs/INVENTORY.md) (em inglês).

## Instalação (Claude Code)

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # pick your engine: mm-godot, mm-unity, mm-unreal, mm-bevy
```

Pacotes opcionais: `/plugin install mm-agents@monkeymode`, `/plugin install mm-art-tools@monkeymode`.

Requisitos: Claude Code v2.1.271 ou mais recente (configurações de plugin com opções fixas), Python 3.11+ e [`uv`](https://docs.astral.sh/uv/) (scripts do fluxo e guardrails), PowerShell 7 para as ferramentas `.ps1`, Node.js 18+ para a página local de conceitos e escolhas.

O `mm-core` tem duas configurações sobre você, definidas em `/plugin` → MonkeyMode core → configure (ou `claude plugin configure mm-core@monkeymode`). Se você deixá-las em branco, o `/mm-setup` pergunta.

| Configuração | Opções |
|---|---|
| `coding_level` | I can read code / I can't read code (sei ler código / não sei) |
| `uses_chatgpt` | yes / no ("Para imagens, recomendamos o ChatGPT") |

## Primeiros passos

1. Abra o projeto do seu jogo no Claude Code e rode **`/mm-setup`**. Ele pergunta sobre a engine, se você trabalha sozinho ou em equipe, gênero e plataformas, multiplayer, a fase do projeto, o nível dos guardrails (só se você lê código) e a pasta de documentos; depois instala tudo e diz qual é o próximo passo. O fluxo completo com as ramificações está em [`docs/ONBOARDING.md`](docs/ONBOARDING.md).
2. Rode a skill recomendada, por exemplo `/mm-brainstorm-game` para uma ideia nova ou `/mm-document-project` para um código que já existe.
3. Pergunte ao `/mm-help` sempre que não souber o que vem a seguir.

O que é adicionado ao seu projeto:

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

## Sem o Claude Code (agentes que leem AGENTS.md)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

Ele faz as mesmas perguntas, instala os mesmos arquivos e copia as skills para `.agents/skills/`. Veja [`docs/ONBOARDING.md`](docs/ONBOARDING.md#without-claude-code-codex-and-other-agentsmd-agents).

## Documentação

- [Guia do usuário](docs/GUIDE.md): instalação, a entrevista de configuração, o fluxo completo com a skill e o arquivo gerado em cada etapa, guardrails, imagens, notas por engine, perguntas frequentes (em inglês)
- [Integração](docs/ONBOARDING.md): o fluxograma da configuração e o que cada resposta muda (em inglês)
- [Inventário](docs/INVENTORY.md): de onde veio cada parte, comum vs. por engine, tabela de nomes das skills (em inglês)
- [Como contribuir](CONTRIBUTING.md): adicionar skills, adaptadores de engine e regras de guardrails; testes; checklist de PR (em inglês)

## Personalização

- Regras do projeto: edite `AGENTS.md` (fora dos marcadores do MonkeyMode), `docs/ai/` e `docs/engine/` no seu projeto. Eles têm prioridade sobre as instruções das skills.
- Comportamento das skills: coloque suas alterações em `_mm/custom/<skill-name>.toml` (equipe) ou `<skill-name>.user.toml` (pessoal). Arrays como `persistent_facts` são adicionados aos padrões da skill. O `/mm-customize` guia você.
- Guardrails: adicione regras em `guardrails/<engine>.json` ou crie um perfil novo `guardrails/<name>.json` (formato em `docs/ai/12`). Mude só de propósito; os agentes são instruídos a nunca afrouxá-los por conta própria.

## Testando a instalação

```
claude plugin validate .                      # marketplace
claude plugin validate plugins/mm-core       # each plugin
claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity
```

O último comando inicia o Claude Code com os plugins carregados só para uma sessão, sem adicionar o marketplace. Quem contribui também roda os testes dos scripts e `uv run tools/scrub.py` (veja [CONTRIBUTING.md](CONTRIBUTING.md)).

## Créditos e licença

O MonkeyMode usa a licença MIT ([LICENSE](LICENSE)). Suas skills de fluxo se baseiam no [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) e no módulo BMad Game Dev Studio (MIT), e as skills de ferramentas gráficas no [CLI-Anything](https://github.com/HKUDS/CLI-Anything) (Apache-2.0). O MonkeyMode é independente e não tem o endosso desses autores. Detalhes e todas as modificações: [NOTICE](NOTICE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Contribuições são bem-vindas: veja [CONTRIBUTING.md](CONTRIBUTING.md) e o [Código de Conduta](CODE_OF_CONDUCT.md). Correções nos adaptadores de Godot, Unreal e Bevy são especialmente bem-vindas: eles foram conferidos com a documentação oficial, mas ainda não foram usados em um projeto real, e os itens em aberto estão marcados como *needs verification* em cada adaptador.
