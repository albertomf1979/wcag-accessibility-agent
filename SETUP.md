# WCAG Accessibility Agent — Referencia técnica

> Referencia técnica detallada para desarrolladores. Para las instrucciones de uso generales, consulta [README.md](README.md).

**Fuente de conocimiento**: [W3C Web Accessibility Initiative (WAI)](https://www.w3.org/WAI/)  
**Estándar base**: [WCAG 2.1](https://www.w3.org/TR/WCAG21/) — niveles A, AA y AAA  
**Ámbito**: UX · UI · Desarrollo tecnológico

---

## Qué hace este agente

El agente opera en cinco modos:

| Modo | Descripción |
|---|---|
| **Análisis** | Identifica y prioriza barreras de accesibilidad |
| **Auditoría** | Informe formal de conformidad WCAG con criterios referenciados |
| **Evaluación** | Score de conformidad + brechas para alcanzar el nivel objetivo |
| **Corrección** | Código corregido con explicación del criterio satisfecho |
| **Handoff** | Documento entregable estructurado por roles para equipos |

En modo interactivo, el agente CLI pregunta antes de actuar:
1. Nivel disciplinar: **UX / UI / Desarrollo** (o combinación)
2. Nivel de conformidad objetivo: **A / AA / AAA**

La skill portable (`skills/wcag-accessibility/`), en cambio, aplica valores por defecto (Desarrollo · WCAG 2.1 AA · análisis sin modificar archivos) y solo pregunta cuando falta información relevante.

---

## Arquitectura

| Capa | Dónde | Función |
|---|---|---|
| Skill y referencias | `skills/wcag-accessibility/SKILL.md`, `references/` | Instrucciones y conocimiento WCAG (fuente de verdad) |
| Herramientas deterministas | `skills/wcag-accessibility/scripts/axe-scan.mjs` | Evidencias automáticas (axe-core), sin modelo de IA |
| Agente anfitrión | Claude Code, Codex, Copilot, Claude.ai... | Lee la skill, ejecuta herramientas, analiza y propone cambios |
| CLI Python independiente | `agent.py`, `system_prompt.py`, `tools.py`, `exporters/` | Usa la API de Anthropic; carga la misma skill como system prompt y el mismo script de axe-core |

Las instrucciones de instalación de la skill (`gh skill`, plugin de Claude Code, instalación manual y Claude.ai) están en el [README](README.md#instalación-de-la-skill).

---

## Requisitos

- Python 3.11 o superior
- Node.js 18 o superior
- Una [API key de Anthropic](https://console.anthropic.com/)
- pip

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/albertomf1979/wcag-accessibility-agent.git
cd wcag-accessibility-agent

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias Python
pip install -r requirements.txt

# 4. Pre-instalar axe-core CLI (descarga Chromium la primera vez, ~120 MB)
npx -y @axe-core/cli --version

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env y añadir tu ANTHROPIC_API_KEY
```

---

## axe-core: escaneo con DOM renderizado

El agente integra [@axe-core/cli](https://github.com/dequelabs/axe-core-npm/tree/develop/packages/cli) para lanzar un escaneo con Chrome headless antes de cada análisis de URL:

- **DOM renderizado**: axe evalúa el DOM con JS y CSS ejecutados, no el HTML crudo.
- **ARIA dinámico**: aria-expanded, aria-hidden y otros atributos establecidos por JavaScript se evalúan en su estado real.
- **Límites**: las herramientas automáticas solo detectan una parte de los fallos WCAG. Cero violaciones no implica conformidad; los resultados `incomplete` requieren revisión manual.

La lógica vive en un único script, `skills/wcag-accessibility/scripts/axe-scan.mjs`, que usan tanto la herramienta `axe_scan` del CLI como los agentes que instalan la skill. Por defecto comprueba las reglas `wcag2a,wcag2aa,wcag21a,wcag21aa` (WCAG 2.1 A + AA).

El agente llama a `axe_scan` primero (siempre), luego a `fetch_url` para obtener contexto HTML y producir el informe.

Si `node` no está disponible, el agente avisa y usa `fetch_url` como fallback.

### Verificar que el escaneo funciona

```bash
node skills/wcag-accessibility/scripts/axe-scan.mjs https://example.com
```

Si aparece un error de versión de ChromeDriver (`This version of ChromeDriver only supports Chrome version N`), instala un driver compatible con tu Chrome y exporta su ruta:

```bash
npx @puppeteer/browsers install chromedriver@<versión-mayor-de-chrome>
export CHROMEDRIVER_PATH=/ruta/al/chromedriver
```

---

## Uso

```bash
# Modo interactivo (recomendado para empezar)
python agent.py

# Analizar una URL directamente
python agent.py --url https://ejemplo.com

# Analizar un archivo local
python agent.py --file ruta/al/archivo.html

# Analizar y exportar informe en PDF
python agent.py --url https://ejemplo.com --export pdf

# Analizar y exportar informe en DOCX (handoff para equipos)
python agent.py --file componente.html --export docx

# Analizar Y aplicar correcciones directamente sobre el proyecto
python agent.py --url https://ejemplo.com --fix /ruta/a/tu/proyecto

# Corrección con exportación del informe previo
python agent.py --file index.html --export docx --fix /ruta/a/tu/proyecto
```

### Flujo de corrección activa

Tras entregar cualquier informe, el agente siempre ofrece aplicar las correcciones directamente:

```
╔══════════════════════════════════════════════════════╗
║  Corrección activa disponible                        ║
║                                                      ║
║  ¿Quieres que corrija los errores directamente?      ║
║                                                      ║
║  Vuelve a ejecutar añadiendo:                        ║
║  --fix /ruta/de/tu/proyecto                          ║
║                                                      ║
║  O en modo interactivo escribe:                      ║
║  corregir /ruta/de/tu/proyecto                       ║
╚══════════════════════════════════════════════════════╝
```

Cuando se activa la corrección, el agente:
1. Explora la estructura del proyecto con `list_directory`
2. Lee cada archivo afectado antes de modificarlo
3. Muestra el diff exacto del cambio con el criterio WCAG que satisface
4. Pide confirmación antes de escribir
5. Crea una copia de seguridad `.bak` automática de cada archivo modificado

> La corrección activa requiere acceso al código fuente. El agente nunca escribe
> sin confirmación explícita y siempre puede revertirse desde los `.bak`.

### Ejemplo de sesión

```
$ python agent.py --url https://ejemplo.com

╔══════════════════════════════════════════════╗
║       WCAG Accessibility Agent v1.0          ║
║       Basado en W3C WAI WCAG 2.1             ║
╚══════════════════════════════════════════════╝

Antes de comenzar, necesito dos confirmaciones:

1. ¿Qué nivel disciplinar quieres trabajar?
   [1] UX — Flujos, navegación, formularios, interacción
   [2] UI — Contraste, tipografía, color, componentes visuales
   [3] Desarrollo — HTML semántico, ARIA, código, testing
   [4] Combinación (especifica cuáles)

Tu elección: 3

2. ¿Cuál es tu objetivo de conformidad WCAG?
   [A] Nivel A — Requisitos mínimos
   [AA] Nivel AA — Estándar legal (recomendado)
   [AAA] Nivel AAA — Excelencia

Tu elección: AA

→ Analizando https://ejemplo.com en modo Desarrollo · Objetivo: WCAG 2.1 AA...
```

---

## Estructura del proyecto

```
wcag-accessibility-agent/
├── .claude-plugin/
│   ├── plugin.json             # Manifiesto del plugin de Claude Code (wcag)
│   └── marketplace.json        # Marketplace (wcag-accessibility) que apunta a este repositorio
├── skills/
│   └── wcag-accessibility/     # Agent Skill portable (gh skill, plugin, Claude.ai)
│       ├── SKILL.md            # Skill de accesibilidad (núcleo del agente)
│       ├── references/         # Base de conocimiento WCAG (fuente: W3C WAI)
│       │   ├── ux-accesible.md
│       │   ├── ui-accesible.md
│       │   ├── dev-accesible.md
│       │   ├── modos-operacion.md
│       │   ├── criterios-wcag21.md
│       │   └── tecnicas-fallos.md
│       └── scripts/
│           └── axe-scan.mjs    # Escaneo axe-core compartido por la skill y el CLI
├── agent.py                    # Punto de entrada — bucle agéntico principal
├── system_prompt.py            # Construye el system prompt desde el skill
├── tools.py                    # Herramientas del agente (fetch, parse, export)
├── exporters/
│   ├── pdf.py                  # Exportación a PDF
│   └── docx.py                 # Exportación a DOCX (handoff)
├── tests/                      # Validaciones locales (sin API key): make test
├── outputs/                    # Informes generados (no se sube a Git)
├── wcag-accessibility.skill    # Paquete para Claude.ai (make skill-package)
├── Makefile
├── requirements.txt
├── .env.example
└── README.md
```

---

## Cómo construir tu propio agente desde el skill

La carpeta `skills/wcag-accessibility/` (`SKILL.md`, `references/` y `scripts/`) es el **conocimiento portátil** de este agente. Puedes usarla para construir tu propio agente en cualquier stack:

### Opción 1: Usar el skill en Claude.ai

1. Ve a **Settings → Skills** en claude.ai
2. Sube el archivo `wcag-accessibility.skill`
3. Claude lo usará automáticamente cuando detecte preguntas de accesibilidad

El paquete se regenera desde `skills/wcag-accessibility/` con `make skill-package` (requiere `zip`). `make test` comprueba que el paquete versionado coincide con la skill.

### Opción 2: Construir tu propio agente en Python

```python
from anthropic import Anthropic
from system_prompt import build_system_prompt

client = Anthropic()

# El system prompt incluye todo el conocimiento WCAG del skill
system = build_system_prompt(
    discipline="desarrollo",   # ux | ui | desarrollo | todos
    wcag_level="AA"            # A | AA | AAA
)

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    system=system,
    messages=[
        {"role": "user", "content": "Analiza este componente: <button onclick='...'>✕</button>"}
    ]
)
```

### Opción 3: Integrar como MCP server

El skill puede exponerse como un MCP server para que otros agentes lo consuman.
Ver rama `mcp-server` del repositorio para la implementación (pendiente de publicar).

### Opción 4: Desplegar interfaz web con Cloudflare

```bash
# Requiere cuenta Cloudflare y Wrangler CLI
npm install -g wrangler
wrangler login

# Desplegar Worker (backend)
cd cloudflare/worker
wrangler deploy

# Desplegar Pages (frontend)
cd cloudflare/pages
wrangler pages deploy
```

Ver `cloudflare/README.md` para instrucciones detalladas (carpeta pendiente de implementar).

---

## Marco legal de referencia

| Normativa | Ámbito | Nivel requerido |
|---|---|---|
| Real Decreto 1112/2018 | Sector público español | WCAG 2.1 AA |
| EN 301 549 | Europa (ICT products) | WCAG 2.1 AA |
| European Accessibility Act (EAA) | Sector privado europeo (desde jun 2025) | WCAG 2.1 AA |
| ADA (Section 508) | Sector público EE.UU. | WCAG 2.0 AA |
| ISO/IEC 40500:2012 | Internacional | WCAG 2.0 |

---

## Contribuir

Las contribuciones son bienvenidas, especialmente:
- Mejoras a las referencias WCAG en `skills/wcag-accessibility/references/`
- Nuevos modos de operación
- Integraciones con herramientas de diseño (Figma, Storybook)
- Traducciones del skill a otros idiomas

Por favor, abre un issue antes de hacer un PR para coordinar.

### Validaciones locales

```bash
make test                       # Skill, manifiestos, paquete y carga del system prompt (sin API key)
gh skill publish --dry-run      # Validación de la skill con GitHub CLI
claude plugin validate .        # Validación del plugin y del marketplace
```

---

## Licencia

MIT — Puedes usar, modificar y distribuir libremente.  
El conocimiento WCAG proviene de [W3C WAI](https://www.w3.org/WAI/) bajo licencia [W3C Document License](https://www.w3.org/copyright/document-license/).

---

## Créditos

Desarrollado con base en el estándar [WCAG 2.1 del W3C](https://www.w3.org/TR/WCAG21/).  
Construido con la [API de Anthropic](https://www.anthropic.com/api) y el modelo Claude.
