# My Automation App

This project demonstrates a production-grade CAE automation workflow integrated with a web-based visualization dashboard.

## Overview

- **Automation Module:**  
  Runs a static FEA simulation using ANSYS MAPDL via PyMAPDL. The simulation imports a CAD model, applies meshing, material properties, and boundary conditions, then exports nodal stress results to a CSV file.

- **Data Module:**  
  Stores simulation results (CSV file) and the CAD model (e.g., differential_piece.iges).

- **API Module:**  
  A Flask web application that:
  - Provides an endpoint to trigger the simulation (`/simulate`).
  - Serves a dashboard (`/`) that visualizes simulation results interactively with Plotly.
  - Offers an endpoint to retrieve raw results in JSON format (`/results`).

## Setup Instructions

1. **Prerequisites:**
   - Python 3.7+ is required.
   - ANSYS MAPDL must be installed and licensed.
   - Ensure that the CAD file (`differential_piece.iges`) is in the `data/` folder.

2. **Install API Dependencies:**

   Navigate to the `api` folder and run:
   ```bash
   cd api
   pip install -r requirements.txt
