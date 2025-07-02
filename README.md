# Anti Procrastination

![Python 3.12](https://img.shields.io/badge/Python-3.12-blue)
![GitHub license](https://img.shields.io/github/license/zhouzhoushen/anti_procrastination)
![GitHub issues](https://img.shields.io/github/issues/zhouzhoushen/anti_procrastination)

A lightweight CLI tool to help you overcome procrastination with structured Pomodoro sessions and motivational support from a local LLM.

---

## 📋 Table of Contents
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✅ Features
- **Pomodoro Sessions**: Customize focus time and interval reminders.
- **LLM Motivation**: Fetch motivational quotes from a local model (`tinyllama`) with static fallback.
- **Distraction Tracking**: Log number of distractions and session durations.
- **Session Logging**: JSON-based logs in `logs/task_log.json` for review.
- **Easy CLI**: Single-command launch with clean interactive menu.

---

## 🚀 Demo
<p align="center">
  <img src="https://raw.githubusercontent.com/zhouzhoushen/anti_procrastination/main/demo.gif" alt="CLI Demo" width="600">
</p>

---

## 🔧 Installation

### Prerequisites
- Python 3.12+
- [Poetry](https://python-poetry.org/)
- [Ollama](https://ollama.com/) (for LLM quotes, optional)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/zhouzhoushen/anti_procrastination.git
   cd anti_procrastination
   ```

2. **Configure Python environment**

   `conda activate <vitual_env_name>` or `poetry env use python3.12`

   and then
   ```bash
   poetry install
   ```

3. **Pull LLM model** (optional, for dynamic quotes)
   ```bash
   ollama pull tinyllama
   ```

---

## 🏃 Usage

Run the CLI tool:
```bash
poetry run python cli.py
```

**Menu Options:**
1. **Start new task session** – enter task name and duration.
2. **View task log** – review past sessions and distractions.
3. **Exit**

---

## 🗂 Project Structure

```text
anti_procrastination/
├── assistant/           # Core modules
│   ├── __init__.py
│   ├── core.py          # Session management & logging
│   ├── prompts.py       # Static + LLM prompt logic
│   └── llm_quotes.py    # Ollama integration
├── logs/                # Session logs (JSON)
│   └── task_log.json
├── cli.py               # Entry-point CLI script
├── run.sh               # Optional launcher script
├── pyproject.toml       # Poetry configuration
├── README.md            # Project documentation
└── requirements.txt     # (Optional) pip dependencies
```

---

## ⚙️ Configuration

- **Session Duration**: Default 25 minutes; change in the prompt.
- **Prompt Interval**: Every 5 minutes; modify `prompt_interval` in `core.py`.
- **Log File**: `logs/task_log.json`; move or rename in `core.py` if needed.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Open a Pull Request

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE.txt) for details.

---

## 📞 Contact

Created by [Zhouzhou Shen](https://github.com/zhouzhoushen). Feel free to open an issue or reach out on GitHub!