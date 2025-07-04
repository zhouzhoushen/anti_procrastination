uv run pyinstaller  --onefile --clean --log-level=INFO --icon=favicon.ico --name anti_procrastination cli.py
:: --noconsole --add-data "cli.py;." --hidden-import=rich --collect-all=tkinter 