# nanopybot_selflearn_cron

Asisten AI ringan dengan memori sederhana dan scheduler berbasis cron.

## Prasyarat

- Python 3.10+
- API key untuk provider yang kompatibel OpenAI

## Instalasi

```bash
cd nanopy
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python3 -m pip install --upgrade pip
pip install -e .
```

## Konfigurasi

Saat pertama kali dijalankan, file konfigurasi akan dibuat di:
`~/.nanopybot/config.json`

Isi minimal yang perlu diubah:

```json
{
  "provider": {
    "api_key": "ISI_API_KEY_ANDA",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4.1-mini"
  }
}
```

## Menjalankan Agent

```bash
nanopy agent "halo"
```

Jika ada feedback seperti `jangan jawab panjang`, aturan terakhir akan disimpan dan dipakai pada prompt berikutnya.

## Menjalankan Tool (Built-in)

Format pesan untuk tool:

```text
tool:<nama_tool> <json_args>
```

Contoh tool bawaan (`time`):

```bash
nanopy agent 'tool:time {}'
```

## Menambah Job Cron

```bash
nanopy cron-add --name daily --message "ringkas agenda hari ini" --cron "0 7 * * *"
```

## Menjalankan Scheduler

```bash
nanopy cron-run
```

## Troubleshooting

- `ModuleNotFoundError`:
  - Pastikan virtual environment sudah aktif.
  - Jalankan ulang `pip install -e .`.
- `Provider error: HTTP 401`:
  - Cek `provider.api_key` di `~/.nanopybot/config.json`.
- `Invalid cron expression`:
  - Gunakan format 5 bagian: `minute hour day month day_of_week`.
  - Contoh valid: `0 7 * * *`.
