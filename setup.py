import sys
from cx_Freeze import setup, Executable
# Dependencies are automatically detected, but it might need fine tuning.
base = None
if sys.platform == "win32":
    base = "Win32GUI"
includefiles = ["images/exit.png",
                "images/bp_btn4.png",
                "images/failed.png",
                "images/new.png",
                "images/process.png",
                "images/success.png",
                "images/user16.png",
                "images/waiting.png"
                ]
options = {
   'build_exe': {       
        'includes': ['whichdb', 'lxml.etree', 'lxml._elementpath', 'wx'],
    "include_files": includefiles
    }
}

setup( name = "SMS Lite Client",
    version = "1.3",
    description = "SMS Lite Client Application",
    options = options,
    executables = [Executable("CMS.py", base=base)])
