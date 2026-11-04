# Version history

A package version names the jxl-photo release it carries: `v2.15.2-exe1` is
the first package of jxl-photo v2.15.2. What changed in jxl-photo itself is
in [its version history](https://github.com/rsilvabr/jxl-photo/blob/main/docs/version_history.md).

| Version | Date | jxl-photo | Highlights |
|---------|------|-----------|------------|
| **[v2.22.5-exe1](#v2225-exe1)** | 2026-11-04 | v2.22.5 | jxl-photo v2.22.5: distances up to 25 (cjxl's own limit) |
| [v2.22.4-exe1](#v2224-exe1) | 2026-11-04 | v2.22.4 | jxl-photo v2.22.4: named distances for smaller JXL copies too |
| [v2.22.3-exe1](#v2223-exe1) | 2026-11-04 | v2.22.3 | jxl-photo v2.22.3: each distance named in the wizard; the film-scan distance on the review |
| [v2.22.1-exe1](#v2221-exe1) | 2026-11-04 | v2.22.1 | jxl-photo v2.22.1: every wizard question on one question layer; same questions and command lines |
| [v2.22.0-exe1](#v2220-exe1) | 2026-11-04 | v2.22.0 | jxl-photo v2.22.0: the wizard by task, one review screen with every option; the program says when a newer package is out |
| [v2.21.0-exe1](#v2210-exe1) | 2026-11-04 | v2.21.0 | jxl-photo v2.21.0: JPEG/PNG from cautious-strategy masters carry their real profile; less memory per worker |
| [v2.20.0-exe1](#v2200-exe1) | 2026-11-04 | v2.20.0 | jxl-photo v2.20.0: hardening from a full read of the scripts; modes 6/7 skip the other scripts' folders |
| [v2.19.2-exe1](#v2192-exe1) | 2026-11-03 | v2.19.2 | jxl-photo v2.19.2: IrfanView shows the EXIF of JPEG → JXL files; older ones repaired in place |
| [v2.19.1-exe1](#v2191-exe1) | 2026-11-02 | v2.19.1 | jxl-photo v2.19.1: IrfanView shows the EXIF of new JXLs again; older files repaired in place |
| [v2.19.0-exe1](#v2190-exe1) | 2026-11-02 | v2.19.0 | jxl-photo v2.19.0: the ICC profile's copy moves out of "creator software" into a jxl-photo marker |
| [v2.18.1-exe1](#v2181-exe1) | 2026-11-01 | v2.18.1 | jxl-photo v2.18.1: a recompressor sync plans only what it will process |
| [v2.18.0-exe1](#v2180-exe1) | 2026-10-29 | v2.18.0 | jxl-photo v2.18.0: runs that delete TIFFs check every JXL's pixels first; hardening |
| [v2.17.0-exe1](#v2170-exe1) | 2026-10-24 | v2.17.0 | jxl-photo v2.17.0: film scans archived lossless and kept the way their scanner software expects them |
| [v2.16.2-exe1](#v2162-exe1) | 2026-10-23 | v2.16.2 | Built by GitHub Actions with a build attestation; jxl-photo v2.16.2 and jxl-thumb 0.2.1 |
| [v2.16.0-exe2](#v2160-exe2) | 2026-10-22 | v2.16.0 | First regular release (no longer a pre-release); Python's license in the package |
| [v2.16.0-exe1](#v2160-exe1) | 2026-10-22 | v2.16.0 | jxl-photo v2.16.0 (Explorer thumbnails for lossless files) and jxl-thumb 0.2.0; offers the jxl-thumb update |
| [v2.15.2-exe3](#v2152-exe3) | 2026-10-22 | v2.15.2 | The thumbnail offer also replaces Microsoft's slow handler |
| [v2.15.2-exe2](#v2152-exe2) | 2026-10-22 | v2.15.2 | Explorer thumbnails: jxl-thumb included; ExifTool in a non-ANSI program folder |
| [v2.15.2-exe1](#v2152-exe1) | 2026-10-22 | v2.15.2 | First package (experimental) |

---

## v2.22.5-exe1

*2026-11-04*

- jxl-photo [v2.22.5](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.22.5):
  distances up to 25, cjxl's own limit (the toolkit stopped at 15). Nothing
  to do.
- Same tools as v2.22.4-exe1.

## v2.22.4-exe1

*2026-11-04*

- jxl-photo [v2.22.4](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.22.4):
  "Make smaller or resized JXL copies" offers named distances in cjxl's
  recommended range (0.5 to 3). Nothing to do.
- Same tools as v2.22.3-exe1.

## v2.22.3-exe1

*2026-11-04*

- jxl-photo [v2.22.3](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.22.3)
  (with [v2.22.2](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.22.2)):
  the wizard names each distance it offers and the review shows the
  film-scan distance. Nothing to do. (v2.22.2-exe1 was built but never
  published.)
- Rebuilt the same day after jxl-photo's v2.22.3 tag moved to a one-line
  wording fix ("finest lossy" names what cjxl rounds).
- Same tools as v2.22.1-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

## v2.22.1-exe1

*2026-11-04*

- jxl-photo [v2.22.1](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.22.1):
  every wizard question goes through the same question layer as the New job;
  same questions, same order, same command lines. Nothing to do.
- Same tools as v2.22.0-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

## v2.22.0-exe1

*2026-11-04*

- jxl-photo [v2.22.0](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.22.0):
  the wizard is organised by task (a New job asks what to do, where and how,
  then shows one review screen with every option) and the menu numbers
  changed; presets carry over by themselves. New menus for renamed folders,
  the ICC test cache and the scripts' own settings; a JXL → JPEG never
  deletes the JXL. See its
  [upgrading notes](https://github.com/rsilvabr/jxl-photo/blob/main/docs/upgrading.md#v2220-a-jxl--jpeg-never-deletes-the-jxl-modes-67-anchor-below-the-input-and-leave-derivatives-out).
- The menu says when a newer **package** is out (this repository's latest
  release, checked at most once a day; nothing is downloaded).
- Same tools as v2.21.0-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

## v2.21.0-exe1

*2026-11-04*

- jxl-photo [v2.21.0](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.21.0):
  the rest of the 2026-11-03 audit. A JXL → JPEG/PNG conversion of a master
  that keeps its profile only in XMP (scanner and table-curve profiles)
  carries that profile instead of an sRGB label; less memory per worker in
  the encoder and the decoder; a failed metadata copy in a lossy conversion
  keeps the source. See its
  [upgrading notes](https://github.com/rsilvabr/jxl-photo/blob/main/docs/upgrading.md#v2210-lossy-jxl--jpegpng-keeps-the-masters-profile-metadata-failures-keep-the-source).
- Same tools as v2.20.0-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

## v2.20.0-exe1

*2026-11-04*

- jxl-photo [v2.20.0](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.20.0):
  hardening from a full read of the five scripts. An output whose provenance
  record cannot be read is refused instead of overwritten; modes 6/7 of the
  decoder and the recompressor skip the other scripts' output folders; the
  planning phase reports progress. See its
  [upgrading notes](https://github.com/rsilvabr/jxl-photo/blob/main/docs/upgrading.md#v2200-unreadable-provenance-records-are-refused-modes-67-skip-other-scripts-folders).
- Same tools as v2.19.2-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

## v2.19.2-exe1

*2026-11-03*

- jxl-photo [v2.19.2](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.19.2):
  IrfanView shows the EXIF of JPEG → JXL files (cjxl stored it compressed,
  which IrfanView cannot read; it is now stored uncompressed, about 2 KB per
  photo). Menu option 8 repairs older files in place; the rebuilt JPEG stays
  byte-identical. See its
  [upgrading notes](https://github.com/rsilvabr/jxl-photo/blob/main/docs/upgrading.md#v2192-irfanview-shows-the-exif-of-jpeg--jxl-files-repair-older-ones-in-place).
- Same tools as v2.19.1-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

## v2.19.1-exe1

*2026-11-02*

- jxl-photo [v2.19.1](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.19.1):
  IrfanView shows the EXIF of new JXLs again (files written by v2.17.0 to
  v2.19.0 had it after the XMP, where IrfanView does not look). Menu option 9
  repairs older files in place without re-encoding. See its
  [upgrading notes](https://github.com/rsilvabr/jxl-photo/blob/main/docs/upgrading.md#v2191-irfanview-shows-the-exif-again-repair-older-files-in-place).
- Same tools as v2.19.0-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

## v2.19.0-exe1

*2026-11-02*

- jxl-photo [v2.19.0](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.19.0):
  the copy of the original ICC profile moves out of XMP `CreatorTool`
  ("creator software") into a `jxlphoto-iccprofile` marker. Older files are
  still read; older versions cannot read the new marker, so update every
  copy together. See its
  [upgrading notes](https://github.com/rsilvabr/jxl-photo/blob/main/docs/upgrading.md#v2190-the-icc-copy-moves-to-a-jxlphoto-iccprofile-marker).
- Same tools as v2.18.1-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

## v2.18.1-exe1

*2026-11-01*

- jxl-photo [v2.18.1](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.18.1):
  a recompressor sync skips files whose output is already up to date
  without reading them first, so a scheduled sync starts converting sooner.
- Same tools as v2.18.0-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

## v2.18.0-exe1

*2026-10-29*

- jxl-photo [v2.18.0](https://github.com/rsilvabr/jxl-photo/releases/tag/v2.18.0):
  runs that delete TIFFs check every JXL's pixels first (`VERIFY_ROUNDTRIP`
  is on by default), plus hardening around lossless JPEG archives, thumbnail
  pages and in-place edits. See its
  [upgrading notes](https://github.com/rsilvabr/jxl-photo/blob/main/docs/upgrading.md#v2180-deleting-tiffs-checks-pixels-old-thumbnail-pages-are-removed-derivatives-skip-them).
- Same tools as v2.17.0-exe1 (libjxl, ExifTool, ImageMagick, jxl-thumb 0.2.1).

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
