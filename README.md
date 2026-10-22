# jxl-photo-exe — jxl-photo as a Windows program (experimental)

[jxl-photo](https://github.com/rsilvabr/jxl-photo) packaged as `jxl-photo.exe`:
no Python to install, and the tools it calls (cjxl/djxl, ExifTool,
ImageMagick) come in the same folder. Unzip and run.

> **If you can use Python, use the Python version.**
> [jxl-photo](https://github.com/rsilvabr/jxl-photo) itself is what its author
> runs on their own photo archive every day, so it is by far the more tested
> of the two. Both pass the same real-photo test battery, but the program
> here is a newer, experimental way of packaging it. It is meant for people
> who would rather not install Python and the tools themselves.

**Current version: v2.15.2-exe1** (2026-10-22) · packages jxl-photo
[v2.15.2](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.15.2) ·
libjxl 0.12.0 · ExifTool 13.59 · ImageMagick 7.1.2-27 (Q16-HDRI) ·
[All releases](docs/version_history.md) · [How it works](docs/how_it_works.md)

---

## Contents

- [What it is](#what-it-is)
- [Download and first run](#download-and-first-run)
- [Command line](#command-line)
- [Where settings, presets and logs go](#where-settings-presets-and-logs-go)
- [Updating and removing](#updating-and-removing)
- [What is in the folder](#what-is-in-the-folder)
- [Good to know](#good-to-know)
- [Testing](#testing)
- [Building from source](#building-from-source)
- [License](#license) · [Acknowledgments](#acknowledgments)

---

## What it is

jxl-photo converts photo archives between TIFF/JPEG/PNG and JPEG XL, keeping
colour profiles and metadata, with safety checks before anything is deleted.
Everything it does is described in its own
[README](https://github.com/rsilvabr/jxl-photo#readme) and documentation;
this repository only packages it:

- The five jxl-photo scripts inside are **byte-for-byte** those of the
  jxl-photo release named above. No feature is added or removed.
- A small launcher starts them, and puts the bundled tools first on `PATH`.
- Each version of this package names the jxl-photo version it carries
  (`v2.15.2-exe1` = jxl-photo v2.15.2, first package of it).

## Download and first run

1. Download `jxl-photo-<version>-x64.zip` from
   [Releases](https://github.com/rsilvabr/jxl-photo-exe/releases).
2. Unzip it to a folder of your own, for example `D:\Programs\jxl-photo`.
   Avoid `C:\Program Files` (the folder must stay writable) and do not run it
   from inside the zip.
3. Double-click **`jxl-photo.exe`**. The interactive wizard opens in a console
   window and asks, step by step, what to convert and how.

The first time, Windows SmartScreen may say *"Windows protected your PC"*:
the program is not code-signed. Choose **More info → Run anyway**.

## Command line

From a terminal (`cmd` or PowerShell) in the program's folder:

```
jxl-photo.exe                                the interactive wizard
jxl-photo.exe --run-preset "MY PRESET"       a preset saved in the wizard, unattended
jxl-photo.exe --list-presets
jxl-photo.exe encode     "F:\Photos" --mode 6     TIFF -> JXL       (jxl_tiff_encoder.py)
jxl-photo.exe decode     "F:\Photos" --mode 1     JXL -> TIFF       (jxl_tiff_decoder.py)
jxl-photo.exe recompress "F:\Photos" --mode 1     JXL -> JXL        (jxl_recompressor.py)
jxl-photo.exe transcode  "F:\Photos" --mode 1     JPEG/PNG <-> JXL  (jxl_jpeg_transcoder.py)
```

`jxl-photo.exe encode --help` (and so on) prints every option of that script.
Each `encode`/`decode`/`recompress`/`transcode` line takes exactly what the
matching Python script takes: jxl-photo's per-script documentation applies
word for word — replace `py jxl_tiff_encoder.py` with
`jxl-photo.exe encode`, and so on.

A preset can be run from a scheduled task or a shortcut:

```
"D:\Programs\jxl-photo\jxl-photo.exe" --run-preset "SYNC PHOTOS"
```

## Where settings, presets and logs go

| What | Where |
|---|---|
| Settings and presets | `%USERPROFILE%\.jxl_tools_config.json` — the same file the Python version uses, so both see the same presets |
| Manifests the wizard creates | `scripts\manifests\` inside the program folder (where jxl-photo keeps them next to its scripts). A manifest you wrote yourself can live anywhere |
| Logs | `%LOCALAPPDATA%\jxl-photo\Logs` (set the `JXLPHOTO_LOG_DIR` environment variable to change it) |
| ICC profile cache | `%APPDATA%\jxl-photo\icc-cache` |
| Temporary files | `%TEMP%`, or the staging folder you choose in the wizard |

Nothing goes to the Windows registry.

## Updating and removing

- **Update:** unzip the new version over the old folder. Settings, presets
  and the manifests in `scripts\manifests\` are kept. If you unzip to a new
  folder instead, copy `scripts\manifests\` across (presets point at those
  files).
- **Remove:** delete the folder (with any manifests in it). Settings, logs and
  the ICC cache stay in the places above until you delete them too.

## What is in the folder

| Path | What |
|---|---|
| `jxl-photo.exe`, `_internal\` | Python 3.12 and the libraries the scripts use (numpy, tifffile, imagecodecs, Pillow, rich) |
| `scripts\` | The five jxl-photo scripts, unchanged |
| `tools\libjxl\` | `cjxl.exe`, `djxl.exe`, `jxlinfo.exe` — official libjxl 0.12.0 static build |
| `tools\exiftool\` | ExifTool 13.59 (Windows build) |
| `tools\imagemagick\` | `magick.exe` 7.1.2-27 portable (Q16-HDRI) and its configuration |
| `licenses\` | The licenses of everything above |

The program always uses its own tools, even when other versions are
installed on the PC: jxl-photo was tested with exactly these.

## Good to know

- **Antivirus:** some engines flag unsigned programs built with PyInstaller.
  This package uses the one-folder layout, the one they object to least; if
  yours quarantines a file, restore it and add the folder as an exception.
- **Size:** about 200 MB unzipped (85 MB zipped), mostly Python with numpy,
  ImageMagick and ExifTool.
- **Speed:** the conversions themselves run exactly as fast as with Python
  (the same cjxl/djxl do the work). Each script start costs a little more, so
  a run of many small batches is slightly slower.
- **Paths:** folders with Japanese or other non-Latin names, brackets,
  spaces, `%` and paths longer than 260 characters are supported and tested.
- **Bugs:** a problem with what jxl-photo *does* (a conversion, a colour, a
  metadata field) belongs in [jxl-photo's issues](https://github.com/rsilvabr/jxl-photo/issues);
  a problem with the program itself (it does not start, a tool is missing)
  belongs [here](https://github.com/rsilvabr/jxl-photo-exe/issues).

## Testing

`python tests/battery_on_exe.py` runs jxl-photo's real-photo battery
(`tools/real_photo_battery.py` from a jxl-photo checkout next to this one)
against the built program: every script run goes through `jxl-photo.exe`, and
the only cjxl, djxl, exiftool and magick on `PATH` are the bundled ones.

The battery converts real photos (camera exports from 18 cameras and phones,
film scans, JPEGs of every structure) through all four scripts inside a
folder named with Japanese, brackets, spaces and `%`, runs the wizard's
presets end to end, kills runs in the middle of a write, and checks the
files on disk: colour profiles, pixels, metadata, the delete gates.
`v2.15.2-exe1` passed all 110 checks in 886 s (711 s with Python).

## Building from source

Needs Python 3.12 on `PATH` and an internet connection:

```
python build.py
```

It creates a virtual environment in `.venv` (pinned packages and
PyInstaller), downloads the jxl-photo tag and the tools (each SHA-256
checked), and writes `dist\jxl-photo-<version>-x64\` plus its zip. The
jxl-photo tag and the tool versions are settings at the top of `build.py`.
Details: [How it works](docs/how_it_works.md).

## License

MIT for this packaging (see [LICENSE](LICENSE)). The package also contains
jxl-photo (MIT), libjxl (BSD-3-Clause), ExifTool (the same terms as Perl:
GPL or Artistic License), ImageMagick (its own Apache-2.0-style license) and
Python with its libraries (PSF and their own licenses). They are listed in
`licenses\` and in the PyInstaller-collected notices under `_internal\`.

## Acknowledgments

- [libjxl](https://github.com/libjxl/libjxl), [ExifTool](https://exiftool.org)
  (Phil Harvey) and [ImageMagick](https://imagemagick.org), which do the real
  work
- [PyInstaller](https://pyinstaller.org), which makes the Python program a
  Windows one
- [Claude](https://www.anthropic.com/claude) (Anthropic), among other AI tools,
  for code assistance, reviews and technical discussion
