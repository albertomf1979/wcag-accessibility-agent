"""
tools.py
Tool definitions for the WCAG accessibility agent.
Uses Anthropic tool use format.
"""

import json
import base64
import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional

import httpx
from bs4 import BeautifulSoup

# ──────────────────────────────────────────────
# Tool schemas (passed to Anthropic API)
# ──────────────────────────────────────────────

TOOL_DEFINITIONS = [
    {
        "name": "axe_scan",
        "description": (
            "Run a full axe-core WCAG accessibility scan on a URL using a headless Chromium browser. "
            "Unlike fetch_url (static HTML only), axe_scan executes JavaScript and CSS, evaluating "
            "the rendered DOM — this detects dynamic ARIA states, CSS-hidden elements, and "
            "JS-driven content that fetch_url cannot see. Returns the violations axe-core can detect "
            "automatically; it cannot verify every WCAG criterion, so manual checks are still needed. "
            "ALWAYS use this as the FIRST tool when analyzing a URL. "
            "Then use fetch_url to get HTML context for interpreting and explaining the violations."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to scan. Must be publicly accessible."
                },
                "tags": {
                    "type": "string",
                    "description": (
                        "Comma-separated WCAG tag filters. "
                        "Default: 'wcag2a,wcag2aa,wcag21a,wcag21aa' (WCAG 2.1 A + AA). "
                        "Add 'wcag2aaa' for AAA rules or 'wcag22aa' for WCAG 2.2 rules."
                    )
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "fetch_url",
        "description": (
            "Fetch the HTML content of a web page for accessibility analysis. "
            "Returns the page title, meta info, and cleaned HTML structure."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the web page to fetch and analyze."
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "read_file",
        "description": (
            "Read the contents of a local file for accessibility analysis or correction. "
            "Supports HTML, CSS, JavaScript, JSX, TSX, Vue, Svelte, and plain text files. "
            "For images (PNG, JPG), returns a base64 representation for visual analysis."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute or relative path to the file."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "list_directory",
        "description": (
            "List the contents of a directory to explore the project's tech stack. "
            "Use this when the user grants access to their codebase so you can understand "
            "the file structure before reading and correcting specific files. "
            "Returns file names, types, and sizes."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute or relative path to the directory to list."
                },
                "recursive": {
                    "type": "boolean",
                    "description": "If true, list subdirectories recursively (max depth 3). Default false."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": (
            "Write corrected file content to disk, applying accessibility fixes. "
            "Always creates a backup of the original file before overwriting. "
            "Use ONLY when the user has explicitly granted access to their codebase "
            "and confirmed they want corrections applied."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute or relative path to the file to write."
                },
                "content": {
                    "type": "string",
                    "description": "The corrected file content to write."
                },
                "backup": {
                    "type": "boolean",
                    "description": "Whether to create a .bak backup before writing. Default true."
                }
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "export_report",
        "description": (
            "Export the accessibility report to a downloadable file. "
            "Use this when the user requests a PDF or DOCX output of the analysis."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The full markdown content of the report to export."
                },
                "format": {
                    "type": "string",
                    "enum": ["pdf", "docx"],
                    "description": "Export format: 'pdf' or 'docx'."
                },
                "filename": {
                    "type": "string",
                    "description": "Output filename without extension (e.g. 'auditoria-homepage')."
                }
            },
            "required": ["content", "format"]
        }
    }
]


# ──────────────────────────────────────────────
# Tool implementations
# ──────────────────────────────────────────────

AXE_SCAN_SCRIPT = (
    Path(__file__).resolve().parent / "skills" / "wcag-accessibility" / "scripts" / "axe-scan.mjs"
)
DEFAULT_AXE_TAGS = "wcag2a,wcag2aa,wcag21a,wcag21aa"


def _find_node() -> Optional[str]:
    """Locate the node binary across common macOS/Linux install paths."""
    found = shutil.which("node")
    if found:
        return found
    candidates = [
        "/usr/local/bin/node",
        "/opt/homebrew/bin/node",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    # nvm: find highest installed version
    nvm_node = Path.home() / ".nvm" / "versions" / "node"
    if nvm_node.exists():
        for version_dir in sorted(nvm_node.iterdir(), reverse=True):
            node_path = version_dir / "bin" / "node"
            if node_path.exists():
                return str(node_path)
    return None


def axe_scan(url: str, tags: str = DEFAULT_AXE_TAGS) -> dict[str, Any]:
    """
    Run axe-core on a URL via headless Chromium.
    Delegates to the skill's scripts/axe-scan.mjs, shared with AI coding agents.
    """
    node = _find_node()
    if not node:
        return {
            "success": False,
            "error": (
                "node not found. Install Node.js 18+ and run "
                "`npx -y @axe-core/cli --version` once to pre-install axe-cli. "
                "See SETUP.md for instructions."
            ),
            "fallback": "Use fetch_url as a partial fallback (static HTML only)."
        }

    try:
        result = subprocess.run(
            [node, str(AXE_SCAN_SCRIPT), url, tags],
            capture_output=True,
            text=True,
            timeout=150,
        )
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "axe-scan timed out after 150 seconds."}
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "axe-scan.mjs produced invalid JSON.",
            "stderr": result.stderr[:500],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def fetch_url(url: str) -> dict[str, Any]:
    """Fetch and parse a web page for accessibility analysis."""
    try:
        headers = {
            "User-Agent": "WCAG-Accessibility-Agent/1.0 (accessibility audit bot)"
        }
        response = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Extract key accessibility-relevant information
        title = soup.find("title")
        lang = soup.find("html")
        meta_desc = soup.find("meta", attrs={"name": "description"})
        headings = [(h.name, h.get_text(strip=True)) for h in soup.find_all(["h1","h2","h3","h4","h5","h6"])]
        images = [{"src": img.get("src",""), "alt": img.get("alt")} for img in soup.find_all("img")]
        links = [{"href": a.get("href",""), "text": a.get_text(strip=True)} for a in soup.find_all("a")]
        forms = soup.find_all("form")
        buttons = [{"text": b.get_text(strip=True), "type": b.get("type",""), "aria-label": b.get("aria-label","")} for b in soup.find_all("button")]
        inputs = [{"type": i.get("type","text"), "id": i.get("id",""), "name": i.get("name",""), "aria-label": i.get("aria-label",""), "placeholder": i.get("placeholder","")} for i in soup.find_all("input")]

        # Get labels to cross-reference with inputs
        labels = [{"for": l.get("for",""), "text": l.get_text(strip=True)} for l in soup.find_all("label")]

        # Raw HTML (truncated for context window)
        raw_html = str(soup)[:15000]

        return {
            "success": True,
            "url": url,
            "status_code": response.status_code,
            "title": title.get_text(strip=True) if title else None,
            "lang": lang.get("lang") if lang else None,
            "meta_description": meta_desc.get("content") if meta_desc else None,
            "headings": headings,
            "images_count": len(images),
            "images_missing_alt": [img for img in images if img["alt"] is None],
            "images_empty_alt": [img for img in images if img["alt"] == ""],
            "links": links[:50],  # first 50
            "forms_count": len(forms),
            "buttons": buttons[:30],
            "inputs": inputs[:30],
            "labels": labels[:30],
            "raw_html_excerpt": raw_html,
        }

    except httpx.HTTPStatusError as e:
        return {"success": False, "error": f"HTTP {e.response.status_code}: {e.request.url}"}
    except httpx.RequestError as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def read_file(path: str) -> dict[str, Any]:
    """Read a local file for accessibility analysis."""
    file_path = Path(path)

    if not file_path.exists():
        return {"success": False, "error": f"File not found: {path}"}

    suffix = file_path.suffix.lower()

    try:
        # Text-based files
        if suffix in [".html", ".htm", ".css", ".js", ".jsx", ".tsx", ".vue", ".svelte", ".md", ".txt"]:
            content = file_path.read_text(encoding="utf-8")

            if suffix in [".html", ".htm"]:
                soup = BeautifulSoup(content, "lxml")
                return {
                    "success": True,
                    "path": path,
                    "type": "html",
                    "content": content[:20000],
                    "title": soup.find("title").get_text() if soup.find("title") else None,
                    "lang": soup.find("html").get("lang") if soup.find("html") else None,
                }
            return {
                "success": True,
                "path": path,
                "type": suffix.lstrip("."),
                "content": content[:20000],
            }

        # Images
        elif suffix in [".png", ".jpg", ".jpeg", ".webp", ".gif"]:
            image_data = file_path.read_bytes()
            b64 = base64.standard_b64encode(image_data).decode("utf-8")
            media_type = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".webp": "image/webp",
                ".gif": "image/gif",
            }.get(suffix, "image/png")
            return {
                "success": True,
                "path": path,
                "type": "image",
                "media_type": media_type,
                "base64": b64,
                "note": "Image provided for visual accessibility analysis (contrast, layout, focus indicators, etc.)"
            }

        # PDF
        elif suffix == ".pdf":
            try:
                import fitz  # pymupdf
                doc = fitz.open(path)
                text = ""
                for page in doc:
                    text += page.get_text()
                return {
                    "success": True,
                    "path": path,
                    "type": "pdf",
                    "pages": len(doc),
                    "text_content": text[:15000],
                }
            except ImportError:
                return {"success": False, "error": "pymupdf not installed. Run: pip install pymupdf"}

        else:
            return {"success": False, "error": f"Unsupported file type: {suffix}"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def list_directory(path: str, recursive: bool = False) -> dict[str, Any]:
    """List directory contents to explore the project tech stack."""
    dir_path = Path(path)

    if not dir_path.exists():
        return {"success": False, "error": f"Directory not found: {path}"}
    if not dir_path.is_dir():
        return {"success": False, "error": f"Not a directory: {path}"}

    # Extensions relevant for accessibility correction
    RELEVANT_EXTENSIONS = {
        ".html", ".htm", ".css", ".js", ".jsx", ".tsx", ".ts",
        ".vue", ".svelte", ".astro", ".json", ".md"
    }
    IGNORE_DIRS = {"node_modules", ".git", ".next", "dist", "build", "__pycache__", ".venv", "venv"}

    def scan(p: Path, depth: int = 0) -> list:
        if depth > 3:
            return []
        entries = []
        try:
            for item in sorted(p.iterdir()):
                if item.name.startswith(".") and item.name not in [".env.example"]:
                    continue
                if item.is_dir():
                    if item.name in IGNORE_DIRS:
                        continue
                    entry = {"name": item.name, "type": "dir", "path": str(item)}
                    if recursive:
                        entry["children"] = scan(item, depth + 1)
                    entries.append(entry)
                elif item.is_file():
                    size = item.stat().st_size
                    entries.append({
                        "name": item.name,
                        "type": "file",
                        "extension": item.suffix.lower(),
                        "size_kb": round(size / 1024, 1),
                        "path": str(item),
                        "relevant": item.suffix.lower() in RELEVANT_EXTENSIONS
                    })
        except PermissionError:
            pass
        return entries

    entries = scan(dir_path, depth=0)
    relevant_files = [e for e in entries if e.get("type") == "file" and e.get("relevant")]

    return {
        "success": True,
        "path": str(dir_path),
        "entries": entries,
        "relevant_files_count": len(relevant_files),
        "relevant_files": relevant_files,
        "note": "Files marked as relevant are candidates for accessibility correction."
    }


def write_file(path: str, content: str, backup: bool = True) -> dict[str, Any]:
    """Write corrected content to a file, with automatic backup."""
    file_path = Path(path)

    try:
        # Create backup before overwriting
        backup_path = None
        if backup and file_path.exists():
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            backup_path.write_text(file_path.read_text(encoding="utf-8"), encoding="utf-8")

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write corrected content
        file_path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "path": str(file_path),
            "backup": str(backup_path) if backup_path else None,
            "bytes_written": len(content.encode("utf-8")),
            "message": (
                f"File written successfully: {file_path}"
                + (f"\nBackup saved at: {backup_path}" if backup_path else "")
            )
        }

    except PermissionError:
        return {"success": False, "error": f"Permission denied writing to: {path}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def export_report(content: str, format: str, filename: str = "wcag-report") -> dict[str, Any]:
    """Export the accessibility report to PDF or DOCX."""
    import os
    output_dir = Path(os.getenv("WCAG_OUTPUT_DIR", "./outputs"))
    output_dir.mkdir(parents=True, exist_ok=True)

    if format == "pdf":
        from exporters.pdf import export_to_pdf
        output_path = output_dir / f"{filename}.pdf"
        result = export_to_pdf(content, output_path)
    elif format == "docx":
        from exporters.docx import export_to_docx
        output_path = output_dir / f"{filename}.docx"
        result = export_to_docx(content, output_path)
    else:
        return {"success": False, "error": f"Unknown format: {format}"}

    return result


# ──────────────────────────────────────────────
# Tool dispatcher
# ──────────────────────────────────────────────

def execute_tool(tool_name: str, tool_input: dict) -> str:
    """
    Execute a tool by name and return JSON string result.
    Called by the agent loop when Claude requests a tool use.
    """
    if tool_name == "axe_scan":
        result = axe_scan(
            url=tool_input["url"],
            tags=tool_input.get("tags", DEFAULT_AXE_TAGS),
        )
    elif tool_name == "fetch_url":
        result = fetch_url(tool_input["url"])
    elif tool_name == "read_file":
        result = read_file(tool_input["path"])
    elif tool_name == "list_directory":
        result = list_directory(
            tool_input["path"],
            recursive=tool_input.get("recursive", False)
        )
    elif tool_name == "write_file":
        result = write_file(
            path=tool_input["path"],
            content=tool_input["content"],
            backup=tool_input.get("backup", True)
        )
    elif tool_name == "export_report":
        result = export_report(
            content=tool_input["content"],
            format=tool_input["format"],
            filename=tool_input.get("filename", "wcag-report")
        )
    else:
        result = {"success": False, "error": f"Unknown tool: {tool_name}"}

    return json.dumps(result, ensure_ascii=False, indent=2)
