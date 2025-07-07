"""cli.py
The entrance of the program.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt


from assistant.core import (
    start_focus_session,
    view_log,
    create_checkin_task,
    checkin,
    view_checkin_records,
)
from assistant.db import init_db
from assistant.utils import ultimate_clear
from assistant.statistics import display_checkin_statistics

console = Console(force_terminal=True, force_interactive=True)


def wait_and_clear():
    input("\nPress Enter to return to main menu...")
    ultimate_clear(console)


def main_menu():
    init_db()
    while True:
        ultimate_clear(console)
        panel = Panel(
            "[bold cyan]1.[/bold cyan] Start new task session\n"
            "[bold cyan]2.[/bold cyan] View task log\n"
            "[bold cyan]3.[/bold cyan] Create check-in task\n"
            "[bold cyan]4.[/bold cyan] Check-in\n"
            "[bold cyan]5.[/bold cyan] View check-in records\n"
            "[bold cyan]6.[/bold cyan] View Check-in Statistics\n"
            "[bold cyan]7.[/bold cyan] Exit",
            title="[bold magenta]Apologies for Being Human[/bold magenta]",
            border_style="bright_blue",
        )
        console.print(panel)

        choice = Prompt.ask(
            "[yellow]Choose an option[/yellow]",
            choices=["1", "2", "3", "4", "5", "6", "7"],
            default="1",
        )
        if choice == "1":
            task_name = Prompt.ask("Enter your task name")
            try:
                duration = int(
                    Prompt.ask("Enter session duration in minutes", default="25")
                )
                start_focus_session(task_name, duration, console=console)
                wait_and_clear()
            except ValueError:
                console.print("[red]Invalid duration. Try again.[/red]")
                wait_and_clear()
        elif choice == "2":
            view_log(console=console)
            wait_and_clear()
        elif choice == "3":
            create_checkin_task(console=console)
            wait_and_clear()
        elif choice == "4":
            checkin(console=console)
            wait_and_clear()
        elif choice == "5":
            view_checkin_records(console=console)
            wait_and_clear()
        elif choice == "6":
            display_checkin_statistics(console=console)
            wait_and_clear()
        elif choice == "7":
            console.print("[green]Goodbye. Stay mindful and consistent.[/green]")
            break


if __name__ == "__main__":
    main_menu()
