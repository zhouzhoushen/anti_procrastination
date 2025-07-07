@echo off
cd /d "%~dp0"

:: Activate virtual environment
call .venv\Scripts\activate

:: Directly call poetry (now in the activated environment)
uv run python src/apologies_for_being_human/__main__.py

if %errorlevel% neq 0 (
    echo [Error] CLI execution failed.
)
pause