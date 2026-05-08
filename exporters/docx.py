"""
exporters/docx.py
Export accessibility reports to DOCX (Word) for team handoff.
"""

import re
from pathlib import Path
from datetime import datetime


def export_to_docx(content: str, output_path: Path) -> dict:
    """Export markdown report content to DOCX."""
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor, Inches
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement

        doc = Document()

        # ── Styles ──
        style = doc.styles['Normal']
        style.font.name = 'Calibri'
        style.font.size = Pt(11)

        # ── Title page header ──
        title_para = doc.add_paragraph()
        title_run = title_para.add_run("Informe de Accesibilidad WCAG 2.1")
        title_run.bold = True
        title_run.font.size = Pt(22)
        title_run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x6e)
        title_para.alignment = WD_ALIGN_PARAGRAPH.LEFT

        meta_para = doc.add_paragraph()
        meta_run = meta_para.add_run(
            f"Generado por WCAG Accessibility Agent · {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
            f"Basado en W3C WAI WCAG 2.1 — https://www.w3.org/WAI/"
        )
        meta_run.font.size = Pt(9)
        meta_run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

        doc.add_paragraph()  # spacer

        # ── Parse and render markdown ──
        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]

            # Code block
            if line.strip().startswith('```'):
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                code_para = doc.add_paragraph('\n'.join(code_lines))
                code_para.style = 'No Spacing'
                for run in code_para.runs:
                    run.font.name = 'Courier New'
                    run.font.size = Pt(9)
                    # Light gray background via paragraph shading
                i += 1
                continue

            # H1
            if line.startswith('# '):
                p = doc.add_heading(line[2:].strip(), level=1)
                for run in p.runs:
                    run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x6e)
            # H2
            elif line.startswith('## '):
                p = doc.add_heading(line[3:].strip(), level=2)
                for run in p.runs:
                    run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x6e)
            # H3
            elif line.startswith('### '):
                doc.add_heading(line[4:].strip(), level=3)
            # H4
            elif line.startswith('#### '):
                doc.add_heading(line[5:].strip(), level=4)

            # Table row
            elif '|' in line and line.strip().startswith('|'):
                # Collect all table rows
                table_rows = []
                while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                    row_text = lines[i].strip().strip('|')
                    cells = [c.strip() for c in row_text.split('|')]
                    if not re.match(r'^[-: ]+$', row_text.replace('|', '')):
                        table_rows.append(cells)
                    i += 1

                if table_rows:
                    max_cols = max(len(r) for r in table_rows)
                    table = doc.add_table(rows=len(table_rows), cols=max_cols)
                    table.style = 'Table Grid'

                    for row_idx, row_data in enumerate(table_rows):
                        for col_idx, cell_text in enumerate(row_data):
                            if col_idx < max_cols:
                                cell = table.cell(row_idx, col_idx)
                                cell.text = cell_text
                                if row_idx == 0:
                                    for para in cell.paragraphs:
                                        for run in para.runs:
                                            run.bold = True
                                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                                    # Header row background
                                    tc = cell._tc
                                    tcPr = tc.get_or_add_tcPr()
                                    shd = OxmlElement('w:shd')
                                    shd.set(qn('w:val'), 'clear')
                                    shd.set(qn('w:color'), 'auto')
                                    shd.set(qn('w:fill'), '1A1A6E')
                                    tcPr.append(shd)

                    doc.add_paragraph()
                continue

            # Bullet list
            elif line.startswith('- ') or line.startswith('* '):
                text = line[2:].strip()
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # strip bold markers
                doc.add_paragraph(text, style='List Bullet')

            # Numbered list
            elif re.match(r'^\d+\. ', line):
                text = re.sub(r'^\d+\. ', '', line).strip()
                doc.add_paragraph(text, style='List Number')

            # Horizontal rule
            elif line.strip() in ['---', '***', '___']:
                doc.add_paragraph()

            # Empty line
            elif not line.strip():
                doc.add_paragraph()

            # Regular paragraph
            else:
                para = doc.add_paragraph()
                # Handle inline bold
                parts = re.split(r'(\*\*[^*]+\*\*)', line)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        run = para.add_run(part[2:-2])
                        run.bold = True
                    else:
                        # Handle inline code
                        code_parts = re.split(r'(`[^`]+`)', part)
                        for cp in code_parts:
                            if cp.startswith('`') and cp.endswith('`'):
                                run = para.add_run(cp[1:-1])
                                run.font.name = 'Courier New'
                                run.font.size = Pt(10)
                            else:
                                para.add_run(cp)

            i += 1

        # ── Footer ──
        section = doc.sections[0]
        footer = section.footer
        footer_para = footer.paragraphs[0]
        footer_para.text = (
            f"WCAG Accessibility Agent · Basado en W3C WAI · "
            f"https://www.w3.org/WAI/  ·  {datetime.now().strftime('%d/%m/%Y')}"
        )
        footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in footer_para.runs:
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

        doc.save(str(output_path))

        return {
            "success": True,
            "format": "docx",
            "path": str(output_path),
            "message": f"Handoff exportado correctamente: {output_path}"
        }

    except ImportError:
        return {
            "success": False,
            "error": "python-docx no está instalado. Ejecuta: pip install python-docx"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
