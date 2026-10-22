"""Runs jxl-photo's real-photo battery against the built program.

    python tests/battery_on_exe.py [--fixtures E:\\TESTE] [--keep] [--ascii-app]

Uses tools/real_photo_battery.py from a jxl-photo checkout (the sibling folder
../jxl-photo, or JXLPHOTO_REPO), unchanged: every script run goes through
dist/jxl-photo-<version>-x64/jxl-photo.exe and its bundled scripts, and the
only cjxl/djxl/exiftool/magick on PATH are the bundled ones (the battery's
own checks use them too). The report lands in AI_tools/ of this repo.

The program itself runs from a copy in a HOSTILE folder on the fixtures'
drive (Japanese, brackets, a space, % and &), not from dist/: ExifTool's
Windows launcher fails in a folder outside the ANSI code page, and a drive
without 8.3 short names (E: here) also exercises the launcher's fallback
copy. --ascii-app runs it from dist/ instead.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL_EXES = ("cjxl.exe", "djxl.exe", "exiftool.exe", "magick.exe")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # hostile paths
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", default=os.environ.get("JXLPHOTO_FIXTURES", r"E:\TESTE"))
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--app", default=None, help="the built folder (default: newest in dist/)")
    ap.add_argument("--ascii-app", action="store_true",
                    help="run the program from the built folder, not a hostile copy")
    args = ap.parse_args()

    app = Path(args.app) if args.app else max(
        (p for p in (ROOT / "dist").glob("jxl-photo-*-x64") if p.is_dir()),
        key=lambda p: p.stat().st_mtime)
    # Absolute: the battery runs each script from its own working folder.
    app = app.resolve()
    if not args.ascii_app:
        hostile = (Path(Path(args.fixtures).anchor) / "jxlphoto_exe_battery_app"
                   / "吾妻山 [app] 100% & co" / app.name)
        if hostile.parent.exists():
            # ExifTool's archive marks some folders read-only.
            shutil.rmtree(hostile.parent, onexc=lambda f, q, e: (os.chmod(q, 0o777), f(q)))
        shutil.copytree(app, hostile)
        app = hostile
    exe, scripts, tools = app / "jxl-photo.exe", app / "scripts", app / "tools"
    repo = Path(os.environ.get("JXLPHOTO_REPO", ROOT.parent / "jxl-photo"))

    # Only the bundled tools: drop every PATH entry holding one of them.
    kept = [p for p in os.environ.get("PATH", "").split(os.pathsep)
            if p and not any((Path(p) / t).exists() for t in TOOL_EXES)]
    # The battery's own exiftool calls need the folder the launcher picks.
    sys.path.insert(0, str(ROOT / "src"))
    import jxl_photo_exe as launcher
    launcher.TOOLS = tools
    exiftool_dir = launcher._exiftool_dir()
    print(f"exiftool from: {exiftool_dir}", flush=True)
    bundled = [str(tools / "libjxl"), str(exiftool_dir), str(tools / "imagemagick")]
    os.environ["PATH"] = os.pathsep.join(bundled + kept)
    os.environ["MAGICK_HOME"] = str(tools / "imagemagick")
    for t in TOOL_EXES:
        found = shutil.which(t)
        assert found and (Path(found).resolve().is_relative_to(app.resolve())
                          or Path(found).parent == exiftool_dir), (t, found)

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
