"""Apply the Medsathi launcher icons to a freshly generated Android project.

`npx cap add android` writes Capacitor's default icon and splash artwork into
the generated project. This script copies the Medsathi icon set and branded
splash screens from `resources/android/` over those files and sets the
adaptive-icon background colour, so the installed app shows the real logo
instead of the Capacitor placeholder.

Safe to run more than once; it only overwrites icon files it owns.
"""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "resources" / "android"
RES = ROOT / "android" / "app" / "src" / "main" / "res"

DENSITIES = ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]
BACKGROUND = "#084A5A"

# Explicit source -> destination pairs. Do NOT classify by substring: the
# word "foreground" contains "round", which used to send the transparent
# adaptive foreground into ic_launcher_round.png and leave the Capacitor
# placeholder as the real adaptive foreground (white-on-white launcher).
ICON_FILES = (
    ("ic_launcher_{density}.png", "ic_launcher.png"),
    ("ic_launcher_round_{density}.png", "ic_launcher_round.png"),
    ("ic_launcher_foreground_{density}.png", "ic_launcher_foreground.png"),
)

SPLASH_FILES = (
    ("splash_base.png", "drawable/splash.png"),
    *((f"splash_port_{d}.png", f"drawable-port-{d}/splash.png") for d in DENSITIES),
    *((f"splash_land_{d}.png", f"drawable-land-{d}/splash.png") for d in DENSITIES),
)


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
        for source_name, target_name in ICON_FILES:
            src = SRC / source_name.format(density=density)
            if not src.exists():
                continue
            shutil.copyfile(src, target_dir / target_name)
            copied += 1

    # Branded launch background behind the WebView (styles.xml points at
    # @drawable/splash) instead of Capacitor's white/blue placeholder.
    for source_name, target_rel in SPLASH_FILES:
        src = SRC / source_name
        if not src.exists():
            continue
        out = RES / target_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)
        copied += 1

    # Adaptive icons reference @color/ic_launcher_background in
    # mipmap-anydpi-v26/ic_launcher.xml; keep it on brand teal.
    values = RES / "values"
    values.mkdir(parents=True, exist_ok=True)
    colors = values / "ic_launcher_background.xml"
    colors.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<resources>\n"
        f'    <color name="ic_launcher_background">{BACKGROUND}</color>\n'
        "</resources>\n"
    )

    print(f"Applied Medsathi icons: {copied} files, background {BACKGROUND}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
