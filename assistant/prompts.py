"""assistant/prompts.py"""

import random
from assistant.llm_quotes import get_llm_quote

STATIC_QUOTES = [
    "Start where you are. Use what you have. Do what you can. – Arthur Ashe",
    "You don’t have to be great to start, but you have to start to be great. – Zig Ziglar",
    "Done is better than perfect. – Sheryl Sandberg",
    "Success is the sum of small efforts, repeated day in and day out. – Robert Collier",
    "Focus on being productive instead of busy. – Tim Ferriss",
]


def gentle_prompt(task_name: str, return_str: bool = False):
    try:
        quote = get_llm_quote()
    except Exception:
        quote = random.choice(STATIC_QUOTES)

    message = f"⏰ Stay focused on {task_name} — {quote} 💪"
    if return_str:
        return message
    print("\n" + message)
    print("Even a small step forward counts. You've got this!")
