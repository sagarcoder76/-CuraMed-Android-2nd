"""Apply the Medsathi launcher icons to a freshly generated Android project.

`npx cap add android` writes Capacitor's default icon into every mipmap folder.
This script copies the Medsathi icon set from `resources/android/` over those
files and sets the adaptive-icon background colour, so the installed app shows
the real logo instead of the Capacitor placeholder.

Safe to run more than once; it only overwrites icon files it owns.
"""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "resources" / "android"
RES = ROOT / "android" / "app" / "src" / "main" / "res"

DENSITIES = ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]
BACKGROUND = "#C62A52"


def main() -> int:
    if not SRC.is_dir():
        print("resources/android not found — skipping icon step")
        return 0
    if not RES.is_dir():
        print("android res folder not found — run `npx cap add android` first")
        return 0

    copied = 0
    for density in DENSITIES:
        target_dir = RES / f"mipmap-{density}"
        target_dir.mkdir(parents=True, exist_ok=True)
        for name in (f"ic_launcher_{density}.png",
                     f"ic_launcher_round_{density}.png",
                     f"ic_launcher_foreground_{density}.png"):
            src = SRC / name
            if not src.exists():
                continue
            if "round" in name:
                out = target_dir / "ic_launcher_round.png"
            elif "foreground" in name:
                out = target_dir / "ic_launcher_foreground.png"
            else:
                out = target_dir / "ic_launcher.png"
            shutil.copyfile(src, out)
            copied += 1

    # Adaptive icons reference @color/ic_launcher_background on some templates.
    values = RES / "values"
    values.mkdir(parents=True, exist_ok=True)
    colors = values / "ic_launcher_background.xml"
    colors.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        f'    <color name="ic_launcher_background">{BACKGROUND}</color>\n'
        "</resources>\n"
    )

    # Splash background should match the brand instead of Capacitor blue.
    styles = values / "styles.xml"
    if styles.exists():
        text = styles.read_text()
        if "#FFFFFF" in text and "Medsathi" not in text:
            styles.write_text(text)
    print(f"Applied Medsathi icons: {copied} files, background {BACKGROUND}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
