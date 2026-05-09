# WCAG Accessibility Agent

> Agente de accesibilidad digital basado en WCAG 2.1, construido sobre la API de Anthropic.  
> Audita, analiza, evalúa y corrige productos digitales. Genera informes PDF/DOCX y handoffs para equipos.

**Fuente de conocimiento**: [W3C Web Accessibility Initiative (WAI)](https://www.w3.org/WAI/)  
**Estándar**: [WCAG 2.1](https://www.w3.org/TR/WCAG21/) — niveles A, AA y AAA  
**Ámbito**: UX · UI · Desarrollo tecnológico  
**Modelo**: Claude (Anthropic API)

---

## Contenido

- [Qué es este repositorio](#qué-es-este-repositorio)
- [Opción A — Usar solo la Skill en Claude.ai](#opción-a--usar-solo-la-skill-en-claudeai)
- [Opción B — Instalar el agente CLI completo](#opción-b--instalar-el-agente-cli-completo)
- [Capacidades del agente](#capacidades-del-agente)
- [Referencia de comandos](#referencia-de-comandos)
- [Construir tu propio agente desde la skill](#construir-tu-propio-agente-desde-la-skill)
- [Marco legal](#marco-legal)
- [Contribuir](#contribuir)

---

## Qué es este repositorio

Este repositorio contiene dos artefactos independientes que puedes usar por separado o juntos:

**1. La Skill** (`SKILL.md` + `references/`)  
Base de conocimiento WCAG 2.1 estructurada para agentes de IA. Cubre los 78 criterios de éxito, técnicas de fallo, patrones UX/UI/desarrollo y marcos legales. Puede instalarse directamente en Claude.ai o usarse como system prompt en cualquier agente basado en la API de Anthropic.

**2. El Agente CLI** (`agent.py` y el resto del código)  
Implementación completa del agente con bucle de tool use, análisis de URLs y archivos, exportación de informes y corrección activa de código fuente.

---

## Opción A — Usar solo la Skill en Claude.ai

La forma más rápida. No requiere código ni API key propia.

**1.** Descarga el archivo `wcag-accessibility.skill` desde la sección [Releases](../../releases) de este repositorio.

**2.** En [claude.ai](https://claude.ai), ve a **Settings → Skills**.

**3.** Haz clic en **Upload skill** y selecciona el archivo `.skill`.

**4.** A partir de ese momento, Claude activará automáticamente el conocimiento WCAG cuando detecte preguntas relacionadas con accesibilidad.

**Qué puedes hacer desde Claude.ai con la skill instalada:**
- Pegar código HTML/CSS/JS y pedir un análisis de accesibilidad
- Pedir auditorías formales con referencia a criterios WCAG
- Solicitar correcciones de código con explicación del criterio que se satisface
- Generar checklists y documentación de handoff para tu equipo
- Consultar cualquier criterio WCAG 2.1 con contexto de implementación

---

## Opción B — Instalar el agente CLI completo

Para uso avanzado: análisis automatizado de URLs, procesamiento de archivos, exportación PDF/DOCX y corrección directa sobre el código fuente del proyecto.

### Requisitos

- Python 3.11 o superior
- Node.js 18 o superior (`node --version` para comprobar)
- Una [API key de Anthropic](https://console.anthropic.com/)
- pip

> **¿Por qué Node.js?** El agente usa [axe-core](https://github.com/dequelabs/axe-core) vía `axe-cli` para lanzar un escaneo completo con Chromium antes de cada análisis. Esto permite detectar todas las violaciones WCAG en el DOM renderizado (con JS y CSS ejecutados), no solo en el HTML estático.

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/wcag-accessibility-agent.git
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

### Protocolo de inicio obligatorio

Antes de actuar, el agente siempre pregunta:

1. **Nivel disciplinar**: UX / UI / Desarrollo / Todos
2. **Nivel de conformidad WCAG objetivo**: A / AA / AAA

Ningún análisis comienza sin estas dos confirmaciones. Pueden responderse en el diálogo interactivo o pasarse como flags en la CLI.

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
- Tabla de resultados: ✅ Pasa / ❌ Falla / ⚠️ Revisar manualmente / N/A
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

- **78 criterios de éxito** indexados (25 nivel A + 13 AA + 28 AAA + 12 nuevos en 2.1)
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

La skill (`SKILL.md` + `references/`) es el artefacto portable. Puedes usarla como base para construir tu propio agente en cualquier stack.

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

El archivo `SKILL.md` contiene el protocolo de inicio, los modos de operación y las referencias cargadas. Puedes pegarlo directamente como system prompt en cualquier interfaz o API compatible con Claude.

### Con Claude Code

Si usas Claude Code, coloca `CLAUDE.md` en la raíz del proyecto. Claude Code lo leerá automáticamente al arrancar y tendrá todo el contexto del agente sin necesidad de explicaciones adicionales.

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

Las contribuciones son bienvenidas. Áreas de mayor interés:

- Mejoras a los archivos en `references/` (siempre ancladas en W3C WAI)
- Soporte para nuevos tipos de archivo (Astro, Svelte, Angular)
- Integración con Figma REST API para análisis de UI directamente desde diseño
- Integración con axe-core para combinar análisis automatizado y razonamiento del agente
- Traducciones del skill a otros idiomas

Abre un issue antes de hacer un PR para coordinar el enfoque.

---

## Licencia

MIT — libre para usar, modificar y distribuir.

El conocimiento WCAG proviene de [W3C WAI](https://www.w3.org/WAI/) bajo [W3C Document License](https://www.w3.org/copyright/document-license/).

---

*Construido con [Anthropic API](https://www.anthropic.com/api) · Conocimiento basado en [W3C WAI WCAG 2.1](https://www.w3.org/TR/WCAG21/)*
