"""
simple_language.py  ("Explain Simply" feature - Phase 2)
---------------------------------------------------------
Rule-based simple explanations of medical terms.

IMPORTANT DESIGN RULE: these explanations come from this fixed,
human-written dictionary — NOT from any AI service. Nothing is
generated on the fly, so nothing can be invented.

Phase 7 will add a Hindi layer on top of the same dictionary
(each term will get {"en": ..., "hi": ...}).
"""

import re
from typing import Dict, List, Tuple

# Medical term (lowercase) -> simple everyday explanation.
# Keep language at roughly a 10-year-old's reading level.
SIMPLE_EXPLANATIONS: Dict[str, str] = {
    "non-steroidal anti-inflammatory": "a medicine for pain and swelling (it is NOT a steroid)",
    "nsaid": "a medicine for pain and swelling",
    "analgesic": "a pain-relieving medicine",
    "antipyretic": "a fever-reducing medicine",
    "antihistamine": "an anti-allergy medicine",
    "antibiotic": "a medicine that fights bacterial infections (it does NOT work on viruses like cold/flu)",
    "penicillin": "a common family of antibiotics",
    "oral rehydration salts": "a drink mix that replaces water and body salts lost in diarrhoea or vomiting",
    "oral rehydration": "replaces water and body salts lost by the body",
    "electrolyte": "essential body salts (like sodium and potassium)",
    "dosage form": "the physical form of the medicine (tablet, capsule, syrup, etc.)",
    "generic name": "the common medical name of the active ingredient",
    "active ingredient": "the main chemical in the medicine that does the work",
    "contraindication": "a situation where the medicine should NOT be used",
    "drug interaction": "when one medicine changes the effect of another medicine",
}


def find_simple_explanations(text: str) -> List[Tuple[str, str]]:
    """
    Scan `text` for known medical terms and return a list of
    (term, simple_explanation) pairs for each term found.

    Longer terms are checked first, so "oral rehydration salts" wins
    over "oral rehydration" if both appear.
    """
    if not text:
        return []

    found: List[Tuple[str, str]] = []
    lowered = text.lower()
    already_covered = ""

    for term in sorted(SIMPLE_EXPLANATIONS, key=len, reverse=True):
        # \b = word boundary, so "nsaid" does not match inside another word.
        if re.search(r"\b" + re.escape(term) + r"\b", lowered):
            if term not in already_covered:  # skip terms already inside a longer match
                found.append((term, SIMPLE_EXPLANATIONS[term]))
                already_covered += " " + term
    return found


def explain_in_simple_words(text: str) -> str:
    """
    Return a human-friendly "In simple words: ..." line for the medical
    terms found in `text`. Returns "" if there is nothing to explain.
    """
    pairs = find_simple_explanations(text)
    if not pairs:
        return ""
    parts = [f'"{term}" = {explanation}' for term, explanation in pairs]
    return "In simple words: " + "; ".join(parts) + "."
