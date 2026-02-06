# 🤖 NanoPyBot

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.2.0-green.svg)](https://github.com/kikiginanjar16/nanopy)

**NanoPyBot** is a lightweight, self-learning AI assistant designed for simplicity and automation. It features a persistent memory system for "self-learning" from user feedback and a built-in cron scheduler for running periodic AI tasks.

---

## 🚀 Key Features

- **🧠 Self-Learning Memory**: Remembers user preferences and rules ("don't answer too long") and applies them to future prompts.
- **⏰ Cron Scheduler**: Automate AI tasks using standard cron expressions, backed by a persistent SQLite job store.
- **🛠️ Extensible Tools**: Simple modular tool system (includes `time` tool out-of-the-box).
- **🔌 Provider Agnostic**: Supports any OpenAI-compatible API (OpenAI, Groq, Local LLMs, etc.).
- **🪶 Ultra Lightweight**: Built with Python, Typer, and Rich for a beautiful CLI experience.

---

## 📦 Installation

Ensure you have **Python 3.10+** installed.

```bash
# Clone the repository
git clone https://github.com/kikiginanjar16/nanopy.git
cd nanopy

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in editable mode
pip install --upgrade pip
pip install -e .
```

---

## ⚙️ Configuration

NanoPyBot stores its data in `~/.nanopybot/`. On the first run, a default `config.json` will be created.

Update your configuration at `~/.nanopybot/config.json`:

```json
{
  "provider": {
    "api_key": "your-api-key-here",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o-mini"
  }
}
```

---

## 🛠️ Usage

### 💬 Chat with Agent
Run the agent directly from your terminal. NanoPyBot will remember "rules" if you provide feedback.

```bash
nanopy agent "Hello, please give me a short logic puzzle."
```

### 🧠 Self-Learning Prompt
If you tell the agent "Please answer in Indonesian from now on", it will store this as a persistent rule and apply it to all subsequent requests.

### 🔧 Running Tools
Execute built-in tools using the `tool:` prefix:

```bash
# Get the current Unix timestamp
nanopy agent 'tool:time {}'
```

### 📅 Automation (Cron)
Schedule tasks to run periodically.

```bash
# Add a daily task at 07:00 AM
nanopy cron-add --name "daily-summary" --message "Summarize my day" --cron "0 7 * * *"

# List and run the scheduler service
nanopy cron-run
```

---

## 🏗️ Architecture

NanoPyBot is designed with modularity in mind:
- **CLI**: Powered by `Typer` and `Rich`.
- **Memory**: JSON-based KV store for simplicity.
- **Scheduler**: `APScheduler` with `SQLAlchemy` (SQLite) persistence.
- **Provider**: `httpx` based OpenAI-compatible adapter.

For a detailed breakdown, see [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## 🛠️ Troubleshooting

- **Provider Error (401)**: Double-check your API key in `~/.nanopybot/config.json`.
- **Invalid Cron**: Ensure you use the 5-field format (`* * * * *`).
- **Persistence**: If jobs or memory aren't saving, check write permissions for `~/.nanopybot/`.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
*Created with ❤️ by [Kiki Ginanjar](https://github.com/kikiginanjar16)*
