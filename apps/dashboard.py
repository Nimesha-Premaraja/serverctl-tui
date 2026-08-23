import platform
import socket
import time
from typing import TYPE_CHECKING

import psutil
from textual.widgets import Static

if TYPE_CHECKING:
    from app import LinuxDashboard


def update_dashboard(app: "LinuxDashboard") -> None:
    # CPU
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_count = psutil.cpu_count()

    app.query_one("#cpu", Static).update(
        f"[b]CPU[/b]\n\n"
        f"Usage: {cpu_percent:.1f}%\n"
        f"Cores: {cpu_count}"
    )

    # Memory
    memory = psutil.virtual_memory()

    app.query_one("#memory", Static).update(
        f"[b]MEMORY[/b]\n\n"
        f"Usage: {memory.percent:.1f}%\n"
        f"Used: {app.bytes_to_gb(memory.used):.2f} GB\n"
        f"Total: {app.bytes_to_gb(memory.total):.2f} GB"
    )

    # Disk
    disk = psutil.disk_usage("/")

    app.query_one("#disk", Static).update(
        f"[b]DISK[/b]\n\n"
        f"Usage: {disk.percent:.1f}%\n"
        f"Used: {app.bytes_to_gb(disk.used):.2f} GB\n"
        f"Total: {app.bytes_to_gb(disk.total):.2f} GB"
    )

    # System
    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time

    app.query_one("#system-info", Static).update(
        f"Hostname: {socket.gethostname()}\n"
        f"OS: {platform.system()} {platform.release()}\n"
        f"Kernel: {platform.version()}\n"
        f"Architecture: {platform.machine()}\n"
        f"Uptime: {app.format_uptime(uptime)}"
    )

    # Network
    net = psutil.net_io_counters()

    app.query_one("#network-info", Static).update(
        f"Bytes Sent: {app.bytes_to_mb(net.bytes_sent):.2f} MB\n"
        f"Bytes Received: {app.bytes_to_mb(net.bytes_recv):.2f} MB\n"
        f"Packets Sent: {net.packets_sent:,}\n"
        f"Packets Received: {net.packets_recv:,}"
    )
