# PikaOps CLI ⚡

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

**PikaOps CLI** is a modern, terminal-based operations dashboard designed for DevOps engineers. It combines local system monitoring, Docker management, Kubernetes operations, and network utilities into a single, keyboard-centric interface.

Built with [Textual](https://textual.textualize.io/), PikaOps delivers a high-performance TUI (Terminal User Interface) that feels like a native desktop app but runs entirely in your terminal.

---

## 🚀 Features

### 🖥️ Local System Dashboard
-   **Real-time Monitoring**: CPU, RAM, Disk, and Network usage with live sparklines.
-   **Process Manager**: View top processes, kill rogue tasks directly from the UI.
-   **File Browser**: Navigate your filesystem and preview files.
-   **Integrated Terminal**: Full-featured terminal emulator (PowerShell on Windows, Bash/Zsh on Linux) with collapsible panels to maximize workspace.

### 🐳 Docker Management
-   **Container Control**: List, Start, Stop, and Restart containers interactively.
-   **Status at a Glance**: Color-coded indicators for container health.
-   **One-Click Actions**: No need to memorize `docker` CLI commands.

### ⎈ Kubernetes Operations
-   **Script Runner**: Organize and execute K8s scripts (`.sh`, `.py`) from a centralized library.
-   **Cluster Tunneling**: Built-in SSH tunnel manager (`-L 6443...`) to securely connect to remote clusters.

### 🛠️ Network & Testing Sandbox
-   **Port Scanner**: Async multi-threaded port scanner to check connectivity.
-   **Ping Test**: Quick latency checks.
-   **Alert Simulation**: Test your monitoring alerts by simulating high CPU/Disk load.

---

## 📦 Installation

### Option 1: Run from Source (Recommended for Devs)

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/pikaops.git
    cd pikaops
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run**:
    ```bash
    python main.py
    ```

### Option 2: Standalone Executable
Download the latest release from the [Releases Page](#).
-   **Windows**: `PikaOps.exe`
-   **Linux**: `PikaOps`

---

## ⌨️ Usage

### Navigation
| Key | Action |
| :--- | :--- |
| **Click Tabs** | Switch between Local, prod, Docker, K8s, etc. |
| `q` | Quit the application |

### Local Dashboard
-   **Expand/Collapse**: Click the `▶` arrow on "System Metrics" or "File Browser" to toggle visibility.
-   **Terminal**: Type commands in the input box at the bottom. Autocomplete enabled for files.

---

## 🏗️ Building for Release

To compile PikaOps into a single executable file:

### Windows
```powershell
python build.py
```
*Output will be in `dist/PikaOps.exe`*

### Linux
```bash
pyinstaller --onefile --name PikaOps --add-data "tui/styles.tcss:tui" --hidden-import textual main.py
```

---

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.
