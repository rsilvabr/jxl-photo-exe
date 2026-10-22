# How it works

## One program, five scripts

jxl-photo is five Python scripts: the wizard (`jxl_photo.py`) and four
backends it starts as separate processes. The wizard starts a backend with
`[sys.executable, <script>, ...]`, the usual way for a Python program to run
another script.

In the packaged program `sys.executable` is `jxl-photo.exe` itself. So the
launcher (`src/jxl_photo_exe.py`) only has to route its command line:

| Command line | Runs |
|---|---|
| `jxl-photo.exe [options]` | `scripts\jxl_photo.py` (the wizard) |
| `jxl-photo.exe encode\|decode\|recompress\|transcode ...` | the matching backend |
| `jxl-photo.exe <program folder>\scripts\<name>.py ...` | that script — how the wizard starts a backend |

A `.py` path outside the program's `scripts\` folder is refused: this is not
a general Python launcher. The script runs through `runpy` as `__main__`,
exactly as `python <script>` would run it, so its exit codes, prompts and
output are unchanged. No line of jxl-photo is modified.

## Python and its libraries

PyInstaller builds a one-folder program: `jxl-photo.exe` plus `_internal\`
with Python 3.12 and every module the scripts import. To find those modules,
the build imports the five scripts as modules (`hiddenimports` in
`jxl-photo.spec`), and collects imagecodecs, tifffile and rich completely
(their codecs and data files are loaded dynamically). The scripts also ship
as plain `.py` files in `scripts\`: that is what runs, and what the wizard
finds next to itself.

imagecodecs builds against a few codecs jxl-photo never uses (JPEG XS,
Jetraw, HEIF); PyInstaller warns that their DLLs are missing, which is
harmless.

## The tools

Before running a script the launcher puts `tools\libjxl`, `tools\exiftool`
and `tools\imagemagick` first on `PATH`, and sets `MAGICK_HOME` to the
ImageMagick folder (the portable build reads its configuration there). The
scripts look tools up on `PATH`, so they use the bundled ones; processes they
start inherit the same `PATH`.

| Tool | Source | Notes |
|---|---|---|
| cjxl, djxl, jxlinfo | libjxl 0.12.0 official `jxl-x64-windows-static.7z` | static, no DLLs |
| ExifTool 13.59 | the official Windows build | `exiftool(-k).exe` is renamed `exiftool.exe`: the `(-k)` name waits for a key press after every call |
| ImageMagick 7.1.2-27 | official portable Q16-HDRI x64 | only `magick.exe` and its `.xml`/`.icc` configuration; the other programs in the archive are aliases of it |

## Logs

The scripts write their logs into a `Logs\` folder next to themselves unless
`JXLPHOTO_LOG_DIR` says otherwise. Next to them is the program folder, which
may not be writable, so the launcher sets `JXLPHOTO_LOG_DIR` to
`%LOCALAPPDATA%\jxl-photo\Logs` when it is not already set.

## Files next to the scripts

The wizard keeps the manifests it creates in a `manifests\` folder next to
its scripts: `scripts\manifests\` in the program folder. That is the one
thing written inside it. A settings file named `.jxl_tools_config.json`
placed in `scripts\` would also be used instead of the one in
`%USERPROFILE%` (jxl-photo's rule for a portable setup).

## The build

`build.py`:

1. creates `.venv` with the pinned packages and PyInstaller;
2. downloads the jxl-photo tag `JXLPHOTO_TAG` from GitHub, takes the five
   scripts and the license, and checks that their `TOOLKIT_VERSION` matches
   the tag;
3. downloads the three tools, checks each SHA-256, and copies what is needed
   into `build\app\tools`;
4. runs PyInstaller with `jxl-photo.spec` (the Windows version information
   is written from the tag);
5. assembles `dist\jxl-photo-<version>-x64\` and zips it.

Packaging a new jxl-photo release: change `JXLPHOTO_TAG`, run `build.py`,
then `tests/battery_on_exe.py`; publish only when every check passes.
