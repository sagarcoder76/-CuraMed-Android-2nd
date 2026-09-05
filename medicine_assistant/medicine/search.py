"""
search.py
---------
Phase 1 medicine search.

How it works:
  1. The user's query is normalized (lowercase, cleaned spaces).
  2. Every medicine's name / brand / generic / active ingredient is
     normalized the same way.
  3. A medicine is an:
       EXACT match    -> normalized query EQUALS one of its names
       POSSIBLE match -> normalized query is CONTAINED IN one of its names
  4. Exact matches are always returned before possible matches.

Safety design:
  * Blank/empty queries return nothing (the UI shows a helpful message).
  * Unknown names return an empty list — the app NEVER guesses.
  * Spelling mistakes return nothing in Phase 1. Fuzzy matching is a
    Phase 4 feature, and even there it will only ever say "possible match".
"""

import sqlite3
from dataclasses import dataclass
from typing import List

from database.database import fetch_all_medicines
from database.models import Medicine
from utils.text_cleaner import normalize_text

EXACT = "exact"
POSSIBLE = "possible"


@dataclass
class SearchMatch:
    """One search result: the medicine plus HOW confidently it matched."""
    medicine: Medicine
    match_type: str  # EXACT or POSSIBLE


def _searchable_names(medicine: Medicine) -> List[str]:
    """All normalized names a medicine can be searched by."""
    raw_names = [
        medicine.medicine_name,
        medicine.brand_name,
        medicine.generic_name,
        medicine.active_ingredient,
    ]
    return [normalize_text(name) for name in raw_names if name]


def search_medicines(connection: sqlite3.Connection, query: str) -> List[SearchMatch]:
    """
    Search the database for `query`.

    Returns a list of SearchMatch objects: exact matches first, then
    possible matches (both sorted alphabetically). Returns [] for empty
    or unknown queries — never a wild guess.
    """
    normalized_query = normalize_text(query)
    if not normalized_query:
        return []

    exact_matches: List[SearchMatch] = []
    possible_matches: List[SearchMatch] = []

    for medicine in fetch_all_medicines(connection):
        names = _searchable_names(medicine)
        if normalized_query in names:
            exact_matches.append(SearchMatch(medicine, EXACT))
        elif any(normalized_query in name for name in names):
            possible_matches.append(SearchMatch(medicine, POSSIBLE))

    exact_matches.sort(key=lambda m: m.medicine.medicine_name.lower())
    possible_matches.sort(key=lambda m: m.medicine.medicine_name.lower())
    return exact_matches + possible_matches
