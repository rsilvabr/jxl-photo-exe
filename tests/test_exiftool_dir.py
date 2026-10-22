"""Where the launcher points PATH for exiftool (_exiftool_dir).

ExifTool's Windows launcher cannot start from a folder outside the ANSI code
page (Japanese, Cyrillic, ...): bug #1 in docs/bug_tracking.md.

    python -m pytest tests/test_exiftool_dir.py
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import jxl_photo_exe as exe   # noqa: E402


@pytest.fixture
def bundled(tmp_path, monkeypatch):
    tools = tmp_path / "吾妻山 [app] 100% & co" / "tools"
    d = tools / "exiftool"
    (d / "exiftool_files" / "lib").mkdir(parents=True)
    (d / "exiftool.exe").write_bytes(b"MZ")
    (d / "exiftool_files" / "lib" / "x.pm").write_text("1;")
    (d / "VERSION.txt").write_text("13.59\n")
    monkeypatch.setattr(exe, "TOOLS", tools)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    return d


def test_an_ansi_folder_is_used_as_is(bundled, monkeypatch):
    monkeypatch.setattr(exe, "_ansi_safe", lambda p: True)
    assert exe._exiftool_dir() == bundled


def test_the_short_name_when_the_volume_has_one(bundled, monkeypatch):
    monkeypatch.setattr(exe, "_ansi_safe", lambda p: "吾妻山" not in p)
    monkeypatch.setattr(exe, "_short_path", lambda p: r"C:\PROGRA~1\APP~1\tools\exiftool")
    assert exe._exiftool_dir() == Path(r"C:\PROGRA~1\APP~1\tools\exiftool")


def test_a_copy_when_there_is_no_short_name(bundled, tmp_path, monkeypatch):
    monkeypatch.setattr(exe, "_ansi_safe", lambda p: "吾妻山" not in p)
    monkeypatch.setattr(exe, "_short_path", lambda p: str(p))   # 8.3 names off
    got = exe._exiftool_dir()
    assert got == tmp_path / "local" / "jxl-photo" / "exiftool-13.59"
    assert (got / "exiftool.exe").is_file()
    assert (got / "exiftool_files" / "lib" / "x.pm").is_file()
    assert not list(got.parent.glob("*.tmp")), "the temporary copy is renamed into place"
    # The next start reuses it.
    (bundled / "exiftool.exe").write_bytes(b"MZ-changed")
    assert exe._exiftool_dir() == got
    assert (got / "exiftool.exe").read_bytes() == b"MZ"


def test_the_real_ansi_check():
    if sys.platform != "win32":
        pytest.skip("the mbcs codec is Windows-only")
    assert exe._ansi_safe(r"C:\Programs\jxl-photo")
    assert not exe._ansi_safe("C:\\吾妻山\\jxl-photo")
