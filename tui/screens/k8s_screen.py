from textual.app import ComposeResult
from textual.widgets import Static, DataTable, Button, Label, Input, RichLog
from textual.containers import Vertical, Horizontal
import asyncio
from utils.k8s_lib import list_k8s_scripts, run_script, start_tunnel, stop_tunnel, is_tunnel_active

class KubernetesDashboard(Static):
    def compose(self) -> ComposeResult:
        yield Label("Kubernetes Cluster Management", id="k8s-header")
        
        with Horizontal(id="k8s-content"):
            # Left Panel: Script Manager
            with Vertical(id="k8s-scripts-panel"):
                yield Label("Scripts (scripts/k8s/)", classes="section-title")
                yield DataTable(id="k8s-script-table", cursor_type="row")
                yield Button("Run Selected Script", id="btn-run-script", variant="primary")
            
            # Right Panel: Tunnel & Output
            with Vertical(id="k8s-right-panel"):
                with Vertical(id="k8s-tunnel-panel"):
                    yield Label("Cluster Tunnel (6443 -> 127.0.0.1:6443)", classes="section-title")
                    yield Input(placeholder="User (e.g. root)", id="tunnel-user")
                    yield Input(placeholder="Remote IP", id="tunnel-ip")
                    yield Button("Start Tunnel", id="btn-tunnel", variant="warning")
                    yield Label("Status: Inactive", id="tunnel-status", classes="status-inactive")
                
                yield Label("Output / Logs", classes="section-title")
                yield RichLog(id="k8s-output", markup=True)

    def on_mount(self) -> None:
        # Setup Script Table
        table = self.query_one("#k8s-script-table", DataTable)
        table.add_columns("Script Name")
        self.refresh_scripts()

    def refresh_scripts(self):
        table = self.query_one("#k8s-script-table", DataTable)
        table.clear()
        scripts = list_k8s_scripts()
        for s in scripts:
            table.add_row(s, key=s)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        output = self.query_one("#k8s-output", RichLog)
        
        if event.button.id == "btn-run-script":
            table = self.query_one("#k8s-script-table", DataTable)
            if table.cursor_row is None:
                self.notify("Select a script first.", severity="error")
                return
            
            script = table.get_row_at(table.cursor_row)[0]
            output.write(f"[yellow]Running {script}...[/]")
            
            # Run in background
            res = await run_script(script)
            output.write(res)
            output.write(f"[green]Finished {script}[/]")

        elif event.button.id == "btn-tunnel":
            btn = self.query_one("#btn-tunnel", Button)
            status_lbl = self.query_one("#tunnel-status", Label)
            
            if is_tunnel_active():
                # Stop Tunnel
                success, msg = await stop_tunnel()
                if success:
                    btn.label = "Start Tunnel"
                    btn.variant = "warning"
                    status_lbl.update("Status: Inactive")
                    status_lbl.remove_class("status-active")
                    status_lbl.add_class("status-inactive")
                    output.write(f"[yellow]{msg}[/]")
                else:
                    output.write(f"[red]{msg}[/]")
            else:
                # Start Tunnel
                user = self.query_one("#tunnel-user", Input).value
                ip = self.query_one("#tunnel-ip", Input).value
                
                if not user or not ip:
                    self.notify("User and IP required", severity="error")
                    return
                
                output.write(f"[cyan]Starting tunnel to {user}@{ip}...[/]")
                success, msg = await start_tunnel(user, ip)
                
                if success:
                    btn.label = "Stop Tunnel"
                    btn.variant = "error"
                    status_lbl.update("Status: TUNNEL ACTIVE")
                    status_lbl.remove_class("status-inactive")
                    status_lbl.add_class("status-active")
                    output.write(f"[green]{msg}[/]")
                else:
                    output.write(f"[red]{msg}[/]")
