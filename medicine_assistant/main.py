"""
main.py — Medicine Assistant (Phase 1 + Phase 2: console version)
------------------------------------------------------------------
What it does now:
  * Creates the local SQLite database and seeds DEMO data     (Phase 1)
  * Search by name / brand / generic                          (Phase 1)
  * Open a full MEDICINE DETAILS PAGE with warnings,
    side effects, "Explain Simply" and the disclaimer         (Phase 2)

Later phases (OCR, voice, GUI) plug into the same modules.

Run from inside the project folder:
    cd medicine_assistant
    python main.py        (Mac/Linux: python3 main.py)
"""

from database.database import (
    get_connection,
    initialize_database,
    fetch_all_medicines,
    DB_PATH,
)
from database.seed_data import seed_demo_data
from medicine.search import search_medicines, EXACT
from medicine.information import format_details_page, DISCLAIMER


def setup_database():
    """Open the database, create the table, and seed demo data if empty."""
    connection = get_connection(DB_PATH)
    initialize_database(connection)
    inserted = seed_demo_data(connection)
    if inserted:
        print(f"(Loaded {inserted} DEMO medicines for development.)")
    return connection


def print_result_list(results) -> None:
    """Show a short numbered list of search results."""
    print(f"\nFound {len(results)} result(s):")
    for number, match in enumerate(results, start=1):
        medicine = match.medicine
        if match.match_type == EXACT:
            tag = "EXACT MATCH"
        else:
            tag = "possible match - please confirm"
        print(f"  [{number}] {medicine.medicine_name} "
              f"({medicine.generic_name or 'generic unknown'}) - {tag}")


def do_search(connection) -> None:
    """Search, then let the user OPEN one result to see its details page."""
    query = input("\nEnter medicine name (or brand/generic): ").strip()
    results = search_medicines(connection, query)

    if not query:
        print("Please type a medicine name to search.")
        return
    if not results:
        # Deliberately NOT a guess — honest "not found".
        print(f"\nNo medicine matching '{query}' was found in the database.")
        print("Please check the spelling, or ask a pharmacist for help.")
        return

    print_result_list(results)

    choice = input(
        "\nEnter the number of a medicine to see its full details "
        "(or press Enter to go back): "
    ).strip()

    if not choice:
        return
    if not choice.isdigit() or not 1 <= int(choice) <= len(results):
        print("That number is not on the list - going back to the menu.")
        return

    selected = results[int(choice) - 1]
    print()
    print(format_details_page(selected.medicine, selected.match_type))


def do_list_all(connection) -> None:
    """Print the names of everything currently in the database."""
    medicines = fetch_all_medicines(connection)
    print(f"\n{len(medicines)} medicine(s) in the local database:")
    for medicine in medicines:
        print(f"  - {medicine.medicine_name} ({medicine.generic_name or 'generic unknown'})")


def main() -> None:
    print("=" * 62)
    print("        MEDICINE ASSISTANT  (Phase 2 - Details Page)")
    print("=" * 62)
    print(DISCLAIMER)
    print("=" * 62)

    connection = setup_database()

    menu = (
        "\nWhat would you like to do?\n"
        "  [1] Search medicine\n"
        "  [2] List all medicines in the database\n"
        "  [3] Quit\n"
        "Choose 1, 2 or 3: "
    )

    while True:
        choice = input(menu).strip()
        if choice == "1":
            do_search(connection)
        elif choice == "2":
            do_list_all(connection)
        elif choice == "3":
            print("Goodbye. Stay safe!")
            break
        else:
            print("Please enter 1, 2 or 3.")

    connection.close()


if __name__ == "__main__":
    main()
