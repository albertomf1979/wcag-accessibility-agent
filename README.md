# WCAG Accessibility Agent

> Skill de accesibilidad digital basada en WCAG 2.1, instalable en agentes de programación con IA (Claude Code, Codex, GitHub Copilot y otros) y en Claude.ai, más un agente CLI construido sobre la API de Anthropic.  
> Audita, analiza, evalúa y corrige productos digitales. Genera informes PDF/DOCX y handoffs para equipos.

**Fuente de conocimiento**: [W3C Web Accessibility Initiative (WAI)](https://www.w3.org/WAI/)  
**Estándar**: [WCAG 2.1](https://www.w3.org/TR/WCAG21/) — niveles A, AA y AAA  
**Ámbito**: UX · UI · Desarrollo tecnológico  
**Modelo**: Claude (Anthropic API)

---

## Contenido

- [Qué es este repositorio](#qué-es-este-repositorio)
- [Instalación de la skill](#instalación-de-la-skill)
  - [1. GitHub CLI (`gh skill`)](#1-github-cli-gh-skill)
  - [2. Plugin (Claude Code, Codex, Copilot CLI, Antigravity)](#2-plugin-claude-code-codex-copilot-cli-antigravity)
  - [3. Instalación manual como Agent Skill](#3-instalación-manual-como-agent-skill)
  - [4. Claude.ai (paquete `.skill`)](#4-claudeai-paquete-skill)
- [Ejemplos de uso de la skill](#ejemplos-de-uso-de-la-skill)
- [5. Instalar el agente CLI Python](#5-instalar-el-agente-cli-python)
- [Capacidades del agente](#capacidades-del-agente)
- [Referencia de comandos](#referencia-de-comandos)
- [Construir tu propio agente desde la skill](#construir-tu-propio-agente-desde-la-skill)
- [Marco legal](#marco-legal)
- [Contribuir](#contribuir)

---

## Qué es este repositorio

Este repositorio contiene dos artefactos independientes que puedes usar por separado o juntos:

**1. La Skill** (`skills/wcag-accessibility/`: `SKILL.md` + `references/` + `scripts/`)  
Base de conocimiento WCAG 2.1 estructurada para agentes de IA, siguiendo la especificación [Agent Skills](https://agentskills.io/specification). Cubre los 78 criterios de éxito de WCAG 2.1 (y lista aparte los 9 añadidos en WCAG 2.2), técnicas de fallo, patrones UX/UI/desarrollo y marcos legales. Incluye `scripts/axe-scan.mjs`, un escaneo determinista con axe-core que aporta evidencias. Se instala en Claude Code, Codex, GitHub Copilot, Antigravity y otros agentes con `gh skill` o `npx skills`, como plugin (Claude Code, Codex, Copilot CLI, Antigravity) o en Claude.ai. **No requiere Python ni API key**: el agente anfitrión lee la skill, ejecuta las herramientas disponibles y propone los cambios.

**2. El Agente CLI** (`agent.py` y el resto del código Python)  
Implementación completa e independiente del agente con bucle de tool use sobre la API de Anthropic, análisis de URLs y archivos, exportación de informes PDF/DOCX y corrección activa de código fuente. Usa la misma skill como system prompt y el mismo script de axe-core.

| | Skill portable | Agente CLI Python |
|---|---|---|
| Dónde se ejecuta | Dentro de tu agente (Claude Code, Codex, Copilot, Antigravity, Claude.ai...) | En tu terminal, como programa propio |
| Requisitos | Ninguno. Opcional: Node.js 18+ y Chrome para axe-core | Python 3.11+, dependencias de `requirements.txt`, `ANTHROPIC_API_KEY`; Node.js 18+ para axe-core |
| Modelo de IA | El de tu agente | Claude vía API de Anthropic (`WCAG_MODEL`) |
| Configuración inicial | Valores por defecto: Desarrollo · WCAG 2.1 AA · análisis sin modificar archivos | Protocolo interactivo (disciplina + nivel) o flags |
| Informes PDF/DOCX | Los genera el agente anfitrión si tiene herramientas para ello | Integrado (`--export pdf|docx`) |

---

## Instalación de la skill

### 1. GitHub CLI (`gh skill`)

Requiere una versión reciente de [GitHub CLI](https://cli.github.com/) con el comando `gh skill` (en preview).

```bash
# Claude Code
gh skill install albertomf1979/wcag-accessibility-agent wcag-accessibility --agent claude-code --scope user

# Codex
gh skill install albertomf1979/wcag-accessibility-agent wcag-accessibility --agent codex --scope user

# GitHub Copilot
gh skill install albertomf1979/wcag-accessibility-agent wcag-accessibility --agent github-copilot --scope user
```

`--scope project` la instala solo en el repositorio actual. Consulta `gh skill install --help` para la lista completa de agentes compatibles. Para actualizarla: `gh skill update`.

> `gh skill install` usa la última release publicada del repositorio si existe. Para instalar una rama o un commit concretos, añade `--pin <rama|sha>`.

**Alternativa con `npx skills`** ([Vercel Agent Skills](https://github.com/vercel-labs/skills), requiere Node.js):

```bash
npx skills add albertomf1979/wcag-accessibility-agent
```

### 2. Plugin (Claude Code, Codex, Copilot CLI, Antigravity)

El repositorio es también un marketplace de plugins (`.claude-plugin/marketplace.json`) con el plugin `wcag`, que reutiliza la misma carpeta `skills/`.

**Claude Code** — dentro de Claude Code:

```
/plugin marketplace add albertomf1979/wcag-accessibility-agent
/plugin install wcag@wcag-accessibility
```

O desde la terminal:

```bash
claude plugin marketplace add albertomf1979/wcag-accessibility-agent
claude plugin install wcag@wcag-accessibility
```

En Claude Code 2.1.275 o superior también puedes hacerlo en un paso: `/plugin install wcag --marketplace albertomf1979/wcag-accessibility-agent`.

La skill se activa automáticamente al hablar de accesibilidad, o de forma explícita con:

```
/wcag:wcag-accessibility audita src/components/Modal.tsx
```

**Codex CLI**:

```bash
codex plugin marketplace add albertomf1979/wcag-accessibility-agent
codex plugin add wcag@wcag-accessibility
```

**GitHub Copilot CLI** — dentro de Copilot CLI:

```
/plugin marketplace add albertomf1979/wcag-accessibility-agent
/plugin install wcag@wcag-accessibility
```

O desde la terminal: `copilot plugin marketplace add albertomf1979/wcag-accessibility-agent` y `copilot plugin install wcag@wcag-accessibility`.

**Antigravity CLI**:

```bash
agy plugin install https://github.com/albertomf1979/wcag-accessibility-agent
```

### 3. Instalación manual como Agent Skill

Copia la carpeta `skills/wcag-accessibility/` completa al directorio de skills de tu agente, por ejemplo:

```bash
git clone https://github.com/albertomf1979/wcag-accessibility-agent.git
cp -R wcag-accessibility-agent/skills/wcag-accessibility ~/.claude/skills/     # Claude Code
cp -R wcag-accessibility-agent/skills/wcag-accessibility ~/.agents/skills/     # Codex y otros agentes compatibles
cp -R wcag-accessibility-agent/skills/wcag-accessibility ~/.copilot/skills/    # GitHub Copilot
```

### 4. Claude.ai (paquete `.skill`)

**1.** Descarga el archivo `wcag-accessibility.skill` de la raíz de este repositorio o de la sección [Releases](../../releases).

**2.** En [claude.ai](https://claude.ai), ve a **Settings → Skills**.

**3.** Haz clic en **Upload skill** y selecciona el archivo `.skill`.

**4.** A partir de ese momento, Claude activará automáticamente el conocimiento WCAG cuando detecte preguntas relacionadas con accesibilidad.

El paquete es un ZIP de `skills/wcag-accessibility/` (los mismos archivos que usan `gh skill` y el plugin). Para regenerarlo tras modificar la skill:

```bash
make skill-package     # requiere zip; genera wcag-accessibility.skill
make test              # comprueba, entre otras cosas, que el paquete está actualizado
```

**Qué puedes hacer desde Claude.ai con la skill instalada:**
- Pegar código HTML/CSS/JS y pedir un análisis de accesibilidad
- Pedir auditorías formales con referencia a criterios WCAG
- Solicitar correcciones de código con explicación del criterio que se satisface
- Generar checklists y documentación de handoff para tu equipo
- Consultar cualquier criterio WCAG 2.1 con contexto de implementación

---

## Ejemplos de uso de la skill

Con la skill instalada, pide en lenguaje natural a tu agente:

- **Analizar un componente**: «Analiza la accesibilidad de `src/components/Dropdown.tsx`»
- **Auditar una URL con axe-core**: «Audita https://example.com con axe-core a nivel AA» (el agente ejecuta `node scripts/axe-scan.mjs <url>` y completa con revisión manual)
- **Revisar un pull request**: «Revisa la accesibilidad de los cambios de este PR» o «de `git diff main`»
- **Identificar problemas de un proyecto**: «¿Qué problemas de accesibilidad tiene este proyecto?»
- **Proponer o aplicar correcciones**: «Propón correcciones para los fallos de contraste» / «Aplica las correcciones y ejecuta los tests»
- **Generar un informe**: «Genera un informe de auditoría WCAG 2.1 AA en Markdown» o «un handoff para el equipo de diseño»

Por defecto la skill trabaja en **Desarrollo · WCAG 2.1 AA · modo análisis**, sin modificar archivos. Indica otros valores si los necesitas («nivel AAA», «enfoque UX», «incluye WCAG 2.2»). Cada hallazgo distingue entre incumplimientos verificados con herramientas, detectados por inspección de código, comprobaciones manuales necesarias, criterios no evaluados y no aplicables.

---

## 5. Instalar el agente CLI Python

Para uso avanzado: análisis automatizado de URLs, procesamiento de archivos, exportación PDF/DOCX y corrección directa sobre el código fuente del proyecto.

### Requisitos

- Python 3.11 o superior
- Node.js 18 o superior (`node --version` para comprobar)
- Una [API key de Anthropic](https://console.anthropic.com/)
- pip

> **¿Por qué Node.js?** El agente usa [axe-core](https://github.com/dequelabs/axe-core) vía `@axe-core/cli` (a través de `skills/wcag-accessibility/scripts/axe-scan.mjs`) para lanzar un escaneo con Chrome headless antes de cada análisis. Así detecta las violaciones automatizables en el DOM renderizado (con JS y CSS ejecutados), no solo en el HTML estático. Las herramientas automáticas no cubren todos los criterios: siempre hace falta revisión manual.

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/albertomf1979/wcag-accessibility-agent.git
cd wcag-accessibility-agent

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias Python
pip install -r requirements.txt

# 4. Pre-instalar axe-core CLI (descarga Chromium la primera vez, ~120 MB)
npx -y @axe-core/cli --version

# 5. Configurar credenciales
cp .env.example .env
# Edita .env y añade tu ANTHROPIC_API_KEY
```

### Verificar la instalación

```bash
python agent.py --help
```

Si ves la lista de opciones disponibles, todo está correcto.

---

## Capacidades del agente

### Protocolo de inicio

En el **agente CLI** en modo interactivo, el agente pregunta antes de actuar:

1. **Nivel disciplinar**: UX / UI / Desarrollo / Todos
2. **Nivel de conformidad WCAG objetivo**: A / AA / AAA

También pueden pasarse como flags (`--discipline`, `--level`); con `--url` o `--file` se usan por defecto `todos` y `AA`.

En la **skill portable** no se pregunta al inicio: se aplican valores por defecto (Desarrollo en repositorios de código · WCAG 2.1 AA · análisis sin modificar archivos) y solo se pregunta cuando falta información que cambia el resultado.

---

### Cinco modos de operación

#### 🔍 Análisis
Identifica y prioriza barreras de accesibilidad en un artefacto dado.

- Clasifica hallazgos por severidad: 🔴 Crítico / 🟠 Mayor / 🟡 Menor
- Mapea cada hallazgo al criterio WCAG 2.1 correspondiente
- Indica el impacto por perfil de usuario (visual, auditivo, motor, cognitivo)
- Cubre los tres niveles disciplinares: UX, UI y código

#### 📋 Auditoría
Informe formal de conformidad WCAG referenciable y documentado.

- Referencia explícita al criterio de éxito (ej: "1.4.3 Contraste mínimo — Nivel AA")
- Técnica de fallo documentada de la serie F del W3C (ej: F79, F68...)
- Tabla de resultados: ✅ Pasa / ❌ Falla / ⚠️ Revisar manualmente / ⏸️ No evaluado / N/A
- Cada hallazgo indica su evidencia: herramienta ejecutada (axe-core...), inspección de código o comprobación manual
- Metodología basada en WCAG-EM (Evaluation Methodology)
- Enlace al documento W3C Understanding por cada criterio

#### 📊 Evaluación
Calcula el nivel de conformidad actual y las brechas para alcanzar el objetivo.

- Score de conformidad por nivel: A / AA / AAA (porcentaje de criterios que pasan)
- Escala de madurez: Inicial / Básico / Intermedio / Avanzado / Excelente
- Roadmap de remediación priorizado por impacto y esfuerzo
- Útil para preparar una Declaración de Accesibilidad

#### 🔧 Corrección
Aplica las correcciones de accesibilidad, en dos modalidades:

**Corrección descriptiva** (sin acceso al código fuente): devuelve el fragmento corregido con explicación del criterio que satisface y el diff antes/después.

**Corrección activa** (con acceso al código fuente): explora el proyecto, lee los archivos afectados, muestra el diff exacto, pide confirmación y escribe los cambios. Crea automáticamente una copia de seguridad `.bak` de cada archivo antes de modificarlo.

> Para activar la corrección activa, el agente necesita acceso a la ruta local del proyecto.
> Ningún archivo se modifica sin confirmación explícita del usuario.

#### 📄 Handoff
Genera documentación estructurada por roles para que equipos trabajen de forma autónoma.

- Sección para equipo de UX: flujos, navegación, formularios
- Sección para equipo de UI/Diseño: especificaciones de contraste, tipografía, componentes
- Sección para equipo de Desarrollo: código correcto, ARIA, testing
- Sección para QA: checklist de verificación con criterios de aceptación binarios
- Exportable como PDF o DOCX

---

### Inputs que acepta

| Tipo | Cómo proporcionarlo |
|---|---|
| URL de página web | `--url https://ejemplo.com` |
| Archivo HTML local | `--file ruta/archivo.html` |
| Componente JS/JSX/TSX | `--file src/components/Button.jsx` |
| Archivo CSS | `--file styles/main.css` |
| Componente Vue / Svelte | `--file componente.vue` |
| Imagen / captura de pantalla | `--file captura.png` |
| PDF | `--file documento.pdf` |
| Código pegado directamente | Modo interactivo |
| Proyecto completo | `--fix /ruta/del/proyecto` |

---

### Outputs que genera

| Formato | Cuándo usarlo |
|---|---|
| Texto en terminal | Análisis rápido, iteración |
| PDF | Informe formal, presentaciones |
| DOCX | Handoff para equipos, editable |
| Código corregido | Aplicar fixes directamente |

---

### Cobertura WCAG 2.1

- **78 criterios de éxito** indexados (30 nivel A + 20 AA + 28 AAA; 17 de ellos nuevos en 2.1)
- Los 9 criterios añadidos en **WCAG 2.2** se listan aparte y solo se evalúan si se piden; las guías de referencia están orientadas a WCAG 2.1, así que la cobertura de 2.2 es parcial
- **Principios POUR**: Perceivable, Operable, Understandable, Robust
- **Técnicas de fallo** de la serie F del W3C referenciadas en auditorías
- **Patrones WAI-ARIA** para componentes interactivos
- **Tres disciplinas**: UX (flujos, navegación, formularios), UI (contraste, tipografía, motion), Desarrollo (HTML semántico, ARIA, JavaScript, testing)

---

## Referencia de comandos

```bash
# Modo interactivo — el agente hace las preguntas del protocolo
python agent.py

# Analizar una URL
python agent.py --url https://ejemplo.com

# Analizar un archivo local
python agent.py --file src/index.html

# Especificar disciplina y nivel WCAG
python agent.py --url https://ejemplo.com --discipline desarrollo --level AA

# Exportar informe en PDF
python agent.py --url https://ejemplo.com --export pdf

# Exportar handoff en DOCX
python agent.py --file componente.html --export docx --mode handoff

# Analizar y corregir directamente sobre el proyecto
python agent.py --url https://ejemplo.com --fix /ruta/del/proyecto

# Combinación completa: analizar, exportar informe y aplicar correcciones
python agent.py --url https://ejemplo.com --level AA --discipline todos --export docx --fix /ruta/del/proyecto
```

**Opciones disponibles:**

| Flag | Valores | Por defecto | Descripción |
|---|---|---|---|
| `--url` | URL | — | Página web a analizar |
| `--file` | ruta | — | Archivo local a analizar |
| `--discipline` | `ux` `ui` `desarrollo` `todos` | `todos` | Nivel disciplinar |
| `--level` | `A` `AA` `AAA` | `AA` | Nivel de conformidad WCAG objetivo |
| `--mode` | `análisis` `auditoría` `evaluación` `corrección` `handoff` | `análisis` | Modo de operación |
| `--export` | `pdf` `docx` | — | Exportar informe |
| `--fix` | ruta | — | Ruta del proyecto para corrección activa |

**Comandos en modo interactivo:**

| Comando | Acción |
|---|---|
| `exportar pdf` | Exporta el último informe a PDF |
| `exportar docx` | Exporta el último informe a DOCX |
| `corregir /ruta` | Activa corrección activa sobre el proyecto |
| `salir` | Termina la sesión |

---

## Construir tu propio agente desde la skill

La skill (`skills/wcag-accessibility/`) es el artefacto portable. Puedes usarla como base para construir tu propio agente en cualquier stack.

### Con la API de Anthropic (Python)

```python
from anthropic import Anthropic
from system_prompt import build_system_prompt

client = Anthropic()

# Construir el system prompt desde la skill
system = build_system_prompt(
    discipline="desarrollo",  # ux | ui | desarrollo | todos
    wcag_level="AA"           # A | AA | AAA
)

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    system=system,
    messages=[{
        "role": "user",
        "content": "Analiza este componente para accesibilidad: <button onclick='x()'>✕</button>"
    }]
)

print(response.content[0].text)
```

### Usando el SKILL.md directamente como system prompt

El archivo `skills/wcag-accessibility/SKILL.md` contiene la configuración por defecto, los modos de operación y las referencias a cargar. Puedes pegarlo directamente como system prompt en cualquier interfaz o API compatible con Claude.

### Con Claude Code, Codex, Copilot o Antigravity

Instala la skill con `gh skill`, `npx skills` o como plugin (ver [Instalación de la skill](#instalación-de-la-skill)). No hace falta el agente CLI.

---

## Marco legal

| Normativa | Ámbito | Nivel requerido |
|---|---|---|
| Real Decreto 1112/2018 | Sector público español | WCAG 2.1 AA |
| EN 301 549 | Europa — productos y servicios TIC | WCAG 2.1 AA |
| European Accessibility Act (EAA) | Sector privado europeo (desde junio 2025) | WCAG 2.1 AA |
| ADA / Section 508 | Sector público EE.UU. | WCAG 2.0 AA |
| ISO/IEC 40500:2012 | Internacional | WCAG 2.0 |

---

## Variables de entorno

| Variable | Requerida | Descripción |
|---|---|---|
| `ANTHROPIC_API_KEY` | Sí | API key de Anthropic |
| `WCAG_MODEL` | No | Modelo a usar. Por defecto: `claude-sonnet-4-6` |
| `WCAG_OUTPUT_DIR` | No | Directorio de outputs. Por defecto: `./outputs` |

---

## Contribuir

Las contribuciones son bienvenidas. Tras modificar la skill, ejecuta `make skill-package` y `make test`. Áreas de mayor interés:

- Mejoras a los archivos en `skills/wcag-accessibility/references/` (siempre ancladas en W3C WAI)
- Soporte para nuevos tipos de archivo (Astro, Svelte, Angular)
- Integración con Figma REST API para análisis de UI directamente desde diseño
- Cobertura completa de WCAG 2.2 en las guías de referencia
- Traducciones del skill a otros idiomas

Abre un issue antes de hacer un PR para coordinar el enfoque.

---

## Licencia

MIT — libre para usar, modificar y distribuir.

El conocimiento WCAG proviene de [W3C WAI](https://www.w3.org/WAI/) bajo [W3C Document License](https://www.w3.org/copyright/document-license/).

---

*Construido con [Anthropic API](https://www.anthropic.com/api) · Conocimiento basado en [W3C WAI WCAG 2.1](https://www.w3.org/TR/WCAG21/)*
