"""
agent.py
WCAG Accessibility Agent — main entry point.
Agentic loop with tool use over Anthropic API.
"""

import os
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from dotenv import load_dotenv
from anthropic import Anthropic

from system_prompt import build_system_prompt, build_initial_prompt
from tools import TOOL_DEFINITIONS, execute_tool

load_dotenv(Path(__file__).parent / ".env", override=True)

app = typer.Typer()
console = Console()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = os.getenv("WCAG_MODEL", "claude-sonnet-4-5")
MAX_TOKENS = 8096


# ──────────────────────────────────────────────
# Agent loop
# ──────────────────────────────────────────────

def run_agent_loop(
    system_prompt: str,
    messages: list,
    max_iterations: int = 20,
) -> str:
    """
    Core agentic loop. Handles tool use until a final text response is returned.
    Returns the final assistant text.
    """
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        # Check stop reason
        if response.stop_reason == "end_turn":
            # Extract final text
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            return final_text

        elif response.stop_reason == "tool_use":
            # Add assistant response to messages
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            # Execute all requested tools
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    console.print(f"[dim]→ Usando herramienta: [bold]{block.name}[/bold][/dim]")

                    result = execute_tool(block.name, block.input)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # Add tool results to messages
            messages.append({
                "role": "user",
                "content": tool_results
            })

        else:
            # Unexpected stop reason
            break

    return "El agente alcanzó el límite de iteraciones sin completar la tarea."


# ──────────────────────────────────────────────
# Protocol: ask discipline + level
# ──────────────────────────────────────────────

def ask_protocol() -> tuple[str, str]:
    """Ask the mandatory protocol questions and return (discipline, level)."""

    console.print(Panel(
        "[bold]Antes de comenzar, necesito dos confirmaciones:[/bold]",
        border_style="blue"
    ))

    console.print("\n[bold]1. ¿Qué nivel disciplinar quieres trabajar?[/bold]")
    console.print("   [1] UX — Flujos, navegación, formularios, interacción")
    console.print("   [2] UI — Contraste, tipografía, color, componentes visuales")
    console.print("   [3] Desarrollo — HTML semántico, ARIA, código, testing")
    console.print("   [4] Todos — Los tres niveles combinados")

    discipline_choice = Prompt.ask("\nTu elección", choices=["1", "2", "3", "4"], default="3")
    discipline_map = {"1": "ux", "2": "ui", "3": "desarrollo", "4": "todos"}
    discipline = discipline_map[discipline_choice]

    console.print("\n[bold]2. ¿Cuál es tu objetivo de conformidad WCAG?[/bold]")
    console.print("   [A]  Nivel A  — Requisitos mínimos")
    console.print("   [AA] Nivel AA — Estándar legal (recomendado)")
    console.print("   [AAA] Nivel AAA — Excelencia en accesibilidad")

    level = Prompt.ask("\nTu elección", choices=["A", "AA", "AAA"], default="AA")

    console.print(f"\n[green]✓ Configuración: [bold]{discipline.upper()}[/bold] · WCAG 2.1 [bold]{level}[/bold][/green]\n")

    return discipline, level


# ──────────────────────────────────────────────
# CLI commands
# ──────────────────────────────────────────────

