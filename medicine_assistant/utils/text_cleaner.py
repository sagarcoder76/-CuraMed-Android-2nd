"""
text_cleaner.py
---------------
Small, reusable text-cleaning helpers.

Phase 1 use: normalizing medicine names so that
    "Paracetamol"  ==  "paracetamol"  ==  "  PARACETAMOL   "
Later phases (OCR) will add more aggressive cleaning here.
"""

import re

# Pre-compiled pattern for "one or more whitespace characters".
_WHITESPACE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """
    Return a normalized version of `text` for safe comparison.

    Rules:
      1. Convert to lowercase          -> "PARACETAMOL" -> "paracetamol"
      2. Remove leading/trailing space -> "  dolo 650 " -> "dolo 650"
      3. Collapse repeated inner space -> "dolo   650"  -> "dolo 650"

    Note: we intentionally do NOT remove characters or 'fix' spelling here.
    Spelling tolerance (fuzzy matching) is a Phase 4 feature and must stay
    clearly labelled as "possible match" — never a confident guess.
    """
    if text is None:
        return ""
    return _WHITESPACE.sub(" ", str(text)).strip().lower()
