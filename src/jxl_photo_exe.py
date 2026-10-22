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
    jxl-photo.exe thumbnails [status|install|uninstall]
                                           Explorer thumbnails for JXL files,
                                           with the bundled jxl-thumb

Before running anything it puts tools/ first on PATH (the scripts find cjxl,
djxl, exiftool and magick there) and, unless JXLPHOTO_LOG_DIR is set, sends
the logs to %LOCALAPPDATA%\\jxl-photo\\Logs instead of the program folder.
"""

import json
import os
import runpy
import shutil
import subprocess
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


def _ansi_safe(path: str) -> bool:
    """True when `path` survives the ANSI code page (the "mbcs" codec)."""
    try:
        path.encode("mbcs", "strict")
        return True
    except UnicodeEncodeError:
        return False


def _short_path(path: Path):
    import ctypes
    buf = ctypes.create_unicode_buffer(32768)
    n = ctypes.windll.kernel32.GetShortPathNameW(str(path), buf, len(buf))
    return buf.value if 0 < n < len(buf) else None


def _exiftool_dir() -> Path:
    """The folder to put on PATH for exiftool.

    ExifTool's Windows launcher looks for its exiftool_files folder through
    an ANSI path: in a program folder named in Japanese, Cyrillic or any
    script outside the ANSI code page it fails ("Could not find ...???...
    perl5*.dll") while cjxl, djxl and magick work. The 8.3 short name of the
    folder fixes that where the volume has short names (usually C:); on one
    without them, ExifTool is copied once to an ANSI-safe folder.
    """
    bundled = TOOLS / "exiftool"
    if not bundled.is_dir() or _ansi_safe(str(bundled)):
        return bundled
    short = _short_path(bundled)
    if short and _ansi_safe(short):
        return Path(short)
    version_file = bundled / "VERSION.txt"
    version = (version_file.read_text(encoding="utf-8").strip()
               if version_file.is_file() else "unknown")
    bases = [os.environ.get("LOCALAPPDATA"), os.environ.get("ProgramData"),
             (os.environ.get("SystemDrive") or "C:") + "\\"]
    for base in bases:
        if not base:
            continue
        target = Path(base) / "jxl-photo" / f"exiftool-{version}"
        if not _ansi_safe(str(target)):
            continue
        if (target / "exiftool.exe").is_file():
            return target
        tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
        try:
            shutil.copytree(bundled, tmp)
            for f in tmp.rglob("*"):   # deletable later, like the package
                os.chmod(f, 0o666 if f.is_file() else 0o777)
            os.replace(tmp, target)
            return target
        except OSError:
            shutil.rmtree(tmp, ignore_errors=True)
            if (target / "exiftool.exe").is_file():   # another start won the race
                return target
    return bundled   # nothing better: the scripts report exiftool as missing


def _setup_environment() -> None:
    tool_dirs = [TOOLS / "libjxl", _exiftool_dir(), TOOLS / "imagemagick"]
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


# --- Explorer thumbnails (the bundled jxl-thumb) -----------------------------
# Explorer looks up a .jxl thumbnail handler under this shell-extension GUID
# (IThumbnailProvider), per extension or under SystemFileAssociations.
_THUMB_HANDLER_KEYS = (r".jxl\ShellEx\{e357fccd-a995-4576-b01f-234630154e96}",
                       r"SystemFileAssociations\.jxl\ShellEx"
                       r"\{e357fccd-a995-4576-b01f-234630154e96}")
JXL_THUMB = TOOLS / "jxl-thumb"
JXL_THUMB_CLSID = "{EF830030-FBD6-4B62-BFD4-0DBD590D6135}"
WIC_THUMB_CLSID = "{C7657C4A-9F68-40fa-A4DF-96BC08EB3551}"
# Same place as jxl-thumb's own install.cmd: the DLL Explorer loads must not
# live in a program folder that may be moved or deleted.
THUMB_DEST = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "jxl-thumb"
STATE_FILE = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "jxl-photo" / "exe.json"
THUMB_TIP = ("Tip: Explorer shows no thumbnails for JXL files on this PC. "
             "Run 'jxl-photo.exe thumbnails install' to add them (no admin rights).")


def _thumbnail_handler():
    """The CLSID Explorer uses for .jxl thumbnails, or None when there is none."""
    import winreg
    for sub in _THUMB_HANDLER_KEYS:
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, sub) as key:
                value = str(winreg.QueryValue(key, None) or "").strip()
        except OSError:
            continue
        if value:
            return value
    return None


def _regsvr32(*args) -> int:
    exe = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "regsvr32.exe"
    return subprocess.run([str(exe), "/s", *args]).returncode


def _install_thumbnails() -> int:
    """What jxl-thumb's install.cmd does, without cmd.exe (a program folder
    named with % or & would break a batch file)."""
    dll = JXL_THUMB / "jxl_thumb.dll"
    if not dll.is_file():
        print(f"jxl_thumb.dll is missing from {JXL_THUMB}")
        return 1
    THUMB_DEST.mkdir(parents=True, exist_ok=True)
    target = THUMB_DEST / "jxl_thumb.dll"
    # Explorer may hold the old DLL open: a loaded DLL cannot be overwritten,
    # but it can be renamed. Leftovers of earlier updates go once they are free.
    for old in THUMB_DEST.glob("*.old"):
        try:
            old.unlink()
        except OSError:
            pass
    if target.exists():
        target.rename(THUMB_DEST / f"jxl_thumb.dll.{os.getpid()}.old")
    shutil.copy2(dll, target)
    if _regsvr32(str(target)) != 0:
        print("INSTALL FAILED: regsvr32 could not register jxl_thumb.dll")
        return 1
    print(f"jxl-thumb installed in {THUMB_DEST} (for this Windows user only).\n"
          "New thumbnails use it now. Thumbnails Windows already cached stay until\n"
          f"the cache is cleared: {JXL_THUMB / 'clear_thumbnail_cache.cmd'}")
    return 0


def _uninstall_thumbnails() -> int:
    target = THUMB_DEST / "jxl_thumb.dll"
    if target.exists():
        _regsvr32("/u", str(target))
    shutil.rmtree(THUMB_DEST, ignore_errors=True)
    if THUMB_DEST.exists():
        print(f"jxl-thumb is unregistered. Explorer still has the DLL open, so the folder\n"
              f"{THUMB_DEST} could not be deleted yet: delete it after signing out.")
    else:
        print("jxl-thumb removed.")
    return 0


def _thumbnails_command(args) -> int:
    action = args[0].lower() if args else "status"
    if action == "install":
        return _install_thumbnails()
    if action == "uninstall":
        return _uninstall_thumbnails()
    if action == "status":
        handler = _thumbnail_handler()
        if handler is None:
            print("Explorer has no thumbnail handler for JXL files.")
        elif handler.lower() == JXL_THUMB_CLSID.lower():
            print(f"Explorer uses jxl-thumb for JXL thumbnails ({THUMB_DEST}).")
        elif handler.lower() == WIC_THUMB_CLSID.lower():
            print("Explorer uses Windows' own image thumbnail handler for JXL files\n"
                  "(Microsoft's JPEG XL extension). 'thumbnails install' replaces it\n"
                  "with jxl-thumb for this Windows user; 'uninstall' brings it back.")
        else:
            print(f"Explorer uses another thumbnail handler for JXL files: {handler}")
        return 0
    print("usage: jxl-photo.exe thumbnails [status|install|uninstall]")
    return 2


def _load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _offer_thumbnails() -> None:
    """Before the wizard: once, offer jxl-thumb when Explorer has no JXL
    thumbnail handler at all, or only Windows' own (Microsoft's JPEG XL
    extension, which ships with many Windows 11 installs: slow on large
    photos and not colour-managed). Any other handler — jxl-thumb itself, or
    one installed on purpose — is left alone."""
    handler = _thumbnail_handler()
    if handler is None:
        # From now on the wizard's own tip (jxl-photo 2.15.3+) names the
        # bundled command instead of the jxl-thumb download page.
        os.environ.setdefault("JXLPHOTO_THUMBNAIL_TIP", THUMB_TIP)
        message = ("Windows Explorer shows no thumbnails for JXL files on this PC.\n"
                   "jxl-photo comes with jxl-thumb, which adds them (for this Windows user only,\n"
                   "no admin rights; 'jxl-photo.exe thumbnails uninstall' removes it).")
    elif handler.lower() == WIC_THUMB_CLSID.lower():
        message = ("Windows Explorer makes JXL thumbnails with Microsoft's JPEG XL extension:\n"
                   "slow on large photos, and not colour-managed (ProPhoto and Adobe RGB\n"
                   "photos look washed out). jxl-photo comes with jxl-thumb, which is much\n"
                   "faster and converts the colours (for this Windows user only, no admin\n"
                   "rights; 'jxl-photo.exe thumbnails uninstall' brings Windows' own back).")
    else:
        return
    state = _load_state()
    if state.get("thumbnail_offer_answered") or not sys.stdin.isatty():
        return
    print(message)
    try:
        answer = input("Install it now? [y/N]: ").strip().lower()
    except EOFError:
        return
    state["thumbnail_offer_answered"] = True
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state), encoding="utf-8")
    except OSError:
        pass
    if answer.startswith("y"):
        if _install_thumbnails() == 0:
            os.environ.pop("JXLPHOTO_THUMBNAIL_TIP", None)
    print()


def main() -> None:
    # A redirected stdout falls back to the ANSI code page, where a program
    # folder named in Japanese cannot be printed (the scripts do the same).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    _setup_environment()
    argv = sys.argv[1:]
    if argv and argv[0].lower() == "thumbnails":
        sys.exit(_thumbnails_command(argv[1:]))
    if not argv:
        try:
            _offer_thumbnails()
        except Exception as exc:   # never keep the wizard from starting
            print(f"(thumbnail check skipped: {exc})")
    script, args = _resolve(argv)
    sys.argv = [str(script)] + list(args)
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
