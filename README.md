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

**Current version: v2.15.2-exe2** (2026-10-22) · packages jxl-photo
[v2.15.2](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.15.2) ·
libjxl 0.12.0 · ExifTool 13.59 · ImageMagick 7.1.2-27 (Q16-HDRI) ·
jxl-thumb 0.1.1 ·
[All releases](docs/version_history.md) · [How it works](docs/how_it_works.md) ·
[Bug tracking](docs/bug_tracking.md)

---

## Contents

- [What it is](#what-it-is)
- [Download and first run](#download-and-first-run)
- [Command line](#command-line)
- [Thumbnails in Explorer](#thumbnails-in-explorer)
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

## Thumbnails in Explorer

Windows Explorer shows no thumbnails for JXL files unless something adds them.
The package comes with [jxl-thumb](https://github.com/rsilvabr/jxl-thumb),
which shows them quickly and with correct colours, also for wide-gamut
profiles such as ProPhoto and Adobe RGB.

When Explorer has no JXL thumbnail handler at all, the first double-click on
`jxl-photo.exe` offers to install it, once (`y`/`N`; the answer is
remembered). If you already use another handler, for example Microsoft's
JPEG XL extension, nothing is offered or replaced. The same from a terminal:

```
jxl-photo.exe thumbnails status       which handler Explorer uses for JXL
jxl-photo.exe thumbnails install      install jxl-thumb (or update it)
jxl-photo.exe thumbnails uninstall    remove it
```

The install is for the current Windows user only and needs no admin rights:
the DLL is copied to `%LOCALAPPDATA%\jxl-thumb` (so moving or deleting the
program folder does not break it) and registered under
`HKEY_CURRENT_USER\Software\Classes`. It is exactly what jxl-thumb's own
`install.cmd` does, and a jxl-thumb installed either way is the same
install. Thumbnails Windows cached before stay until the cache is cleared:
`tools\jxl-thumb\clear_thumbnail_cache.cmd`.

## Where settings, presets and logs go

| What | Where |
|---|---|
| Settings and presets | `%USERPROFILE%\.jxl_tools_config.json` — the same file the Python version uses, so both see the same presets |
| Manifests the wizard creates | `scripts\manifests\` inside the program folder (where jxl-photo keeps them next to its scripts). A manifest you wrote yourself can live anywhere |
| Logs | `%LOCALAPPDATA%\jxl-photo\Logs` (set the `JXLPHOTO_LOG_DIR` environment variable to change it) |
| ICC profile cache | `%APPDATA%\jxl-photo\icc-cache` |
| A copy of ExifTool | `%LOCALAPPDATA%\jxl-photo\exiftool-13.59`, only when the program folder's name is outside the Windows ANSI code page (Japanese, Cyrillic, ...) on a drive without 8.3 short names: ExifTool cannot start from such a folder ([#1](docs/bug_tracking.md)) |
| Temporary files | `%TEMP%`, or the staging folder you choose in the wizard |

The wizard also records in the settings file the tool paths it found at
start. With both versions in use they show whichever ran last; they are
informational only, every start looks the tools up again.

Nothing goes to the Windows registry, except the thumbnail handler when you
install it ([Thumbnails in Explorer](#thumbnails-in-explorer)). The answer to
the thumbnail offer is kept in `%LOCALAPPDATA%\jxl-photo\exe.json`.

## Updating and removing

- **Update:** unzip the new version over the old folder. Settings, presets
  and the manifests in `scripts\manifests\` are kept. If you unzip to a new
  folder instead, copy `scripts\manifests\` across (presets point at those
  files).
- **Remove:** run `jxl-photo.exe thumbnails uninstall` if you installed the
  thumbnails, then delete the folder (with any manifests in it). Settings, logs and
  the ICC cache stay in the places above until you delete them too.

## What is in the folder

| Path | What |
|---|---|
| `jxl-photo.exe`, `_internal\` | Python 3.12 and the libraries the scripts use (numpy, tifffile, imagecodecs, Pillow, rich) |
| `scripts\` | The five jxl-photo scripts, unchanged |
| `tools\libjxl\` | `cjxl.exe`, `djxl.exe`, `jxlinfo.exe` — official libjxl 0.12.0 static build |
| `tools\exiftool\` | ExifTool 13.59 (Windows build) |
| `tools\imagemagick\` | `magick.exe` 7.1.2-27 portable (Q16-HDRI) and its configuration |
| `tools\jxl-thumb\` | jxl-thumb 0.1.1 (Explorer thumbnails), with its own install/uninstall scripts |
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
  spaces, `%`, `&` and paths longer than 260 characters are supported and
  tested, for the photos and for the program's own folder.
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
The program itself runs from a copy in a folder named
`吾妻山 [app] 100% & co` on a drive without 8.3 short names.
`v2.15.2-exe2` passed all 110 checks in 999 s.

The wizard was also driven key by key through a real console and a real
double-click: the thumbnail offer (declined, remembered, accepted), a full
TIFF → JXL conversion with hostile folder and file names, and the
settings. See [Bug tracking](docs/bug_tracking.md) for what that found.

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
GPL or Artistic License), ImageMagick (its own Apache-2.0-style license), jxl-thumb (MIT) and
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
