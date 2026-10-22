"""jxl-photo.exe: the jxl-photo toolkit as a Windows program, no Python needed.

The five jxl-photo scripts ship unchanged in `scripts/` next to the program,
and the codecs and tools they call in `tools/`. This launcher only routes:

    jxl-photo.exe                          the interactive wrapper (jxl_photo.py)
    jxl-photo.exe --run-preset NAME ...    the wrapper, with its own options
    jxl-photo.exe encode|decode|recompress|transcode ARGS
                                           one backend directly
    jxl-photo.exe <scripts>\\<name>.py ARGS
                                           how the wrapper starts a backend: it
                                           runs [sys.executable, script, ...],
                                           and sys.executable is this program

Before running anything it puts tools/ first on PATH (the scripts find cjxl,
djxl, exiftool and magick there) and, unless JXLPHOTO_LOG_DIR is set, sends
the logs to %LOCALAPPDATA%\\jxl-photo\\Logs instead of the program folder.
"""

import os
import runpy
import sys
from pathlib import Path

BACKENDS = {
    "encode": "jxl_tiff_encoder.py",
    "decode": "jxl_tiff_decoder.py",
    "recompress": "jxl_recompressor.py",
    "transcode": "jxl_jpeg_transcoder.py",
}

def _app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent / "build" / "app"


APP = _app_dir()
SCRIPTS = APP / "scripts"
TOOLS = APP / "tools"


def _setup_environment() -> None:
    tool_dirs = [TOOLS / d for d in ("libjxl", "exiftool", "imagemagick")]
    found = [str(d) for d in tool_dirs if d.is_dir()]
    os.environ["PATH"] = os.pathsep.join(found + [os.environ.get("PATH", "")])
    # The portable ImageMagick reads its configuration from its own folder.
    if (TOOLS / "imagemagick").is_dir():
        os.environ.setdefault("MAGICK_HOME", str(TOOLS / "imagemagick"))
    if not os.environ.get("JXLPHOTO_LOG_DIR"):
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home())
        os.environ["JXLPHOTO_LOG_DIR"] = str(base / "jxl-photo" / "Logs")
    sys.path.insert(0, str(SCRIPTS))


def _resolve(argv):
    """(script path, remaining arguments) for this command line."""
    if argv:
        first = argv[0]
        if first.lower() in BACKENDS:
            return SCRIPTS / BACKENDS[first.lower()], argv[1:]
        if first.lower().endswith(".py"):
            script = Path(first).resolve()
            # Only the bundled scripts: this is not a general Python launcher.
            if script.parent == SCRIPTS.resolve() and script.is_file():
                return script, argv[1:]
            sys.exit(f"jxl-photo: not one of the bundled scripts: {first}")
    return SCRIPTS / "jxl_photo.py", argv


def main() -> None:
    _setup_environment()
    script, args = _resolve(sys.argv[1:])
    sys.argv = [str(script)] + list(args)
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
