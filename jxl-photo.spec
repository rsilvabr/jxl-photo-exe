# PyInstaller spec for jxl-photo.exe (a one-folder build). Run through build.py,
# which first puts the five jxl-photo scripts in build/app/scripts.
import os
from PyInstaller.utils.hooks import collect_all

SCRIPTS = os.path.join("build", "app", "scripts")

# The scripts are imported as modules so PyInstaller bundles everything they
# use (numpy, tifffile, imagecodecs, Pillow, rich and the standard library);
# they also ship as plain .py files in scripts/, which is what actually runs.
hidden = ["jxl_tiff_encoder", "jxl_tiff_decoder", "jxl_recompressor",
          "jxl_jpeg_transcoder", "jxl_photo"]
datas, binaries = [], []
for pkg in ("imagecodecs", "tifffile", "rich"):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hidden += h

a = Analysis(
    [os.path.join("src", "jxl_photo_exe.py")],
    pathex=[SCRIPTS],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden,
    excludes=["tkinter", "matplotlib", "IPython", "pytest"],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="jxl-photo",
          console=True, version=os.path.join("build", "version_info.txt"),
          icon=None, upx=False)
coll = COLLECT(exe, a.binaries, a.datas, name="jxl-photo", upx=False)
