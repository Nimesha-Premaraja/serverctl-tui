import platform
import socket
import time
from typing import TYPE_CHECKING

import psutil
from textual.widgets import Digits, ProgressBar, Static

if TYPE_CHECKING:
    from app import LinuxDashboard


def _severity(percent: float) -> str:
    """Return a CSS class name based on usage thresholds."""
    if percent >= 90:
        return "critical"
    if percent >= 70:
        return "warning"
    return "healthy"


def _apply_gauge(app: "LinuxDashboard", card_id: str, percent: float) -> None:
    """Update a metric card's digits, progress bar and severity color."""
    severity = _severity(percent)

    value = app.query_one(f"#{card_id}-value", Digits)
    value.update(f"{percent:.1f}")

    bar = app.query_one(f"#{card_id}-bar", ProgressBar)
    bar.update(progress=percent)

    for element in (value, bar):
        element.remove_class("healthy", "warning", "critical")
        element.add_class(severity)


def update_dashboard(app: "LinuxDashboard") -> None:
    # CPU
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_count = psutil.cpu_count(logical=True)
    cpu_physical = psutil.cpu_count(logical=False) or cpu_count

    try:
        load1, load5, load15 = psutil.getloadavg()
        load_line = f"Load avg  {load1:.2f} {load5:.2f} {load15:.2f}"
    except (AttributeError, OSError):
        load_line = "Load avg  n/a"

    _apply_gauge(app, "cpu", cpu_percent)
    app.query_one("#cpu-detail", Static).update(
        f"{cpu_physical} cores · {cpu_count} threads\n{load_line}"
    )

    # Memory
    memory = psutil.virtual_memory()
    _apply_gauge(app, "memory", memory.percent)
    app.query_one("#memory-detail", Static).update(
        f"{app.bytes_to_gb(memory.used):.1f} / "
        f"{app.bytes_to_gb(memory.total):.1f} GB used\n"
        f"{app.bytes_to_gb(memory.available):.1f} GB available"
    )

    # Disk
    disk = psutil.disk_usage("/")
    _apply_gauge(app, "disk", disk.percent)
    app.query_one("#disk-detail", Static).update(
        f"{app.bytes_to_gb(disk.used):.1f} / "
        f"{app.bytes_to_gb(disk.total):.1f} GB used\n"
        f"{app.bytes_to_gb(disk.free):.1f} GB free"
    )

    # System
    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time
    boot_stamp = time.strftime("%Y-%m-%d %H:%M", time.localtime(boot_time))

    app.query_one("#system-info", Static).update(
        f"[b]Hostname[/b]      {socket.gethostname()}\n"
        f"[b]OS[/b]            {platform.system()} {platform.release()}\n"
        f"[b]Architecture[/b]  {platform.machine()}\n"
        f"[b]Processes[/b]     {len(psutil.pids())}\n"
        f"[b]Uptime[/b]        {app.format_uptime(uptime)}\n"
        f"[b]Booted[/b]        {boot_stamp}"
    )

    # Network
    net = psutil.net_io_counters()
    app.query_one("#network-info", Static).update(
        f"[b]Sent[/b]        {app.bytes_to_mb(net.bytes_sent):,.1f} MB\n"
        f"[b]Received[/b]    {app.bytes_to_mb(net.bytes_recv):,.1f} MB\n"
        f"[b]Pkts Sent[/b]   {net.packets_sent:,}\n"
        f"[b]Pkts Recv[/b]   {net.packets_recv:,}\n"
        f"[b]Errors[/b]      {net.errin + net.errout:,}\n"
        f"[b]Drops[/b]       {net.dropin + net.dropout:,}"
    )

    app.mark_updated()
