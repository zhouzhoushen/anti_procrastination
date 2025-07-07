"""assistant/utils.py"""

import os
import platform
from rich.console import Console


def ultimate_clear(console: Console):
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    print("\033c", end="")  # VT100 control code to force reset
    console.clear()
