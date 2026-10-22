"""The launcher's one-time offer to install the bundled jxl-thumb.

    python -m pytest tests/test_thumbnail_offer.py
"""
import io
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import jxl_photo_exe as exe   # noqa: E402


@pytest.fixture
def launcher(tmp_path, monkeypatch):
    monkeypatch.setattr(exe, "STATE_FILE", tmp_path / "jxl-photo" / "exe.json")
    monkeypatch.delenv("JXLPHOTO_THUMBNAIL_TIP", raising=False)
    installs = []
    monkeypatch.setattr(exe, "_install_thumbnails", lambda: installs.append(1) or 0)

    def setup(handler=None, tty=True, answers=()):
        monkeypatch.setattr(exe, "_thumbnail_handler", lambda: handler)
        stdin = io.StringIO()
        stdin.isatty = lambda: tty
        monkeypatch.setattr(sys, "stdin", stdin)
        it = iter(answers)
        asked = []
        monkeypatch.setattr("builtins.input", lambda prompt="": asked.append(prompt) or next(it))
        return asked
    setup.installs = installs
    return setup


def test_asks_once_and_remembers_a_no(launcher, monkeypatch):
    asked = launcher(answers=["n"])
    exe._offer_thumbnails()
    assert len(asked) == 1
    assert json.loads(exe.STATE_FILE.read_text())["thumbnail_offer_answered"] is True
    # The wizard's tip then names the bundled command.
    assert "thumbnails install" in exe.os.environ["JXLPHOTO_THUMBNAIL_TIP"]
    monkeypatch.delenv("JXLPHOTO_THUMBNAIL_TIP")
    asked = launcher(answers=[])
    exe._offer_thumbnails()
    assert asked == [] and not launcher.installs
    assert "thumbnails install" in exe.os.environ["JXLPHOTO_THUMBNAIL_TIP"]


def test_yes_installs_and_silences_the_tip(launcher):
    launcher(answers=["y"])
    exe._offer_thumbnails()
    assert launcher.installs == [1]
    assert "JXLPHOTO_THUMBNAIL_TIP" not in exe.os.environ


@pytest.mark.parametrize("handler", [
    "{EF830030-FBD6-4B62-BFD4-0DBD590D6135}",   # jxl-thumb already
    "{12345678-1234-1234-1234-123456789ABC}",   # another one, installed on purpose
])
def test_other_handlers_are_left_alone(launcher, handler):
    asked = launcher(handler=handler)
    exe._offer_thumbnails()
    assert asked == [] and not launcher.installs
    assert "JXLPHOTO_THUMBNAIL_TIP" not in exe.os.environ


def test_microsofts_handler_gets_the_offer_too(launcher, capsys):
    # Windows' WIC handler (Microsoft's JPEG XL extension): on many Windows 11
    # installs out of the box, so the offer would otherwise never show.
    asked = launcher(handler="{C7657C4A-9F68-40fa-A4DF-96BC08EB3551}", answers=["y"])
    exe._offer_thumbnails()
    assert len(asked) == 1 and launcher.installs == [1]
    assert "Microsoft's JPEG XL extension" in capsys.readouterr().out
    # Explorer does show thumbnails there: no "no thumbnails" tip for the wizard.
    assert "JXLPHOTO_THUMBNAIL_TIP" not in exe.os.environ


def test_microsofts_handler_declined_is_not_asked_again(launcher):
    launcher(handler="{C7657C4A-9F68-40fa-A4DF-96BC08EB3551}", answers=["n"])
    exe._offer_thumbnails()
    asked = launcher(handler="{C7657C4A-9F68-40fa-A4DF-96BC08EB3551}", answers=[])
    exe._offer_thumbnails()
    assert asked == [] and not launcher.installs


def test_no_console_no_question(launcher):
    asked = launcher(tty=False)
    exe._offer_thumbnails()
    assert asked == [] and not exe.STATE_FILE.exists()


def test_closed_stdin_is_not_an_answer(launcher, monkeypatch):
    launcher()
    monkeypatch.setattr("builtins.input", lambda prompt="": (_ for _ in ()).throw(EOFError))
    exe._offer_thumbnails()
    assert not exe.STATE_FILE.exists(), "asked again next time"
