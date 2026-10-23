# Version history

A package version names the jxl-photo release it carries: `v2.15.2-exe1` is
the first package of jxl-photo v2.15.2. What changed in jxl-photo itself is
in [its version history](https://github.com/rsilvabr/jxl-photo/blob/main/docs/version_history.md).

| Version | Date | jxl-photo | Highlights |
|---------|------|-----------|------------|
| **[v2.17.0-exe1](#v2170-exe1)** | 2026-10-24 | v2.17.0 | jxl-photo v2.17.0: film scans archived lossless and kept the way their scanner software expects them |
| [v2.16.2-exe1](#v2162-exe1) | 2026-10-23 | v2.16.2 | Built by GitHub Actions with a build attestation; jxl-photo v2.16.2 and jxl-thumb 0.2.1 |
| [v2.16.0-exe2](#v2160-exe2) | 2026-10-22 | v2.16.0 | First regular release (no longer a pre-release); Python's license in the package |
| [v2.16.0-exe1](#v2160-exe1) | 2026-10-22 | v2.16.0 | jxl-photo v2.16.0 (Explorer thumbnails for lossless files) and jxl-thumb 0.2.0; offers the jxl-thumb update |
| [v2.15.2-exe3](#v2152-exe3) | 2026-10-22 | v2.15.2 | The thumbnail offer also replaces Microsoft's slow handler |
| [v2.15.2-exe2](#v2152-exe2) | 2026-10-22 | v2.15.2 | Explorer thumbnails: jxl-thumb included; ExifTool in a non-ANSI program folder |
| [v2.15.2-exe1](#v2152-exe1) | 2026-10-22 | v2.15.2 | First package (experimental) |

---

## v2.17.0-exe1

*2026-10-24*

- jxl-photo [v2.17.0](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.17.0):
  film scans are archived lossless by default and the recompressor no longer
  re-encodes them lossy unless asked; a SilverFast scan comes back with its
  IR channel, dust removal and browser icon; thumbnail pages are kept by
  default (except Capture One's); file names with a `%` keep their metadata.
  Two defaults change: see its
  [upgrading notes](https://github.com/rsilvabr/jxl-photo/blob/main/docs/upgrading.md#v2170-thumbnail-pages-are-kept-by-default-film-scans-are-lossless).
- Same tools as v2.16.2-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

## v2.16.2-exe1

*2026-10-23*

- **Built by GitHub Actions** from the tagged code
  ([workflow](../.github/workflows/release.yml)), with the same `build.py`,
  instead of on the author's PC; GitHub records a build attestation for the
  zip and `jxl-photo.exe` (README, "Verifying a download"). The real-photo
  battery ran against that zip before the release was published.
- jxl-photo [v2.16.2](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.16.2):
  a run killed at an unlucky moment no longer leaves a temp file beside an
  output (v2.16.1), and a deleting JPEG → JXL run no longer keeps a JPEG
  because two workers finished at once. This package's battery runs found
  both: a v2.16.0-exe3 and a v2.16.1-exe1 were built, failed one check each,
  and were never released.
- jxl-thumb [0.2.1](https://github.com/rsilvabr/jxl-thumb/releases/tag/v0.2.1):
  the same code as 0.2.0, built by GitHub Actions with its own attestation.
  With 0.2.0 installed, the first start offers the update once; thumbnails
  stay the same either way.

## v2.16.0-exe2

*2026-10-22* — the first regular release; the earlier packages were
pre-releases.

- Same program as exe1 (jxl-photo v2.16.0, jxl-thumb 0.2.0, the same tools).
- `licenses\` now also holds Python's own license (PSF): PyInstaller bundles
  the runtime without it.

## v2.16.0-exe1

*2026-10-22* — pre-release.

- jxl-photo [v2.16.0](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.16.0):
  lossless outputs carry a small thumbnail that jxl-thumb shows in Explorer
  in milliseconds; menu option 9 adds it to existing files.
- jxl-thumb [0.2.0](https://github.com/rsilvabr/jxl-thumb/releases/tag/v0.2.0),
  which reads that thumbnail.
- When an older jxl-thumb is installed (from exe2/exe3), the first start
  offers the update, once per version.

## v2.15.2-exe3

*2026-10-22* — pre-release.

- The thumbnail offer also appears when Explorer uses Microsoft's JPEG XL
  extension, which many Windows 11 installs have out of the box: exe2
  offered jxl-thumb only on PCs with no JXL thumbnails at all, so most
  people never saw it. Once, as before; `thumbnails uninstall` brings
  Windows' own handler back. A handler installed on purpose is still left
  alone.
- Everything else is unchanged from exe2.

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
