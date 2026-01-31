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

            with Vertical(classes="test-box"):
                yield Label("Port Scanner")
                yield Input(placeholder="Host (e.g., localhost)", id="scan-host")
                yield Input(placeholder="Start Port (e.g., 80)", id="scan-start")
                yield Input(placeholder="End Port (e.g., 90)", id="scan-end")
                yield Button("Scan Ports", id="btn-scan")
        
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
        log = self.query_one("#test-output", RichLog)
        
        if event.button.id == "btn-ping":
            inp = self.query_one("#ping-input", Input).value
            if inp:
                asyncio.create_task(self.run_ping(inp))
        
        elif event.button.id == "btn-alert-cpu":
            log.write("[bold red blink]CRITICAL: CPU USAGE > 90% (SIMULATED)[/]")
            log.write("Compacting garbage... Done.")
            
        elif event.button.id == "btn-alert-disk":
            log.write("[bold orange1]WARNING: Disk Space Low < 10% (SIMULATED)[/]")
            log.write("Please clear temp files.")
            
        elif event.button.id == "btn-scan":
            host = self.query_one("#scan-host", Input).value
            start = self.query_one("#scan-start", Input).value
            end = self.query_one("#scan-end", Input).value
            if host and start and end:
                asyncio.create_task(self.run_port_scan(host, int(start), int(end)))

    async def run_port_scan(self, host: str, start_port: int, end_port: int):
        log = self.query_one("#test-output", RichLog)
        log.write(f"[cyan]Scanning {host} ports {start_port}-{end_port}...[/]")
        
        open_ports = []
        for port in range(start_port, end_port + 1):
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(host, port), timeout=0.1
                )
                writer.close()
                await writer.wait_closed()
                open_ports.append(port)
                log.write(f"[green]Port {port} is OPEN[/]")
            except:
                pass
        
        if not open_ports:
            log.write("[yellow]No open ports found in range.[/]")
        else:
            log.write(f"[bold green]Scan Complete. Open: {open_ports}[/]")
