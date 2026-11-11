# Medsathi — 7-slide pitch deck prompt

Copy everything inside the box below into your deck tool (Gamma, Canva AI, SlidesAI,
Tome, ChatGPT, Claude, etc.).

---

```
Create a 7-slide presentation for a mobile app called Medsathi.
Tagline: "All info in one app."

CONTEXT
Medsathi is an Android medicine companion built for Indian users who take
medicines daily but cannot read English labels comfortably. It answers three
questions in one app: "What is this medicine?", "What should I take for this
symptom?", and "When do I take it?"

AUDIENCE
Doctors, pharmacists, clinic owners, health-tech investors and college judges.
They care about safety, real-world usefulness, and that the app already works.

TONE
Clear, calm, confident. Short sentences. No hype words. Digits over adjectives.
Every claim must be something the app actually does today.

DESIGN
- Colours: teal #005264 (primary), crimson #C62A52 (brand accent), cream #F3FAFF
  (background), mint #A5F1E0 (highlights).
- Font: Plus Jakarta Sans headings, highly readable sans for body.
- Style: flat, generous white space, rounded cards, one accent colour per slide,
  phone mockups where useful.
- Max 5 bullets per slide, max 10 words per bullet. No walls of text.

EXACTLY 7 SLIDES — DO NOT ADD AN 8TH

SLIDE 1 — TITLE
- Medsathi — All info in one app.
- One line: "Search, scan, understand and remember your medicines — in Hindi,
  Hinglish and English."
- Sub-line: Native Android app + lightweight Python backend. Built for Indian households.
- Visual: app icon (white heart with an ECG pulse on a crimson squircle) plus one
  phone mockup of the home screen showing the crimson "Check" hero card.

SLIDE 2 — THE PROBLEM
- Medicine strips are printed in English, in tiny type many Indian users cannot read.
- People ask neighbours or WhatsApp groups "which tablet for fever?" — and get unsafe answers.
- Reminders live in memory, not in the phone, so doses are missed.
- Pharmacies sell what is asked for, with no explanation of dose or side effects.
- Result: wrong medicine, wrong dose, wrong timing.
- Visual: three icons — pill strip, confused user, missed alarm.

SLIDE 3 — THE SOLUTION
- One app that answers three questions:
  1. "What is this medicine?" → search the name or scan the strip
  2. "What should I take for this symptom?" → say it in Hindi/Hinglish, by voice
  3. "When do I take it?" → reminders with native Android alarms
- Offline by default; live medical data switches on when API keys are added.
- Visual: three-column layout, one icon per pillar.

SLIDE 4 — THE FEATURE SET (what ships today)
- SYMPTOM → MEDICINE (headline): type or speak "sar dard aur halka bukhar 2 din se,
  kya lu?" and get home care, OTC options with dose notes, when to see a doctor.
  Hindi, Hinglish and English. 15 common complaints. One-tap buy links (1mg,
  PharmEasy, Netmeds).
- SCAN: point the camera at a strip → on-device OCR reads Latin and Devanagari →
  the app shows uses, dose, side effects and precautions. No photo leaves the phone.
- REMIND: daily / weekdays / once, Android alarms that fire with the app closed,
  15-minute snooze, adherence ring and full dose history.
- Visual: three stacked mini-mockups — Check card, scan result, reminder card.

SLIDE 5 — TECHNICAL APPROACH & WORKFLOW
- Architecture: one Capacitor 8 WebView app (single-page HTML/CSS/JS, Tailwind) over
  a Python-standard-library backend. No heavy framework, no cloud database.
- On-device intelligence: ML Kit OCR (Latin + Devanagari) with a Tesseract.js
  fallback, optional Gemini vision when a key exists, Web Speech API + recorder for
  voice input — so the core features work in airplane mode with bundled JSON libraries.
- Optional live layer, all key-optional: TinyFish search, OpenFDA drug labels,
  RxNav and Gemini. RxNav runs with no key at all.
- Data & privacy: reminders, history and profile live in device storage only.
- Key handling: user keys are entered once in Profile and stored on the phone; a CI
  step injects build-time keys from GitHub repository secrets into a git-ignored
  config file, and a server-proxy mode keeps keys off the client for public releases.
- Delivery workflow: push to main → GitHub Actions installs Node + JDK + Android SDK,
  injects keys, applies launcher icons, patches the exact-alarm permission, runs
  Gradle → a signed debug APK appears as a downloadable artifact in ~4 minutes.
  Every push is therefore a release.
- Visual: simple horizontal pipeline diagram — Code → GitHub Actions → APK →
  Install, with a small architecture strip beneath it (UI ⇄ device storage /
  optional APIs).

SLIDE 6 — SAFETY & TRUST (this slide wins the room)
- Emergency guard: 39 red-flag terms (chest pain, breathlessness, fainting, stroke
  signs, fits, severe bleeding, poisoning) immediately show "Call 108 / 112" and the
  app refuses to suggest any medicine.
- Never a diagnosis: every screen states it is general information, not medical advice.
- Prescription-only drugs are labelled "Ask pharmacist" instead of being dosed.
- Privacy: symptoms, photos and history stay on the device — no account, no tracking.
- Honest sourcing: WHO, NHS and National Health Portal India, cited on every result.
- Visual: red emergency card beside a green "everything stays on your phone" badge.

SLIDE 7 — STATUS, IMPACT & NEXT
- Working today: Android APK built automatically from GitHub; symptom checker in three
  languages; AI scan; offline search; reminders with native alarms; adherence history;
  dark mode; English / Hindi / Punjabi UI.
- Impact goal: fewer wrong-medicine incidents, better adherence in households that do
  not read English labels.
- Next: first-launch disclaimer acceptance, verified database for the top 500 Indian
  brands, pharmacist-reviewed symptom content, iOS build, offline Hindi voice model.
- Ask: pilot with 50 patients at one clinic, plus pharmacist review of the symptom
  guidance before wider release.
- Visual: roadmap as three columns (Now / Next / Later) and a "Try the APK" QR placeholder.

CLOSING RULE
Slide 7 ends with the tagline: "Medsathi — all info in one app."
Exactly 7 slides. Nothing else.
```

