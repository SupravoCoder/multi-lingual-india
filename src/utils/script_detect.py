import re
from typing import Optional

# Unicode ranges for scripts
RANGES = {
    "devanagari": (0x0900, 0x097F),  # Hindi
    "bengali": (0x0980, 0x09FF),     # Bengali
    "tamil": (0x0B80, 0x0BFF),       # Tamil
}

SCRIPT_LABELS = {
    "devanagari": "hi",
    "bengali": "bn",
    "tamil": "ta",
}


def detect_script(text: str) -> Optional[str]:
    """Return 'hi'|'bn'|'ta' if a dominant script is detected, else None.
    Uses simple counting of chars in script-specific Unicode ranges.
    """
    counts = {k: 0 for k in RANGES.keys()}
    for ch in text:
        cp = ord(ch)
        for name, (lo, hi) in RANGES.items():
            if lo <= cp <= hi:
                counts[name] += 1
                break
    if not any(counts.values()):
        return None
    dominant = max(counts.items(), key=lambda x: x[1])[0]
    return SCRIPT_LABELS[dominant]


def is_code_mixed(text: str) -> bool:
    """Heuristic: returns True if multiple scripts appear with significant counts."""
    counts = {k: 0 for k in RANGES.keys()}
    for ch in text:
        cp = ord(ch)
        for name, (lo, hi) in RANGES.items():
            if lo <= cp <= hi:
                counts[name] += 1
                break
    nonzero = [c for c in counts.values() if c > 0]
    return len(nonzero) > 1
