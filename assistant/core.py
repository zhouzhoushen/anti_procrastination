"""assistant/core.py
Core functions are defined here.
"""

import time
from datetime import datetime
import os

from rich.console import Console
from rich.table import Table
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
from threading import Timer

from assistant.db import (
    log_task,
    get_all_sessions,
    get_sessions_by_date,
    get_sessions_by_task,
    get_distinct_tasks,
    get_logs,  # 已有：最近 N 条
)
from assistant.prompts import gentle_prompt


console = Console()
LOG_FILE = os.path.join(os.getcwd(), "logs", "task_log.json")

latest_reminder = {"text": "Stay focused..."}


class ReminderColumn(ProgressColumn):
    def render(self, task):
        return Text(latest_reminder["text"], style="yellow")


def make_prompt_callback(task_name):
    def callback():
        try:
            quote_text = gentle_prompt(task_name, return_str=True)
        except Exception:
            quote_text = "Even a small step forward counts. You've got this!"
        latest_reminder["text"] = quote_text

    return callback


def start_focus_session(task_name, duration_minutes):
    duration_seconds = duration_minutes * 60
    start_time = datetime.now()
    console.print(
        f"\n[bold green]🎯 Starting session:[/bold green] {task_name} ({duration_minutes} min)"
    )

    default_interval = 1 * 60  # Remind every 1 minute, can be adjusted
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

    log_task(task_name, start_time, end_time, distractions)


def view_log():
    console.clear()
    choice = Prompt.ask(
        "[yellow]Select log view mode[/yellow]",
        choices=["all", "date", "task", "latest"],
        default="latest",
    )

    if choice == "all":
        rows = get_all_sessions()
    elif choice == "date":
        # —— 日期校验循环 ——
        while True:
            date_str = Prompt.ask("Enter date (YYYY-MM-DD)")
            try:
                # 验证输入格式
                datetime.strptime(date_str, "%Y-%m-%d")
                break
            except ValueError:
                console.print("[red]Invalid date format. Please use YYYY-MM-DD[/red]")
        rows = get_sessions_by_date(date_str)
    elif choice == "task":
        # 可先获取所有任务列表供选择：
        tasks = get_distinct_tasks()
        task_name = Prompt.ask("Select task", choices=tasks)
        rows = get_sessions_by_task(task_name)
    else:  # latest N entries
        n = int(Prompt.ask("How many recent entries?", default="20"))
        rows = get_logs(limit=n)

    if not rows:
        console.print("[yellow]No matching records.[/yellow]")
        return

    # —— 分页展示 ——
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

        # 如果还有未展示的，等待用户确认再继续
        if offset + page_size < total:
            Prompt.ask(
                f"Showing {offset + 1}–{min(offset + page_size, total)} of {total}. Press Enter to continue",
                default="",
            )

    # 所有页面展示完毕后，按任意键返回主菜单
    # Prompt.ask("End of logs. Press Enter to return to menu", default="")