---

## Feature list (source material for slides 3–4)

**Symptom → medicine (headline)**
- Text or voice input; Hindi, Hinglish, English
- 15 common complaints with home care, OTC options, dose notes
- Red-flag emergency triage → Call 108 / 112, no medicine suggested
- "See a doctor if…" for every result, sources cited
- One-tap buy links (1mg, PharmEasy, Netmeds)

**Scan**
- Capacitor Camera / gallery
- ML Kit on-device OCR (Latin + Devanagari), Tesseract.js fallback, optional Gemini vision
- Fuzzy match to medicine library, prefill reminder from scan

**Search**
- Offline library search with fuzzy scoring
- Live results: TinyFish web, OpenFDA labels, RxNav (keyless)
- Buy links on every result

**Reminders**
- Daily / weekdays / one-time, native local notifications, exact alarms
- 30-day rolling schedule, snooze 15 min, per-reminder ON/OFF

**History & adherence**
- Dose logs (taken / snoozed), live adherence ring and count, clear history

**Drug information**
- Uses, administration, side effects, precautions, interactions, storage, source

**Profile & settings**
- Name + initials avatar, English/Hindi/Punjabi UI, dark mode
- Notification status, API key manager (TinyFish, OpenFDA, AI Studio) with per-key test

**Platform & delivery (slide 5)**
- Capacitor 8 Android app, Python stdlib backend (`/api/search`, `/api/medicine`,
  `/api/external/*`, `/api/config/status`)
- Device storage only: `curamed.reminders.v3`, `curamed.history.v3`,
  `curamed.profile.v2`, `curamed.api.v2`; channel `medicine-reminders`
- Keys: on-device entry, CI secrets → git-ignored `www/config.js`, env vars on the backend
- GitHub Actions builds the APK on every push to `main` (≈4 min), artifact `Medsathi-debug-apk`
- Brand: white heart + ECG pulse on crimson squircle, launcher icons for every density
