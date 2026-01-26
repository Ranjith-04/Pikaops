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
        
        # Poll all servers concurrently
        for s in config.get("servers", []):
            url = s.get("exporter_url")
            name = s.get("name")
            
            if not url:
                continue

            # Run fetch in background task to avoid blocking
            asyncio.create_task(self.fetch_server_metrics(name, url))

    async def fetch_server_metrics(self, name: str, url: str):
        table = self.query_one("#prod-server-table", DataTable)
        metrics_view = self.query_one("#prod-metrics-view", Static)
        
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=3.0)
                
                if resp.status_code == 200:
                    lines = resp.text.splitlines()
                    # Robust parsing with defaults
                    load1 = "-"
                    mem_free = "-"
                    
                    try:
                        load1 = next((l for l in lines if l.startswith("node_load1 ")), "0.0").split()[-1]
                    except Exception:
                        pass
                        
                    try:
                        mem_bytes = next((l for l in lines if l.startswith("node_memory_MemFree_bytes ")), "0").split()[-1]
                        mem_gb = float(mem_bytes) / (1024**3)
                        mem_free = f"{mem_gb:.1f} GB"
                    except Exception:
                        mem_free = "Err"

                    # Update Table Row (Thread-safe in Textual usually via call_from_thread if needed, but async is on main loop)
                    # We match row by key (Name)
                    try:
                        # Columns: Name(0), IP(1), Status(2), Load(3), Mem(4)
                        table.update_cell(name, "Status", "[green]ONLINE[/]")
                        table.update_cell(name, "Load", load1)
                        table.update_cell(name, "Mem Free", mem_free)
                    except Exception as e:
                        # Row might not exist if config changed rapidly
                        pass
                else:
                    table.update_cell(name, "Status", f"[yellow]HTTP {resp.status_code}[/]")

        except httpx.ConnectTimeout:
             table.update_cell(name, "Status", "[red]TIMEOUT[/]")
        except httpx.ConnectError:
             table.update_cell(name, "Status", "[red]DOWN[/]")
        except Exception as e:
             # Catch-all for other parsing/network errors
             table.update_cell(name, "Status", "[red]ERROR[/]")
             metrics_view.update(f"[red]Error fetching {name}: {str(e)}[/]")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-ssh":
            table = self.query_one("#prod-server-table", DataTable)
            cursor_row = table.cursor_row
            if cursor_row is None:
                self.notify("Please select a server first.", severity="error")
                return

            row_data = table.get_row_at(cursor_row)
            server_name = row_data[0] # Name is first col
            server_ip = row_data[1]
            
            from utils.config import load_config
            config = load_config()
            server_conf = next((s for s in config.get("servers", []) if s["name"] == server_name), None)

            if server_conf:
                user = server_conf.get("user", "root")
                cmd = f"ssh {user}@{server_ip}"
                
                with self.app.suspend_application_mode():
                    import os
                    import platform
                    print(f"--- Connecting to {server_name} ({server_ip}) ---")
                    try:
                        if platform.system() == "Windows":
                            os.system(cmd)
                        else:
                            os.system(cmd)
                    except Exception as e:
                        print(f"SSH Launch Failed: {e}")
                    
                    print("\n--- Session End ---")
                    input("Press Enter...")
