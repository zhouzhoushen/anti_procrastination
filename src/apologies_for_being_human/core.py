"""assistant/core.py
Core functions are defined here.
"""

import time
from datetime import datetime

from rich.table import Table, Column
from rich.prompt import Prompt
from rich.progress import (
    Progress,
    BarColumn,
    TimeRemainingColumn,
    SpinnerColumn,
    TextColumn,
    ProgressColumn,
)
from rich.text import Text

from apologies_for_being_human.db import (
    log_task,
    get_all_sessions,
    get_sessions_by_date,
    get_sessions_by_task,
    get_distinct_tasks,
    get_logs,
    create_checkin_task as db_create_checkin_task,
    get_checkin_tasks,
    log_checkin,
    get_checkin_records,
)
from apologies_for_being_human.prompts import gentle_prompt


latest_reminder = {"text": "Stay focused..."}


class ReminderColumn(ProgressColumn):
    """Custom column that displays dynamic motivational reminders."""

    def __init__(self, reminder_text_func):
        super().__init__()
        self.reminder_text_func = reminder_text_func

    def render(self, task):
        text = self.reminder_text_func() or ""
        return Text(text, style="bold yellow")

    def get_table_column(self) -> Column:
        """Return a Column for the reminder."""
        return Column(
            header="Reminder",
            justify="left",
            no_wrap=False,
        )


def start_focus_session(task_name, duration_minutes, console):
    duration_seconds = duration_minutes * 60
    start_time = datetime.now()
    console.print(
        f"\n[bold green]🎯 Starting session:[/bold green] {task_name} ({duration_minutes} min)"
    )

    default_interval = 2 * 60
    prompts_count = max(1, int(duration_seconds / default_interval))
    timings = [
        duration_seconds / (prompts_count + 1) * (i + 1) for i in range(prompts_count)
    ]
    next_reminder_index = 0

    reminder_column = ReminderColumn(lambda: latest_reminder["text"])

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeRemainingColumn(),
        reminder_column,
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Focusing...", total=duration_seconds)

        elapsed_time = 0
        try:
            while not progress.finished:
                time.sleep(1)
                elapsed_time += 1
                progress.update(task, advance=1)

                if (
                    next_reminder_index < len(timings)
                    and elapsed_time >= timings[next_reminder_index]
                ):
                    try:
                        quote_text = gentle_prompt(task_name, return_str=True)
                    except Exception:
                        quote_text = (
                            "Even a small step forward counts. You've got this!"
                        )
                    latest_reminder["text"] = quote_text
                    next_reminder_index += 1
        except KeyboardInterrupt:
            console.print("\n[red]⛔ Session interrupted by user.[/red]")

    end_time = datetime.now()
    console.print(
        f"\n[green]✅ Session complete! End time: {end_time.strftime('%H:%M:%S')}[/green]"
    )

    while True:
        try:
            distractions = int(
                Prompt.ask(
                    "How many distractions did you feel during this session?",
                    default="0",
                )
            )
            if distractions <= 2:
                console.print("[blue]Few distractions noted. Great job![/blue]")
            else:
                console.print(
                    "[yellow]Try deep breathing when distracted. Stay focused![/yellow]"
                )
            break
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")

    latest_reminder["text"] = "Stay focused..."
    log_task(task_name, start_time, end_time, distractions)


