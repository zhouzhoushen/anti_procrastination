# Apologies for Being Human

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
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✅ Features
- **Pomodoro Sessions**: Customize focus time and interval reminders.
- **LLM Motivation**: Fetch motivational quotes from a local model (`tinyllama`) with static fallback.
- **Distraction Tracking**: Log number of distractions and session durations.
- **Session Logging**: JSON-based logs in `logs/tasks.db` for review.
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
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/) (for LLM quotes, optional)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/zhouzhoushen/apologies_for_being_human.git
   cd apologies_for_being_human
   ```

2. **Configure Python environment**

   ```bash
   uv venv   
   source .venv/bin/activate
   uv pip install -e . [--link-mode=symlink]
   [uv pip install <package_name> [--link-mode=symlink]](if error occurs when installing some packages during the last step)
   ```

3. **Pull LLM model** (optional, for dynamic quotes)
   ```bash
   ollama pull tinyllama
   ollama serve
   ```

---

## 🏃 Usage

Run the CLI tool:
```bash
apologies_for_being_human
```

---

## ⚙️ Configuration

- **Session Duration**: Default 25 minutes; change in the prompt.
- **Prompt Interval**: Every 2 minutes; modify `prompt_interval` in `core.py`.
- **Log File**: `logs/apologies_for_being_human.db`; move or rename in `core.py` if needed.

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

## 💕 Reference

* `cmatrix`
* `fortune`
* `sl`