import os
import logging
from flask import Flask, jsonify, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

def create_app(test_config=None):
    app = Flask(__name__)

    # Configuration settings
    app.config['CSV_FILE_PATH'] = os.path.join(os.getcwd(), 'data', 'simulation_results.csv')
    
    # Production-grade logging setup
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    @app.route('/api/simulation', methods=['GET'])
    def get_simulation_data():
        """
        Reads the simulation CSV file and returns the data as JSON.
        This endpoint simulates the post-automation step when the CSV is generated.
        """
        csv_file = app.config['stress_results.csv']
        if not os.path.exists(csv_file):
            app.logger.error("CSV file not found at: %s", csv_file)
            return jsonify({"error": "Simulation results not available"}), 404
        try:
            df = pd.read_csv(csv_file)
            data = df.to_dict(orient='records')
            app.logger.info("Simulation data loaded successfully")
            return jsonify(data), 200
        except Exception as e:
            app.logger.exception("Error reading CSV file:")
            return jsonify({"error": "Failed to process simulation results"}), 500

    @app.route('/plot', methods=['GET'])
    def get_simulation_plot():
        """
        Reads the simulation CSV file and returns an interactive Plotly chart as HTML.
        Assumes the CSV contains at least 'Time' and 'Force' columns.
        """
        csv_file = app.config['stress_results.csv']
        if not os.path.exists(csv_file):
            app.logger.error("CSV file not found at: %s", csv_file)
            return "Simulation results not available", 404
        try:
            df = pd.read_csv(csv_file)
            # Check if expected columns exist; otherwise, plot generic data.
            if 'Time' in df.columns and 'Force' in df.columns:
                fig = px.line(df, x='Time', y='Force', title='Simulation Force Over Time')
            else:
                fig = px.scatter(df, title='Simulation Data')
            app.logger.info("Plot generated successfully")
            # Return full HTML that embeds the Plotly chart.
            html = pio.to_html(fig, full_html=True)
            return html, 200
        except Exception as e:
            app.logger.exception("Error generating plot:")
            return "Failed to generate plot", 500

    return app

if __name__ == '__main__':
    app = create_app()
    # Do not run in debug mode in production.
    app.run(host='0.0.0.0', port=5000, debug=False)
