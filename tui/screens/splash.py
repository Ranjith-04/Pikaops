from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Container
import asyncio

# Frame 1: Darkness / Neutral (Pokemon Yellow Sprite style)
FRAME_DARK = r"""
        
      \.:/
     /o o\
     \ - /   
     
      ...
"""

# Frame 2: Charging (Cheeks sparking)
FRAME_CHARGE = r"""
     4   4
      \.:/
    * /o o\ *
     \ - /   
      " "
    Charging...
"""

# Frame 3: THE FLASH (Thunderbolt / Light Up)
FRAME_FLASH = r"""
   \  |  /
  --\.:/--  
 =< [O O] >=  !!!!
  --/ - \--
   /  |  \
   
  * FLASH *
"""

# Frame 4: Lit Up (Happy/Result)
# Frame 4: Lit Up (Pixel Art Style)
# Using half-blocks or full blocks with colors to simulate pixels
Y = "[#fcd14d]██[/]" # Yellow
B = "[#2c2c2c]██[/]" # Black/Outline
R = "[#e74c3c]██[/]" # Red Cheeks
W = "[#ffffff]██[/]" # White/Sparkle
_ = "  "             # Transparent/Space

FRAME_LIT = (
    f"{_}{_}{_}{_}{B}{B}{_}{_}{_}{_}{_}{_}{_}{B}{B}{_}{_}\n"
    f"{_}{_}{_}{B}{Y}{Y}{B}{_}{_}{_}{_}{_}{B}{Y}{Y}{B}{_}\n"
    f"{_}{_}{_}{B}{Y}{Y}{B}{_}{_}{_}{_}{_}{B}{Y}{Y}{B}{_}\n"
    f"{_}{_}{_}{_}{B}{Y}{Y}{B}{_}{_}{_}{B}{Y}{Y}{B}{_}{_}\n"
    f"{_}{_}{_}{_}{B}{Y}{Y}{Y}{B}{B}{B}{Y}{Y}{Y}{B}{_}{_}\n"
    f"{_}{_}{_}{B}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{B}{_}\n"
    f"{_}{_}{B}{Y}{B}{B}{Y}{Y}{Y}{Y}{Y}{B}{B}{Y}{Y}{B}{_}\n"
    f"{_}{B}{Y}{Y}{B}{W}{B}{Y}{Y}{Y}{B}{W}{B}{Y}{Y}{Y}{B}\n"
    f"{B}{Y}{Y}{Y}{B}{B}{Y}{Y}{B}{Y}{Y}{B}{B}{Y}{Y}{Y}{B}\n"
    f"{B}{Y}{Y}{Y}{Y}{Y}{R}{R}{B}{R}{R}{Y}{Y}{Y}{Y}{Y}{B}\n"
    f"{B}{Y}{Y}{Y}{Y}{Y}{R}{R}{Y}{R}{R}{Y}{Y}{Y}{Y}{Y}{B}\n"
    f"{_}{B}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{B}{_}\n"
    f"{_}{_}{B}{B}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{Y}{B}{B}{_}{_}\n"
    f"{_}{_}{_}{_}{B}{B}{Y}{Y}{Y}{Y}{Y}{B}{B}{_}{_}{_}{_}\n"
    f"{_}{_}{_}{_}{_}{_}{B}{B}{B}{B}{B}{_}{_}{_}{_}{_}{_}\n"
    "           [bold yellow]PIKAOPS CLI[/]"
)

BOOT_SEQUENCE = [
    "[grey50]Pika...?[/grey50]",
    "[yellow]Pika... Pika...[/yellow]",
    "[bold white on yellow]*** PCKAAAA - CHUUUUUU! ***[/bold white on yellow]",
    "[bold yellow]Pika Pi![/bold yellow]",
]

class SplashScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static(FRAME_DARK, id="logo"),
            Static("", id="boot_log"),
            id="splash-container"
        )

    def on_mount(self) -> None:
        asyncio.create_task(self.run_animation())

    async def run_animation(self):
        log_widget = self.query_one("#boot_log", Static)
        logo_widget = self.query_one("#logo", Static)
        
        # 1. Darkness
        logo_widget.update(FRAME_DARK)
        log_widget.update(BOOT_SEQUENCE[0])
        await asyncio.sleep(1.5)
        
        # 2. Charging (Blink a few times)
        for _ in range(3):
            logo_widget.update(FRAME_CHARGE)
            log_widget.update(BOOT_SEQUENCE[1])
            await asyncio.sleep(0.3)
            logo_widget.update(FRAME_DARK)
            await asyncio.sleep(0.3)
            
        # 3. FLASH!
        logo_widget.update(FRAME_FLASH)
        log_widget.update(BOOT_SEQUENCE[2])
        # Force a style change if possible, or just rely on the text markup
        await asyncio.sleep(0.8)
        
        # 4. Lit Up / Reveal
        logo_widget.update(FRAME_LIT)
        log_widget.update(BOOT_SEQUENCE[3])
        await asyncio.sleep(1.5)
        
        self.app.switch_screen("dashboard")
