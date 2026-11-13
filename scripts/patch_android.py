from pathlib import Path
import re

manifest = Path("android/app/src/main/AndroidManifest.xml")
if not manifest.exists():
    raise SystemExit("AndroidManifest.xml not found")

# Permissions the web layer needs but Capacitor's template does not ship:
#   SCHEDULE_EXACT_ALARM  -> timer alarms that fire at the exact minute
#   RECORD_AUDIO          -> symptom checker voice input (native recognizer +
#                            getUserMedia fallback). Without this line Android
#                            denies every microphone request, so the mic button
#                            only ever showed "Microphone permission needed."
#   MODIFY_AUDIO_SETTINGS -> audio focus while recording
PERMISSIONS = [
    "android.permission.SCHEDULE_EXACT_ALARM",
    "android.permission.RECORD_AUDIO",
    "android.permission.MODIFY_AUDIO_SETTINGS",
]

s = manifest.read_text()
added = []

for name in PERMISSIONS:
    tag = f'<uses-permission android:name="{name}" />'
    if name in s:
        continue
    match = re.search(r"<manifest\b[^>]*>", s, re.DOTALL)
    if not match:
        raise SystemExit("Could not find <manifest> root element")
    s = s[: match.end()] + "\n    " + tag + s[match.end() :]
    added.append(name)

if added:
    manifest.write_text(s)
    print("Added permissions:", ", ".join(added))
else:
    print("All permissions already present")

# Fail loudly if the microphone permission did not land - a silent miss here is
# exactly how the mic ended up broken in a shipped APK.
if "android.permission.RECORD_AUDIO" not in manifest.read_text():
    raise SystemExit("RECORD_AUDIO permission missing after patch")
print("RECORD_AUDIO verified in AndroidManifest.xml")
