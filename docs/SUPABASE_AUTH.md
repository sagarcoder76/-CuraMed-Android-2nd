# Login (Supabase) — setup and how it works

Medsathi uses **Supabase** for two things: email + password **login**, and an
opt-in **backup of reminders and the dose log** so the same data appears on a second
phone. Scans and the medicine library never leave the device, and the app works
fully offline as a guest.

Working project: **medsathi** (`ljuertzeznwzyskluptz`, region `ap-south-1`, free plan).

---

## 1. Keys used by the app

**The app is connected out of the box.** Login and cloud sync need no setup, no
GitHub secret and no key typed on the phone: `www/config.default.js` is committed
and ships the project URL plus the anon (publishable) key.

Three layers, highest priority first:

| Layer | File / place | Committed? | Purpose |
|---|---|---|---|
| 1. Device | pasted in the app (**Connect Supabase** panel) | never leaves the phone | explicit override, stored in `localStorage` as `curamed.supabase.v1` |
| 2. Build | `www/config.js`, written by CI from the `SUPABASE_URL` / `SUPABASE_ANON_KEY` secrets | **no**, git-ignored | point a build at another project |
| 3. Shipped default | `www/config.default.js` | **yes** | makes a fresh install work immediately |

`www/index.html` loads both files and merges them, keeping any non-empty value from
the higher layer. Because layer 3 always exists, `sbConfig().ready` is true on a
clean install, the in-app setup panel stays hidden, and the Profile → Account row
reads *Sign in to back up reminders and sync across phones.*

The anon key is a *public client key* by design — it is meant to ship inside web
and mobile clients, and it grants nothing on its own. What protects the data is
row level security, below. The `service_role` / `sb_secret_…` key must **never**
appear in this repository, in `config.default.js`, or in any APK.

## 2. Database

Applied as migration `create_profiles`:

```sql
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  email text,
  language text default 'en',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table public.profiles enable row level security;

create policy "profiles_select_own" on public.profiles for select using (auth.uid() = id);
create policy "profiles_insert_own" on public.profiles for insert with check (auth.uid() = id);
create policy "profiles_update_own" on public.profiles for update using (auth.uid() = id) with check (auth.uid() = id);

-- one profile row per new auth user
create function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, full_name, email)
  values (new.id, coalesce(new.raw_user_meta_data->>'full_name',''), new.email)
  on conflict (id) do nothing;
  return new;
end; $$;

create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();
```

Result: a user can read and write **only their own row**. There is no policy that
lets one user see another's data, and no anonymous access at all.

### Synced tables (migration `create_sync_tables`)

```sql
create table public.reminders (
  id text primary key,                  -- the phone's own id, so rows merge 1:1
  user_id uuid not null references auth.users(id) on delete cascade,
  medicine_name text not null,
  dosage text,
  reminder_time text not null,
  repeat_type text default 'daily',
  enabled boolean default true,
  last_taken timestamptz,
  updated_at timestamptz default now()
);
create table public.dose_events (
  id text primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  reminder_id text,
  medicine_name text,
  dosage text,
  action text,
  action_time timestamptz not null,
  created_at timestamptz default now()
);

alter table public.reminders  enable row level security;
alter table public.dose_events enable row level security;

create policy "reminders_own_all" on public.reminders
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "dose_events_own_all" on public.dose_events
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
```

`id` is `text`, not `uuid`, because the phone already generates IDs with
`Date.now()`. Using the phone's ID as the primary key means a row is inserted once
and re-pushed safely (`Prefer: resolution=merge-duplicates` acts as an upsert).

## 3. Auth settings

| Setting | Value | Why |
|---|---|---|
| Email provider | enabled | the only login method |
| Phone provider | disabled | SMS costs money, not needed yet |
| Confirm email | **off** (`mailer_autoconfirm`) | hackathon demo: sign up and you are in, no SMTP needed |
| Signups | allowed | anyone can create an account |
| Min password length | 6 | Supabase default |
| Site URL | `https://localhost` | Capacitor origin |
| Redirect allow list | `capacitor://localhost`, `https://localhost`, `http://localhost:8000` | password reset links |

Turn **Confirm email** back on before a public release.

## 4. What the app does

- **Sign up** → `POST /auth/v1/signup` with `data.full_name`; a trigger creates the
  profile row.
- **Sign in** → `POST /auth/v1/token?grant_type=password`.
- **Session** cached in `localStorage` under `curamed.auth.v1` (`access_token`,
  `refresh_token`, `expires_at`, user id/email/name) and refreshed silently when it
  is within 60 s of expiry.
