"""
test_phase1.py
--------------
Phase 1 test suite. Uses only the Python standard library (unittest),
so it runs with no extra installs:

    cd medicine_assistant
    python -m unittest discover tests -v

Every test uses a TEMPORARY database file, so the real
medicine_database.db is never touched by tests.
"""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from database.database import (
    get_connection,
    initialize_database,
    count_medicines,
    fetch_all_medicines,
)
from database.seed_data import seed_demo_data, SAMPLE_MEDICINES
from medicine.search import search_medicines, EXACT, POSSIBLE


class Phase1TestCase(unittest.TestCase):
    """Base class: gives every test a fresh, seeded temporary database."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_medicines.db"
        self.conn = get_connection(self.db_path)
        initialize_database(self.conn)
        seed_demo_data(self.conn)

    def tearDown(self):
        self.conn.close()
        self.temp_dir.cleanup()


class TestDatabase(Phase1TestCase):

    def test_table_is_created(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='medicines'"
        )
        self.assertEqual(cursor.fetchone()[0], "medicines")

    def test_demo_data_is_seeded(self):
        self.assertEqual(count_medicines(self.conn), len(SAMPLE_MEDICINES))
        self.assertGreater(len(SAMPLE_MEDICINES), 0)

    def test_seeding_twice_does_not_duplicate(self):
        inserted_again = seed_demo_data(self.conn)
        self.assertEqual(inserted_again, 0)
        self.assertEqual(count_medicines(self.conn), len(SAMPLE_MEDICINES))

    def test_demo_rows_are_clearly_labelled(self):
        """Safety: no demo row may look like verified medical data."""
        for medicine in fetch_all_medicines(self.conn):
            self.assertTrue(
                medicine.is_demo_data(),
                f"'{medicine.medicine_name}' is missing the DEMO source label!",
            )


class TestSearch(Phase1TestCase):

    def test_exact_name_search(self):
        results = search_medicines(self.conn, "Dolo 650")
        self.assertEqual(results[0].match_type, EXACT)
        self.assertEqual(results[0].medicine.medicine_name, "Dolo 650")

    def test_search_is_case_insensitive(self):
        expected = ["PARACETAMOL", "paracetamol", "Paracetamol"]
        for spelling in expected:
            results = search_medicines(self.conn, spelling)
            exact = [m for m in results if m.match_type == EXACT]
            self.assertTrue(exact, f"'{spelling}' should find an exact match")

    def test_search_ignores_extra_spaces(self):
        results = search_medicines(self.conn, "   paracetamol    ")
        self.assertTrue(any(m.match_type == EXACT for m in results))

    def test_search_by_brand_name(self):
        results = search_medicines(self.conn, "crocin 500 (demo example)")
        self.assertEqual(results[0].match_type, EXACT)
        self.assertEqual(results[0].medicine.generic_name, "Paracetamol")

    def test_search_by_generic_name_finds_brands(self):
        """Searching the generic 'ibuprofen' must also find the brand row."""
        results = search_medicines(self.conn, "Ibuprofen")
        names = [m.medicine.medicine_name for m in results]
        self.assertIn("Ibuprofen 400", names)

    def test_partial_name_is_only_a_possible_match(self):
        results = search_medicines(self.conn, "paracet")
        self.assertTrue(results, "Partial name should return candidates")
        self.assertTrue(all(m.match_type == POSSIBLE for m in results))

    def test_unknown_medicine_returns_nothing(self):
        results = search_medicines(self.conn, "zzqx-not-a-medicine")
        self.assertEqual(results, [])

    def test_empty_search_returns_nothing(self):
        self.assertEqual(search_medicines(self.conn, ""), [])
        self.assertEqual(search_medicines(self.conn, "     "), [])

    def test_spelling_mistake_is_not_guessed(self):
        """Phase 1 must never pretend a typo is a confident match."""
        results = search_medicines(self.conn, "paracetamoll")
        self.assertEqual(results, [])
        exact = [m for m in results if m.match_type == EXACT]
        self.assertEqual(exact, [])

    def test_exact_matches_come_before_possible(self):
        results = search_medicines(self.conn, "paracetamol")
        types = [m.match_type for m in results]
        self.assertEqual(types, sorted(types, key=lambda t: t != EXACT))


class TestErrorHandling(unittest.TestCase):

    def test_search_on_closed_connection_raises_error(self):
        """Database errors must surface loudly, not silently return junk."""
        conn = get_connection(Path(tempfile.mkdtemp()) / "err.db")
        initialize_database(conn)
        conn.close()
        with self.assertRaises(sqlite3.ProgrammingError):
            search_medicines(conn, "paracetamol")


if __name__ == "__main__":
    unittest.main()
