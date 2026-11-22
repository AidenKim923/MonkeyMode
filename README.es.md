# MonkeyMode

[English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · **Español** · [Português (Brasil)](README.pt-BR.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [Tiếng Việt](README.vi.md)

> **I'm Monkey Game Developer 🐒**
>
> Hasta un agente (o un dev) no muy listo se vuelve listo cuando trabaja con MonkeyMode.

MonkeyMode es un kit de desarrollo de videojuegos de código abierto para agentes de programación con IA. Le da al agente una forma probada de trabajar en un juego: un flujo de trabajo del diseño al lanzamiento (brief → GDD → arquitectura → historias → desarrollo → revisión → playtest), reglas que lo obligan a verificar su propio trabajo en lugar de declarar éxito, barreras de protección que bloquean los errores que los agentes repiten en el código de juegos, y conocimiento específico para **Godot, Unity, Unreal y Bevy**.

Se distribuye como un marketplace de plugins de Claude Code y también funciona con agentes que leen `AGENTS.md` (Codex y otros).

## Qué incluye

| Plugin | Qué obtienes |
|---|---|
| **`mm-core`** (obligatorio) | 42 skills de flujo de trabajo `mm-` (brief del juego, GDD, narrativa, UX, arquitectura, épicas e historias, historia de desarrollo, revisión de código, planificación y estado del sprint, plan de playtest, diseño de pruebas y de rendimiento, retrospectiva, investigación, desarrollo rápido, revisión, ayuda, ...), la configuración inicial `mm-setup`, documentos operativos para el agente (`docs/ai/`: política de ejecución, manual de verificación, autoridad de red, traspaso, procedimiento previo al commit, barreras, ...), el verificador de barreras con un hook tras cada edición, un perfil de secretos y rutas personales, y una galería de conceptos con página de elección |
| **`mm-unity`** | APIs de C# prohibidas, reglas de dirección entre ensamblados, scripts de pruebas y compilación en modo batch, notas de Mirror y Netcode, lista de verificación para importar assets. *Probado en un proyecto real* |
| **`mm-godot`** | Reglas de rutas de nodos y señales en GDScript, comandos de pruebas sin interfaz, notas de multijugador de alto nivel. *Verificado con la documentación de Godot 4.7* |
| **`mm-unreal`** | Reglas de UObject/GC, patrones de C++ prohibidos, comandos de UBT y pruebas automatizadas, notas de replicación. *Verificado en parte con la documentación de Unreal Engine 5.9* |
| **`mm-bevy`** | Nada de bloqueos dentro de los sistemas, orden de los sistemas, prohibiciones de Clippy, comandos de pruebas con cargo, notas de lightyear/replicon/renet. *Verificado con Bevy 0.20* |
| `mm-agents` (opcional) | Agentes con personaje (diseñador de juegos, arquitecto, desarrollador, desarrollador en solitario, redactor técnico, analista, PM, diseñador UX) y modo fiesta |
| `mm-art-tools` (opcional) | `mm-concept-art` (prompts para ChatGPT, Codex CLI u otras opciones) y herramientas de línea de comandos para Blender, RenderDoc y Nsight Graphics |

### Común vs. por motor

| Común (mm-core) | Por motor (mm-&lt;engine&gt;) |
|---|---|
| Plantillas del flujo: brief del juego, GDD, narrativa, UX, PRD, arquitectura, épicas/historias, historia, plan de playtest, plan de pruebas de rendimiento, diseño de pruebas, lista de revisión de código, retrospectiva, registro de decisiones, contexto del proyecto | Plantilla de contexto del proyecto |
| Comportamiento del agente, verificación, traspaso, control del alcance, higiene de Git, flujo de equipo | Anexo de arquitectura (estructura de escenas y assets; GDScript/C#, C#, C++/Blueprint, Rust/ECS) |
| Verificador de barreras, hooks tras editar y antes del commit, perfil de secretos | Perfil de barreras del motor y patrones prohibidos |
| Herramientas de autoverificación (logs, capturas, lanzamiento de varias instancias) | Comandos de compilación y pruebas (Unity también incluye scripts) |
| Reglas de autoridad de red y niveles de prueba independientes del motor | Notas de multijugador (Mirror/NGO, replicación, multijugador de alto nivel, lightyear/renet) |
| Guías de producción de assets y personajes | Pistas para `.gitignore` / LFS, importación de assets (Unity) |

## Instalación (Claude Code)

```
/plugin marketplace add <owner>/MonkeyMode
/plugin install mm-core@monkeymode
/plugin install mm-unity@monkeymode   # pick your engine: mm-godot, mm-unity, mm-unreal, mm-bevy
```

Paquetes opcionales: `/plugin install mm-agents@monkeymode`, `/plugin install mm-art-tools@monkeymode`.

Requisitos: Claude Code v2.1.271 o posterior (ajustes de plugin con opciones fijas), Python 3.11+ y [`uv`](https://docs.astral.sh/uv/) (scripts del flujo y barreras), PowerShell 7 para las herramientas `.ps1`, Node.js 18+ para la página local de conceptos y elecciones.

`mm-core` tiene dos ajustes sobre ti, que se configuran en `/plugin` → MonkeyMode core → configure (o con `claude plugin configure mm-core@monkeymode`). Si los dejas sin definir, `/mm-setup` te los preguntará.

| Ajuste | Opciones |
|---|---|
| `coding_level` | I can read code / I can't read code (sé leer código / no sé) |
| `uses_chatgpt` | yes / no ("Para imágenes recomendamos ChatGPT") |

## Inicio rápido

1. Abre tu proyecto de juego en Claude Code y ejecuta **`/mm-setup`**. Te pregunta por el motor, si trabajas solo o en equipo, el género y las plataformas, si es multijugador, la etapa del proyecto, el nivel de las barreras (solo si sabes leer código) y la carpeta de documentos; luego lo instala todo y te dice el siguiente paso. El flujo completo con sus ramas está en [`docs/ONBOARDING.md`](docs/ONBOARDING.md).
2. Ejecuta la skill que te recomiende, por ejemplo `/mm-brainstorm-game` para una idea nueva o `/mm-document-project` para un código ya existente.
3. Pregunta a `/mm-help` siempre que no sepas qué viene después.

Lo que se añade a tu proyecto:

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

## Sin Claude Code (agentes que leen AGENTS.md)

```
git clone <MonkeyMode repo URL>
uv run MonkeyMode/plugins/mm-core/skills/mm-setup/scripts/setup_project.py --target <your game> --interactive --apply --copy-skills agents
```

Hace las mismas preguntas, instala los mismos archivos y copia las skills en `.agents/skills/`. Consulta [`docs/ONBOARDING.md`](docs/ONBOARDING.md#without-claude-code-codex-and-other-agentsmd-agents).

## Documentación

- [Guía de usuario](docs/GUIDE.md): instalación, la entrevista de configuración, el flujo completo con la skill y el archivo que produce cada paso, barreras, imágenes, notas por motor, preguntas frecuentes (en inglés)
- [Incorporación](docs/ONBOARDING.md): el diagrama de configuración y qué cambia cada respuesta (en inglés)
- [Inventario](docs/INVENTORY.md): común vs. por motor, tabla de nombres de skills (en inglés)
- [Cómo contribuir](CONTRIBUTING.md): añadir skills, adaptadores de motor y reglas de barreras; pruebas; lista para PR (en inglés)

## Personalización

- Reglas del proyecto: edita `AGENTS.md` (fuera de los marcadores de MonkeyMode), `docs/ai/` y `docs/engine/` en tu proyecto. Tienen prioridad sobre las instrucciones de las skills.
- Comportamiento de las skills: pon tus cambios en `_mm/custom/<skill-name>.toml` (equipo) o `<skill-name>.user.toml` (personal). Los arrays como `persistent_facts` se añaden a los valores por defecto de la skill. `/mm-customize` te guía.
- Barreras: añade reglas a `guardrails/<engine>.json` o crea un perfil nuevo `guardrails/<name>.json` (formato en `docs/ai/12`). Cámbialas solo a propósito; los agentes tienen orden de no relajarlas por su cuenta.

## Probar la instalación

```
claude plugin validate .                      # marketplace
claude plugin validate plugins/mm-core       # each plugin
claude --plugin-dir ./plugins/mm-core --plugin-dir ./plugins/mm-unity
```

El último comando inicia Claude Code con los plugins cargados durante una sola sesión, sin añadir el marketplace. Quienes contribuyen también ejecutan las pruebas de los scripts y `uv run tools/scrub.py` (ver [CONTRIBUTING.md](CONTRIBUTING.md)).

## Créditos y licencia

MonkeyMode tiene licencia MIT ([LICENSE](LICENSE)). Sus skills de flujo se basan en [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) y el módulo BMad Game Dev Studio (MIT), y las skills de herramientas gráficas en [CLI-Anything](https://github.com/HKUDS/CLI-Anything) (Apache-2.0). MonkeyMode es independiente y no cuenta con el respaldo de sus autores. Detalles y todas las modificaciones: [NOTICE](NOTICE), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Las contribuciones son bienvenidas: consulta [CONTRIBUTING.md](CONTRIBUTING.md) y el [Código de conducta](CODE_OF_CONDUCT.md). Agradecemos especialmente las correcciones a los adaptadores de Godot, Unreal y Bevy: se verificaron con la documentación oficial, pero aún no se han usado en un proyecto real, y los puntos pendientes están marcados como *needs verification* en cada adaptador.
