#!/usr/bin/env python3
"""
Production-grade CAE automation script using ANSYS MAPDL via PyMAPDL.
This script:
  - Imports a CAD model (IGES format) from the ../data folder.
  - Sets up meshing, material properties, and boundary conditions.
  - Runs a static FEA simulation.
  - Extracts nodal stress data and writes it to a CSV file in ../data.
"""

import os
import logging
import pandas as pd
from ansys.mapdl.core import launch_mapdl

# Configure logging for production-level output.
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def run_simulation():
    try:
        # Launch ANSYS MAPDL.
        logging.info("Launching ANSYS MAPDL...")
        mapdl = launch_mapdl()
        
        # Clear previous data and enter pre-processing mode.
        mapdl.clear()
        mapdl.prep7()
        
        # Build the path to the CAD model.
        # Per README, ensure that 'differential_piece.iges' is in the data folder.
        cad_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'FirstResolt.IGS')
        if not os.path.exists(cad_file):
            logging.error(f"CAD file not found at {cad_file}. Please ensure the file exists.")
            return
        
        logging.info(f"Importing CAD model from {cad_file}...")
        mapdl.igesin(cad_file)
        
        # Set element type and mesh parameters.
        logging.info("Setting element type and meshing the geometry...")
        mapdl.et(1, 185)            # Use SOLID185 for 3D structural analysis.
        mesh_size = 0.005           # Global element size (5 mm).
        mapdl.esize(mesh_size)
        mapdl.vmesh('ALL')
        
        # Define material properties (example: steel).
        logging.info("Defining material properties (Steel)...")
        mapdl.mp('EX', 1, 210e9)    # Young's modulus in Pascals.
        mapdl.mp('PRXY', 1, 0.3)    # Poisson's ratio.
        
        # Apply boundary conditions.
        logging.info("Applying boundary conditions...")
        # Fix nodes at X = 0 (support face).
        mapdl.nsel('S', 'LOC', 'X', 0)
        mapdl.d('ALL', 'ALL', 0)
        mapdl.allsel()
        
        # Apply a force on nodes at X = 0.1 m (load face).
        mapdl.nsel('S', 'LOC', 'X', 0.1)
        force_value = -1000  # 1000 N in the negative X-direction.
        mapdl.f('ALL', 'FX', force_value)
        mapdl.allsel()
        
        # Solve the simulation.
        logging.info("Solving the simulation...")
        mapdl.run('/SOLU')
        mapdl.solve()
        mapdl.finish()
        
        # Post-processing: extract nodal stress data (example: stress component SX).
        logging.info("Extracting nodal stress data...")
        mapdl.post1()
        mapdl.set(1, 1)  # Set to load step 1, substep 1.
        nodal_stress = mapdl.post_processing.nodal_stress()
        
        # Convert nodal stress data to a DataFrame and export to CSV.
        df = pd.DataFrame(nodal_stress)
        output_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'stress_results.csv')
        df.to_csv(output_csv, index=False)
        logging.info(f"Simulation complete. Results saved to {output_csv}")
        
        # Exit MAPDL session.
        mapdl.exit()
        
    except Exception as e:
        logging.exception("An error occurred during simulation:")
        raise

if __name__ == '__main__':
    run_simulation()
