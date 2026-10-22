# Version history

A package version names the jxl-photo release it carries: `v2.15.2-exe1` is
the first package of jxl-photo v2.15.2. What changed in jxl-photo itself is
in [its version history](https://github.com/rsilvabr/jxl-photo/blob/main/docs/version_history.md).

| Version | Date | jxl-photo | Highlights |
|---------|------|-----------|------------|
| **[v2.15.2-exe1](#v2152-exe1)** | 2026-10-22 | v2.15.2 | First package (experimental) |

---

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
