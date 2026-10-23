"""Builds dist/jxl-photo-<version>-x64.zip: jxl-photo.exe, the five scripts of
a published jxl-photo tag, and the tools they call.

    python build.py            (Python 3.12 on PATH; first run ~5 minutes)

Everything downloaded is pinned: the jxl-photo scripts come from the tag below
(TOOLKIT_VERSION inside must match it), the tools from their official
releases with a SHA-256 check. A virtual environment in .venv holds the
pinned Python packages and PyInstaller, so the system Python is not touched.
"""

import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

# --- settings --------------------------------------------------------------
JXLPHOTO_TAG = "v2.17.0"
# Package revision for this jxl-photo tag: v2.16.0 + 1 -> release "v2.16.0-exe1".
PACKAGE_REVISION = 1
TOOLS = {
    "libjxl": ("https://github.com/libjxl/libjxl/releases/download/v0.12.0/"
               "jxl-x64-windows-static.7z",
               "ff147dc7ac4ce55392974ccc70f2a8a8ec0eff3ae28529b072258b66c8f01ab2"),
    "exiftool": ("https://sourceforge.net/projects/exiftool/files/"
                 "exiftool-13.59_64.zip/download",
                 "44b512b25af500724ba579d0a53c8fc5851628b692dd5e5d94ae4a15c2cba9ec"),
    "imagemagick": ("https://github.com/ImageMagick/ImageMagick/releases/download/"
                    "7.1.2-27/ImageMagick-7.1.2-27-portable-Q16-HDRI-x64.7z",
                    "c7d6f13b3021db5d2e23876d85f06d6039a9a345236f0d32cdb73886ddfe70ed"),
    "jxl-thumb": ("https://github.com/rsilvabr/jxl-thumb/releases/download/v0.2.1/"
                  "jxl-thumb-0.2.1-x64.zip",
                  "fe924f2f065cd7c11c727d9455f60b6b3882c81df049ea119a6b0e5906a9e9dd"),
}
REQUIREMENTS = ["numpy==2.5.1", "tifffile==2026.6.1", "imagecodecs==2026.6.26",
                "pillow==12.3.0", "rich==15.0.0", "pyinstaller==6.22.2"]
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
DEPS, BUILD, DIST = ROOT / "deps", ROOT / "build", ROOT / "dist"
VENV = ROOT / ".venv"
WINTAR = Path(r"C:\Windows\System32\tar.exe")   # bsdtar: reads .zip and .7z
SCRIPT_NAMES = ["jxl_tiff_encoder.py", "jxl_tiff_decoder.py", "jxl_recompressor.py",
                "jxl_jpeg_transcoder.py", "jxl_photo.py"]


def rmtree(path):
    """shutil.rmtree that also removes read-only files (ExifTool's archive
    marks some of its files read-only, and copies keep the attribute)."""
    def _clear(func, p, _exc):
        os.chmod(p, 0o666)
        func(p)
    shutil.rmtree(path, onexc=_clear)


def step(msg):
    print(f"\n== {msg}", flush=True)


def fetch(url, dest, sha256=None):
    if not dest.exists():
        print(f"   downloading {url}")
        DEPS.mkdir(exist_ok=True)
        with urllib.request.urlopen(url, timeout=300) as r:
            data = r.read()
        dest.write_bytes(data)
    if sha256:
        got = hashlib.sha256(dest.read_bytes()).hexdigest()
        if got != sha256:
            dest.unlink()
            sys.exit(f"SHA-256 mismatch for {dest.name}: {got} (deleted)")
    return dest


def extract(archive, into):
    if into.exists():
        rmtree(into)
    into.mkdir(parents=True)
    subprocess.run([str(WINTAR), "-xf", str(archive), "-C", str(into)], check=True)
    return into


def venv_python():
    py = VENV / "Scripts" / "python.exe"
    if not py.exists():
        step("Python environment (.venv)")
        subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)
    subprocess.run([str(py), "-m", "pip", "install", "--quiet", "--disable-pip-version-check"]
                   + REQUIREMENTS, check=True)
    return py


