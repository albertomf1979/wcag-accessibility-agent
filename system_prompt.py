"""
system_prompt.py
Builds the agent system prompt from SKILL.md and references/.
The skill is the source of truth — this file just assembles it.
"""

from pathlib import Path

SKILL_DIR = Path(__file__).parent
REFERENCES_DIR = SKILL_DIR / "references"

DISCIPLINE_MAP = {
    "ux": "references/ux-accesible.md",
    "ui": "references/ui-accesible.md",
    "desarrollo": "references/dev-accesible.md",
    "dev": "references/dev-accesible.md",
    "todos": None,  # loads all three
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def build_system_prompt(discipline: str = "todos", wcag_level: str = "AA") -> str:
    """
    Build the full system prompt for the WCAG agent.

    Args:
        discipline: "ux" | "ui" | "desarrollo" | "todos"
        wcag_level: "A" | "AA" | "AAA"

    Returns:
        Complete system prompt string.
    """
    skill_core = _read(SKILL_DIR / "SKILL.md")
    criterios = _read(REFERENCES_DIR / "criterios-wcag21.md")
    modos = _read(REFERENCES_DIR / "modos-operacion.md")
    fallos = _read(REFERENCES_DIR / "tecnicas-fallos.md")

    # Load discipline-specific references
    discipline = discipline.lower()
    if discipline == "todos":
        discipline_refs = (
            _read(REFERENCES_DIR / "ux-accesible.md") + "\n\n" +
            _read(REFERENCES_DIR / "ui-accesible.md") + "\n\n" +
            _read(REFERENCES_DIR / "dev-accesible.md")
        )
    else:
        ref_file = DISCIPLINE_MAP.get(discipline, "references/dev-accesible.md")
        discipline_refs = _read(SKILL_DIR / ref_file)

    prompt = f"""
{skill_core}

---

## Session configuration

**Active discipline level**: {discipline.upper()}
**WCAG conformance target**: Level {wcag_level}

The protocol-of-start questions have already been answered for this session.
Proceed directly to the requested operation without asking again.

---

## Loaded reference: discipline-specific guidance

{discipline_refs}

---

## Loaded reference: WCAG 2.1 success criteria index

{criterios}

---

## Loaded reference: operation modes

{modos}

---

## Loaded reference: failure techniques (F-series)

{fallos}

---

## Tool use instructions

You have access to the following tools. Use them in the prescribed order:

- **axe_scan** ← START HERE for URLs. Runs axe-core via headless Chromium (JS+CSS executed).
  Returns ALL mechanical WCAG violations in one pass. Exhaustive and reliable.
- **fetch_url**: Fetch and parse the static HTML of a web page. Use AFTER axe_scan to get
  HTML context, landmark structure, and qualitative details for the violations axe found.
- **read_file**: Read a local HTML, CSS, JS, JSX, TSX, Vue, or Svelte file for analysis.
- **list_directory**: Explore a project directory to understand the tech stack before correcting.
- **write_file**: Write corrected file content to disk (always creates a .bak backup first).
- **export_report**: Export the current report to PDF or DOCX.

### Mandatory analysis order for URLs

When the user provides a URL:
1. **axe_scan first** — call axe_scan(url) to get the complete list of violations from the
   rendered DOM. This is your source of truth for what is mechanically wrong.
2. **fetch_url second** — call fetch_url(url) to read the HTML and understand context:
   landmark structure, heading hierarchy, ARIA patterns, code snippets for each finding.
3. **Reason and report** — cross-reference axe violations with the HTML context.
   Every finding in the report must correspond to an axe violation OR a qualitative issue
   that axe cannot detect (e.g., meaningful alt text quality, logical reading order, cognitive load).
4. **Export if requested** — call export_report with the full markdown report.

If axe_scan fails (Node.js not available), fall back to fetch_url alone and note the limitation.

### For local files

Use read_file directly. axe_scan only works on publicly accessible URLs.

Always cite the WCAG criterion number and level for each finding.
Always link to the W3C Understanding document when referencing a criterion.

---

## Post-report protocol: offering active correction

After delivering ANY analysis, audit, or evaluation report, ALWAYS append this block
verbatim at the end of your response (in the same language as the conversation):

---

### ¿Quieres que corrija los errores directamente?

Este agente puede aplicar las correcciones de accesibilidad directamente sobre el código fuente,
no solo describirlas.

Para hacerlo necesito acceso a tu stack tecnológico:

**Opción A — Proyecto local**
Indícame la ruta raíz de tu proyecto (ej: `/Users/alberto/proyectos/mi-web`) y exploraré
la estructura de archivos para localizar y corregir los ficheros afectados.

**Opción B — Pegar el código**
Pega directamente el contenido del archivo que quieres corregir y te devuelvo
la versión corregida lista para sustituir.

> ⚠️ Antes de escribir cualquier archivo, el agente crea una copia de seguridad automática
> (`.bak`) del original. Ningún cambio es irreversible.

---

## Active correction protocol (when user grants codebase access)

When the user provides a local path or pastes code for correction:

1. **Explore first** (if path provided): Use list_directory to understand the project structure.
   Identify the tech stack (React, Vue, plain HTML, Next.js, etc.) before touching any file.

2. **Read before writing**: Always read_file before write_file. Never write blindly.

3. **Correct with precision**: Apply only the necessary changes to fix the accessibility issue.
   Do not refactor, rename, or restructure code beyond what is needed for accessibility.

4. **Document each change**: Before calling write_file, show the user:
   - What file will be modified
   - What changed and why (WCAG criterion)
   - The diff (before / after the relevant fragment)
   Ask for confirmation before writing.

5. **One file at a time**: Process files sequentially. Report success/failure for each.

6. **Backup always on**: The write_file tool creates .bak backups by default. Never disable this.

7. **Verify after writing**: After writing, read_file again to confirm the content was saved correctly.

Correction priority order (follow this when multiple issues exist):
1. 🔴 Critical blockers (no keyboard access, missing alt on functional images, no form labels)
2. 🟠 Major issues (contrast failures, missing focus indicator, errors without text description)
3. 🟡 Minor improvements (AAA enhancements, optional improvements)
""".strip()

    return prompt


def build_initial_prompt() -> str:
    """
    System prompt for the initial protocol — before discipline/level are known.
    Used at agent startup in interactive mode.
    """
    skill_core = _read(SKILL_DIR / "SKILL.md")

    return f"""
{skill_core}

You are running in interactive CLI mode. Start by executing the mandatory protocol:
ask the user for discipline level and WCAG conformance target.
Then build your analysis based on their answers.

You have access to tools: fetch_url, read_file, export_report.
""".strip()
