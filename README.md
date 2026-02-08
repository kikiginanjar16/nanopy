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

NanoPyBot checks for `config.json` in the current directory first, making it easy for local development. If not found, it falls back to `~/.nanopybot/config.json`.

1. **Option A (Local)**: Edit `config.json` in the project root.
2. **Option B (Global)**: Edit `~/.nanopybot/config.json`.

Example configuration:

```json
{
  "provider": {
    "api_key": "your-openai-api-key",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o-mini"
  },
  "serper_api_key": "your-serper-api-key"
}
```

> **Catatan**: `serper_api_key` digunakan oleh tool `search` untuk melakukan pencarian di Google. Anda bisa mendapatkan API key gratis di [Serper.dev](https://serper.dev/).

---

## 🛠️ Usage

### 💬 Chat with Agent
Run the agent directly from your terminal. NanoPyBot will remember "rules" if you provide feedback.

```bash
nanopy agent "Hello, please give me a short logic puzzle."
```

### 🧠 Self-Learning Prompt
If you tell the agent "Please answer in Indonesian from now on", it will store this as a persistent rule and apply it to all subsequent requests.

### 🔧 Penggunaan Tools
Tools memungkinkan NanoPyBot melakukan tugas teknis seperti cek waktu, kalkulasi, atau akses API.

#### 1. Cara Menggunakan Tool (Manual)
Anda bisa memicu tool secara langsung dari terminal menggunakan prefix `tool:` diikuti nama tool dan argumen dalam format JSON.
```bash
# Contoh menggunakan tool bawaan 'time'
nanopy agent 'tool:time {}'

# Contoh menggunakan tool 'search' untuk mencari di Google
nanopy agent 'tool:search {"q": "harga bitcoin hari ini"}'

# Contoh menggunakan tool 'weather' untuk cek cuaca
nanopy agent 'tool:weather {"city": "Jakarta"}'

# Contoh menggunakan tool 'currency' untuk konversi mata uang
nanopy agent 'tool:currency {"from": "USD", "to": "IDR", "amount": 100}'
```

#### 2. Cara Menambah Tool Baru
Ada dua cara untuk mendaftarkan tool ke dalam NanoPyBot:

**A. Melalui Chat (Dynamic Creation)**
Ini cara termudah. Cukup minta bot di dalam chat untuk membuatkan fungsi baru.
- **Perintah**: `"Buatkan saya tool untuk [tugas tertentu]"`
- **Proses**: Bot akan menulis kode Python secara otomatis ke folder `custom_tools/`.
- **Hasil**: Tool langsung aktif dan bisa digunakan selamanya.

**B. Melalui File Python (Manual Registration)**
Jika Anda ingin menulis kode sendiri, Anda bisa menambahkan file `.py` ke folder `~/.nanopybot/custom_tools/`.
1. Buat file baru, misal `hello.py`.
2. Pastikan memiliki variabel `DESCRIPTION` dan fungsi `run(args)`.
   ```python
   DESCRIPTION = "Tool sederhana untuk menyapa"

   def run(args):
       name = args.get("name", "User")
       return f"Halo {name} dari file kustom!"
   ```
3. Restart bot atau jalankan perintah `nanopy`, tool akan otomatis terdaftar.

---

## 🏗️ Mekanisme Internal

NanoPyBot is designed with modularity in mind:
- **CLI**: Powered by `Typer` and `Rich`.
- **Memory**: JSON-based KV store for simplicity.
- **Scheduler**: `APScheduler` with `SQLAlchemy` (SQLite) persistence.
- **Provider**: `httpx` based OpenAI-compatible adapter.

For a detailed breakdown, see [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## 🛠️ Troubleshooting

- **Provider Error (401)**: Double-check your API key in `config.json` or `~/.nanopybot/config.json`.
- **Command Not Found**: Ensure you have activated the virtual environment (`source .venv/bin/activate`) and installed the package (`pip install -e .`).
- **Invalid Cron**: Ensure you use the 5-field format (`* * * * *`).
- **Persistence**: Jika jadwal atau memori tidak tersimpan, pastikan program memiliki izin tulis (write permission) di folder project atau `~/.nanopybot/`.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
*Created with ❤️ by [Kiki Ginanjar](https://github.com/kikiginanjar16)*
