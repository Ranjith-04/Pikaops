# Release Instructions

This document describes how to build and release PikaOps CLI for Windows and Linux.

## Prerequisites

-   Python 3.10+
-   `pip install pyinstaller colorama textual psutil`

## 1. Windows Release

We have included a build script (`build.py`) that automates the PyInstaller process on Windows.

1.  Open PowerShell in the project root.
2.  Run the build script:
    ```powershell
    python build.py
    ```
3.  The single-file executable will be generated at:
    ```
    dist/PikaOps.exe
    ```
4.  **Test**: Run `dist/PikaOps.exe` to ensure it starts and all icons/styles load correctly.

## 2. Linux Release

To build a binary for Linux, you must run PyInstaller **on a Linux machine** (or WSL). Cross-compilation from Windows to Linux is generally not supported by PyInstaller.

1.  Clone the repo on your Linux machine.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt pyinstaller
    ```
3.  Run the build command:
    ```bash
    pyinstaller --noconfirm --onefile --name PikaOps \
      --add-data "tui/styles.tcss:tui" \
      --hidden-import textual \
      main.py
    ```
    *(Note: On Linux, the path separator for `--add-data` is `:`, whereas on Windows it is `;`)*

4.  The binary will be at `dist/PikaOps`.
5.  Make it executable: `chmod +x dist/PikaOps`

## 3. GitHub Release

1.  Tag the version (e.g., `v1.0.0`).
2.  Create a "New Release" on GitHub.
3.  Upload the artifacts:
    -   `PikaOps.exe` (Windows)
    -   `PikaOps` (Linux Binary)
4.  Paste the contents of `RELEASE_NOTES.md` (or summarize changes) into the description.
