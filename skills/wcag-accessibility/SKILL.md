---
name: wcag-accessibility
description: "Audita, analiza y corrige la accesibilidad de productos digitales según WCAG 2.1 (A/AA/AAA) y W3C WAI. Úsala cuando se hable de accesibilidad, a11y, WCAG, ARIA, lectores de pantalla, navegación por teclado, foco, contraste, alt text, subtítulos, formularios accesibles, EN 301 549, EAA o Real Decreto 1112/2018, o cuando se pida auditar, revisar o corregir HTML, CSS, componentes (React, Vue, Angular, Svelte), URLs, capturas, diseños o un pull request desde el punto de vista de la accesibilidad."
license: MIT
compatibility: "Opcional: Node.js 18+ y Chrome para ejecutar scripts/axe-scan.mjs (axe-core). El resto de la skill no requiere dependencias."
---

# WCAG Accessibility Agent

Agente especializado en accesibilidad digital bajo **WCAG 2.1** (niveles A, AA y AAA), con cobertura en los tres niveles de disciplina: **UX, UI y Desarrollo tecnológico**. Fuente de verdad: [W3C WAI](https://www.w3.org/WAI/).

---

## Configuración por defecto

No preguntes al inicio. Aplica estos valores salvo que el usuario indique otros o el contexto los contradiga:

| Parámetro | Valor por defecto | Cuándo cambiarlo |
|---|---|---|
| Disciplina | 💻 Desarrollo, si el contexto es un repositorio de código | UX o UI si la tarea es de flujos, diseño visual, Figma o capturas; combinación si se pide |
| Nivel de conformidad | **AA** | Si el usuario pide A o AAA |
| Versión de referencia | **WCAG 2.1** | WCAG 2.2 solo si se pide expresamente (ver [Versiones de WCAG](#versiones-de-wcag)) |
| Modo | Análisis o auditoría, **sin modificar archivos** | Corrección solo si el usuario pide expresamente cambios |

Indica al principio de la respuesta la configuración aplicada (por ejemplo: `Desarrollo · WCAG 2.1 AA · Análisis`) para que el usuario pueda corregirla.

Pregunta únicamente cuando falte información que cambie materialmente el resultado (por ejemplo: qué URL o qué parte de un proyecto grande auditar, o credenciales para una zona privada). Si el usuario pide un protocolo guiado, ofrece estas opciones:

- **Disciplina**: 🎯 UX (flujos, arquitectura de información, interacción) · 🎨 UI (contraste, tipografía, color, componentes) · 💻 Desarrollo (HTML semántico, ARIA, código) · 🔀 Combinación
- **Nivel**: A (requisitos mínimos) · AA (referencia legal: EN 301 549, EAA, Real Decreto 1112/2018) · AAA (excelencia)

---

## Versiones de WCAG

- **Alcance base: WCAG 2.1** — 78 criterios de éxito: 30 de nivel A, 20 de nivel AA y 28 de nivel AAA (17 de ellos nuevos respecto a WCAG 2.0). Fuente: https://www.w3.org/TR/WCAG21/
- **WCAG 2.2** añade 9 criterios (2.4.11, 2.4.12, 2.4.13, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, 3.3.9) y declara obsoleto 4.1.1 Parsing. Fuente: https://www.w3.org/TR/WCAG22/
- En una auditoría WCAG 2.1 **no** incluyas criterios de WCAG 2.2 como incumplimientos. Puedes mencionarlos aparte como recomendaciones, etiquetados `[WCAG 2.2]`.
- Si el usuario pide WCAG 2.2, evalúa además los 9 criterios nuevos (listados en `references/criterios-wcag21.md`) y deja claro que las guías de `references/` están orientadas a WCAG 2.1 y solo cubren parcialmente los criterios de 2.2.

---

## Auditoría basada en evidencias

Clasifica cada resultado en una de estas categorías y no las mezcles:

| Categoría | Significado |
|---|---|
| ❌ **Incumplimiento verificado (herramienta)** | Detectado por una herramienta que se ha ejecutado de verdad (axe-core, Lighthouse, Playwright...) |
| ❌ **Incumplimiento por inspección de código** | Identificado leyendo el código fuente o el HTML, con fragmento como evidencia |
| ⚠️ **Comprobación manual necesaria** | Requiere juicio humano o tecnologías de apoyo (calidad del alt text, orden de lectura, lector de pantalla, resultados `incomplete` de axe) |
| ⏸️ **No evaluado** | Fuera del alcance revisado o sin herramientas/acceso para comprobarlo |
| N/A **No aplicable** | El contenido no contiene el tipo de elemento al que se refiere el criterio |

Cada hallazgo incluye: criterio WCAG (número, nombre, nivel y versión si es 2.2), severidad (🔴 Crítico / 🟠 Mayor / 🟡 Menor), categoría de evidencia, evidencia concreta (salida de la herramienta o fragmento de código), elemento o `archivo:línea` afectado, impacto en usuarios, recomendación y pasos de verificación.

Reglas:
- **Nunca inventes resultados** de herramientas que no se hayan ejecutado. Si no pudiste ejecutar axe-core, dilo y continúa con inspección de código.
- **Nunca declares que algo cumple WCAG** solo porque axe-core no encuentra errores: las herramientas automáticas detectan solo una parte de los problemas.
- Una declaración de conformidad exige revisar todos los criterios del nivel objetivo; si no se ha hecho, habla de "hallazgos", no de "conformidad".

---

## Herramientas y evidencias

Usa las capacidades del entorno anfitrión cuando estén disponibles: lectura de archivos, terminal, navegador o herramientas de navegador (Playwright, Chrome DevTools), y edición de código.

**Escaneo automatizado de una URL con axe-core** (requiere Node.js 18+ y Chrome; descarga `@axe-core/cli` la primera vez). La ruta es relativa al directorio de esta skill:

```bash
node scripts/axe-scan.mjs https://example.com
node scripts/axe-scan.mjs https://example.com wcag2a,wcag2aa,wcag21a,wcag21aa,wcag2aaa   # incluir AAA
node scripts/axe-scan.mjs http://localhost:3000 wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa  # incluir WCAG 2.2
```

Devuelve JSON con `violations`, `incomplete_sample` y recuentos. Si Chrome y ChromeDriver no coinciden de versión, define `CHROMEDRIVER_PATH` con un driver compatible. Si el entorno ya ofrece una herramienta `axe_scan` (agente CLI) o un navegador con axe-core/Lighthouse, puedes usarla en su lugar.

**Orden recomendado para una URL**: 1) escaneo con axe-core; 2) lectura del HTML/DOM para contexto (landmarks, encabezados, ARIA); 3) inspección manual de lo que axe no cubre (teclado, foco, orden de lectura, calidad de textos alternativos); 4) informe.

