import os
import platform
from rich.console import Console


def ultimate_clear(console: Console):
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    print("\033c", end="")  # VT100控制码强制重置
    console.clear()
