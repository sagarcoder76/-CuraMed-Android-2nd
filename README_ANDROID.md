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
Profile & Settings → **API keys (optional)** → paste any or all three → **Save keys** → **Test**.

| # | Key | Used for | Needed? |
|---|---|---|---|
| 1 | **TinyFish** | Live web search: finds the medicine on medical sites, snippet + "Open source" link | Optional (free 12,000 searches/day) |
| 2 | **OpenFDA** | Live drug-label data: brand/generic name, manufacturer, indications | Optional — works without a key at lower limits |
| 3 | **Google AI Studio (Gemini)** | Vision scan: reads the label photo when OCR struggles | Optional |

All three can be saved at the same time — they do not replace each other:

- **Search** runs TinyFish (if set) and OpenFDA (always) in parallel, merges and
  de-duplicates the results under "Live results", and falls back to RxNav (free,
  no key) if both return nothing.
- **Scan** uses the AI Studio key first (vision), then native ML Kit OCR, then
  Tesseract.js — and appends live search matches for whatever text was read.

Keys are stored in the WebView's `localStorage` on that device only. They are not
baked into the APK, so a leaked APK does not leak them. Tap **Clear** on a shared
device. The **Test** button reports each key as ✓ or ✗ individually.

Get keys: TinyFish — https://agent.tinyfish.ai/api-keys ·
OpenFDA — https://open.fda.gov/apis/authentication/ ·
AI Studio — https://aistudio.google.com/apikey

Cross-origin calls (TinyFish, OpenFDA, RxNav, Gemini) go through Capacitor's
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

### 3. Shipping the app with keys already inside (zero-setup install)

If you want someone to download the APK and use it immediately — no key entry —
there are two ways. Pick by how public the app will be.

**Option A — keys compiled into the build (fastest, least safe)**

The app reads `www/config.js` at startup. If no keys are saved on the device yet,
it copies those keys in once, so a fresh install works instantly. The file is
git-ignored, so real keys never land in the repository.

Local build:
```bash
cp www/config.example.js www/config.js   # then paste your three keys
npx cap copy android && npx cap sync android
```

GitHub Actions build (no key in the repo — recommended version of Option A):
1. Repo → **Settings → Secrets and variables → Actions → New repository secret**.
2. Add `TINYFISH_API_KEY`, `OPENFDA_API_KEY`, `GEMINI_API_KEY`.
3. Run the **Build CuraMed APK** workflow. The step *"Inject API keys into app
   build"* writes `www/config.js` from those secrets before Capacitor copies the
   web assets, so the APK is self-contained. With no secrets set it simply builds
   an app without built-in keys.

The user can still replace the keys in Settings; a built-in key is only seeded
once per install, and **Clear** stays cleared.

> ⚠️ **Any key inside an APK is extractable.** Someone can unzip the APK, run
> `strings` on it, or read `config.js` directly — treat shipped keys as public.
> Use free tiers, rotate them if usage spikes, and never ship a paid/billing key.
> This is why Option A is fine for a personal or small-group APK, not for a
> store-wide release.

**Option B — backend proxy (recommended for public distribution)**

Keys stay on a server; the APK only knows a URL.

1. Deploy `medicine_assistant/` (any host that runs Python — Vercel/Fly/Render/a VPS).
2. Set `TINYFISH_API_KEY`, `OPENFDA_API_KEY`, `GEMINI_API_KEY` in that host's env
   (or its `.env`).
3. In `www/config.js` set only the URL, and leave `apiKeys` empty:
   ```js
   window.CURAMED_CONFIG = { backendUrl: 'https://your-api.example.com', apiKeys: { tinyfish:'', openfda:'', gemini:'' } };
   ```
4. Rebuild. The app now calls `/api/external/search` and `/api/external/scan` on
   your server; the status badge shows **Server API**, and no key is present on
   the phone. Because the same URL ships in every APK, you can rotate keys
   server-side without shipping a new build.

### Never do this
Do **not** paste a real key into `www/index.html`, `app.py`, or any committed
file. Anything in the APK or repo is extractable. Use the Settings screen,
`www/config.js` (git-ignored, injected by CI), or `.env`.

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