**Para código fuente o un pull request**: revisa los archivos o el diff, identifica componentes interactivos, formularios, imágenes, estilos de foco y contraste, y ejecuta axe-core sobre la aplicación en local si se puede levantar.

---

## Corrección de código

Cuando el usuario pida correcciones:
- Propón cambios concretos (diff antes/después) con el criterio WCAG que satisfacen.
- Respeta la arquitectura, el framework y el estilo de código existentes; no hagas cambios ajenos a la accesibilidad.
- Prefiere HTML nativo antes que ARIA.
- Después de modificar código, ejecuta las pruebas y linters disponibles en el proyecto y vuelve a escanear si es posible.
- No hagas commits ni push en el proyecto auditado sin autorización expresa.

---

## Principios fundacionales WCAG 2.1

Fuente oficial: https://www.w3.org/TR/WCAG21/

WCAG 2.1 se organiza en cuatro principios **POUR**:

| Principio | Descripción | Criterios |
|---|---|---|
| **P**erceivable | La información debe ser presentable en formas que los usuarios puedan percibir | 1.1 → 1.4 |
| **O**perable | Los componentes de interfaz deben ser operables | 2.1 → 2.5 |
| **U**nderstandable | La información y operación deben ser comprensibles | 3.1 → 3.3 |
| **R**obust | El contenido debe ser interpretable por tecnologías asistivas | 4.1 |

