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

VISUAL SYSTEM — infographic deck, not slide-clipart
Use this repeatable grid on every content slide. It reads as one designed system
instead of seven unrelated layouts.

- Canvas: 16:9.
- Top-left kicker in 10pt caps: "01 · THE PROBLEM" (crimson, letter-spaced).
- Headline below it, 30pt semibold, max 7 words, ending in a full stop.
- A 0.9 in crimson rule under the headline; nothing else decorates the top.
- Body zone: a strict 3-column grid of white cards, 0.28 in apart, equal widths,
  rounded 12px corners, no borders, no shadows.
- Each card = one bold 13pt line + one 10pt grey line. No third level of text.
- One full-width result or takeaway bar at the bottom in a solid colour.
- Footer on every slide: "Medsathi · all info in one app" left, slide number right,
  9pt grey, 0.25 in from the bottom edge.
- Title slide is the opposite: full-bleed crimson, white type, one ghosted white
  heart mark at 12% opacity, three translucent pill chips summarising the product.

DO NOT, this is what makes templates look cheap
- No stock photos of smiling doctors, no generic "team" grid, no lorem placeholders.
- No gradients on body slides, no three-colour rainbow icon sets.
- Do not use a curved ribbon label with a word inside it as decoration.
- No chart unless real numbers exist. Use a stat bar with real figures instead.
- No bullet lists longer than 3 lines per card; if it does not fit, cut it.
- No shadowed boxes, no bevels, no clip-art stethoscopes.

EXACTLY 7 SLIDES — DO NOT ADD AN 8TH

SLIDE 1 — TITLE
- Medsathi — All info in one app.
- One line: "Search, scan, understand and remember your medicines — in Hindi,
  Hinglish and English."
- Chips: 15 conditions · 3 languages · works offline.
- Visual: full-bleed crimson, ghosted white heart mark, app icon.

SLIDE 2 — THE PROBLEM
- Headline: "Strips speak English. Patients don't."
- Three cards: "Printed in English, in tiny type" · "Unsafe advice from WhatsApp" ·
  "Doses live in memory".
- Result bar: "wrong medicine · wrong dose · wrong timing".

SLIDE 3 — THE SOLUTION
- Headline: "One app. Three questions."
- Three cards with numbered circles: "What is this medicine?" · "What should I take?" ·
  "When do I take it?"
- Takeaway line: offline by default, live data only when a key is added.

SLIDE 4 — WHAT SHIPS TODAY
- Headline: "Symptom → medicine · scan · remind".
- Card 1 in crimson (the headline feature): voice or text in Hindi/Hinglish/English,
  home care + OTC options + when to see a doctor, one-tap buy links.
- Card 2: on-device scan — camera → ML Kit OCR → uses, dose, side effects.
- Card 3: reminders — daily/weekdays/once, native alarms, snooze, adherence ring.
- Chip strip: voice in 3 languages · buy links · on-device OCR · adherence history.

SLIDE 5 — TECHNICAL APPROACH & WORKFLOW
- Headline: "On-device first. Keys optional."
- Chevron pipeline across the top: Code → GitHub Actions → APK artifact → Install.
- Left card "Architecture": Capacitor 8 WebView + single HTML/CSS/JS surface;
  Python standard-library backend; bundled JSON → airplane mode works.
- Right card "Keys & privacy": user keys in device storage; CI injects build keys
  from GitHub secrets; proxy mode for public builds.
- Takeaway line: every push to main rebuilds the APK in about 4 minutes.

SLIDE 6 — SAFETY & TRUST
- Headline: "It knows when to stop."
- Red-tint card: emergency guard — 39 red-flag terms, "Call 108 / 112", and the app
  refuses to suggest any medicine.
- Green-tint card: privacy — symptoms, photos and history stay on the device.
- Chips: never a diagnosis · Rx-only → ask pharmacist · WHO/NHS/NHPI cited.

SLIDE 7 — STATUS, IMPACT & NEXT
- Headline: "Working today. Piloting next."
- Three columns: Now (shipping) · Next (4 weeks) · Later.
- Impact line: fewer wrong-medicine incidents, better adherence at home.
- Crimson ask bar: pilot with 50 patients at one clinic + pharmacist review.
- Closing line: "Medsathi — all info in one app."

CLOSING RULE
Exactly 7 slides, no appendix, no thank-you slide. Slide 7 ends on the tagline.
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

## Built deck

A generated copy lives in Google Slides, built directly against this spec:

**https://docs.google.com/presentation/d/1Cwvio7XVHDpZ-Jg82-h4OKwGjjz3de0So3DiifI88eg/edit**

- 7 slides, 16:9, every element a real shape or text box (fully editable, no placeholder junk)
- Slide 1 full-bleed crimson with a ghosted heart mark and three chip pills
- Slides 2–7 share one grid: kicker, 27pt headline, crimson rule, 3-column card row,
  coloured result/ask bar, footer with tagline and slide number
- Slide 5 carries a 4-step chevron pipeline (Code → GitHub Actions → APK → Install)
- Speaker notes on every slide, starting with "SAY THIS:" — one line of delivery coaching each
