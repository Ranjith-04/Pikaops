from textual.app import ComposeResult
from textual.widgets import Static, Collapsible, Label
from tui.widgets.metrics import SystemMetrics
from tui.widgets.terminal import TerminalRunner
from tui.widgets.processes import ProcessMonitor
from tui.widgets.alerts import AlertsPanel
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import DirectoryTree
import os

class LocalDashboard(Container):
    def compose(self) -> ComposeResult:
        # Top: Collapsible System Metrics
        with Collapsible(title="System Metrics", collapsed=True):
            yield SystemMetrics(id="system-metrics")
        
        # Middle: Horizontal split (Sidebar + Terminal)
        with Horizontal(id="main-area"):
             # Sidebar: File Browser & Alerts
            with Vertical(id="sidebar-container"):
                with Collapsible(title="File Browser & Alerts", collapsed=True):
                    yield AlertsPanel(id="alerts-panel")
                    yield DirectoryTree(os.path.expanduser("~"), id="file-browser")

            # Terminal takes the remaining space and is the PRIMARY visible element
            yield TerminalRunner(id="terminal-area")
        
        # Bottom: Collapsible Processes
        with Collapsible(title="Process Manager", collapsed=True):
            yield ProcessMonitor(id="process-panel")
