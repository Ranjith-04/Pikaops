# PikaOps Release Guide

## 1. Windows Release (.exe)
We use `PyInstaller` to bundle the application into a single executable.

### Build Steps
1.  **Install PyInstaller**:
    ```powershell
    pip install pyinstaller
    ```

2.  **Build**:
    Run the following command to bundle everything (including the CSS files):
    ```powershell
    pyinstaller --noconfirm --onefile --name "PikaOps" --add-data "tui/styles.tcss;tui" --hidden-import="textual" main.py
    ```
    *Note: The `--add-data` separator is `;` on Windows and `:` on Linux.*
    *Note: Do not use `--windowed` as this is a TUI application that requires a terminal.*

    **Alternative**: Run the included build script:
    ```powershell
    python build.py
    ```

3.  **Result**: 
    The `dist/PikaOps.exe` file is your portable application. You can upload this to GitHub Releases or distribute it directly.

## 2. Linux Release (APT / .deb)
To create a `.deb` package to host in an APT repository.

### prerequisites 
(Run on a Linux machine or WSL)
```bash
sudo apt-get install python3-stdeb fakeroot python3-all-dev
```

### Build Steps
1.  **Generate Source Package**:
    ```bash
    python3 setup.py --command-packages=stdeb.command sdist_dsc
    ```

2.  **Build .deb**:
    ```bash
    cd deb_dist/pikaops-2.0.0/
    dpkg-buildpackage -rfakeroot -uc -us
    ```

3.  **Result**:
    You will have a `.deb` file in the `deb_dist` directory.

### Hosting in APT Repo
1.  Create a repo directory.
2.  Copy the `.deb` file there.
3.  Run `dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz`.
4.  Users can add your repo URL to their `sources.list`.

## 3. Cross-Platform Verify
The codebase uses:
-   `#!/usr/bin/env python3` shebang for direct Linux execution.
-   `os.path.join` for file paths.
-   `platform.system()` checks to run the correct shell commands (SSH/Ping).
