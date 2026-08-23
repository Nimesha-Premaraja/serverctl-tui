# serverctl-tui — automation
#
# Usage:
#   make install   Create a virtual environment and install dependencies
#   make run       Launch the dashboard (installs first if needed)
#   make dev       Editable install (exposes the `serverctl` command)
#   make clean     Remove the virtual environment and caches

VENV    := .venv
PYTHON  := $(VENV)/bin/python
PIP     := $(VENV)/bin/pip

.PHONY: install run dev clean

$(VENV):
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: $(VENV)
	$(PIP) install -r requirements.txt

dev: $(VENV)
	$(PIP) install -e .

run: install
	$(PYTHON) apps/app.py

clean:
	rm -rf $(VENV) **/__pycache__ *.egg-info
