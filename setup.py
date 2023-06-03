from setuptools import setup

setup(
    name="ste",
    version="1.0",
    py_modules=["main", "GuitarProTools", "GuitarPro_midi", "gui", "ui_mainwindow"],
    entry_points={
        "console_scripts": [
            "ste = main:main"
        ]
    },
    install_requires=[
        "PyGuitarPro",
        "MIDIUtil"
    ]
)