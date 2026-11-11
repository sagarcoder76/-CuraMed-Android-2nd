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


## Optional API keys (live medicine search & AI scan)

CuraMed works fully offline with **no key**. Adding a key is optional and only
turns on *live* data. The key is **never hardcoded in the app source**.

### 1. In the Android app (recommended for the APK)
Profile & Settings → **Live medicine API (optional)**:
1. Pick a **Provider**.
2. Paste the key.
3. Tap **Save key**, then **Test** (it should report live results for "paracetamol").

| Provider | Key needed? | What it gives you |
|---|---|---|
| Off — local library only | — | 6 bundled demo medicines, fully offline |
| RxNav (NLM) | No | Live US drug-name lookup, free |
| OpenFDA | Optional | Live brand/generic names, uses, manufacturer. A key only raises rate limits |
| Google Gemini | **Yes** | AI reads the label photo during Scan (better on blurry/angled packs) |
| TinyFish | **Yes** | Live web search — finds the medicine on medical sites, shows a snippet + "Open source" link. Free 12,000 searches/day |

The key is stored in the WebView's `localStorage` on that device only. It is not
baked into the APK, so a leaked APK does not leak the key. If a device is shared,
tap **Clear** to remove it.

Get keys: OpenFDA — https://open.fda.gov/apis/authentication/ ·
Gemini — https://aistudio.google.com/apikey ·
TinyFish — https://agent.tinyfish.ai/api-keys

Cross-origin calls (OpenFDA, RxNav, Gemini, TinyFish) go through Capacitor's
built-in native HTTP bridge inside the APK, so browser CORS rules do not apply.
In a desktop browser preview they fall back to plain `fetch` and may be blocked
by the provider's CORS policy — this only affects previewing, not the APK.

### 2. In the Python backend (server-side proxy)
Safest option: the key never reaches the phone.

```bash
cd medicine_assistant
cp .env.example .env      # then edit .env and paste keys
python3 app.py
```

`.env` is git-ignored. New endpoints:

- `GET  /api/external/search?q=paracetamol` → live RxNav + OpenFDA results
- `POST /api/external/scan` with `{"image_base64": "..."}` → AI-read label text
- `GET  /api/config/status` → which providers are configured (never returns keys)

Set `TINYFISH_API_KEY` in `.env` to have `/api/external/search` also return
TinyFish web results (`X-API-Key` header, `GET https://api.search.tinyfish.ai`).

### Never do this
Do **not** paste a real key into `www/index.html`, `app.py`, or any committed
file. Anything in the APK or repo is extractable. Use the Settings screen or
`.env`.

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
