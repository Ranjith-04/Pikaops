from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Input, Button
from textual.containers import Vertical, Horizontal

class SSHDialog(ModalScreen):
    """A modal dialog to request SSH connection details."""

    def compose(self) -> ComposeResult:
        with Vertical(id="ssh-dialog"):
            yield Label("Quick Connect (Temporary)", id="ssh-title")
            yield Label("User:")
            yield Input(placeholder="root", id="ssh-user")
            yield Label("IP Address / Host:")
            yield Input(placeholder="192.168.1.10", id="ssh-ip")
            
            with Horizontal(id="ssh-buttons"):
                yield Button("Connect", variant="primary", id="btn-connect")
                yield Button("Cancel", variant="default", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-connect":
            user = self.query_one("#ssh-user", Input).value or "root"
            ip = self.query_one("#ssh-ip", Input).value
            
            if ip:
                self.dismiss((user, ip))
            else:
                self.notify("IP Address is required", severity="error")
                
        elif event.button.id == "btn-cancel":
            self.dismiss(None)
