uv run pyinstaller  --onefile --clean --log-level=INFO --icon=favicon.ico --name apologies_for_being_human cli.py
:: --noconsole --add-data "cli.py;." --hidden-import=rich --collect-all=tkinter 