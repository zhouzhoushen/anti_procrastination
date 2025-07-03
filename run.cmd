@echo off
cd /d "%~dp0"

:: Activate virtual environment
call conda activate py3.12

:: Directly call poetry (now in the activated environment)
poetry run python cli.py

if %errorlevel% neq 0 (
    echo [Error] CLI execution failed.
)
pause