"""
test_phase2.py
--------------
Phase 2 test suite: the Medicine Details Page + "Explain Simply".

Run from the project folder:
    cd medicine_assistant
    python -m unittest discover tests -v
"""

import unittest

from database.models import Medicine
from medicine.information import (
    format_details_page,
    DISCLAIMER,
    NOT_AVAILABLE,
)
from medicine.search import EXACT, POSSIBLE
from utils.simple_language import explain_in_simple_words, find_simple_explanations
from tests.test_phase1 import Phase1TestCase  # reuse the seeded temp database


def get_dolo(self):
    """Fetch the seeded demo Paracetamol 500 row as a Medicine object."""
    from medicine.search import search_medicines
    results = search_medicines(self.conn, "Paracetamol 500")
    return results[0].medicine


class TestExplainSimply(unittest.TestCase):

    def test_medical_terms_get_simple_explanations(self):
        simple = explain_in_simple_words("Analgesic and antipyretic")
        self.assertIn("pain-relieving", simple)
        self.assertIn("fever-reducing", simple)

    def test_case_insensitive_lookup(self):
        simple = explain_in_simple_words("ANTIBIOTIC of the penicillin group")
        self.assertIn("bacterial infections", simple)

    def test_plain_text_returns_empty_string(self):
        self.assertEqual(explain_in_simple_words("just some ordinary text"), "")

    def test_empty_input_is_safe(self):
        self.assertEqual(explain_in_simple_words(""), "")
        self.assertEqual(find_simple_explanations(None), [])

    def test_longer_term_wins_over_shorter(self):
        pairs = find_simple_explanations("Oral rehydration salts (ORS)")
        terms = [term for term, _ in pairs]
        self.assertIn("oral rehydration salts", terms)
        self.assertNotIn("oral rehydration", terms)  # already covered


class TestDetailsPage(Phase1TestCase):
    """Runs against the same seeded temporary DB as Phase 1."""

    def setUp(self):
        super().setUp()
        self.medicine = get_dolo(self)
        self.page = format_details_page(self.medicine, EXACT)

    def test_all_required_sections_exist(self):
        for section in [
            "WHAT IS THIS MEDICINE?",
            "WHAT IS IT USED FOR?",
            "HOW IS IT GENERALLY TAKEN?",
            "SAFETY & WARNINGS",
            "SIDE EFFECTS",
            "SERIOUS WARNING SIGNS",
            "DISCLAIMER",
        ]:
            self.assertIn(section, self.page, f"Missing section: {section}")

    def test_name_and_confidence_are_shown(self):
        self.assertIn("Paracetamol 500", self.page)
        self.assertIn("EXACT MATCH", self.page)

    def test_possible_match_is_labelled_carefully(self):
        page = format_details_page(self.medicine, POSSIBLE)
        self.assertIn("POSSIBLE MATCH", page)
        self.assertIn("verify the name on the packaging", page)

    def test_uses_appear_as_bullets(self):
        self.assertIn("- Fever", self.page)

    def test_warnings_are_all_listed(self):
        for label in ["Pregnancy", "Breastfeeding", "Children",
                      "Elderly people", "Kidney problems",
                      "Liver problems", "Food / alcohol"]:
            self.assertIn(label, self.page)

    def test_general_info_vs_doctor_note_is_present(self):
        self.assertIn("GENERAL information only", self.page)
        self.assertIn("doctor", self.page)
        self.assertIn("pharmacist", self.page)

    def test_serious_warnings_are_marked(self):
        self.assertIn("!!", self.page)
        self.assertIn("get medical help", self.page)

    def test_disclaimer_and_emergency_note_present(self):
        self.assertIn(DISCLAIMER, self.page)
        self.assertIn("overdose", self.page.lower())

    def test_explain_simply_appears_in_page(self):
        self.assertIn("In simple words:", self.page)

    def test_demo_source_label_visible(self):
        self.assertIn("DEMO", self.page)


class TestNoFabrication(unittest.TestCase):
    """A medicine with NO data must show blanks, never invented content."""

    def test_empty_medicine_shows_not_available_everywhere(self):
        empty = Medicine(id=99, medicine_name="UnknownMed")
        page = format_details_page(empty, EXACT)
        self.assertIn("UnknownMed", page)          # name always shown
        self.assertGreaterEqual(page.count(NOT_AVAILABLE), 5)  # many blanks
        # And no fabricated medical words:
        self.assertNotIn("cures", page.lower())
        self.assertNotIn("safe to use", page.lower())

    def test_missing_warnings_do_not_crash(self):
        empty = Medicine(id=100, medicine_name="BareMed")
        page = format_details_page(empty, EXACT)
        self.assertIn("SAFETY & WARNINGS", page)


if __name__ == "__main__":
    unittest.main()