def get_scripts(app):
    step(f"jxl-photo {JXLPHOTO_TAG} scripts")
    z = fetch(f"https://github.com/rsilvabr/jxl-photo/archive/refs/tags/{JXLPHOTO_TAG}.zip",
              DEPS / f"jxl-photo-{JXLPHOTO_TAG}.zip")
    dest = app / "scripts"
    dest.mkdir(parents=True)
    with zipfile.ZipFile(z) as zf:
        top = zf.namelist()[0].split("/")[0]
        for name in SCRIPT_NAMES + ["LICENSE"]:
            data = zf.read(f"{top}/{name}")
            (dest if name.endswith(".py") else app / "licenses").mkdir(exist_ok=True)
            out = dest / name if name.endswith(".py") else app / "licenses" / "LICENSE.jxl-photo"
            out.write_bytes(data)
    version = JXLPHOTO_TAG.lstrip("v")
    for name in SCRIPT_NAMES:
        text = (dest / name).read_text(encoding="utf-8")
        m = re.search(r'^TOOLKIT_VERSION = "([^"]+)"', text, re.M)
        if not m or m.group(1) != version:
            sys.exit(f"{name}: TOOLKIT_VERSION {m and m.group(1)} != tag {JXLPHOTO_TAG}")
    return version


def get_tools(app):
    step("tools (libjxl, exiftool, ImageMagick, jxl-thumb)")
    tools, lic = app / "tools", app / "licenses"
    url, sha = TOOLS["libjxl"]
    x = extract(fetch(url, DEPS / "jxl-x64-windows-static.7z", sha), BUILD / "x_libjxl")
    d = tools / "libjxl"
    d.mkdir(parents=True)
    for exe in ("cjxl.exe", "djxl.exe", "jxlinfo.exe"):
        shutil.copy2(next(x.rglob(exe)), d / exe)
    for f in next(x.rglob("licenses")).rglob("*"):
        if f.is_file():
            shutil.copy2(f, lic / f"libjxl-{f.parent.name}-{f.name}")

    url, sha = TOOLS["exiftool"]
    x = extract(fetch(url, DEPS / "exiftool-13.59_64.zip", sha), BUILD / "x_exiftool")
    src = next(x.rglob("exiftool(-k).exe")).parent
    d = tools / "exiftool"
    shutil.copytree(src / "exiftool_files", d / "exiftool_files")
    # Renamed: exiftool(-k).exe waits for a key press after every call.
    shutil.copy2(src / "exiftool(-k).exe", d / "exiftool.exe")
    shutil.copy2(src / "README.txt", lic / "exiftool-README.txt")
    # Names the copy the launcher makes when the program folder is not
    # ANSI-safe (see _exiftool_dir in src/jxl_photo_exe.py).
    ver = re.search(r"exiftool-([\d.]+)_", url).group(1)
    (d / "VERSION.txt").write_text(ver + "\n", encoding="utf-8")

    url, sha = TOOLS["imagemagick"]
    x = extract(fetch(url, DEPS / Path(url).name, sha), BUILD / "x_imagemagick")
    src = next(x.rglob("magick.exe")).parent
    d = tools / "imagemagick"
    d.mkdir()
    # magick.exe alone does every operation; the other programs are aliases.
    for f in src.iterdir():
        if f.suffix.lower() in (".xml", ".icc") or f.name == "magick.exe":
            shutil.copy2(f, d / f.name)
    shutil.copy2(src / "LICENSE.txt", lic / "LICENSE.imagemagick.txt")
    shutil.copy2(src / "NOTICE.txt", lic / "NOTICE.imagemagick.txt")

    url, sha = TOOLS["jxl-thumb"]
    x = extract(fetch(url, DEPS / Path(url).name, sha), BUILD / "x_jxl-thumb")
    src = next(x.rglob("jxl_thumb.dll")).parent
    d = tools / "jxl-thumb"
    d.mkdir()
    # The launcher installs the DLL itself ('jxl-photo.exe thumbnails install');
    # the batch files stay for anyone who prefers jxl-thumb's own.
    for name in ("jxl_thumb.dll", "install.cmd", "uninstall.cmd",
                 "clear_thumbnail_cache.cmd", "README.md"):
        shutil.copy2(src / name, d / name)
    shutil.copy2(src / "LICENSE", lic / "LICENSE.jxl-thumb")


