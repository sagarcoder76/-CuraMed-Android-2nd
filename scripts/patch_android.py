from pathlib import Path

manifest = Path("android/app/src/main/AndroidManifest.xml")
if not manifest.exists():
    raise SystemExit("AndroidManifest.xml not found")

s = manifest.read_text()
perm = '<uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />'

if perm in s:
    print("Exact-alarm permission already present")
else:
    # Insert inside the <manifest> root element, after its opening tag.
    match = __import__('re').search(r'<manifest\b[^>]*>', s, __import__('re').DOTALL)
    if not match:
        raise SystemExit("Could not find <manifest> root element")
    insert_at = match.end()
    s = s[:insert_at] + "\n    " + perm + s[insert_at:]
    manifest.write_text(s)
    print("Added exact-alarm permission")