def view_log(console):
    console.clear()
    choice = Prompt.ask(
        "[yellow]Select log view mode[/yellow]",
        choices=["all", "date", "task", "latest"],
        default="latest",
    )

    if choice == "all":
        rows = get_all_sessions()
    elif choice == "date":
        while True:
            date_str = Prompt.ask("Enter date (YYYY-MM-DD)")
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                break
            except ValueError:
                console.print("[red]Invalid date format. Please use YYYY-MM-DD[/red]")
        rows = get_sessions_by_date(date_str)
    elif choice == "task":
        tasks = get_distinct_tasks()
        task_name = Prompt.ask("Select task", choices=tasks)
        rows = get_sessions_by_task(task_name)
    else:
        n = int(Prompt.ask("How many recent entries?", default="20"))
        rows = get_logs(limit=n)

    if not rows:
        console.print("[yellow]No matching records.[/yellow]")
        return

    page_size = 10
    total = len(rows)
    for offset in range(0, total, page_size):
        chunk = rows[offset : offset + page_size]
        table = Table(title="📘 Task Sessions", title_style="bold green")
        table.add_column("Task")
        table.add_column("Start", no_wrap=True, min_width=20)
        table.add_column("End", no_wrap=True, min_width=20)
        table.add_column("Duration (min)")
        table.add_column("Distractions")

        for task, start, end, duration, distractions in chunk:
            table.add_row(task, start, end, str(duration), str(distractions))

        console.print(table)

        if offset + page_size < total:
            Prompt.ask(
                f"Showing {offset + 1}–{min(offset + page_size, total)} of {total}. Press Enter to continue",
                default="",
            )


def create_checkin_task(console):
    task_name = Prompt.ask("Enter the name of the check-in task")
    description = Prompt.ask("Enter a description (optional)", default="")
    db_create_checkin_task(task_name, description)
    console.print(f"[green]Check-in task '{task_name}' created successfully![/green]")


def checkin(console):
    tasks = get_checkin_tasks()
    if not tasks:
        console.print(
            "[yellow]No check-in tasks found. Please create one first.[/yellow]"
        )
        return
    task_choices = [f"{task[0]}: {task[1]}" for task in tasks]
    console.print("[yellow]Available check-in tasks:[/yellow]")
    for choice in task_choices:
        console.print(choice)
    task_input = Prompt.ask("Enter the task ID or name to check-in")
    try:
        task_id = int(task_input)
        if task_id not in [task[0] for task in tasks]:
            console.print("[red]Invalid task ID.[/red]")
            return
    except ValueError:
        task_names = [task[1].lower() for task in tasks]
        if task_input.lower() in task_names:
            task_id = tasks[task_names.index(task_input.lower())][0]
        else:
            console.print("[red]Invalid task name.[/red]")
            return
    success = (
        Prompt.ask(
            "Did you complete the task successfully?",
            choices=["yes", "no"],
            default="yes",
        )
        == "yes"
    )
    note = Prompt.ask("Add a note (optional)", default="")
    log_checkin(task_id, success, note)
    console.print("[green]Check-in recorded successfully![/green]")


def view_checkin_records(console):
    choice = Prompt.ask(
        "[yellow]Select view mode[/yellow]",
        choices=["all", "by_task", "by_date"],
        default="all",
    )
    if choice == "all":
        records = get_checkin_records()
    elif choice == "by_task":
        tasks = get_checkin_tasks()
        task_choices = [f"{task[0]}: {task[1]}" for task in tasks]
        console.print("[yellow]Available tasks:[/yellow]")
        for choice in task_choices:
            console.print(choice)
        task_input = Prompt.ask("Enter the task ID or name")
        try:
            task_id = int(task_input)
            if task_id not in [task[0] for task in tasks]:
                console.print("[red]Invalid task ID.[/red]")
                return
        except ValueError:
            task_names = [task[1].lower() for task in tasks]
            if task_input.lower() in task_names:
                task_id = tasks[task_names.index(task_input.lower())][0]
            else:
                console.print("[red]Invalid task name.[/red]")
                return
        records = get_checkin_records(checkin_task_id=task_id)
    elif choice == "by_date":
        date_str = Prompt.ask("Enter date (YYYY-MM-DD)")
        records = get_checkin_records(date=date_str)

    if not records:
        console.print("[yellow]No records found.[/yellow]")
        return

    table = Table(title="📘 Check-in Records", title_style="bold green")
    table.add_column("Task Name")
    table.add_column("Check-in Time")
    table.add_column("Success")
    table.add_column("Note")

    for record in records:
        task_name, checkin_time, success, note = record
        success_str = "Yes" if success else "No"
        table.add_row(task_name, checkin_time, success_str, note)

    console.print(table)