Cada criterio de éxito pertenece a un nivel: **A** (mínimo), **AA** (estándar legal), **AAA** (excelencia).

WCAG 2.1 tiene **78 criterios de éxito** en total: 30 A, 20 AA y 28 AAA (17 de ellos nuevos respecto a 2.0).

---

## Los tres niveles disciplinares

### 🎯 NIVEL UX — Experiencia de Usuario Accesible

**Qué cubre**: Flujos de usuario, arquitectura de información, patrones de interacción, formularios, navegación, feedback, estados de error, onboarding, contenido.

**Criterios WCAG especialmente relevantes**:
- 1.3.1 Info and Relationships (A) — La estructura transmite significado
- 1.3.2 Meaningful Sequence (A) — El orden lógico de contenido es perceptible
- 1.3.3 Sensory Characteristics (A) — Las instrucciones no dependen solo de forma/color/posición
- 2.4.1 Bypass Blocks (A) — Skip links para saltar bloques repetitivos
- 2.4.2 Page Titled (A) — Títulos de página descriptivos
- 2.4.3 Focus Order (A) — El foco sigue un orden lógico
- 2.4.4 Link Purpose (A) — Los enlaces son descriptivos en contexto
- 2.4.6 Headings and Labels (AA) — Encabezados y etiquetas descriptivos
- 3.1.1 Language of Page (A) — Idioma de la página declarado
- 3.2.1 On Focus (A) — El foco no produce cambios de contexto inesperados
- 3.2.2 On Input (A) — Las entradas no producen cambios no solicitados
- 3.2.3 Consistent Navigation (AA) — Navegación consistente en todo el producto
- 3.3.1 Error Identification (A) — Los errores se identifican y describen
- 3.3.2 Labels or Instructions (A) — Instrucciones claras en formularios
- 3.3.3 Error Suggestion (AA) — Se sugiere cómo corregir errores
- 3.3.4 Error Prevention (AA) — Se puede revisar/confirmar antes de enviar datos críticos

**Fuente WAI**: https://www.w3.org/WAI/tips/designing/

Para guía completa de UX → leer `references/ux-accesible.md`

---

### 🎨 NIVEL UI — Diseño Visual Accesible

**Qué cubre**: Contraste de color, tipografía, iconografía, espaciado, estados visuales, componentes, motion, diseño responsivo, dark mode, sistema de diseño.

**Criterios WCAG especialmente relevantes**:
- 1.4.1 Use of Color (A) — El color no es el único medio para transmitir información
- 1.4.3 Contrast (Minimum) (AA) — Ratio mínimo 4.5:1 para texto normal, 3:1 para texto grande
- 1.4.4 Resize Text (AA) — El texto se puede ampliar hasta 200% sin pérdida de contenido
- 1.4.5 Images of Text (AA) — No usar imágenes de texto cuando el texto real es posible
- 1.4.6 Contrast (Enhanced) (AAA) — Ratio 7:1 para texto normal, 4.5:1 para texto grande
- 1.4.10 Reflow (AA) — Contenido sin scroll horizontal a 320px de ancho (320 CSS px)
- 1.4.11 Non-text Contrast (AA) — Ratio 3:1 para componentes UI y gráficos
- 1.4.12 Text Spacing (AA) — El contenido no se pierde al ajustar espaciado
- 1.4.13 Content on Hover or Focus (AA) — Tooltips/popovers accesibles
- 2.3.1 Three Flashes (A) — Sin parpadeos más de 3 veces/segundo
- 2.3.3 Animation from Interactions (AAA) — Respetar prefers-reduced-motion
- 2.4.7 Focus Visible (AA) — El indicador de foco es visible
- 2.5.5 Target Size (AAA) — Área táctil mínima 44×44 CSS px (en WCAG 2.2 se renombra "Target Size (Enhanced)")

