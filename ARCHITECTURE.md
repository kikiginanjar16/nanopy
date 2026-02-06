# Architecture Overview

Dokumen ini menjelaskan arsitektur aplikasi `nanopybot_selflearn_cron` berdasarkan implementasi saat ini.

## System Context

```mermaid
flowchart LR
    U["User (CLI)"] --> C["Typer CLI (`nanopybot/cli.py`)"]
    C --> A["Agent (`nanopybot/agent.py`)"]
    A --> P["OpenAI-Compatible Provider (`nanopybot/provider.py`)"]
    A --> M["Memory Store (`nanopybot/memory.py`)"]
    A --> T["Tool Registry (`nanopybot/tools.py`)"]
    C --> S["Scheduler (`nanopybot/scheduler.py`)"]
    S --> J["Cron Runner (`nanopybot/cron_runner.py`)"]
    J --> A
```

## Core Components

- `nanopybot/cli.py`
  - Entry point command `nanopy`.
  - Menyediakan command:
    - `agent <message>`
    - `cron-add --name --message --cron`
    - `cron-run`
  - Menangani error provider (`ProviderError`) untuk command `agent`.

- `nanopybot/config.py`
  - Load dan bootstrap konfigurasi dari `~/.nanopybot/config.json`.
  - Menyimpan konfigurasi provider (`api_key`, `base_url`, `model`), memory path, scheduler db path.

- `nanopybot/agent.py`
  - Orkestrator utama request.
  - Deteksi feedback user via `detect_feedback`.
  - Simpan feedback terakhir ke memory key `rules.last`.
  - Menyuntikkan `rules.last` ke system prompt untuk request selanjutnya.
  - Menangani jalur tool call lokal dengan format pesan `tool:<name> <json_args>`.

- `nanopybot/provider.py`
  - Adapter HTTP ke endpoint OpenAI-compatible `/chat/completions`.
  - Input: list `ChatMessage`.
  - Output: `choices[0].message.content`.
  - Error handling:
    - HTTP status error -> `ProviderError` dengan detail response.
    - Network/request error -> `ProviderError`.
    - Response format invalid -> `ProviderError`.

- `nanopybot/memory.py`
  - KV store berbasis file JSON.
  - Operasi utama: `get`, `put`, `delete`, `keys`.
  - Persistence ke file pada setiap update.

- `nanopybot/tools.py`
  - Registry tool sederhana (`register`, `has`, `call`).
  - Tool default saat ini:
    - `time`: mengembalikan Unix timestamp.

- `nanopybot/scheduler.py`
  - Inisialisasi `APScheduler` dengan `SQLAlchemyJobStore` (SQLite).
  - Parser cron expression 5 field (`minute hour day month day_of_week`) + validasi format.

- `nanopybot/cron_runner.py`
  - Job function untuk scheduler.
  - Membaca payload JSON, lalu menjalankan agent secara async (`asyncio.run`).

## Runtime Flows

### 1) Direct Chat Flow (`nanopy agent "..."`)

```mermaid
sequenceDiagram
    participant User
    participant CLI as CLI
    participant Agent as Agent
    participant Memory as MemoryStore
    participant Provider as Provider

    User->>CLI: nanopy agent "message"
    CLI->>Agent: run(message)
    Agent->>Memory: detect/store feedback (optional)
    Agent->>Memory: get("rules.last")
    Agent->>Provider: chat(messages)
    Provider-->>Agent: content / error
    Agent-->>CLI: response
    CLI-->>User: print output
```

### 2) Tool Call Flow (`nanopy agent 'tool:time {}'`)

```mermaid
sequenceDiagram
    participant User
    participant CLI as CLI
    participant Agent as Agent
    participant Tools as ToolRegistry

    User->>CLI: nanopy agent "tool:time {}"
    CLI->>Agent: run(message)
    Agent->>Tools: has("time")
    Agent->>Tools: call("time", {})
    Tools-->>Agent: unix timestamp
    Agent-->>CLI: [tool:time] <value>
    CLI-->>User: print output
```

### 3) Scheduled Flow (`nanopy cron-add` + `nanopy cron-run`)

```mermaid
sequenceDiagram
    participant User
    participant CLI as CLI
    participant Scheduler as APScheduler
    participant Runner as cron_runner
    participant Agent as Agent

    User->>CLI: nanopy cron-add --name ... --cron ...
    CLI->>Scheduler: add_job(run_agent_job, CronTrigger)
    Scheduler-->>CLI: job stored in sqlite

    User->>CLI: nanopy cron-run
    CLI->>Scheduler: start()
    Scheduler->>Runner: execute run_agent_job(payload_json) on schedule
    Runner->>Agent: build_agent().run(message)
```

## Data & Storage

- Config: `~/.nanopybot/config.json`
- Memory: `~/.nanopybot/memory.json`
- Scheduler job store: `~/.nanopybot/jobs.sqlite`

## Current Architectural Characteristics

- Sederhana, file-based persistence, mudah dijalankan lokal.
- Provider terpisah sebagai adapter, memudahkan ganti backend kompatibel OpenAI.
- Scheduler persisten via SQLite (job tetap ada setelah restart proses).
- Tool-calling masih berbasis parsing string sederhana (belum function-calling native model).
- Memory belum punya rotasi/TTL/locking; cocok untuk skala kecil/single-process.
