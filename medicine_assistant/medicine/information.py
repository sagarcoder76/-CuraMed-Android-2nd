"""
information.py  (Phase 2 - the Medicine Details Page)
------------------------------------------------------
Takes ONE Medicine object and turns it into a complete, readable
details page with fixed sections:

    1. Name + identification confidence + source label
    2. What is this medicine?          (with "Explain Simply")
    3. What is it used for?
    4. How is it generally taken?      (general info vs doctor's advice)
    5. Safety & warnings
    6. Side effects (common + serious warning signs)
    7. Disclaimer

Phase 2 renders it as TEXT for the console. In Phase 9 the SAME
function's sections will be shown inside the CustomTkinter UI — the
content logic will not change.

Golden rules enforced here:
  * Missing data is shown as "Not available in the database."
    — never invented.
  * Serious warnings are clearly marked as warnings.
  * General information is always separated from the
    doctor/pharmacist's instructions.
"""

from typing import List, Optional, Tuple

from database.models import Medicine
from medicine.search import EXACT
from utils.simple_language import explain_in_simple_words

NOT_AVAILABLE = "Not available in the database."
LINE = "=" * 62
THIN_LINE = "-" * 62

DISCLAIMER = (
    "This application provides general medicine information for educational "
    "purposes only. It does not replace advice from a qualified doctor or "
    "pharmacist. Always check the medicine packaging and follow your "
    "healthcare professional's instructions."
)
URGENT_NOTE = (
    "For urgent symptoms, suspected overdose, or poisoning, seek immediate "
    "medical help. Do not rely on this application in an emergency."
)

# The warning fields, in a fixed display order with human-readable labels.
WARNING_FIELDS: List[Tuple[str, str]] = [
    ("pregnancy_warning", "Pregnancy"),
    ("breastfeeding_warning", "Breastfeeding"),
    ("children_warning", "Children"),
    ("elderly_warning", "Elderly people"),
    ("kidney_warning", "Kidney problems"),
    ("liver_warning", "Liver problems"),
    ("drug_interactions", "Interactions with other medicines"),
    ("food_interactions", "Food / alcohol"),
]


def _confidence_line(match_type: Optional[str]) -> str:
    """Human-readable identification confidence."""
    if match_type is None:
        return "Confidence: opened from history/manual selection"
    if match_type == EXACT:
        return "Confidence: EXACT MATCH"
    return "Confidence: POSSIBLE MATCH - please verify the name on the packaging"


def format_details_page(medicine: Medicine, match_type: Optional[str] = EXACT) -> str:
    """
    Build the full details page for `medicine` as one printable string.

    `match_type` is the search confidence (exact/possible) so the user
    always knows how sure the identification is.
    """
    out: List[str] = []
    add = out.append

    # ---------------- Header: name + confidence + source ----------------
    add(LINE)
    add(f"  {medicine.medicine_name}")
    add(LINE)
    add(f"  {_confidence_line(match_type)}")
    add(f"  Generic / active ingredient : {medicine.generic_name or NOT_AVAILABLE}")
    add(f"  Strength                    : {medicine.strength or NOT_AVAILABLE}")
    add(f"  Dosage form                 : {medicine.dosage_form or NOT_AVAILABLE}")
    add(f"  Manufacturer                : {medicine.manufacturer or NOT_AVAILABLE}")
    if medicine.is_demo_data():
        add("  [Source: DEMO data - unverified sample, development use only]")
    elif medicine.source:
        add(f"  [Source: {medicine.source} | last updated: {medicine.last_updated or 'unknown'}]")

    # ------------- Section 1: What is this medicine? (Explain Simply) ---
    add("")
    add(">> WHAT IS THIS MEDICINE?")
    add(THIN_LINE)
    if medicine.general_usage:
        add(f"  {medicine.general_usage}")
    elif medicine.category:
        add(f"  Category: {medicine.category}")
    else:
        add(f"  {NOT_AVAILABLE}")
    if medicine.category:
        add(f"  Official category: {medicine.category}")
        simple = explain_in_simple_words(medicine.category)
        if simple:
            add(f"  {simple}")   # <- the "Explain Simply" feature

    # ------------------- Section 2: What is it used for? ----------------
    add("")
    add(">> WHAT IS IT USED FOR?")
    add(THIN_LINE)
    uses = medicine.uses_list()
    if uses:
        for use in uses:
            add(f"  - {use}")
    else:
        add(f"  {NOT_AVAILABLE}")

    # ---------------- Section 3: How is it generally taken? -------------
    add("")
    add(">> HOW IS IT GENERALLY TAKEN?")
    add(THIN_LINE)
    add(f"  {medicine.administration or NOT_AVAILABLE}")
    add("")
    add("  NOTE: The above is GENERAL information only. Your doctor or")
    add("  pharmacist's instructions for YOU may be different - always")
    add("  follow their advice and the package label.")
    if medicine.storage_information:
        add(f"  Storage: {medicine.storage_information}")

    # ------------------- Section 4: Safety & warnings -------------------
    add("")
    add(">> SAFETY & WARNINGS  (!! read before use)")
    add(THIN_LINE)
    any_warning = False
    for field_name, label in WARNING_FIELDS:
        value = getattr(medicine, field_name, None)
        if value:
            add(f"  * {label}: {value}")
            any_warning = True
    if not any_warning:
        add(f"  {NOT_AVAILABLE}")

    # ----------------------- Section 5: Side effects --------------------
    add("")
    add(">> SIDE EFFECTS")
    add(THIN_LINE)
    effects = medicine.side_effects_list()
    if effects:
        add("  Common (usually mild):")
        for effect in effects:
            add(f"    - {effect}")
    else:
        add(f"  {NOT_AVAILABLE}")
    add("")
    add("  !! SERIOUS WARNING SIGNS - stop and get medical help:")
    add(f"     {medicine.serious_warnings or NOT_AVAILABLE}")

    # --------------------------- Disclaimer -----------------------------
    add("")
    add(LINE)
    add(f"  DISCLAIMER: {DISCLAIMER}")
    add(f"  {URGENT_NOTE}")
    add(LINE)

    return "\n".join(out)
