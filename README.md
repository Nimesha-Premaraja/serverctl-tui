# serverctl-tui

A real-time Linux server monitoring dashboard for your terminal, built with
[Textual](https://textual.textualize.io/) and [psutil](https://github.com/giampaolo/psutil).

`serverctl-tui` turns any SSH session into a clean, production-grade system
monitor — live CPU, memory, disk, network, and host metrics with color-coded
gauges that update in real time.

---

## Features

- **Live metric gauges** — CPU, memory, and disk usage rendered as large digit
  readouts with progress bars.
- **Color-coded severity** — gauges turn green / amber / red automatically as
  usage crosses 70% and 90% thresholds.
- **System panel** — hostname, OS, architecture, process count, uptime, and
  boot time.
- **Network panel** — bytes/packets sent and received, plus error and drop
  counters.
- **CPU insight** — physical vs. logical core counts and 1/5/15-minute load
  average.
- **Auto-refresh** — the dashboard polls every 2 seconds with a live "last
  updated" timestamp and a `● LIVE` status indicator.
- **Light / dark themes** — toggle instantly from the keyboard.

---

## Requirements

- **Python 3.10+** (developed against Python 3.14)
- **Linux** for full functionality (load average and some counters are
  Unix-specific). It also runs on macOS with graceful fallbacks for
  unsupported metrics.

### Python dependencies

| Package  | Purpose                          |
| -------- | -------------------------------- |
| textual  | Terminal UI framework            |
| psutil   | Cross-platform system metrics    |

---

## Installation

Clone the repository:

```bash
git clone git@github.com:Nimesha-Premaraja/serverctl-tui.git
cd serverctl-tui
```

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install textual psutil
```

Run the dashboard from the `apps/` directory:

```bash
cd apps
python app.py
```

Or run it without changing directories:

```bash
python apps/app.py
```

### Keyboard shortcuts

| Key | Action              |
| --- | ------------------- |
| `r` | Refresh immediately |
| `d` | Toggle light / dark theme |
| `q` | Quit                |

---

## Project structure

```
serverctl-tui/
├── apps/
│   ├── app.py          # Textual application, layout, and widgets
│   ├── dashboard.py    # Metric collection and gauge update logic
│   └── app.tcss        # Textual CSS theme and styling
├── LICENSE
└── README.md
```

---

## Configuration

The refresh interval is defined in `app.py`:

```python
refresh_interval: reactive[float] = reactive(2.0)  # seconds
```

Severity thresholds live in `dashboard.py`:

```python
def _severity(percent: float) -> str:
    if percent >= 90:
        return "critical"   # red
    if percent >= 70:
        return "warning"    # amber
    return "healthy"        # green
```

---

## Contributing

Contributions are welcome. To get started:

1. Fork the repository and create a feature branch.
2. Make your changes and verify the app runs (`python apps/app.py`).
3. Open a pull request describing your change.

---

## License

Released under the [MIT License](LICENSE).
Copyright © 2026 Nimesha Dilshan Premaraja.
