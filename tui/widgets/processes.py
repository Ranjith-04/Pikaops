from textual.app import ComposeResult
from textual.widgets import Static, DataTable
import psutil

class ProcessMonitor(Static):
    def compose(self) -> ComposeResult:
        yield DataTable(id="proc-table", zebra_stripes=True, cursor_type="row")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("PID", "Name", "Status", "CPU %", "Mem %")
        
        # Initial populate
        self.update_processes()
        # Update every 3 seconds to avoid heavy load
        self.set_interval(3.0, self.update_processes)

    def update_processes(self) -> None:
        table = self.query_one(DataTable)
        table.clear(columns=False)
        
        # Get top 20 processes by CPU
        procs = []
        for p in psutil.process_iter():
            try:
                procs.append(p.as_dict(attrs=['pid', 'name', 'status', 'cpu_percent', 'memory_percent']))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Filter out System Idle Process (PID 0 on Windows, or heavily sleeping tasks)
        # It confuses users because 'High CPU' here means 'System is Free'
        procs = [p for p in procs if p['pid'] != 0 and p['name'] != "System Idle Process"]
        
        # Sort by CPU desc
        procs.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        cpu_count = psutil.cpu_count() or 1
        
        for p in procs[:20]:
            # Normalize CPU by core count to get 0-100% of TOTAL system capacity
            normalized_cpu = (p['cpu_percent'] or 0) / cpu_count
            
            table.add_row(
                str(p['pid']),
                p['name'],
                p['status'],
                f"{normalized_cpu:.1f}",
                f"{p['memory_percent']:.1f}"
            )
