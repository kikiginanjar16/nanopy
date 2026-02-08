import re

FEEDBACK_HINT = re.compile(
    r"(jangan|hindari|stop|salah|tolong|harap|selalu|wajib|jangan pernah|please|avoid|do not|always)",
    re.I,
)

PREFIXES = (
    "ingat",
    "catat",
    "rule:",
    "aturan:",
    "note:",
)


def normalize_feedback(text: str) -> str:
    cleaned = " ".join(text.strip().split())
    return cleaned[:300]


def detect_feedback(text):
    if not text:
        return None

    normalized = normalize_feedback(text)
    lowered = normalized.lower()

    for p in PREFIXES:
        if lowered.startswith(p):
            payload = normalized[len(p):].strip(" :,-")
            return payload or normalized

    if FEEDBACK_HINT.search(normalized):
        return normalized

    return None
