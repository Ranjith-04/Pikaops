#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane
from textual.screen import Screen
from tui.screens.splash import SplashScreen
from tui.screens.local import LocalDashboard
from tui.screens.production import ProductionDashboard
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
            with TabPane("Testing Sandbox", id="test"):
                yield TestingDashboard()
            with TabPane("Settings", id="settings"):
                yield SettingsScreen()
        yield Footer()

class OpsCliApp(App):
    TITLE = "PikaOps CLI"
    CSS_PATH = "tui/styles.tcss"
    BINDINGS = [("q", "quit", "Quit"), ("d", "toggle_dark", "Toggle Dark Mode")]

    def on_mount(self) -> None:
        self.install_screen(HomeScreen(), name="dashboard")
        self.push_screen(SplashScreen())

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

def main():
    app = OpsCliApp()
    app.run()

if __name__ == "__main__":
    main()
