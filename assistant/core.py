# assistant/core.py
import time
import sys
import datetime
import json
import os
from threading import Timer, Thread
from assistant.prompts import gentle_prompt

LOG_DIR = os.path.join(os.getcwd(), 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'task_log.json')

def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def load_log():
    ensure_log_dir()
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}

def save_log(log):
    ensure_log_dir()
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def log_task(task_name, start_time, end_time, distractions):
    log = load_log()
    if task_name not in log:
        log[task_name] = []
    log[task_name].append({
        'start': start_time.isoformat(),
        'end': end_time.isoformat(),
        'duration_minutes': round((end_time - start_time).total_seconds() / 60, 2),
        'distractions': distractions
    })
    save_log(log)

def elapsed_notifier(start_time, stop_flag, total_duration):
    while not stop_flag["stop"]:
        elapsed = datetime.datetime.now() - start_time
        remaining = max(0, total_duration - elapsed.total_seconds())
        mins, secs = divmod(int(remaining), 60)

        # 使用\r回到行首并清空剩余字符
        sys.stdout.write(f"\r⏳Time remaining: {mins:02d}:{secs:02d}    ")
        sys.stdout.flush()

        time.sleep(1)

def start_focus_session(task_name, duration_minutes=25):
    print(f"\n🎯 Starting session: {task_name} ({duration_minutes} min)")
    start_time = datetime.datetime.now()
    duration_sec = duration_minutes * 60

    default_interval = 5 * 60
    prompts_count = max(1, int(duration_sec / default_interval))
    timings = [duration_sec / (prompts_count + 1) * (i + 1) for i in range(prompts_count)]

    prompt_timers = []
    for t_sec in timings:
        timer = Timer(t_sec, gentle_prompt, args=(task_name,))
        timer.daemon = True
        timer.start()
        prompt_timers.append(timer)

    stop_flag = {"stop": False}
    notifier_thread = Thread(target=elapsed_notifier, args=(start_time, stop_flag, duration_sec), daemon=True)
    notifier_thread.start()

    try:
        time.sleep(duration_sec)
    except KeyboardInterrupt:
        print("\n⛔ Session interrupted by user.")

    stop_flag["stop"] = True
    for timer in prompt_timers:
        timer.cancel()

    end_time = datetime.datetime.now()
    print(f"\n✅ Session complete! End time: {end_time.strftime('%H:%M:%S')}")

    while True:
        distractions = input("How many distractions did you feel during this session? ")
        try:
            distractions = int(distractions)
            if distractions <= 2:
                print("Few distractions noted. Great job!")
            else:
                print("Try deep breathing when distracted! Stay focused! Keep going!")
            break
        except ValueError:
            print("Please enter a valid number for distractions.")

    log_task(task_name, start_time, end_time, distractions)

def view_log():
    log = load_log()
    if not log:
        print("No task logs yet.")
        return

    for task, sessions in log.items():
        print(f"\n📘 Task: {task}")
        for session in sessions:
            print(f" - {session['start']} to {session['end']} ({session['duration_minutes']} min), distractions: {session.get('distractions', 0)}")