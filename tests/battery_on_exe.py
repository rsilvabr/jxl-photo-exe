"""Runs jxl-photo's real-photo battery against the built program.

    python tests/battery_on_exe.py [--fixtures E:\\TESTE] [--keep]

Uses tools/real_photo_battery.py from a jxl-photo checkout (the sibling folder
../jxl-photo, or JXLPHOTO_REPO), unchanged: every script run goes through
dist/jxl-photo-<version>-x64/jxl-photo.exe and its bundled scripts, and the
only cjxl/djxl/exiftool/magick on PATH are the bundled ones (the battery's
own checks use them too). The report lands in AI_reports/ of this repo.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL_EXES = ("cjxl.exe", "djxl.exe", "exiftool.exe", "magick.exe")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", default=os.environ.get("JXLPHOTO_FIXTURES", r"E:\TESTE"))
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--app", default=None, help="the built folder (default: newest in dist/)")
    args = ap.parse_args()

    app = Path(args.app) if args.app else max(
        (p for p in (ROOT / "dist").glob("jxl-photo-*-x64") if p.is_dir()),
        key=lambda p: p.stat().st_mtime)
    exe, scripts, tools = app / "jxl-photo.exe", app / "scripts", app / "tools"
    repo = Path(os.environ.get("JXLPHOTO_REPO", ROOT.parent / "jxl-photo"))

    # Only the bundled tools: drop every PATH entry holding one of them.
    kept = [p for p in os.environ.get("PATH", "").split(os.pathsep)
            if p and not any((Path(p) / t).exists() for t in TOOL_EXES)]
    bundled = [str(tools / d) for d in ("libjxl", "exiftool", "imagemagick")]
    os.environ["PATH"] = os.pathsep.join(bundled + kept)
    os.environ["MAGICK_HOME"] = str(tools / "imagemagick")
    for t in TOOL_EXES:
        found = shutil.which(t)
        assert found and Path(found).resolve().is_relative_to(app.resolve()), (t, found)

    sys.path.insert(0, str(scripts))           # the battery imports the encoder
    sys.path.insert(1, str(repo / "tools"))
    import real_photo_battery as b

    b.PY = str(exe)
    b.ENC, b.DEC, b.REC, b.TR = (str(scripts / n) for n in (
        "jxl_tiff_encoder.py", "jxl_tiff_decoder.py", "jxl_recompressor.py",
        "jxl_jpeg_transcoder.py"))
    b.WRAP = str(scripts / "jxl_photo.py")
    b.REPO = ROOT                              # report and Logs check: this repo
    (ROOT / "AI_tools").mkdir(exist_ok=True)
    print(f"program: {exe}\nbattery: {repo / 'tools' / 'real_photo_battery.py'}", flush=True)
    sys.argv = ["real_photo_battery.py", "--fixtures", args.fixtures,
                "--work", str(Path(args.fixtures).anchor) + "jxlphoto_exe_battery"] \
        + (["--keep"] if args.keep else [])
    b.main()


if __name__ == "__main__":
    main()
