from textual.app import ComposeResult
from textual.widgets import Static, ProgressBar, Label, Sparkline
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive
import psutil

class CPUDisplay(Static):
    def compose(self) -> ComposeResult:
        with Vertical(classes="metric-box"):
            yield Label("CPU Load", classes="metric-label")
            yield ProgressBar(total=100, show_eta=False, id="cpu-bar")
            yield Label("0%", id="cpu-text")

    def update_cpu(self, percent: float):
        self.query_one("#cpu-bar", ProgressBar).update(total=100, progress=percent)
        self.query_one("#cpu-text", Label).update(f"{percent:.1f}%")

class RAMDisplay(Static):
    def compose(self) -> ComposeResult:
        with Vertical(classes="metric-box"):
            yield Label("Memory Usage", classes="metric-label")
            yield ProgressBar(total=100, show_eta=False, id="ram-bar")
            yield Label("0/0 GB", id="ram-text")

    def update_ram(self, percent: float, used: float, total: float):
        self.query_one("#ram-bar", ProgressBar).update(total=100, progress=percent)
        self.query_one("#ram-text", Label).update(f"{used:.1f}GB / {total:.1f}GB")

class DiskDisplay(Static):
    def compose(self) -> ComposeResult:
        with Vertical(classes="metric-box"):
            yield Label("Disk Usage", classes="metric-label")
            yield ProgressBar(total=100, show_eta=False, id="disk-bar")
            yield Label("0/0 GB", id="disk-text")
    
    def update_disk(self, percent: float, used: float, total: float):
        self.query_one("#disk-bar", ProgressBar).update(total=100, progress=percent)
        self.query_one("#disk-text", Label).update(f"{used:.1f}GB / {total:.1f}GB")

class NetDisplay(Static):
    def compose(self) -> ComposeResult:
        with Vertical(classes="metric-box"):
            yield Label("Network", classes="metric-label")
            yield Sparkline(summary_function=max)

class SystemMetrics(Static):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield CPUDisplay(id="cpu-display")
            yield RAMDisplay(id="ram-display")
            yield DiskDisplay(id="disk-display")
            yield NetDisplay(id="net-display")
    
    def on_mount(self) -> None:
        self.net_history = [0.0] * 60
        self.last_net_bytes = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        self.set_interval(1.0, self.update_metrics)

    def update_metrics(self) -> None:
        from utils.metrics import get_local_metrics
        data = get_local_metrics()

        # Update CPU
        self.query_one("#cpu-display", CPUDisplay).update_cpu(data["cpu"])

        # Update RAM
        mem = data["memory"]
        self.query_one("#ram-display", RAMDisplay).update_ram(mem["percent"], mem["used_gb"], mem["total_gb"])

        # Update Disk
        disk = data["disk"]
        self.query_one("#disk-display", DiskDisplay).update_disk(disk["percent"], disk["used_gb"], disk["total_gb"])

        # Update Network
        # The util returns total bytes, our Sparkline logic needs history.
        # Ideally we'd move history tracking to the util too, but for now we keep state here.
        current_bytes = data["network"]["bytes_total"]
        delta_bytes = current_bytes - self.last_net_bytes
        self.last_net_bytes = current_bytes
        
        self.net_history.pop(0)
        self.net_history.append(delta_bytes / 1024) # KB
        
        self.query_one("#net-display", NetDisplay).query_one(Sparkline).data = self.net_history
