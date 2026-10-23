# Computational Magnetic Resonance Imaging Labs WS 2026/27
Code for the lab exercises of Computational Magnetic Resonance Imaging in the winter semester 2026/27

# Structure
Each weekly exercise/lab is its own directory containing the Python code due for submission.
All of the task instructions are contained there.

```
CMRI/
 |   Lab01/
 |     |  __init__.py
 |     |  lab01.py
 |     |  utils.py
 |   Lab02/
 |   ...
 |   Lab10/
```

# Getting Started

Create the default virtual environment with `hatch` from `pyproject.toml`:
```bash
hatch env create
```

Install all dependencies into this environment with any `hatch` command that uses the env, e.g.:
```bash
hatch shell
# or
hatch run python
```

Optionally create dependency lockfile:
```bash
hatch lock --export pylock.toml
```