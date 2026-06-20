from textual.app import ComposeResult
from textual.widgets import Static, DataTable, Button, Label, Footer
from textual.containers import Vertical, Horizontal
import asyncio
from utils.docker_lib import list_containers, manage_container

class DockerDashboard(Static):
    def compose(self) -> ComposeResult:
        yield Label("Docker Container Management", id="docker-header")
        
        with Vertical(id="docker-content"):
            yield DataTable(id="docker-table", cursor_type="row")
            
            with Horizontal(id="docker-actions"):
                yield Button("Start", id="btn-start", variant="success")
                yield Button("Stop", id="btn-stop", variant="error")
                yield Button("Restart", id="btn-restart", variant="warning")
                yield Button("Refresh", id="btn-refresh", variant="primary")
                
            yield Label("", id="docker-status-msg")

    def on_mount(self) -> None:
        table = self.query_one("#docker-table", DataTable)
        table.add_columns("ID", "Name", "Image", "State", "Status")
        self.refresh_containers()
        # Auto-refresh every 5s
        self.set_interval(5.0, self.refresh_containers)

    def refresh_containers(self) -> None:
        asyncio.create_task(self.load_data())

    async def load_data(self):
        containers = await list_containers()
        table = self.query_one("#docker-table", DataTable)
        
        # We'll clear and rebuild for simplicity, 
        # though updating in place is better for selection persistence.
        # Preserving selection is a nice-to-have optimization.
        current_row = table.cursor_row
        table.clear()
        
        for c in containers:
            # Colorize State
            state = c["state"]
            if state == "running":
                state_styled = f"[green]{state}[/]"
            elif state == "exited":
                state_styled = f"[red]{state}[/]"
            else:
                state_styled = f"[yellow]{state}[/]"
                
            table.add_row(
                c["id"], 
                c["name"], 
                c["image"], 
                state_styled, 
                c["status"], 
                key=c["id"]
            )
            
        # Try to restore cursor (approximate)
        if current_row is not None and current_row < table.row_count:
            table.move_cursor(row=current_row)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-refresh":
            self.refresh_containers()
            return
            
        action = ""
        if event.button.id == "btn-start":
            action = "start"
        elif event.button.id == "btn-stop":
            action = "stop"
        elif event.button.id == "btn-restart":
            action = "restart"
            
        if action:
            await self.handle_action(action)

    async def handle_action(self, action: str):
        table = self.query_one("#docker-table", DataTable)
        status_lbl = self.query_one("#docker-status-msg", Label)
        
        if table.cursor_row is None:
            self.notify("No container selected", severity="error")
            return
            
        row = table.get_row_at(table.cursor_row)
        container_id = row[0] # ID is col 0
        container_name = row[1]
        
        status_lbl.update(f"[yellow]{action.title()}ing {container_name}...[/]")
        
        success, msg = await manage_container(container_id, action)
        
        if success:
            self.notify(msg, severity="information")
            status_lbl.update(f"[green]{msg}[/]")
            self.refresh_containers()
        else:
            self.notify(f"Error: {msg}", severity="error")
            status_lbl.update(f"[red]Error: {msg}[/]")
