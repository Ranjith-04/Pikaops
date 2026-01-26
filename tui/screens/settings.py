from textual.app import ComposeResult
from textual.widgets import Static, Button, Input, Label
from textual.containers import Vertical
from utils.config import add_server

class SettingsScreen(Static):
    def compose(self) -> ComposeResult:
        yield Label("PikaOps Configuration", id="settings-header")
        
        with Vertical(id="settings-form"):
            yield Label("Add Production Server")
            yield Input(placeholder="Server Name (e.g. DB-01)", id="set-name")
            yield Input(placeholder="IP Address", id="set-ip")
            yield Input(placeholder="SSH User (e.g. lance)", id="set-user")
            yield Input(placeholder="Metrics URL (e.g. http://ip:9100/metrics)", id="set-url")
            yield Button("Save Server",variant="success", id="btn-save-server")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-save-server":
            name = self.query_one("#set-name", Input).value
            ip = self.query_one("#set-ip", Input).value
            user = self.query_one("#set-user", Input).value
            url = self.query_one("#set-url", Input).value
            
            if name and ip:
                add_server(name, ip, user, url)
                # clear inputs
                for i in ["#set-name", "#set-ip", "#set-user", "#set-url"]:
                    self.query_one(i, Input).value = ""
                
                self.notify("Server configuration saved!")
