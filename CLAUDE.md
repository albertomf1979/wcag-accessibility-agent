# WCAG Accessibility Agent — Project Context

## What this project is
A CLI agent built on the Anthropic SDK that audits, analyzes, evaluates and corrects digital products for WCAG 2.1 accessibility. It generates structured reports and handoff documents (PDF + DOCX) for design and development teams.

The agent is grounded in the official W3C WAI standard (https://www.w3.org/WAI/) and follows a strict protocol: it always asks the user for discipline level (UX / UI / Dev) and WCAG conformance target (A / AA / AAA) before acting.

## Project structure
```
wcag_accessibility/
├── CLAUDE.md                    ← this file
├── SKILL.md                     ← skill core (agent system prompt source)
├── README.md                    ← user-facing instructions (GitHub front page)
├── SETUP.md                     ← detailed developer/technical reference
├── wcag-accessibility.skill     ← installable skill file for claude.ai
├── agent.py                     ← main agent loop (entry point)
├── system_prompt.py             ← builds the system prompt from SKILL.md + references
├── tools.py                     ← tool definitions for Anthropic tool use
├── exporters/
│   ├── __init__.py
│   ├── pdf.py                   ← PDF export via PyMuPDF
│   └── docx.py                  ← DOCX export via python-docx
├── references/
│   ├── ux-accesible.md
│   ├── ui-accesible.md
│   ├── dev-accesible.md
│   ├── modos-operacion.md
│   ├── criterios-wcag21.md
│   └── tecnicas-fallos.md
├── outputs/                     ← generated reports land here (gitignored)
├── requirements.txt
├── .env.example
└── .gitignore
```

## Tech stack
- Python 3.11+
- anthropic SDK (tool use, streaming)
- httpx (URL fetching)
- BeautifulSoup4 (HTML parsing)
- PyMuPDF (PDF export)
- python-docx (DOCX export)
- rich (CLI formatting)
- python-dotenv (env management)
- Cloudflare Workers/Pages (optional deployment for team web interface)

## Agent behavior rules
1. **Protocol first**: Always ask discipline level + WCAG target before any analysis.
2. **Source of truth**: All WCAG knowledge comes from references/ directory, grounded in W3C WAI.
3. **Tool use loop**: The agent uses tools to fetch URLs, read files, load references, and export. It reasons between tool calls.
4. **Five modes**: análisis / auditoría / evaluación / corrección / handoff. User can combine them.
5. **Output**: Always produces structured markdown → optionally exported to PDF or DOCX.

## Key commands
```bash
python agent.py                                        # Interactive mode
python agent.py --url https://example.com              # Analyze a URL
python agent.py --file path/to/file.html               # Analyze a local file
python agent.py --url https://example.com --export pdf # Analyze + export PDF
python agent.py --url https://example.com --export docx # Analyze + export DOCX handoff
python agent.py --file index.html --fix /path/to/project # Analyze + apply fixes
python agent.py --url https://example.com --fix /path/to/project # URL + apply fixes
```

## Agent tools
- **fetch_url**: Fetch and parse HTML from a URL for accessibility analysis
- **read_file**: Read local files (HTML, CSS, JS, JSX, TSX, Vue, Svelte, images, PDF)
- **list_directory**: Explore project structure to understand tech stack before correcting
- **write_file**: Write corrected files to disk (always creates .bak backup first)
- **export_report**: Export reports to PDF or DOCX

## Environment variables
- `ANTHROPIC_API_KEY` — required
- `WCAG_MODEL` — default: claude-sonnet-4-5 (override for faster/cheaper runs)
- `WCAG_OUTPUT_DIR` — default: ./outputs

## Cloudflare integration
If deploying a web interface for teams, use Cloudflare Pages + Workers:
- Worker handles API calls to Anthropic (keeps key server-side)
- Pages serves the frontend
- D1 can store audit history
- Account credentials in .env as CF_API_TOKEN and CF_ACCOUNT_ID

## GitHub
Public repo. The skill (SKILL.md + references/) is the publishable artifact.
The agent code shows how to build an agent from the skill.
README includes step-by-step instructions for anyone to run their own agent.
