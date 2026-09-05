# CuraMed Android — feature-complete build

This version keeps the existing CuraMed UI and adds working Android features:

- Native Android camera capture using Capacitor Camera.
- Gallery image selection.
- Medicine-label OCR using Tesseract.js.
- OCR text can be matched against the bundled medicine library.
- A matched scan can pre-fill the reminder form.
- Medicine reminders and dose history stored locally.
- Native Android local notifications.
- Exact-alarm permission support.
- Daily reminders are scheduled for a rolling 30 days; weekday reminders for 28 occurrences.
- Snooze 15 minutes.
- History/log summary and clear-history control.
- Profile screen with saved name.
- Dark mode that persists and does not remove the existing light UI.
- English, Hindi and Punjabi UI language selection.
- Notification/alarm status screen.

## Build with GitHub Actions

Push the project to GitHub. The workflow at `.github/workflows/build-apk.yml` will:
1. Install Node, Java and Android SDK.
2. Install npm dependencies.
3. Generate the Capacitor Android project.
4. Add the Android exact-alarm permission.
5. Sync Capacitor plugins.
6. Build `app-debug.apk`.
7. Upload it as the `CuraMed-debug-apk` artifact.

## Important

The bundled medicine records are demo/unverified records from the original project. The scanner is an OCR helper; it does not diagnose a medicine or verify its safety. Users should confirm any medicine information with a trusted source or healthcare professional.
OCR uses Tesseract.js loaded from a CDN, so first-time scanning needs internet access. Camera capture itself is native Android.


## Medicine search and scan
The Android build includes Capacitor Camera 8.2.4 and ML Kit Text Recognition 8.2.0. Search opens a full medicine information card showing uses, administration, common side effects, important precautions, interactions, storage and the bundled data source. Scan captures a label and runs on-device OCR when the native plugin is available, then fuzzy-matches the detected text against `www/medicines.json`. The bundled records remain demo/unverified data.


## OCR improvements (v1.2.0)

- Uses native Google ML Kit Text Recognition on Android for Latin and Devanagari text.
- Gallery `content://` images are copied through Capacitor Filesystem into a local cache before native OCR, which avoids local-path failures.
- If native OCR returns no text, the app automatically falls back to enhanced Tesseract.js OCR instead of stopping.
- OCR preprocessing upscales small labels and boosts grayscale contrast.
- Medicine matching now tolerates common OCR spelling errors and partial brand/generic-name matches.
- Camera captures are requested at up to 2200×2200 for better text detail.

For best results, keep the medicine name flat, fill most of the scan area, avoid glare, and use good lighting.
