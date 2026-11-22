"""A TMP of 261 characters or more hangs any program the launcher starts
(jxl-photo #689); regsvr32, which the thumbnail offer and `thumbnails install`
run, is one — and it ran before the wizard's own check.

    python -m pytest tests/test_long_tmp.py
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import jxl_photo_exe as exe   # noqa: E402

STUB = '''
def _long_temp_problem(environ=None):
    return {why!r}
'''


@pytest.fixture
def scripts(tmp_path, monkeypatch):
    def make(why):
        d = tmp_path / "scripts"
        d.mkdir(exist_ok=True)
        (d / "jxl_photo_common.py").write_text(STUB.format(why=why), encoding="utf-8")
        monkeypatch.setattr(exe, "SCRIPTS", d)
    monkeypatch.setattr(exe, "_setup_environment", lambda: None)
    return make


def _run(monkeypatch, *argv):
    calls = {"offer": 0, "thumbs": [], "wizard": 0}
    monkeypatch.setattr(exe, "_offer_thumbnails", lambda: calls.__setitem__("offer", 1))
    monkeypatch.setattr(exe, "_thumbnails_command", lambda a: calls["thumbs"].append(a) or 0)
    monkeypatch.setattr(exe, "_resolve", lambda a: (Path("wizard.py"), []))
    monkeypatch.setattr(exe.runpy, "run_path",
                        lambda *a, **k: calls.__setitem__("wizard", 1))
    monkeypatch.setattr(sys, "argv", ["jxl-photo.exe", *argv])
    code = None
    try:
        exe.main()
    except SystemExit as e:
        code = e.code
    return calls, code


def test_a_long_tmp_skips_the_thumbnail_offer(scripts, monkeypatch):
    scripts("the TMP variable is 300 characters long")
    calls, _ = _run(monkeypatch)
    assert calls["offer"] == 0 and calls["wizard"] == 1   # the wizard says why


def test_a_long_tmp_refuses_thumbnails_install(scripts, monkeypatch, capsys):
    scripts("the TMP variable is 300 characters long")
    calls, code = _run(monkeypatch, "thumbnails", "install")
    assert code == 2 and calls["thumbs"] == []
    assert "300 characters" in capsys.readouterr().out


def test_a_short_tmp_changes_nothing(scripts, monkeypatch):
    scripts(None)
    calls, _ = _run(monkeypatch)
    assert calls["offer"] == 1 and calls["wizard"] == 1
    calls, code = _run(monkeypatch, "thumbnails", "status")
    assert code == 0 and calls["thumbs"] == [["status"]]


def test_the_real_rule_of_the_bundled_module(monkeypatch):
    """The launcher reads jxl-photo's own rule (the sibling checkout here)."""
    repo = Path(__file__).resolve().parents[2] / "jxl-photo"
    if not (repo / "jxl_photo_common.py").is_file():
        pytest.skip("no jxl-photo checkout next to this repo")
    monkeypatch.setattr(exe, "SCRIPTS", repo)
    monkeypatch.setenv("TMP", "C:\\" + "x" * 300)
    assert "TMP" in (exe._long_temp_problem() or "")
    monkeypatch.setenv("TMP", "C:\\short")
    assert exe._long_temp_problem() is None
