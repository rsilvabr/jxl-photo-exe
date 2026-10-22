# Bug tracking

Bugs of the **packaging** — the launcher, the bundled tools, the build —
newest first, one numbered row each. A bug in what jxl-photo itself does
belongs to [jxl-photo's bug tracker](https://github.com/rsilvabr/jxl-photo/blob/main/docs/bug_tracking_since_v1.0.md),
even when it was found while testing this program: those are listed at the
end of a round for reference, and reach this package with the jxl-photo
release that fixes them.

**Next free number: #4.**

| Round | Date | Shipped in | Bugs |
|---|---|---|---|
| [Round 1 — the program in a hostile folder, the wizard in a real console](#round-1--the-program-in-a-hostile-folder-the-wizard-in-a-real-console-2026-10-22) | 2026-10-22 | v2.15.2-exe2 | #1–#3 (3) |

---

## Round 1 — the program in a hostile folder, the wizard in a real console (2026-10-22)

exe1's battery ran the photos inside a hostile folder, but the program from
`dist\`, a plain ASCII path. This round moved the **program itself** into a
folder named `吾妻山 [app] 100% & co` on a drive without 8.3 short names, and
drove the wizard key by key through a real pseudo-console (ConPTY) and a
real double-click: the thumbnail offer, a full TIFF → JXL conversion from the
wizard, Ctrl+C at a prompt.

| # | Bug | Part | Status |
|---|-----|------|--------|
| 1 | **ExifTool did not start when the program folder had a name outside the ANSI code page** (Japanese, Chinese, Cyrillic, Greek, ... — for example under a user folder named in one of them). ExifTool's Windows launcher looks for its own `exiftool_files` folder through an ANSI path and stops with `Could not find ...\???\...\perl5*.dll`. The status bar showed `[✗] exiftool`; cjxl, djxl and magick were not affected. exe1's battery passed because it ran the program from an ASCII folder. Affects v2.15.2-exe1. | launcher | ✅ FIXED (`_exiftool_dir`: the folder's 8.3 short name where the drive has them; otherwise ExifTool is copied once to `%LOCALAPPDATA%\jxl-photo\exiftool-<version>` — or `%ProgramData%`, or the system drive — whichever path is ANSI-safe, and that copy goes on `PATH`) |
| 2 | **The package carried read-only folders** (from ExifTool's archive; exe1 cleared the attribute on files only). A copy of the program folder could not be deleted by a script (`Access denied` on `exiftool_files\lib\...`), and unzipping an update over them depends on the unzip tool. Affects v2.15.2-exe1. | build | ✅ FIXED (`build.py` clears read-only on folders too; the launcher's ExifTool copy does the same) |
| 3 | **`jxl-photo.exe thumbnails install` crashed after installing** when its output was redirected and the program folder had a non-ANSI name: printing the path of `clear_thumbnail_cache.cmd` raised `UnicodeEncodeError` in the console's ANSI code page. Found during development of exe2, never shipped. | launcher | ✅ FIXED (the launcher writes stdout/stderr as UTF-8 with replacement, like the jxl-photo scripts) |

**Test changes.** `tests/battery_on_exe.py` now runs the program from a
copy in the hostile folder by default (`--ascii-app` for the old behaviour),
resolves a relative `--app` (the battery runs each script from its own
working folder) and writes its output as UTF-8.
`tests/test_exiftool_dir.py` covers #1 (ASCII folder, short name, the copy);
`tests/test_thumbnail_offer.py` covers the thumbnail offer.

**Found in jxl-photo while testing this program** (fixed there, in its next
release; v2.15.2-exe2 still carries v2.15.2's scripts):

- jxl-photo #544 — a bracketed word starting with a lowercase letter
  (`[test]`, `[final]`) disappeared from paths on the wizard's screens
  (summary, `Executing:` line). Display only. `[FINAL]` was not affected.
- jxl-photo #545 — end of input at a wizard prompt (Ctrl+Z then Enter, or
  Ctrl+C on Windows in an unlucky moment) ended in a traceback instead of
  "Cancelled"; in a double-clicked window the window closes with it.