def version_info(version):
    nums = (version.split(".") + ["0", "0", "0"])[:3] + ["0"]
    (BUILD / "version_info.txt").write_text(f"""VSVersionInfo(
  ffi=FixedFileInfo(filevers=({','.join(nums)}), prodvers=({','.join(nums)})),
  kids=[StringFileInfo([StringTable('040904B0', [
    StringStruct('CompanyName', 'rsilvabr'),
    StringStruct('FileDescription', 'jxl-photo - JPEG XL photo archive toolkit'),
    StringStruct('FileVersion', '{version}'),
    StringStruct('ProductName', 'jxl-photo'),
    StringStruct('ProductVersion', '{version}'),
    StringStruct('LegalCopyright', 'MIT License')])]),
  VarFileInfo([VarStruct('Translation', [1033, 1200])])])
""", encoding="utf-8")


def repack():
    """`python build.py --repack`: zip dist\\<package>\\ again, as it now stands.
    The release workflow builds, has jxl-photo.exe signed, puts the signed
    file back in the folder, then repacks."""
    out = DIST / f"jxl-photo-{JXLPHOTO_TAG.lstrip('v')}-exe{PACKAGE_REVISION}-x64"
    if not out.is_dir():
        sys.exit(f"{out} does not exist: run python build.py first")
    old = out.parent / (out.name + ".zip")    # not with_suffix: the name has dots
    if old.exists():
        old.unlink()
    z = shutil.make_archive(str(out), "zip", out.parent, out.name)
    print(f"Repacked {Path(z).name} ({Path(z).stat().st_size / 1e6:.0f} MB)")


def main():
    if "--repack" in sys.argv[1:]:
        return repack()
    py = venv_python()
    if BUILD.exists():
        rmtree(BUILD)
    app = BUILD / "app"
    (app / "licenses").mkdir(parents=True)
    version = get_scripts(app)
    get_tools(app)
    version_info(version)

    step("PyInstaller")
    subprocess.run([str(py), "-m", "PyInstaller", "--noconfirm", "--clean",
                    "--distpath", str(BUILD / "pyi_dist"), "--workpath", str(BUILD / "pyi_work"),
                    str(ROOT / "jxl-photo.spec")], check=True, cwd=ROOT)

    step("assemble")
    out = DIST / f"jxl-photo-{version}-exe{PACKAGE_REVISION}-x64"
    if out.exists():
        rmtree(out)
    shutil.copytree(BUILD / "pyi_dist" / "jxl-photo", out)
    for sub in ("scripts", "tools", "licenses"):
        shutil.copytree(app / sub, out / sub)
    shutil.copy2(ROOT / "LICENSE", out / "licenses" / "LICENSE.jxl-photo-exe")
    # PyInstaller bundles the Python runtime but not its license (PSF).
    shutil.copy2(Path(sys.base_prefix) / "LICENSE.txt", out / "licenses" / "LICENSE.python.txt")
    shutil.copy2(ROOT / "README.md", out / "README.md")
    # No read-only files or folders in the package (ExifTool's archive marks
    # some): an update unzips over the old folder, and a copy must be deletable.
    for f in out.rglob("*"):
        os.chmod(f, 0o666 if f.is_file() else 0o777)
    z = shutil.make_archive(str(out), "zip", out.parent, out.name)
    size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
    print(f"\nBuilt {out} ({size / 1e6:.0f} MB) and {Path(z).name} "
          f"({Path(z).stat().st_size / 1e6:.0f} MB)")


if __name__ == "__main__":
    main()