- **Profile sync** → `GET/POST /rest/v1/profiles` after login (upsert with
  `Prefer: resolution=merge-duplicates`). If the cloud has a name and the phone has
  none, the phone adopts it.
- **Sign out** → `POST /auth/v1/logout`, then the local session is dropped. Local
  reminders and history are untouched.
- **Guest mode** → "Continue as guest" hides the screen and everything keeps working
  offline; Profile → Account → "Sign in / Create" reopens it.

### Sync engine

Local storage stays the **source of truth**; the cloud is a mirror, so nothing breaks
in airplane mode.

| Event | What happens |
|---|---|
| Sign in / app start | `flushSyncQueue()` then `pullCloud()` — cloud rows missing on the phone are added, phone rows missing in the cloud are pushed |
| Add / edit / toggle reminder | `pushReminder()` (upsert) |
| Delete reminder | `deleteCloudReminder()` |
| Log a dose (taken / snoozed) | `pushDose()` and, for taken, `pushReminder()` so `last_taken` follows |
| Write fails (offline) | op is queued in `curamed.syncq.v1` and retried on the next sync or when the `online` event fires |
| Sign out | session, queue and sync stamp are dropped; local reminders and history are **kept** |
| Different account signs in on the same phone | pull only — local rows are never pushed into another person's account |

Profile → Account shows the last sync time and a **Sync now** button, plus two
account actions once you are signed in:

- **Change password** — `PUT /auth/v1/user` with the new password and the session
  bearer token. Works fully in the app, no email needed (the emailed reset link
  cannot reopen an APK, so it is not the primary path).
- **Delete account** — `POST /rest/v1/rpc/delete_own_account`, then the session,
  sync queue, sync stamp and sync uid are cleared and the app drops back to guest
  mode. Local reminders and history stay on the phone.

No SDK is bundled — the app talks to the REST endpoints with `fetch`, so it stays
offline-first and small. If the network is down the error says so instead of hanging.

### Account deletion (migration `delete_own_account`)

The anon key cannot touch `auth.users`, so deletion goes through a
`security definer` function that acts only on the caller:

```sql
create or replace function public.delete_own_account()
returns void
language plpgsql
security definer
set search_path = public, auth
as $fn$
declare uid uuid := auth.uid();
begin
  if uid is null then raise exception 'Not signed in' using errcode = '28000'; end if;
  delete from auth.users where id = uid;   -- cascades
end;
$fn$;

revoke all on function public.delete_own_account() from public;
revoke all on function public.delete_own_account() from anon;
grant execute on function public.delete_own_account() to authenticated;
```

`profiles.id`, `reminders.user_id` and `dose_events.user_id` all reference
`auth.users(id) on delete cascade`, so one delete removes the account, its profile,
its reminders and its dose log. A signed-out caller gets `Not signed in`; `anon`
has no `execute` privilege at all.

Verified on the live project inside a rolled-back transaction: the user row, profile,
reminder and dose all disappear, `has_function_privilege('anon', ...)` is `false`,
`has_function_privilege('authenticated', ...)` is `true`.

## 5. Test plan on device

1. Install the APK, first launch shows **Namaste 🙏**.
2. **Create account** with your email → you land on Home, green dot appears on the
   avatar, Profile → Account shows your email.
3. Force-close and reopen → you are still signed in (session restored).
4. **Sign out** in Profile → avatar dot disappears, guests still see all features.
5. Supabase dashboard → Authentication → Users: your account is listed; Table editor
   → `profiles`: one row with your name.
6. Add a reminder and mark a dose taken → Table editor → `reminders` and
   `dose_events` each get a row for your user id.
7. Turn on airplane mode, add another reminder → it still works and Profile → Account
   says "Offline — will retry". Turn the network back on, tap **Sync now** → the row
   appears in Supabase.
8. Sign in on a second phone → the reminders and history arrive.
9. Profile → Account → **Change password**, set a new one, sign out and sign back in
   with it.
10. (Optional, it is irreversible) Profile → Account → **Delete account** → the
    account disappears from Authentication → Users, its rows disappear from
    `reminders` / `dose_events`, and the app falls back to guest mode with the local
    reminders still on the phone.

## 6. Adding the secrets

Repository → Settings → Secrets and variables → Actions → New repository secret:

| Name | Value |
|---|---|
| `SUPABASE_URL` | `https://ljuertzeznwzyskluptz.supabase.co` |
| `SUPABASE_ANON_KEY` | the project's anon public key |

After that every APK build ships with login enabled and no in-app setup.