@app.command()
def main(
    url: str = typer.Option(None, "--url", "-u", help="URL de la página web a analizar"),
    file: str = typer.Option(None, "--file", "-f", help="Ruta al archivo a analizar"),
    export: str = typer.Option(None, "--export", "-e", help="Formato de exportación: pdf o docx"),
    discipline: str = typer.Option(None, "--discipline", "-d", help="Nivel disciplinar: ux|ui|desarrollo|todos"),
    level: str = typer.Option(None, "--level", "-l", help="Nivel WCAG: A|AA|AAA"),
    mode: str = typer.Option("análisis", "--mode", "-m", help="Modo: análisis|auditoría|evaluación|corrección|handoff"),
    fix: str = typer.Option(None, "--fix", help="Ruta raíz del proyecto para aplicar correcciones directamente"),
):
    """
    WCAG Accessibility Agent — audita y corrige productos digitales para WCAG 2.1.
    """

    console.print(Panel(
        "[bold blue]WCAG Accessibility Agent[/bold blue]\n"
        "[dim]Basado en W3C WAI · WCAG 2.1 · A / AA / AAA[/dim]",
        border_style="blue"
    ))

    # Determine discipline and level
    if not discipline or not level:
        if url or file:
            discipline = discipline or "todos"
            level = level or "AA"
            console.print(f"[dim]Configuración automática: {discipline.upper()} · WCAG 2.1 {level}[/dim]\n")
        else:
            discipline, level = ask_protocol()

    # Build system prompt
    system = build_system_prompt(discipline=discipline, wcag_level=level)

    # Build initial user message
    if url:
        user_message = f"Modo: {mode}\n\nAnaliza la siguiente URL para accesibilidad WCAG 2.1 nivel {level} (disciplina: {discipline}):\n\n{url}"
        if export:
            user_message += f"\n\nAl finalizar el análisis, exporta el informe en formato {export} con el nombre 'auditoria-{url.split('//')[-1].split('/')[0].replace('.', '-')}'."
        if fix:
            user_message += f"\n\nTras el informe, el usuario ha concedido acceso al stack tecnológico en: {fix}\nExplora el proyecto y aplica las correcciones de accesibilidad encontradas."

    elif file:
        user_message = f"Modo: {mode}\n\nAnaliza el siguiente archivo para accesibilidad WCAG 2.1 nivel {level} (disciplina: {discipline}):\n\nRuta: {file}"
        if export:
            fname = Path(file).stem
            user_message += f"\n\nAl finalizar el análisis, exporta el informe en formato {export} con el nombre 'auditoria-{fname}'."
        if fix:
            user_message += f"\n\nTras el informe, el usuario ha concedido acceso al stack tecnológico en: {fix}\nExplora el proyecto y aplica las correcciones de accesibilidad encontradas."

    else:
        # Interactive conversation mode
        console.print("[bold]Modo interactivo.[/bold] Escribe tu consulta o describe el artefacto a analizar.")
        console.print(
            "[dim]Comandos especiales:\n"
            "  'salir'              → terminar\n"
            "  'exportar pdf'       → guardar informe en PDF\n"
            "  'exportar docx'      → guardar informe en DOCX\n"
            "  'corregir <ruta>'    → aplicar correcciones al proyecto en <ruta>[/dim]\n"
        )

        messages = []
        while True:
            user_input = Prompt.ask("[bold blue]>[/bold blue]")

            if user_input.lower() in ["salir", "exit", "quit"]:
                console.print("[dim]Hasta luego.[/dim]")
                break

            # Handle inline correction shortcut
            if user_input.lower().startswith("corregir "):
                project_path = user_input[9:].strip()
                user_input = (
                    f"El usuario ha concedido acceso al stack tecnológico en: {project_path}\n"
                    f"Explora el directorio, identifica los archivos relevantes y aplica "
                    f"las correcciones de accesibilidad WCAG 2.1 nivel {level} que hayas encontrado. "
                    f"Muestra el diff de cada cambio y pide confirmación antes de escribir cada archivo."
                )
                console.print(f"[dim]→ Modo corrección activo: [bold]{project_path}[/bold][/dim]\n")

            messages.append({"role": "user", "content": user_input})

            with console.status("[dim]Procesando...[/dim]"):
                response = run_agent_loop(system, messages)

            messages.append({"role": "assistant", "content": response})
            console.print(Markdown(response))
            console.print()

        return

    # Single-shot mode (URL or file provided)
    messages = [{"role": "user", "content": user_message}]

    with console.status(f"[dim]Analizando · {discipline.upper()} · WCAG 2.1 {level}...[/dim]"):
        response = run_agent_loop(system, messages)

    console.print(Markdown(response))

    # If fix path provided, the agent handled it in the loop.
    # If not, show the correction offer explicitly in single-shot mode.
    if not fix and (url or file):
        console.print(Panel(
            "[bold]¿Quieres que corrija los errores directamente?[/bold]\n\n"
            "Vuelve a ejecutar el agente añadiendo [bold cyan]--fix /ruta/de/tu/proyecto[/bold cyan]\n"
            "o usa el modo interactivo ([bold cyan]python agent.py[/bold cyan]) "
            "y escribe [bold cyan]corregir /ruta/de/tu/proyecto[/bold cyan]",
            border_style="yellow",
            title="Corrección activa disponible"
        ))


if __name__ == "__main__":
    app()
