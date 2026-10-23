"""Nettoyage des logs avant envoi au LLM : masquage des secrets et volume borne.

Les logs sont des donnees NON FIABLES : ils ne sont jamais executes ni interpretes
comme des instructions.
"""
import re

PATTERNS = [
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"), "[MASKED_GITHUB_TOKEN]"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "[MASKED_AWS_KEY]"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{10,}"), "Bearer [MASKED]"),
    (re.compile(r"(?i)(password|passwd|secret|token|api[_-]?key|authorization)(\"?\s*[:=]\s*\"?)[^\s\",}]+"),
     r"\1\2[MASKED]"),
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "[MASKED_EMAIL]"),
]


def mask_secrets(text: str) -> str:
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def bound_logs(lines, max_lines: int = 200, max_chars: int = 8000):
    """Garde les dernieres lignes et plafonne la taille totale."""
    kept = list(lines)[-max_lines:]
    out, total = [], 0
    for line in reversed(kept):
        line = mask_secrets(line.rstrip())[:500]
        if total + len(line) > max_chars:
            break
        out.append(line)
        total += len(line)
    return list(reversed(out))