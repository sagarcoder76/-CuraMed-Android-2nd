# Step by step: install Medsathi and check the Supabase sync

Everything here is done from a phone or a browser. No computer setup, no key
typing — the app ships already connected to Supabase.

Project: **medsathi** · `ljuertzeznwzyskluptz` (region `ap-south-1`)

---

## Step 1 — Download the APK

1. Open <https://github.com/sagarcoder76/medsathi-apk/actions/workflows/build-apk.yml>
2. Tap the newest run with a **green tick** ("Build Medsathi APK", branch `main`).
3. Scroll to **Artifacts** → tap **Medsathi-debug-apk**.
4. The zip downloads to `Downloads`. Open it with a file manager and extract
   `app-debug.apk`.

> The name stays `app-debug.apk` — it is a real, installable app, just built in
> debug mode so no Play Store account is needed.

## Step 2 — Install it

1. Tap `app-debug.apk`.
2. Android warns "For your security…". Tap **Settings** → allow **Install unknown
   apps** for that file manager/browser → back → **Install**.
3. Play Protect may ask "Unsafe app blocked?" → **Install anyway** (it is your own
   build, unsigned by Play).
4. Tap **Open**. The Medsathi squircle logo and **Namaste 🙏** screen appear.

## Step 3 — Create your account

1. Tap the **Create account** tab.
2. Fill in: **Your name**, **Email**, **Password** (minimum 6 characters).
3. Tap **Create account**.
4. You land on the home screen straight away — email confirmation is off
   (`mailer_autoconfirm`), so there is no verification mail to hunt for.

If something goes wrong the red box under the form says why:

| Message | Meaning |
|---|---|
| `Invalid login credentials` | wrong email/password — use **Sign in**, not Create account |
| `User already registered` | that email exists; switch to **Sign in** |
| `Password should be at least 6 characters` | longer password |
| `Network problem…` | no internet — the app keeps working offline |

## Step 4 — Add a reminder

1. Bottom bar → **Reminders** (alarm icon).
2. Fill **Medicine name**, **Dose**, **Time**, **Repeat** → save.
3. Allow the notification permission when Android asks — that is what makes the
   native alarm ring on time.

## Step 5 — Confirm the sync happened on the phone

1. Bottom bar → **Profile** (person icon).
2. Under **Account** you should see your email and the note *"Signed in.
   Reminders and dose log back up to your account."*
3. Just below is the sync row: **Sync now**
   - tap it once → it shows `Syncing…` then `Synced`
   - the line under it keeps the last sync time, e.g. *"… synced to your
     account · 13 Nov, 5:26 am"*
   - if you are offline it shows `Offline — will retry` and nothing is lost

## Step 6 — Confirm the rows are in Supabase

1. Open <https://supabase.com/dashboard/project/ljuertzeznwzyskluptz/editor>
2. **Table editor → `reminders`**: one row per medicine — `medicine_name`,
   `reminder_time`, `enabled`, `user_id` (your account's UUID).
3. **Table editor → `dose_events`**: one row each time you tap **Take Now** or
   **Snooze 15m**.
4. Cross-check that `user_id` matches **Authentication → Users → your row → ID**.

You will only ever see *your* rows — that is row level security doing its job.

## Step 7 — Second phone (the real test)

1. Install the same APK on another phone.
2. **Sign in** with the same email and password (do not create a new account).
3. The app pulls your cloud rows on sign-in: the reminder from Step 4 is already
   on the home screen.
4. Now tap **Take Now** on the first phone → open the second phone → **Profile →
   Sync now** → **History & Logs** shows that dose.

## Step 8 — Account actions (optional)

Both live under **Profile → Account** and only appear once you are signed in.

- **Change password** → type a new password (6+ characters) → **Save**. It changes
  right away, no email needed. Test it by signing out and back in.
- **Delete account** → this is permanent. It removes the account, its profile row,
  its reminders and its dose log from Supabase. Reminders already on this phone stay
  on this phone, and the app drops back to guest mode. Use it only on a test account.

## Step 9 — Airplane mode test

1. Turn on airplane mode.
2. Add a reminder or tap **Take Now** — the app behaves normally.
3. Profile → **Sync now** → `Offline — will retry`.
4. Turn airplane mode off. The queued change flushes automatically when the
   network returns (or tap **Sync now**). Nothing is lost, nothing duplicates.

---

## Good to know

- **Guest mode** still works: **Continue as guest** → everything stays on the
  phone, no account, no network.
- **Signing out** removes the session and the sync queue but keeps your reminders
  and history on the phone.
- **A different account on the same phone pulls only.** If someone else signs in
  on your device, their cloud rows come down but your local rows are never pushed
  into their account.
- **Nothing is end-to-end encrypted.** Rows are protected by row level security
  (`auth.uid() = user_id`), not by a password only you know.
- Scans, the medicine library and the symptom checker never leave the device.

## If something looks wrong

| Symptom | Check |
|---|---|
| Profile shows *Supabase not connected* | you installed an old APK — grab the newest run from Step 1 |
| **Sync now** says `Offline — will retry` with internet | the phone is on a captive-portal Wi-Fi; try mobile data |
| Second phone is empty after sign-in | it is signed in with a different email, or the first phone never synced (Step 5) |
| No alarm rings | Android → Settings → Apps → Medsathi → Notifications **on**, and allow **Alarms & reminders** |
