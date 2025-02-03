## Ansys Automation App

This project demonstrates a CAE automation workflow integrated with a web-based visualization dashboard built using Dash.

## Overview

- **Automation Module:**
  - Runs a static FEA simulation using ANSYS MAPDL via PyMAPDL.
  - Imports a CAD model from `FirstResolt.IGS`.
  - Applies meshing, material properties, and boundary conditions.
  - Extracts nodal stress data and writes it to `data/stress_results.csv`.

- **Dash Dashboard:**
  - Provides a button to trigger the simulation.
  - Displays simulation results interactively as a line graph.
  - Refreshes the graph after simulation is run.

## Directory Structure
├── README.md
├── FirstResolt.IGS              # Your CAD file (must be provided)
├── app.py                      # Dash application
├── automation/
│   ├── __init__.py           # (Empty; marks the automation folder as a package)
│   └── automation_script.py  # Automation simulation script
├── data/
│   └── stress_results.csv    # Simulation results CSV (will be generated by the automation script)
└── requirements.txt          # Python dependencies

