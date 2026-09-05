"""
models.py
---------
Defines the `Medicine` dataclass: a plain Python object that mirrors one
row of the `medicines` table. The rest of the app works with `Medicine`
objects instead of raw database rows — this keeps the code beginner-friendly
and makes the database swappable later.
"""

from dataclasses import dataclass, fields
from typing import List, Optional


def split_field(value: Optional[str]) -> List[str]:
    """
    Convert a ';'-separated database text field into a clean Python list.

    Example: "Fever; Headache; Body pain" -> ["Fever", "Headache", "Body pain"]
    Empty/None values become an empty list — the app never invents content.
    """
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


@dataclass
class Medicine:
    # Only `id` and `medicine_name` are mandatory. Everything else is
    # Optional: if the database has no verified value, it stays None and
    # the UI will show "not available" instead of guessing.
    id: int
    medicine_name: str
    brand_name: Optional[str] = None
    generic_name: Optional[str] = None
    active_ingredient: Optional[str] = None
    strength: Optional[str] = None
    category: Optional[str] = None
    common_uses: Optional[str] = None
    general_usage: Optional[str] = None
    administration: Optional[str] = None
    common_side_effects: Optional[str] = None
    serious_warnings: Optional[str] = None
    pregnancy_warning: Optional[str] = None
    breastfeeding_warning: Optional[str] = None
    children_warning: Optional[str] = None
    elderly_warning: Optional[str] = None
    kidney_warning: Optional[str] = None
    liver_warning: Optional[str] = None
    drug_interactions: Optional[str] = None
    food_interactions: Optional[str] = None
    storage_information: Optional[str] = None
    manufacturer: Optional[str] = None
    dosage_form: Optional[str] = None
    source: Optional[str] = None
    last_updated: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "Medicine":
        """Build a Medicine from a sqlite3.Row, ignoring unexpected columns."""
        column_names = {f.name for f in fields(cls)}
        data = {key: value for key, value in dict(row).items() if key in column_names}
        return cls(**data)

    # --- Convenience helpers: list versions of ';'-separated fields ---
    def uses_list(self) -> List[str]:
        return split_field(self.common_uses)

    def side_effects_list(self) -> List[str]:
        return split_field(self.common_side_effects)

    def is_demo_data(self) -> bool:
        """True while the row is labelled demo/unverified data."""
        return bool(self.source) and "DEMO" in self.source.upper()
