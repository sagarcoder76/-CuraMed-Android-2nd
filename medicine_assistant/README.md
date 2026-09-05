# 💊 Medicine Assistant

A **privacy-first, offline** medicine information & identification app in Python.
Built for people with little or no medical knowledge.

> ⚠️ **Disclaimer:** This application provides general medicine information for
> educational purposes only. It does not replace advice from a qualified doctor
> or pharmacist. Never use it for diagnosis. The bundled database is **DEMO data**,
> not verified medical information.

## Guiding principles

1. **No paid AI APIs** — SQLite + rule-based logic + local OCR + offline TTS only.
2. **Never guess** — unknown medicines, unreadable names, and missing expiry
   dates produce honest "could not identify" messages, not inventions.
3. **Everything stays on the device** — no data leaves the user's computer.

## Current status

| Phase | Scope | Status |
|---|---|---|
| 1 | SQLite database + medicine search | ✅ Done |
| 2 | Medicine details page ("Explain Simply", warnings, side effects) | ✅ Done |
| 3 | OCR image scanning (Tesseract + OpenCV) | ⬜ |
| 4 | Fuzzy name matching | ⬜ |
| 5 | Manufacturing/expiry extraction & status | ⬜ |
| 6 | Text-to-Speech (pyttsx3) | ⬜ |
| 7 | Hindi/English support | ⬜ |
| 8 | Medicine history | ⬜ |
| 9 | CustomTkinter UI | ⬜ |
| 10 | Full-app testing | ⬜ |

## Project structure

```
medicine_assistant/
├── main.py                  # Phase 1 console app (UI replaced in Phase 9)
├── database/
│   ├── database.py          # connection, schema, insert, fetch
│   ├── models.py            # Medicine dataclass
│   ├── seed_data.py         # clearly-labelled DEMO dataset
│   └── medicine_database.db # auto-created on first run (not in git)
├── medicine/
│   └── search.py            # exact / possible matching (no guessing)
├── utils/
│   └── text_cleaner.py      # text normalization
├── tests/
│   └── test_phase1.py       # 14 tests (standard-library unittest)
├── requirements.txt         # grouped by phase
└── README.md
```

## Run it (Phase 1)

No installs needed — only Python 3.10+ with its standard library:

```bash
cd medicine_assistant
python main.py
```

## Run the tests

```bash
cd medicine_assistant
python -m unittest discover tests -v
```

## Replacing demo data with verified data (future)

`database/seed_data.py` is deliberately small and labelled
`DEMO DATA (unverified...)`. Before real use, import data from reliable,
official medicine references into the same `medicines` table
(e.g. via a reviewed CSV import script), and keep the `source` and
`last_updated` columns truthful for every row.

## Web UI / Reminders
Run `python3 app.py` to launch the new CuraMed mobile web interface. It includes persistent medicine reminders, dose logging, history, and local medicine search.
