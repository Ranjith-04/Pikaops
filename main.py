#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane
from textual.screen import Screen
from tui.screens.splash import SplashScreen
from tui.screens.local import LocalDashboard
from tui.screens.production import ProductionDashboard
from tui.screens.docker_screen import DockerDashboard
from tui.screens.k8s_screen import KubernetesDashboard
from tui.screens.testing import TestingDashboard
from tui.screens.settings import SettingsScreen

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="local"):
            with TabPane("Local System", id="local"):
                yield LocalDashboard()
            with TabPane("Production Monitor", id="prod"):
                yield ProductionDashboard()
            with TabPane("Docker", id="docker"):
                yield DockerDashboard()
            with TabPane("Kubernetes", id="k8s"):
                yield KubernetesDashboard()
            with TabPane("Testing Sandbox", id="test"):
                yield TestingDashboard()
            with TabPane("Settings", id="settings"):
                yield SettingsScreen()
        yield Footer()

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Setup Logging
import logging
import traceback
from datetime import datetime

# Log to a file in the CURRENT working directory (where the user runs the exe)
log_path = os.path.join(os.getcwd(), "pikacli_debug.log")

logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class OpsCliApp(App):
    TITLE = "PikaOps CLI"
    CSS_PATH = resource_path("tui/styles.tcss")
    BINDINGS = [("q", "quit", "Quit")]

    def on_mount(self) -> None:
        logging.info("App mounting...")
        try:
            self.install_screen(HomeScreen(), name="dashboard")
            self.push_screen(SplashScreen())
            logging.info("Screens installed successfully")
        except Exception as e:
            logging.error(f"Error mounting screens: {e}")
            raise e

def main():
    try:
        logging.info("Starting PikaOps CLI...")
        app = OpsCliApp()
        app.run()
        logging.info("Application exited clean.")
    except Exception:
        # Capture full traceback
        err_msg = traceback.format_exc()
        logging.critical("CRITICAL CRASH:\n" + err_msg)
        
        # Write a separate easy-to-find crash file
        crash_file = os.path.join(os.getcwd(), "pikacli_CRASH_REPORT.txt")
        with open(crash_file, "w") as f:
            f.write(f"PikaOps Crash Report - {datetime.now()}\n")
            f.write("-" * 50 + "\n")
            f.write(err_msg)
        
        print("\n" + "="*50)
        print(f"CRITICAL ERROR! The application has crashed.")
        print(f"Error details saved to: {crash_file}")
        print("="*50 + "\n")
        print(err_msg) 
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
