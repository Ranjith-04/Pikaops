from textual.app import ComposeResult
from textual.widgets import Static, Label, RichLog
from textual.containers import Vertical
import psutil

class AlertsPanel(Static):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("SYSTEM ALERTS", id="alerts-header")
            yield RichLog(id="alerts-log", markup=True)

    def on_mount(self) -> None:
        self.log_widget = self.query_one(RichLog)
        self.log_widget.write("[green]System Normal[/green]")
        self.set_interval(2.0, self.check_thresholds)

    def check_thresholds(self) -> None:
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        # Clear log if too full (simplified rot) or just append
        # For this UI, let's keep it simple: showing active warnings or "All clear"
        
        warnings = []
        if cpu > 80:
            warnings.append(f"[red]HIGH CPU LOAD: {cpu}%[/red]")
        if mem > 85:
            warnings.append(f"[red]HIGH MEMORY: {mem}%[/red]")
        if disk > 90:
            warnings.append(f"[yellow]DISK FULL: {disk}%[/yellow]")
            
        if self.log_widget:
            # Simple simulation: if warnings exist, clear and show them. 
            pass 
            # Actually RichLog is append-only usually. 
            # Let's just monitor and write NEW alerts if state changes.
            # For simplicity in this demo, I'll just write new criticals.
            
            for w in warnings:
                self.log_widget.write(w)
