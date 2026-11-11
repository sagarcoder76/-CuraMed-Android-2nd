# Medsathi Android — all medicine info in one app

This version keeps the existing Medsathi UI and adds working Android features:

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

## Renamed to Medsathi

The app is now **Medsathi — all info in one app**.

- Display name / APK label: `Medsathi` (from `appName` in `capacitor.config.ts`).
- Package / `appId`: `com.medsathi.app` (was `com.curamed.medicineassistant`).
  Because the package changed, Android treats this as a new app — the old
  CuraMed install stays separate and its reminders are not carried over.
- Internal storage keys (`curamed.reminders.v3`, `curamed.history.v3`,
  `curamed.profile.v2`, `curamed.api.v2`) were intentionally **not** renamed so
  nothing breaks for anyone upgrading in place.

## Brand

- **Logo:** white heart with an ECG pulse on a crimson squircle gradient
  (`www/logo.svg`). Used for the header mark, the favicon and every launcher icon.
- **Launcher icons:** `resources/android/` holds the generated set (legacy,
  round and adaptive foregrounds per density, plus a 1024px master).
  `scripts/apply_icons.py` copies them over Capacitor's placeholders and sets
  the adaptive background to `#C62A52`; it runs in the APK workflow.
- **App palette:** the UI stays teal (`#005264` primary) for calm, readable
  medical screens — the crimson mark is the brand accent.

## Build the APK from GitHub (no computer setup needed)

Everything happens on GitHub's servers. You only need a browser or the GitHub app.

**1. Add your API keys once** (optional but recommended — this is what makes the
downloaded APK work with no setup)

Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository
secret**, and add three secrets:

| Name | Value |
|---|---|
| `TINYFISH_API_KEY` | your TinyFish key |
| `OPENFDA_API_KEY` | your OpenFDA key |
| `GEMINI_API_KEY` | your Google AI Studio key |

**2. Start a build**

- Repo → **Actions** tab (top bar).
- Left sidebar → **Build Medsathi APK**.
- Click **Run workflow** (right side), choose the branch
  `arena/63a129af-curamed-android-2nd` or `main`, then **Run workflow**.
- A run appears with a yellow dot → wait ~6–10 minutes for the green tick.

The workflow also runs automatically on any push to `main`.

**3. Download the APK**

- Open the finished run → scroll to **Artifacts** at the bottom.
- Download **Medsathi-debug-apk** (a `.zip`).
- Unzip it → you get `app-debug.apk`.
- Copy it to the phone, tap it, and allow **Install unknown apps** when Android asks.

**4. Install and open**

If Play Protect warns you, choose **Install anyway** — that warning appears for any
unsigned debug APK. The icons, logo, keys and all features are already inside.

**If the build fails:** open the red step, read the last 20 lines, and check that
`package.json` dependencies installed. The build needs no local Android SDK.

### What the workflow does

The workflow at `.github/workflows/build-apk.yml` will:
1. Install Node, Java and Android SDK.
2. Install npm dependencies.
3. Generate the Capacitor Android project.
4. Add the Android exact-alarm permission.
5. Sync Capacitor plugins.
6. Build `app-debug.apk`.
7. Upload it as the `Medsathi-debug-apk` artifact.

## Important

The bundled medicine records are demo/unverified records from the original project. The scanner is an OCR helper; it does not diagnose a medicine or verify its safety. Users should confirm any medicine information with a trusted source or healthcare professional.
OCR uses Tesseract.js loaded from a CDN, so first-time scanning needs internet access. Camera capture itself is native Android.


## Optional API keys (live medicine search & AI scan)

Medsathi works fully offline with **no key**. Adding a key is optional and only
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
3. Run the **Build Medsathi APK** workflow. The step *"Inject API keys into app
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

## Symptom checker (text + voice, Hindi / Hinglish / English)

The symptom checker is the app's headline feature and sits as the **crimson hero
card at the top of the home screen**, plus a permanent **Check** tab in the bottom
navigation. One-tap Hinglish starter chips (Bukhar, Sar dard, Khansi…) and a
dedicated mic button open it straight into voice capture, so a patient can get an
answer in two taps without typing.

The patient can **type or speak** — "sar dard aur halka bukhar 2 din se, kya lu?" —
and gets plain-language guidance plus buy links.

**How it works**

1. **Speech input.** Web Speech API (`hi-IN` by default, `en-IN` selectable) when
   the WebView supports it. Otherwise the app records 6 seconds of audio and has
   Gemini transcribe it — so voice works in the APK with only an AI Studio key.
2. **Language normalisation.** Devanagari input is normalised to English clinical
   keywords through Gemini when a key is present, so Hindi and Hinglish both match.
3. **Matching.** `www/symptoms.json` holds 15 common complaints with English,
   Hindi and Hinglish keywords. Scoring de-weights generic words like “dard” so
   the wrong condition is not suggested.
4. **Answer.** Each match shows what helps at home, OTC options with dose guidance
   ("ask a pharmacist" for anything not OTC), when to see a doctor, and the source.
5. **Buy links.** Every suggested medicine, every search result, every scan match
   and the drug-info sheet carry **Tata 1mg · PharmEasy · Netmeds** links.
   Medsathi earns nothing from these and is not a pharmacy.

**Safety rails**

- A 39-keyword emergency list (chest pain, breathlessness, fainting, stroke signs,
  seizures, severe bleeding, poisoning) short-circuits everything: the app shows
  **Call 108 / 112** and refuses to suggest any medicine.
- Every screen states it is general information, not a diagnosis, and that
  children, pregnancy and long-term illness need a professional.
- Prescription-only items are labelled *Ask pharmacist* rather than dosed.
- No symptom text is stored; it is processed on the device and only sent to the
  API you configured.

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
