# jxl-photo-exe — jxl-photo as a Windows program (experimental)

[jxl-photo](https://github.com/rsilvabr/jxl-photo) packaged as `jxl-photo.exe`:
no Python to install, and the tools it calls (cjxl/djxl, exiftool,
ImageMagick) come in the same folder. Unzip and run.

> **Experimental.** This repository only packages a published jxl-photo
> release; the scripts inside are byte-for-byte those of the tag named below.
> jxl-photo itself (documentation, issues, changes) lives in its own
> repository.

**Packages:** jxl-photo v2.15.2 · libjxl 0.12.0 · ExifTool 13.59 ·
ImageMagick 7.1.2-27 (Q16-HDRI)

---

## Use

1. Download `jxl-photo-<version>-x64.zip` and unzip it anywhere (not inside
   `Program Files`).
2. Run `jxl-photo.exe` for the interactive menu, or from a terminal:

```
jxl-photo.exe                              the interactive wizard
jxl-photo.exe --run-preset "MY PRESET"     a saved preset, unattended
jxl-photo.exe encode  "F:\Photos" --mode 6 TIFF -> JXL (jxl_tiff_encoder.py)
jxl-photo.exe decode  ...                  JXL -> TIFF  (jxl_tiff_decoder.py)
jxl-photo.exe recompress ...               JXL -> JXL   (jxl_recompressor.py)
jxl-photo.exe transcode ...                JPEG/PNG <-> JXL (jxl_jpeg_transcoder.py)
```

Every option and behaviour is jxl-photo's: see its
[README](https://github.com/rsilvabr/jxl-photo#readme) and the per-script
docs. `encode --help` and so on print each script's options.

## What is in the folder

| Path | What |
|---|---|
| `jxl-photo.exe`, `_internal\` | Python and the libraries (numpy, tifffile, imagecodecs, Pillow, rich) |
| `scripts\` | The five jxl-photo scripts, unchanged |
| `tools\libjxl\` | `cjxl.exe`, `djxl.exe`, `jxlinfo.exe` (official static build) |
| `tools\exiftool\` | ExifTool (Windows build) |
| `tools\imagemagick\` | `magick.exe` (portable build) and its configuration |
| `licenses\` | The licenses of everything above |

The program puts `tools\` first on `PATH` for the scripts, so tools installed
elsewhere on the PC are not used. Logs go to `%LOCALAPPDATA%\jxl-photo\Logs`
(set `JXLPHOTO_LOG_DIR` to change it); settings and presets to
`%USERPROFILE%\.jxl_tools_config.json`, shared with a Python install of
jxl-photo.

## Good to know

- **Antivirus:** the program is not code-signed. Some antivirus engines flag
  unsigned programs built with PyInstaller; the one-folder layout used here
  is the one they object to least.
- **Size:** about 250 MB unzipped, most of it ImageMagick, numpy and ExifTool.
- **Starting** takes a second or two longer than `py jxl_photo.py`.

## Building

Needs Python 3.12 on `PATH` and an internet connection:

```
python build.py
```

It creates a virtual environment in `.venv` (pinned packages and
PyInstaller), downloads the jxl-photo tag and the tools (SHA-256 checked),
and writes `dist\jxl-photo-<version>-x64\` plus its zip. The tag and the tool
versions are settings at the top of `build.py`.

## Testing

`python tests/battery_on_exe.py` runs jxl-photo's real-photo battery
(`tools/real_photo_battery.py` from a jxl-photo checkout next to this one)
against the built program: every script run goes through `jxl-photo.exe`, and
the only cjxl, djxl, exiftool and magick on `PATH` are the bundled ones. The
first build (jxl-photo v2.15.2) passed all 110 checks, presets through the
wizard's `--run-preset` and runs killed mid-write included, in 886 s (711 s
with Python: each script start costs a little more).

## License

MIT for this packaging (see [LICENSE](LICENSE)). jxl-photo is MIT; libjxl
BSD-3-Clause; ExifTool is under the same terms as Perl; ImageMagick under its
own Apache-2.0-style license. All are in `licenses\` in the package.
