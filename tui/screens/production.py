import httpx
from textual.app import ComposeResult
from textual.widgets import Static, Button, DataTable, Label
from textual.containers import Vertical, Horizontal
import psutil
import asyncio

class ProductionDashboard(Static):
    def compose(self) -> ComposeResult:
        yield Label("Production Environment Monitor", id="prod-header")
        
        with Horizontal(id="prod-content"):
            with Vertical(id="prod-list-area"):
                yield Label("Servers (Auto-Polling every 5s)", classes="section-title")
                yield DataTable(id="prod-server-table", cursor_type="row")
                with Horizontal(id="prod-actions"):
                    yield Button("SSH Connect", id="btn-ssh", variant="primary")
                    yield Button("Quick Connect", id="btn-quick-ssh", variant="warning")
                    # yield Button("Force Refresh", id="btn-poll", variant="warning") # Auto-polling now
            
            with Vertical(id="prod-details"):
                yield Label("Live Logs / Details", classes="section-title")
                yield Static("System events will appear here...", id="prod-metrics-view")

    def on_mount(self) -> None:
        table = self.query_one("#prod-server-table", DataTable)
        table.add_columns("Name", "IP", "Status", "Load", "Mem Free")
        self.refresh_servers()
        # Auto-poll every 5 seconds
        self.set_interval(5.0, self.auto_poll_metrics)

    def refresh_servers(self):
        from utils.config import load_config
        config = load_config()
        table = self.query_one("#prod-server-table", DataTable)
        table.clear()
        for s in config.get("servers", []):
            # Key is Name for simple matching later
            table.add_row(s["name"], s["ip"], "Pending", "-", "-", key=s["name"])

    async def auto_poll_metrics(self):
        from utils.config import load_config
        config = load_config()
        table = self.query_one("#prod-server-table", DataTable)
        
        import httpx
        
        # Poll all servers concurrently using a single client
        async with httpx.AsyncClient() as client:
            tasks = []
            for s in config.get("servers", []):
                url = s.get("exporter_url")
                name = s.get("name")

                if not url:
                    continue

                # Run fetch in background task to avoid blocking
                tasks.append(asyncio.create_task(self.fetch_server_metrics(name, url, client=client)))

            if tasks:
                await asyncio.gather(*tasks)

    async def fetch_server_metrics(self, name: str, url: str, client: httpx.AsyncClient = None):
        table = self.query_one("#prod-server-table", DataTable)
        metrics_view = self.query_one("#prod-metrics-view", Static)
        
        from utils.metrics import get_remote_metrics
        data = await get_remote_metrics(url, client=client)
        
        # Update Table Row
        try:
            table.update_cell(name, "Status", data["status_style"])
            table.update_cell(name, "Load", data["load"])
            table.update_cell(name, "Mem Free", data["mem_free"])
            
            if data["status"] == "ERROR":
                metrics_view.update(f"[red]Error fetching {name}: {data['error_msg']}[/]")
                
        except Exception:
            # Row might not exist if config changed rapidly
            pass

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-ssh":
            self.handle_saved_ssh()
        elif event.button.id == "btn-quick-ssh":
            from tui.screens.ssh_dialog import SSHDialog
            self.app.push_screen(SSHDialog(), self.handle_quick_ssh)

    def handle_saved_ssh(self):
        table = self.query_one("#prod-server-table", DataTable)
        cursor_row = table.cursor_row
        if cursor_row is None:
            self.notify("Please select a server first.", severity="error")
            return

        row_data = table.get_row_at(cursor_row)
        server_name = row_data[0]
        server_ip = row_data[1]
        
        from utils.config import load_config
        config = load_config()
        server_conf = next((s for s in config.get("servers", []) if s["name"] == server_name), None)

        if server_conf:
            user = server_conf.get("user", "root")
            self.run_ssh_session(user, server_ip, server_name)

    def handle_quick_ssh(self, result):
        if result:
            user, ip = result
            self.run_ssh_session(user, ip, f"Interactive({ip})")

    def run_ssh_session(self, user: str, ip: str, display_name: str):
        with self.app.suspend_application_mode():
            from utils.ssh import launch_ssh_session
            launch_ssh_session(user, ip)
            input("Press Enter to return...")
