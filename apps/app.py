import platform
import socket
import time

import psutil
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Footer, Header, Label, Static


class LinuxDashboard(App):
    """Real-time Linux system dashboard using Textual and psutil."""

    TITLE = "Linux Server Dashboard"

    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="dashboard"):
            with Horizontal(id="stats"):
                yield Static(id="cpu", classes="stat")
                yield Static(id="memory", classes="stat")
                yield Static(id="disk", classes="stat")

            with Horizontal(id="system"):
                with Vertical(classes="panel"):
                    yield Label("SYSTEM", classes="panel-title")
                    yield Static(id="system-info")

                with Vertical(classes="panel"):
                    yield Label("NETWORK", classes="panel-title")
                    yield Static(id="network-info")

            yield Static("Press R to refresh • Press Q to quit", id="footer-info")

        yield Footer()

    def on_mount(self) -> None:
        self.update_dashboard()
        self.set_interval(2, self.update_dashboard)

    def action_refresh(self) -> None:
        self.update_dashboard()

    def update_dashboard(self) -> None:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_count = psutil.cpu_count()

        self.query_one("#cpu", Static).update(
            f"[b]CPU[/b]\n\n"
            f"Usage: {cpu_percent:.1f}%\n"
            f"Cores: {cpu_count}"
        )

        # Memory
        memory = psutil.virtual_memory()

        self.query_one("#memory", Static).update(
            f"[b]MEMORY[/b]\n\n"
            f"Usage: {memory.percent:.1f}%\n"
            f"Used: {self.bytes_to_gb(memory.used):.2f} GB\n"
            f"Total: {self.bytes_to_gb(memory.total):.2f} GB"
        )

        # Disk
        disk = psutil.disk_usage("/")

        self.query_one("#disk", Static).update(
            f"[b]DISK[/b]\n\n"
            f"Usage: {disk.percent:.1f}%\n"
            f"Used: {self.bytes_to_gb(disk.used):.2f} GB\n"
            f"Total: {self.bytes_to_gb(disk.total):.2f} GB"
        )

        # System
        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time

        self.query_one("#system-info", Static).update(
            f"Hostname: {socket.gethostname()}\n"
            f"OS: {platform.system()} {platform.release()}\n"
            f"Kernel: {platform.version()}\n"
            f"Architecture: {platform.machine()}\n"
            f"Uptime: {self.format_uptime(uptime)}"
        )

        # Network
        net = psutil.net_io_counters()

        self.query_one("#network-info", Static).update(
            f"Bytes Sent: {self.bytes_to_mb(net.bytes_sent):.2f} MB\n"
            f"Bytes Received: {self.bytes_to_mb(net.bytes_recv):.2f} MB\n"
            f"Packets Sent: {net.packets_sent:,}\n"
            f"Packets Received: {net.packets_recv:,}"
        )

    @staticmethod
    def bytes_to_gb(value: int) -> float:
        return value / (1024 ** 3)

    @staticmethod
    def bytes_to_mb(value: int) -> float:
        return value / (1024 ** 2)

    @staticmethod
    def format_uptime(seconds: float) -> str:
        days, seconds = divmod(int(seconds), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, _ = divmod(seconds, 60)

        return f"{days}d {hours}h {minutes}m"


if __name__ == "__main__":
    LinuxDashboard().run()
