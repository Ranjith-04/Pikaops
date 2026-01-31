from textual.app import ComposeResult
from textual.widgets import Input, RichLog, Static
from textual.containers import Vertical
import subprocess
import asyncio
import shlex

class TerminalRunner(Vertical):
    def compose(self) -> ComposeResult:
        yield RichLog(id="term-output", highlight=True, markup=True)
        yield Input(placeholder="Enter command (e.g. ls, Get-Process)...", id="term-input")

    BINDINGS = [
        ("tab", "autocomplete", "Autocomplete")
    ]

    def action_autocomplete(self) -> None:
        inp = self.query_one("#term-input", Input)
        current_val = inp.value
        if not current_val:
            return
            
        # Very basic split to get the last word (cursor position logic is harder in Textual < 0.30, assuming end)
        # We'll just look at the last token
        parts = current_val.split()
        if not parts:
            return
            
        target = parts[-1]
        
        # Check files in current dir
        import os
        try:
            # If target has directory structure
            dirname = os.path.dirname(target)
            basename = os.path.basename(target)
            
            search_dir = dirname if dirname else "."
            if not os.path.exists(search_dir):
                return
                
            matches = [f for f in os.listdir(search_dir) if f.startswith(basename)]
            
            if len(matches) == 1:
                completion = matches[0]
                # If directory, append slash
                if os.path.isdir(os.path.join(search_dir, completion)):
                    completion += os.sep
                
                # Replace the last part with the completion
                new_val = current_val[: current_val.rfind(target)] + os.path.join(dirname, completion)
                inp.value = new_val
                # Move cursor to end (hacky reset)
                inp.action_end()
        except Exception:
            pass

    def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        if not command:
            return
            
        term_log = self.query_one("#term-output", RichLog)
        term_log.write(f"[bold green]$ {command}[/]")
        
        event.input.value = "" # Clear input
        
        if command.lower() in ("cls", "clear"):
            term_log.clear()
            return

        # Run command asynchronously to not block UI
        asyncio.create_task(self.run_command(command))

    async def run_command(self, command: str):
        term_log = self.query_one("#term-output", RichLog)
        
        try:
            import platform
            is_windows = platform.system() == "Windows"
            
            if is_windows:
                # Use PowerShell on Windows
                # -NoProfile: Faster startup, avoid user profile noise
                # -Command: Execute the command
                process = await asyncio.create_subprocess_exec(
                    "powershell", "-NoProfile", "-Command", command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            else:
                # Use default shell on Linux/Mac
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            
            stdout, stderr = await process.communicate()
            
            if stdout:
                term_log.write(stdout.decode().strip())
            if stderr:
                term_log.write(f"[red]{stderr.decode().strip()}[/]")
                
        except Exception as e:
            term_log.write(f"[bold red]Error: {e}[/]")
