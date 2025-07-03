"""cli.py
The entrance of the program.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from assistant.core import start_focus_session, view_log

console = Console()


def main_menu():
    while True:
        console.clear()
        panel = Panel(
            "[bold cyan]1.[/bold cyan] Start new task session\n"
            "[bold cyan]2.[/bold cyan] View task log\n"
            "[bold cyan]3.[/bold cyan] Exit",
            title="[bold magenta]Anti-Procrastination Assistant[/bold magenta]",
            border_style="bright_blue",
        )
        console.print(panel)

        choice = Prompt.ask(
            "[yellow]Choose an option[/yellow]", choices=["1", "2", "3"], default="1"
        )
        if choice == "1":
            task_name = Prompt.ask("Enter your task name")
            try:
                duration = int(
                    Prompt.ask("Enter session duration in minutes", default="25")
                )
                start_focus_session(task_name, duration)
            except ValueError:
                console.print("[red]Invalid duration. Try again.[/red]")
        elif choice == "2":
            view_log()
            input("\nPress Enter to return to main menu...")
        elif choice == "3":
            console.print("[green]Goodbye. Stay mindful and consistent.[/green]")
            break


if __name__ == "__main__":
    main_menu()
