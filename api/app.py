import os
import logging
from flask import Flask, jsonify, request, render_template
import pandas as pd
import plotly.express as px

def create_app(test_config=None):
    # Initialize the Flask app with templates and static folder specified.
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Use a consistent file name for simulation results.
    app.config['CSV_FILE_PATH'] = os.path.join(os.getcwd(), 'data', 'stress_results.csv')
    
    # Production-grade logging setup.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # ------------------------------------------------------------------
    # Endpoint to trigger the simulation.
    # This calls the automation script (ANSYS MAPDL simulation via PyMAPDL).
    # ------------------------------------------------------------------
    @app.route('/simulate', methods=['POST'])
    def simulate():
        try:
            # Import and run the simulation from the automation module.
            from automation.automation_script import run_simulation
            run_simulation()
            app.logger.info("Simulation completed successfully.")
            return jsonify({"message": "Simulation completed successfully"}), 200
        except Exception as e:
            app.logger.exception("Simulation failed:")
            return jsonify({"error": "Simulation failed", "details": str(e)}), 500

    # ------------------------------------------------------------------
    # Endpoint to return raw simulation results as JSON.
    # ------------------------------------------------------------------
    @app.route('/results', methods=['GET'])
    def get_results():
        csv_file = app.config['CSV_FILE_PATH']
        if not os.path.exists(csv_file):
            app.logger.error("CSV file not found at: %s", csv_file)
            return jsonify({"error": "Simulation results not available"}), 404
        try:
            df = pd.read_csv(csv_file)
            data = df.to_dict(orient='records')
            app.logger.info("Simulation data loaded successfully.")
            return jsonify(data), 200
        except Exception as e:
            app.logger.exception("Error reading CSV file:")
            return jsonify({"error": "Failed to process simulation results"}), 500

    # ------------------------------------------------------------------
    # Dashboard: renders the main page with an interactive Plotly chart.
    # ------------------------------------------------------------------
    @app.route('/', methods=['GET'])
    def dashboard():
        csv_file = app.config['CSV_FILE_PATH']
        if not os.path.exists(csv_file):
            app.logger.warning("CSV file not found at: %s. Displaying default chart.", csv_file)
            fig = px.scatter(title='No Simulation Data Available')
        else:
            try:
                df = pd.read_csv(csv_file)
                # Choose a chart type based on the available columns.
                if 'node' in df.columns and 'SX' in df.columns:
                    # Create a line plot with markers and text labels for SX values.
                    fig = px.line(
                        df,
                        x='node',
                        y='SX',
                        title='Nodal Stress (SX)'
                    )
                    # Add markers and text labels to the line plot.
                    fig.update_traces(
                        mode='lines+markers+text',
                        text=df['SX'],
                        textposition='top center',
                        marker=dict(size=8)
                    )
                elif 'Time' in df.columns and 'Force' in df.columns:
                    fig = px.line(df, x='Time', y='Force', title='Simulation Force Over Time')
                else:
                    fig = px.scatter(df, title='Simulation Data')
            except Exception as e:
                app.logger.exception("Error generating dashboard plot:")
                fig = px.scatter(title='Error Loading Data')
        # Convert the Plotly figure to JSON for rendering.
        graphJSON = fig.to_json()
        return render_template("index.html", graphJSON=graphJSON)

    return app

if __name__ == '__main__':
    app = create_app()
    # Do not run in debug mode in production.
    app.run(host='0.0.0.0', port=5000, debug=False)
