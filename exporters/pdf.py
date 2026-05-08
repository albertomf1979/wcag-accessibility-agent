"""
exporters/pdf.py
Export accessibility reports to PDF using PyMuPDF (fitz) — no native deps.
"""

import re
from pathlib import Path
from datetime import datetime


def export_to_pdf(content: str, output_path: Path) -> dict:
    """Export markdown report content to PDF using PyMuPDF."""
    try:
        import fitz

        # ── fonts (built-in) ─────────────────────────────────────────────────
        F      = fitz.Font("helv")
        F_BOLD = fitz.Font("hebo")
        F_MONO = fitz.Font("cour")

        def tw(text, font, size):
            return font.text_length(text, fontsize=size)

        # ── page geometry ────────────────────────────────────────────────────
        PW, PH = fitz.paper_size("a4")
        MX, MT, MB = 60, 56, 55
        TW = PW - 2 * MX

        # ── colours ──────────────────────────────────────────────────────────
        NAVY   = (0.10, 0.10, 0.43)
        BLACK  = (0.10, 0.10, 0.10)
        GREY   = (0.40, 0.40, 0.40)
        RED    = (0.75, 0.10, 0.10)
        ORANGE = (0.82, 0.42, 0.04)
        GREEN  = (0.10, 0.50, 0.10)
        WHITE  = (1.00, 1.00, 1.00)
        BG_COD = (0.94, 0.94, 0.94)
        BG_H1  = (0.93, 0.93, 0.97)

        # ── font sizes ───────────────────────────────────────────────────────
        SZ = {"h1": 18, "h2": 14, "h3": 11, "h4": 10,
              "body": 9.5, "code": 8.5, "meta": 7.5}

        doc = fitz.open()

        def new_page():
            pg = doc.new_page(width=PW, height=PH)
            pg.draw_rect(fitz.Rect(0, 0, PW, 34), color=None, fill=NAVY)
            pg.insert_text((MX, 23),
                "WCAG Accessibility Agent · Basado en W3C WAI WCAG 2.1",
                fontname="hebo", fontsize=SZ["meta"], color=WHITE)
            pg.insert_text((PW - MX - 55, 23),
                datetime.now().strftime("%d/%m/%Y"),
                fontname="helv", fontsize=SZ["meta"], color=WHITE)
            pg.draw_line((MX, PH - MB + 8), (PW - MX, PH - MB + 8),
                         color=(0.80, 0.80, 0.80), width=0.5)
            pg.insert_text((MX, PH - MB + 20),
                f"Página {doc.page_count}",
                fontname="helv", fontsize=SZ["meta"], color=GREY)
            return pg, MT + 10

        def check_space(pg, y, needed):
            if y + needed > PH - MB:
                return new_page()
            return pg, y

        def wrapped_lines(text, font, size, available):
            words = text.split()
            lines, line = [], []
            for w in words:
                test = " ".join(line + [w])
                if font.text_length(test, fontsize=size) <= available:
                    line.append(w)
                else:
                    if line:
                        lines.append(" ".join(line))
                    line = [w]
            if line:
                lines.append(" ".join(line))
            return lines or [""]

        def insert_block(pg, y, text, fontname, font_obj, size, color,
                         indent=0, line_gap=1.5):
            lh = size * line_gap
            for ln in wrapped_lines(text, font_obj, size, TW - indent):
                pg, y = check_space(pg, y, lh)
                pg.insert_text((MX + indent, y), ln,
                               fontname=fontname, fontsize=size, color=color)
                y += lh
            return pg, y

        def sev_color(text):
            t = text.lower()
            if any(x in t for x in ["crítico", "falla", "❌", "🔴"]):
                return RED
            if any(x in t for x in ["mayor", "⚠️", "🟠"]):
                return ORANGE
            if any(x in t for x in ["✅", "pasa", "bien", "🟢"]):
                return GREEN
            return BLACK

        # ── render ───────────────────────────────────────────────────────────
        pg, y = new_page()
        lines = content.split("\n")
        i = 0

        while i < len(lines):
            raw = lines[i]
            s = raw.strip()

            # blank
            if s == "":
                y += 3
                i += 1
                continue

            # hr
            if re.match(r'^-{3,}$', s):
                pg, y = check_space(pg, y, 10)
                pg.draw_line((MX, y), (PW - MX, y),
                             color=(0.80, 0.80, 0.80), width=0.4)
                y += 8
                i += 1
                continue

            # fenced code block
            if s.startswith("```"):
                i += 1
                code_lines = []
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                i += 1
                lh = SZ["code"] * 1.4
                block_h = lh * (len(code_lines) or 1) + 10
                pg, y = check_space(pg, y, min(block_h, 120))
                y += 4
                bg = fitz.Rect(MX, y - 4, PW - MX, y + block_h)
                pg.draw_rect(bg, color=None, fill=BG_COD)
                for cl in code_lines:
                    pg, y = check_space(pg, y, lh)
                    pg.insert_text((MX + 6, y), cl.replace("\t", "    "),
                                   fontname="cour", fontsize=SZ["code"], color=BLACK)
                    y += lh
                y += 6
                continue

            # blockquote / callout
            if s.startswith("▌") or s.startswith(">"):
                text_bq = s.lstrip("▌> ").strip()
                lh = SZ["body"] * 1.4
                pg, y = check_space(pg, y, lh + 4)
                pg.draw_line((MX, y - 2), (MX, y + lh),
                             color=NAVY, width=3)
                pg, y = insert_block(pg, y, text_bq, "helv", F,
                                     SZ["body"], GREY, indent=12)
                i += 1
                continue

            # H1
            if re.match(r'^# [^#]', s):
                text_h = s[2:].strip()
                sz = SZ["h1"]
                pg, y = check_space(pg, y, sz * 2.5)
                y += 6
                pg.draw_rect(fitz.Rect(MX - 4, y - 4, PW - MX + 4, y + sz + 8),
                             color=None, fill=BG_H1)
                pg, y = insert_block(pg, y, text_h, "hebo", F_BOLD, sz, NAVY)
                pg.draw_line((MX, y), (PW - MX, y), color=NAVY, width=1.2)
                y += 8
                i += 1
                continue

            # H2
            if re.match(r'^## [^#]', s):
                text_h = s[3:].strip()
                sz = SZ["h2"]
                pg, y = check_space(pg, y, sz * 2.5)
                y += 4
                pg, y = insert_block(pg, y, text_h, "hebo", F_BOLD, sz, NAVY)
                pg.draw_line((MX, y), (PW - MX, y),
                             color=(0.75, 0.75, 0.88), width=0.6)
                y += 6
                i += 1
                continue

            # H3
            if re.match(r'^### [^#]', s):
                text_h = s[4:].strip()
                sz = SZ["h3"]
                pg, y = check_space(pg, y, sz * 2)
                y += 4
                pg, y = insert_block(pg, y, text_h, "hebo", F_BOLD, sz, NAVY)
                y += 3
                i += 1
                continue

            # H4
            if re.match(r'^#### ', s):
                text_h = s[5:].strip()
                pg, y = check_space(pg, y, SZ["body"] * 2)
                y += 2
                pg, y = insert_block(pg, y, text_h, "hebo", F_BOLD,
                                     SZ["body"], BLACK)
                y += 2
                i += 1
                continue

            # table
            if "|" in s and s.startswith("|"):
                rows = []
                while i < len(lines) and "|" in lines[i] and lines[i].strip().startswith("|"):
                    row = lines[i].strip()
                    if not re.match(r'^\|[-| :]+\|$', row):
                        cells = [c.strip() for c in row.strip().strip("|").split("|")]
                        rows.append(cells)
                    i += 1
                if not rows:
                    continue
                cols = max(len(r) for r in rows)
                cw = (TW - 2) / cols
                rh = SZ["body"] * 2.1
                for ri, row in enumerate(rows):
                    pg, y = check_space(pg, y, rh + 2)
                    is_header = ri == 0
                    bg = NAVY if is_header else ((0.96, 0.96, 0.96) if ri % 2 else WHITE)
                    for ci in range(cols):
                        cell = row[ci] if ci < len(row) else ""
                        cx = MX + ci * cw
                        pg.draw_rect(fitz.Rect(cx, y - 1, cx + cw, y + rh - 1),
                                     color=(0.78, 0.78, 0.78), fill=bg, width=0.3)
                        fc = WHITE if is_header else sev_color(cell) if ci == len(row) - 1 else BLACK
                        fn = "hebo" if is_header else "helv"
                        max_chars = max(int(cw / 5.2), 5)
                        display = cell[:max_chars] + "…" if len(cell) > max_chars else cell
                        pg.insert_text((cx + 4, y + SZ["body"] + 1),
                                       display, fontname=fn,
                                       fontsize=SZ["body"], color=fc)
                    y += rh
                y += 5
                continue

            # bullet
            if re.match(r'^[-*•] ', s):
                text_b = re.sub(r'^[-*•] ', '', s)
                text_b = re.sub(r'\*\*(.+?)\*\*', r'\1', text_b)
                text_b = re.sub(r'\*(.+?)\*', r'\1', text_b)
                pg, y = insert_block(pg, y, "• " + text_b, "helv", F,
                                     SZ["body"], BLACK, indent=10)
                i += 1
                continue

            # numbered list
            if re.match(r'^\d+[\.\)] ', s):
                text_n = re.sub(r'^\d+[\.\)] ', '', s)
                text_n = re.sub(r'\*\*(.+?)\*\*', r'\1', text_n)
                num = re.match(r'^(\d+)', s).group(1)
                pg, y = insert_block(pg, y, f"{num}. {text_n}", "helv", F,
                                     SZ["body"], BLACK, indent=12)
                i += 1
                continue

            # normal paragraph
            text_p = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
            text_p = re.sub(r'\*(.+?)\*',     r'\1', text_p)
            text_p = re.sub(r'`(.+?)`',       r'\1', text_p)
            text_p = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text_p)

            has_emoji = any(x in text_p for x in ["❌", "✅", "⚠️", "🔴", "🟠", "🟡", "🟢"])
            col = sev_color(text_p)
            fn  = "hebo" if has_emoji else "helv"
            pg, y = insert_block(pg, y, text_p, fn, F_BOLD if has_emoji else F,
                                 SZ["body"], col)
            y += 2
            i += 1

        doc.save(str(output_path))
        doc.close()

        return {
            "success": True,
            "format": "pdf",
            "path": str(output_path),
            "message": f"Informe exportado correctamente: {output_path}"
        }

    except ImportError:
        return {
            "success": False,
            "error": "PyMuPDF no está instalado. Ejecuta: pip install pymupdf"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
