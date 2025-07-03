"""assistant/core.py
Core functions are defined here.
"""

import time
import sys
import datetime
import json
import os

from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import (
    Progress,
    BarColumn,
    TimeRemainingColumn,
    SpinnerColumn,
    TextColumn,
    ProgressColumn,
)
from rich.live import Live
from rich.text import Text
from threading import Timer, Thread

from assistant.prompts import gentle_prompt


console = Console()
LOG_FILE = os.path.join(os.getcwd(), "logs", "task_log.json")

latest_reminder = {"text": "Stay focused..."}


class ReminderColumn(ProgressColumn):
    def render(self, task):
        return Text(latest_reminder["text"], style="yellow")


def log_task(task_name, start_time, end_time, distractions):
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                log = json.load(f)
        except:
            log = {}
    else:
        log = {}

    if task_name not in log:
        log[task_name] = []
    log[task_name].append(
        {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "duration_minutes": round((end_time - start_time).total_seconds() / 60, 2),
            "distractions": distractions,
        }
    )

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)


def make_prompt_callback(task_name):
    def callback():
        try:
            quote_text = gentle_prompt(task_name, return_str=True)
        except:
            quote_text = "Even a small step forward counts. You've got this!"
        latest_reminder["text"] = quote_text

    return callback


def start_focus_session(task_name, duration_minutes):
    duration_seconds = duration_minutes * 60
    start_time = datetime.datetime.now()
    console.print(
        f"\n[bold green]🎯 Starting session:[/bold green] {task_name} ({duration_minutes} min)"
    )

    default_interval = 5 * 60  # 每5分钟提醒一次
    prompts_count = max(1, int(duration_seconds / default_interval))
    timings = [
        duration_seconds / (prompts_count + 1) * (i + 1) for i in range(prompts_count)
    ]

    reminder_column = ReminderColumn()

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

        prompt_timers = []
        for t_sec in timings:
            timer = Timer(t_sec, make_prompt_callback(task_name))
            timer.daemon = True
            timer.start()
            prompt_timers.append(timer)

        try:
            while not progress.finished:
                time.sleep(1)
                progress.update(task, advance=1)
        except KeyboardInterrupt:
            console.print("\n[red]⛔ Session interrupted by user.[/red]")

        for timer in prompt_timers:
            timer.cancel()

    end_time = datetime.datetime.now()
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

    log_task(task_name, start_time, end_time, distractions)


def view_log():
    if not os.path.exists(LOG_FILE):
        console.print("[red]No log file found.[/red]")
        return

    with open(LOG_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            console.print("[red]Log file is corrupted.[/red]")
            return

    if not data:
        console.print("[yellow]No task logs yet.[/yellow]")
        return

    for task, sessions in data.items():
        table = Table(title=f"📘 Task: {task}", title_style="bold green")
        table.add_column("Start")
        table.add_column("End")
        table.add_column("Duration (min)")
        table.add_column("Distractions")
        for s in sessions:
            table.add_row(
                s["start"], s["end"], str(s["duration_minutes"]), str(s["distractions"])
            )
        console.print(table)
