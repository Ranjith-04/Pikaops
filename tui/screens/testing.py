from textual.app import ComposeResult
from textual.widgets import Static, Button, Input, RichLog, Label
from textual.containers import Vertical, Horizontal
import asyncio

class TestingDashboard(Static):
    def compose(self) -> ComposeResult:
        yield Label("Testing Sandbox & Connectivity", id="test-header")
        
        with Horizontal():
            with Vertical(classes="test-box"):
                yield Label("Ping Test")
                yield Input(placeholder="Enter hostname/IP...", id="ping-input")
                yield Button("Run Ping", id="btn-ping")
            
            with Vertical(classes="test-box"):
                yield Label("Alert Simulation")
                yield Button("Test CPU Alert", id="btn-alert-cpu")
                yield Button("Test Disk Alert", id="btn-alert-disk")
        
        yield RichLog(id="test-output", markup=True)

    async def run_ping(self, host):
        log = self.query_one("#test-output", RichLog)
        
        # Sanitize host input (basic check)
        if any(c in host for c in ";|&"):
            log.write("[red]Invalid characters in hostname[/red]")
            return

        log.write(f"[yellow]Pinging {host}...[/yellow]")
        
        # Use list args to avoid shell injection where possible
        # However, asyncio.create_subprocess_exec (no shell) is safer
        import platform
        cmd = ["ping", "-c", "4", host] if platform.system() != "Windows" else ["ping", "-n", "4", host]
        
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if stdout:
                log.write(stdout.decode())
            if stderr:
                log.write(f"[red]{stderr.decode()}[/red]")
        except Exception as e:
            log.write(f"[red]Error: {e}[/red]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-ping":
            inp = self.query_one("#ping-input", Input).value
            if inp:
                asyncio.create_task(self.run_ping(inp))
