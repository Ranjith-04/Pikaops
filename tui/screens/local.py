from textual.app import ComposeResult
from textual.widgets import Static
from tui.widgets.metrics import SystemMetrics
from tui.widgets.terminal import TerminalRunner
from tui.widgets.processes import ProcessMonitor
from tui.widgets.alerts import AlertsPanel
from textual.containers import Container, Vertical
from textual.widgets import DirectoryTree
import os

class LocalDashboard(Container):
    def compose(self) -> ComposeResult:
        # Grid Layout Components
        yield SystemMetrics(id="system-metrics")
        
        # Sidebar Container with Alerts and File Browser
        with Vertical(id="sidebar-container"):
            yield AlertsPanel(id="alerts-panel")
            yield DirectoryTree(os.path.expanduser("~"), id="file-browser")
            
        yield TerminalRunner(id="terminal-area")
        yield ProcessMonitor(id="process-panel")
