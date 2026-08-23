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

Clone the repository first:

```bash
git clone git@github.com:Nimesha-Premaraja/serverctl-tui.git
cd serverctl-tui
```

Then pick **one** of the automated setups below — no need to create a virtual
environment or install dependencies by hand.

### Option 1 — Script

Sets up the virtual environment, installs dependencies, and launches the app:

```bash
./run.sh
```

Set up only (without launching):

```bash
./run.sh --setup
```

### Option 2 — Make

```bash
make run        # set up (if needed) and run
make install    # set up only
make dev        # editable install, exposes the `serverctl` command
make clean      # remove the virtual environment and caches
```

### Option 3 — pip / pyproject

Install as a package to get a `serverctl` command on your `PATH`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
serverctl
```

### Option 4 — Manual (from requirements.txt)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python apps/app.py
```

---

## Usage

If you installed with the bootstrap script or Make, the app launches for you.
Otherwise, start it with any of:

```bash
serverctl              # if installed via `pip install -e .` or `make dev`
python apps/app.py     # directly, from the repo root
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
