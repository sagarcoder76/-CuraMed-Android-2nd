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
They care about safety, real-world usefulness and that the app already works.

TONE
Clear, calm, confident. Short sentences. No hype words. Digits over adjectives.
Every claim must be something the app actually does today.

DESIGN
- Colours: teal #005264 (primary), crimson #C62A52 (brand accent), cream #F3FAFF (background), mint #A5F1E0 (highlights).
- Font: Plus Jakarta Sans for headings, a highly readable sans for body.
- Style: flat, generous white space, rounded cards, one accent colour per slide, phone mockups where useful.
- Max 5 bullets per slide, max 10 words per bullet. No walls of text.

EXACTLY 7 SLIDES — DO NOT ADD MORE

SLIDE 1 — TITLE
- Medsathi — All info in one app.
- One line: "Search, scan, understand and remember your medicines — in Hindi, Hinglish and English."
- Sub-line: Android app + lightweight Python backend. Built for Indian households.
- Visual: the app icon (white heart with an ECG pulse on a crimson squircle) and one phone mockup of the home screen.

SLIDE 2 — THE PROBLEM
- Medicine strips are printed in English, in tiny type that many Indian users cannot read.
- People ask neighbours or WhatsApp groups: "which tablet for fever?" — and get unsafe answers.
- Reminders are missed because they live in memory, not in the phone.
- Pharmacies sell what is asked for, with no explanation of dose or side effects.
- Result: wrong medicine, wrong dose, wrong timing.
- Visual: 3 small photos/icons — pill strip, confused user, missed alarm.

SLIDE 3 — THE SOLUTION
- One app that answers three questions:
  1. "What is this medicine?" → search or scan the strip
  2. "What should I take for this symptom?" → describe it in Hindi/Hinglish, by voice
  3. "When do I take it?" → reminders with native alarms
- Works offline by default; live medical data switches on when API keys are added.
- Visual: three-column layout with one icon per pillar.

SLIDE 4 — FEATURE 1: SYMPTOM → MEDICINE (the headline feature)
- Patient types or speaks: "sar dard aur halka bukhar 2 din se, kya lu?"
- App understands Hindi, Hinglish and English (voice or text).
- Returns: what helps at home, OTC options with dose guidance, when to see a doctor.
- Each suggestion has one-tap buy links (Tata 1mg, PharmEasy, Netmeds).
- Covers 15 common complaints — fever, cold, cough, acidity, loose motions, period pain and more.
- Visual: phone mockup of the crimson "Check" card, plus a result card with a Buy row.

SLIDE 5 — FEATURE 2 & 3: SCAN + REMIND
- Scan: point the camera at a strip → on-device OCR reads Latin and Devanagari text → the app matches it to a medicine and shows uses, dose, side effects and precautions. No photo leaves the phone.
- Reminders: daily, weekdays or one-time; Android alarms that fire even when the app is closed; snooze 15 minutes; adherence ring shows how many doses were taken today.
- History logs every taken/snoozed dose on the device.
- Visual: scan flow (camera → text → medicine card) as a 3-step arrow, plus a reminder card.

SLIDE 6 — SAFETY & TRUST (this slide wins the room)
- Emergency guard: 39 red-flag terms (chest pain, breathlessness, fainting, stroke signs, fits, severe bleeding, poisoning) immediately show "Call 108 / 112" and the app refuses to suggest any medicine.
- Never a diagnosis: every screen states it is general information, not medical advice.
- Prescription-only drugs are labelled "Ask pharmacist" instead of being dosed.
- Privacy: symptoms and photos stay on the device; no account, no tracking, no cloud storage.
- Honest sourcing: WHO, NHS, National Health Portal India — cited on every result.
- Visual: a red emergency card next to a green "privacy on device" badge.

SLIDE 7 — STATUS, IMPACT & NEXT
- Working today: Android APK built automatically from GitHub, live medicine search, AI scan, symptom checker in three languages, reminders, history, dark mode, English/Hindi/Punjabi UI.
- Impact goal: fewer wrong-medicine incidents and better adherence in households that do not read English labels.
- Next: first-launch disclaimer acceptance, verified medicine database for the top 500 Indian brands, pharmacist-reviewed content, iOS build, offline Hindi voice.
- Ask: pilot with 50 patients at one clinic, and pharmacist review of the symptom guidance.
- Visual: roadmap as three steps (Now / Next / Later) plus a large "Try the APK" QR code placeholder.

CLOSING RULE
Slide 7 must end with the tagline: "Medsathi — all info in one app."
Keep it to 7 slides. Nothing else.
```

---

## Feature list (source material)

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

**Platform**
- Capacitor 8 Android app, Python stdlib backend
- Three keys supported simultaneously; on-device storage, never in the APK
- Zero-setup builds via GitHub Actions secrets; backend-proxy option for public releases
- Medsathi brand: heart + ECG logo, launcher icons for every density
