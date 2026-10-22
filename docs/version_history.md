# Version history

A package version names the jxl-photo release it carries: `v2.15.2-exe1` is
the first package of jxl-photo v2.15.2. What changed in jxl-photo itself is
in [its version history](https://github.com/rsilvabr/jxl-photo/blob/main/docs/version_history.md).

| Version | Date | jxl-photo | Highlights |
|---------|------|-----------|------------|
| **[v2.15.2-exe2](#v2152-exe2)** | 2026-10-22 | v2.15.2 | Explorer thumbnails: jxl-thumb included; ExifTool in a non-ANSI program folder |
| [v2.15.2-exe1](#v2152-exe1) | 2026-10-22 | v2.15.2 | First package (experimental) |

---

## v2.15.2-exe2

*2026-10-22* — pre-release.

- [jxl-thumb](https://github.com/rsilvabr/jxl-thumb) 0.1.1 is included, for
  JXL thumbnails in Windows Explorer. `jxl-photo.exe thumbnails
  status|install|uninstall` manages it (current Windows user only, no admin
  rights).
- When Explorer has no JXL thumbnail handler at all, the first start of the
  wizard offers to install it, once. An existing handler, such as
  Microsoft's JPEG XL extension, is left alone.
- **Fix:** ExifTool did not start when the program folder had a name
  outside the Windows ANSI code page (Japanese, Cyrillic, ...); the status
  bar showed `[✗] exiftool`. The launcher now uses the folder's short
  name, or a one-time copy in `%LOCALAPPDATA%\jxl-photo` ([#1](bug_tracking.md)).
- **Fix:** the package no longer carries read-only folders ([#2](bug_tracking.md)).
- jxl-photo and the other tools are unchanged from exe1. Two display
  issues of jxl-photo's wizard found during this testing (jxl-photo
  #544, #545) are fixed there and arrive with its next release.
- The real-photo battery now runs the program from a hostile folder too:
  110/110.

## v2.15.2-exe1

*2026-10-22* — pre-release.

First package of jxl-photo as a Windows program.

- jxl-photo v2.15.2, its five scripts unchanged.
- libjxl 0.12.0 (cjxl, djxl, jxlinfo), ExifTool 13.59 and ImageMagick
  7.1.2-27 portable (Q16-HDRI), always used instead of any installed copy.
- Python 3.12 with numpy 2.5.1, tifffile 2026.6.1, imagecodecs 2026.6.26,
  Pillow 12.3.0 and rich 15.0.0, built with PyInstaller 6.22.2 (one folder).
- Logs in `%LOCALAPPDATA%\jxl-photo\Logs`; settings and presets shared with
  the Python version.
- jxl-photo's real-photo battery passes against the program: 110/110 checks,
  with only the bundled tools on `PATH`.