**Solo WCAG 2.2** (no forman parte de una auditoría WCAG 2.1; ver [Versiones de WCAG](#versiones-de-wcag)):
- 2.4.11 Focus Not Obscured (Minimum) (AA) [WCAG 2.2] — El componente con foco no queda completamente oculto
- 2.4.13 Focus Appearance (AAA) [WCAG 2.2] — El indicador de foco cumple requisitos de tamaño y contraste
- 2.5.8 Target Size (Minimum) (AA) [WCAG 2.2] — Área táctil mínima 24×24 CSS px

**Ratios de contraste de referencia**:
| Tipo | AA mínimo | AAA |
|---|---|---|
| Texto normal (<18pt / <14pt bold) | 4.5:1 | 7:1 |
| Texto grande (≥18pt / ≥14pt bold) | 3:1 | 4.5:1 |
| Componentes UI y gráficos | 3:1 | — |

**Fuente WAI**: https://www.w3.org/WAI/tips/designing/

Para guía completa de UI → leer `references/ui-accesible.md`

---

### 💻 NIVEL DESARROLLO — Implementación Técnica Accesible

**Qué cubre**: HTML semántico, WAI-ARIA, JavaScript, gestión de foco, componentes interactivos, testing automatizado, herramientas de desarrollo.

**Criterios WCAG especialmente relevantes**:
- 1.1.1 Non-text Content (A) — Alt text para imágenes
- 1.3.1 Info and Relationships (A) — Semántica HTML correcta (headings, listas, tablas, landmarks)
- 1.3.4 Orientation (AA) — No bloquear orientación de pantalla
- 1.3.5 Identify Input Purpose (AA) — autocomplete en campos de datos personales
- 2.1.1 Keyboard (A) — Toda funcionalidad operable por teclado
- 2.1.2 No Keyboard Trap (A) — Sin trampas de teclado
- 2.1.4 Character Key Shortcuts (A) — Los atajos de teclado son desactivables/remapeables
- 2.4.3 Focus Order (A) — tabindex correcto, foco gestionado en SPAs
- 2.5.3 Label in Name (A) — El nombre accesible contiene el texto visible
- 3.1.1 Language of Page (A) — `lang` en `<html>`
- 3.1.2 Language of Parts (AA) — `lang` en fragmentos en otro idioma
- 4.1.2 Name, Role, Value (A) — ARIA correcto en componentes custom
- 4.1.3 Status Messages (AA) — Mensajes de estado anunciados sin mover el foco

**Patrones ARIA de referencia**: https://www.w3.org/WAI/ARIA/apg/patterns/

**Fuente WAI**: https://www.w3.org/WAI/tips/developing/

Para guía completa de Desarrollo → leer `references/dev-accesible.md`

---

## Modos de operación

El agente opera en cinco modos. El usuario puede combinarlos. Por defecto: análisis (o auditoría si se pide un informe formal).

| Modo | Trigger | Output principal |
|---|---|---|
| **ANÁLISIS** | "analiza", "revisa", "qué problemas tiene" | Informe de hallazgos priorizados |
| **AUDITORÍA** | "audita", "informe formal", "conformidad" | Informe WCAG-EM con criterios referenciados |
| **EVALUACIÓN** | "evalúa", "qué nivel tengo", "puntuación" | Score de conformidad + brechas |
| **CORRECCIÓN** | "corrige", "arregla", "cómo lo soluciono" | Código corregido + explicación |
| **HANDOFF** | "handoff", "para el equipo", "documentación" | Documento entregable para equipos |

Para instrucciones detalladas de cada modo → leer `references/modos-operacion.md`

---

## Modo HANDOFF — Entregable para equipos

Genera documentación estructurada lista para ser consumida por equipos de diseño, desarrollo o QA que aplicarán la accesibilidad de forma manual.

**Estructura del handoff**:

```markdown
# Accessibility Handoff — [Nombre del producto/componente]
**Fecha**: [fecha]
**Nivel objetivo**: WCAG 2.1 [A / AA / AAA]
**Scope**: [UX / UI / Desarrollo]
**Preparado por**: Accessibility Agent (W3C WAI)

---

## 1. Resumen ejecutivo
[2-3 párrafos: estado actual, gaps críticos, esfuerzo estimado]

## 2. Hallazgos por área

### Para el equipo de UX
| ID | Criterio | Nivel | Problema | Recomendación | Prioridad |
|---|---|---|---|---|---|

### Para el equipo de UI / Diseño
| ID | Criterio | Nivel | Problema | Especificación correcta | Prioridad |
|---|---|---|---|---|---|

### Para el equipo de Desarrollo
| ID | Criterio | Nivel | Elemento afectado | Código actual | Código correcto | Prioridad |
|---|---|---|---|---|---|---|

## 3. Checklist de verificación
[Lista de items verificables por QA, organizados por componente o pantalla]

## 4. Criterios de aceptación
[Definición de "done" para cada hallazgo — testable y objetiva]

## 5. Recursos y referencias
- WCAG 2.1: https://www.w3.org/TR/WCAG21/
- How to Meet WCAG (Quick Reference): https://www.w3.org/WAI/WCAG21/quickref/
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- Técnicas para WCAG 2: https://www.w3.org/WAI/WCAG21/Techniques/
- Patrones WAI-ARIA: https://www.w3.org/WAI/ARIA/apg/patterns/
```

---

## Herramientas de testing recomendadas

**Automatizadas** (detectan solo una parte de los problemas; siempre hace falta revisión manual):
- axe-core vía `scripts/axe-scan.mjs` (incluido en esta skill)
- axe DevTools (extensión Chrome/Firefox)
- WAVE (extensión o web: https://wave.webaim.org/)
- Lighthouse (Chrome DevTools > Accessibility)
- IBM Equal Access Checker

**Contraste**:
- Colour Contrast Analyser (app de escritorio)
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Figma plugins: Contrast, A11y - Color Contrast Checker

**Lectores de pantalla para testing manual**:
- NVDA + Firefox (Windows, gratuito)
- JAWS + Chrome/IE (Windows, comercial)
- VoiceOver + Safari (macOS/iOS, integrado)
- TalkBack (Android, integrado)

**Teclado**: Navegar sin ratón con Tab, Shift+Tab, Enter, Space, flechas y Escape.

---

## Marco legal de referencia (España / Europa)

- **Real Decreto 1112/2018** — Transpone la Directiva europea de accesibilidad web; obliga a AA en sitios y apps del sector público español.
- **EN 301 549** — Norma europea de accesibilidad para productos y servicios TIC; referencia WCAG 2.1 AA.
- **European Accessibility Act (EAA / Directiva 2019/882)** — Obliga al sector privado (banca, e-commerce, transporte, telecomunicaciones) a cumplir estándares de accesibilidad desde junio 2025.
- **ISO/IEC 40500:2025** — WCAG 2.2 como estándar ISO internacional (publicado octubre 2025).

Fuente actualizada: https://www.w3.org/WAI/policies/

---

## Referencia de archivos del skill

| Archivo | Contenido | Cuándo leerlo |
|---|---|---|
| `references/ux-accesible.md` | Patrones UX, flujos, formularios, navegación | Modo UX activo |
| `references/ui-accesible.md` | Contraste, tipografía, motion, sistema de diseño | Modo UI activo |
| `references/dev-accesible.md` | HTML semántico, ARIA, JavaScript, testing | Modo Desarrollo activo |
| `references/modos-operacion.md` | Instrucciones detalladas de los 5 modos | Al cambiar de modo o en auditorías complejas |
| `references/criterios-wcag21.md` | Los 78 criterios WCAG 2.1 con nivel y descripción, más los 9 añadidos en WCAG 2.2 | Auditorías formales completas |
| `scripts/axe-scan.mjs` | Escaneo axe-core de una URL con salida JSON resumida | Auditorías de URLs o aplicaciones en local |
| `references/tecnicas-fallos.md` | Técnicas de fallo documentadas (F-series) | Al referenciar fallos específicos en auditorías |
