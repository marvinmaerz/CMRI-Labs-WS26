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

PyCharm: to run labs cell-by-cell, mark the selected LabXX directory 
as sources root to include their path in the Python Console that opens:

1. Right-click LabXX directory -> Mark Directory As -> Sources Root

2. Open LabXX/labxx.py in PyCharm

3. Go to the `if __name__ == "__main__"` block

4. Click on green triangle that says "Execute cell in Console"

5. Upon working on a new / different lab, unmark the other lab as sources root, and mark the new one. 
This reduces the probability of two packages with the same name being confused on import.
