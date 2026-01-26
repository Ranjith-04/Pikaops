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
        # Update CPU
        cpu_pct = psutil.cpu_percent(interval=None) or 0
        self.query_one("#cpu-display", CPUDisplay).update_cpu(cpu_pct)

        # Update RAM
        mem = psutil.virtual_memory()
        used_gb = mem.used / (1024**3)
        total_gb = mem.total / (1024**3)
        self.query_one("#ram-display", RAMDisplay).update_ram(mem.percent, used_gb, total_gb)

        # Update Disk
        disk = psutil.disk_usage('/')
        d_used = disk.used / (1024**3)
        d_total = disk.total / (1024**3)
        self.query_one("#disk-display", DiskDisplay).update_disk(disk.percent, d_used, d_total)

        # Update Network (Calculate Delta)
        net = psutil.net_io_counters()
        current_bytes = net.bytes_sent + net.bytes_recv
        delta_bytes = current_bytes - self.last_net_bytes
        self.last_net_bytes = current_bytes
        
        # Normalize to some readable scale for the graph (KB/s approx) or just raw magnitude
        # Sparkline autoscales, but large spikes flatten history. 
        # Let's cap logical max or just append.
        
        self.net_history.pop(0)
        self.net_history.append(delta_bytes / 1024) # KB
        
        self.query_one("#net-display", NetDisplay).query_one(Sparkline).data = self.net_history
