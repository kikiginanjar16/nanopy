# TODO

## High Priority

- [x] Fix circular import between CLI and cron runner.
  - File: `/Users/kiki/Downloads/nanopybot_selflearn_cron/nanopybot/cli.py`
  - File: `/Users/kiki/Downloads/nanopybot_selflearn_cron/nanopybot/cron_runner.py`
  - Action: remove unused `run_agent_job` import from `cli.py` so cron job path import is safe.

- [x] Improve provider error handling for API/network failures.
  - File: `/Users/kiki/Downloads/nanopybot_selflearn_cron/nanopybot/provider.py`
  - Action: catch `httpx` errors and return clear, user-friendly error messages.

- [x] Add cron expression validation and clear error messages.
  - File: `/Users/kiki/Downloads/nanopybot_selflearn_cron/nanopybot/scheduler.py`
  - Action: validate 5-part cron format before building `CronTrigger`.

## Medium Priority

- [x] Fix typing in memory model (`any` -> `Any`).
  - File: `/Users/kiki/Downloads/nanopybot_selflearn_cron/nanopybot/memory.py`
  - Action: import `Any` from `typing` and update annotation.

- [x] Make self-learning actually influence future responses.
  - File: `/Users/kiki/Downloads/nanopybot_selflearn_cron/nanopybot/agent.py`
  - Action: inject saved feedback (`rules.last`) into system prompt.

- [x] Integrate tools registry into agent flow or remove dead code.
  - File: `/Users/kiki/Downloads/nanopybot_selflearn_cron/nanopybot/tools.py`
  - File: `/Users/kiki/Downloads/nanopybot_selflearn_cron/nanopybot/agent.py`
  - Action: implement minimal tool-calling path, or remove unused tool layer.

## Documentation

- [x] Improve README robustness and standardize filename.
  - File: `/Users/kiki/Downloads/nanopybot_selflearn_cron/README.md`
  - Action: rename to `README.md`, standardize `python3` usage, add troubleshooting section.

## Testing

- [ ] Add baseline automated tests.
  - Suggested scope:
    - `parse_cron` validation cases
    - `detect_feedback` behavior
    - `MemoryStore` put/get/delete
    - `provider.chat` with mocked HTTP responses
