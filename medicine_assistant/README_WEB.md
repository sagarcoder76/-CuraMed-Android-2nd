# Medicine Assistant — CuraMed Web UI

This version keeps the existing SQLite medicine database/search modules and adds a mobile-first CuraMed web interface plus persistent medicine reminders.

## Features
- CuraMed UI based on the supplied `index.html`
- Local medicine search using the existing database
- Add daily, weekday, or one-time reminders
- Enable/disable and delete reminders
- Upcoming dose card
- Take Now / Snooze 15m
- Dose history and logs
- Browser notification permission + audible alert while the web app is active
- All reminder data stays in the local SQLite database

## Run on Mac
```bash
cd medicine_assistant
python3 app.py
```
Then open `http://127.0.0.1:5000` in a browser.

No third-party Python package is required for the web server; it uses Python's standard library and the existing project modules.

## Important reminder limitation
A normal browser page cannot guarantee a true Android alarm when the app is completely killed or the device is asleep. For a production Android APK, wrap the UI with a native Android/Capacitor layer and use Android local notifications/AlarmManager. The project is structured so the reminder API and UI can be reused for that APK.
