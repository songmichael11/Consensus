from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error
import numpy as np
from backend.ml_models.logistic import predict_gini 
from backend.ml_models.deep_neural_network.deep_neural_network import predict_unemployment_rate
import json


FEATURES_NO_REGION = """Population, GDP_per_capita, Trade_union_density, Unemployment_rate,
                       Health, Education, Housing, Community_development,
                       Corporate_tax_rate, Inflation, IRLT"""

REGION = """Region_East_Asia_and_Pacific, Region_Europe_and_Central_Asia, 
            Region_Latin_America_and_Caribbean, Region_Middle_East_and_North_Africa"""

FEATURE_MAP = {
    "Population":"Population", 
    "GDP_per_capita": "GDP per Capita", 
    "Trade_union_density": "Trade Union Density", 
    "Unemployment_rate": "Unemployment Rate",
    "Health": "Health Spending (% of GDP) <br>  ", 
    "Education": "Education Spending (% of GDP) <br>  ", 
    "Housing": "Housing Spending (% of GDP) <br>  ", 
    "Community_development": "Community Development Spending (% of GDP) <br>  ",
    "Corporate_tax_rate": "Corporate Tax Rate", 
    "Inflation": "Inflation", 
    "IRLT": "IRLT"  
}

# Create a Blueprint for models routes
models = Blueprint("models", __name__)

# the below routes can def be abstracted, but that's a slightly later issue

# GET request to get a plotly prediction graph for a post
@models.route("/posts/predict/<int:graphID>", methods=["GET"])
def get_post_predictions(graphID):
    try:
        current_app.logger.info(f"Starting gini_plot request for GraphID {graphID}")
        cursor = db.get_db().cursor()

        # get the graph row
        cursor.execute(f"""SELECT XAxis, XMin, XMax, XStep, {FEATURES_NO_REGION}, {REGION} FROM Graphs WHERE GraphID = %s""", (graphID,))
        row = cursor.fetchone()
        current_app.logger.info(row)

        if row is None:
            return jsonify({"error": "Graph not found"}), 404

        output = predict_from_features(row)
        return output
        
    except Exception as e:
        current_app.logger.error(f"Error in gini_plot: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# POST request to get a plotly prediction graph for the data playground
@models.route("/playground/predict", methods=["POST"])
def get_playground_predictions():
    try:
        row = request.get_json()
        current_app.logger.info(row)

        output = predict_from_features(row)
        return output

    except Exception as e:
        current_app.logger.error(f"Error in gini_plot: {str(e)}")
        return jsonify({"error": str(e)}), 500

# POST request to get a plotly prediction graph for the data playground BUT USING DEEP NEURAL NETWORK
@models.route("/playground/predict/deep_neural_network", methods=["POST"]) # NOTE: work in progress
def get_playground_predictions_deep_neural_network():
    try:
        row = request.get_json()
        current_app.logger.info(row)

        output = predict_from_features_deep_neural_network(row)
        return output

    except Exception as e:
        current_app.logger.error(f"Error in deep neural network route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@models.route("/playground/stds", methods=["GET"])
def get_stds():
    try:
        # get describe metrics
        cursor = db.get_db().cursor()
        cursor.execute(f"""SELECT {FEATURES_NO_REGION} FROM PredictMetrics WHERE Metric = 'std'""")
        rows = cursor.fetchall()
        
        current_app.logger.info(rows)

        cursor.close()

        # columns = [col for col in rows[0].keys() if col != 'Metric']

        # describe = [
        #     [row[col] for col in columns] for row in rows
        #     ]
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# abstracted prediction function for both routes.
# takes in a list of feature values and output a jsonified set of outputs
def predict_from_features(row):
    try:
        cursor = db.get_db().cursor()

            # get weights of graph
        cursor.execute(f"""SELECT {FEATURES_NO_REGION}, {REGION}
                       FROM ModelWeights WHERE ModelName = 'Logistic Regression'""")
        weights = list(cursor.fetchone().values())
        current_app.logger.info(weights)

        # get describe metrics
        cursor.execute(f"""SELECT {FEATURES_NO_REGION} FROM PredictMetrics ORDER BY Metric""")
        rows = cursor.fetchall()
        
        current_app.logger.info(rows)

        cursor.close()

        columns = [col for col in rows[0].keys() if col != 'Metric']

        describe = [
            [row[col] for col in columns] for row in rows
            ]

        # get XAxis and range
        x_axis = row["XAxis"]
        x_min = row["XMin"]
        x_max = row["XMax"]
        num_steps = int(row["XStep"])  
        x_values = np.linspace(x_min, x_max, num_steps)

        gini_values = []

        current_app.logger.info(f"Predicting GINI for {len(x_values)} points")

        for x_val in x_values:
            x_input = row.copy()

            x_input[x_axis] = x_val
            
            x_input.pop("XAxis", None)
            x_input.pop("XMin", None)
            x_input.pop("XMax", None)
            x_input.pop("XStep", None)

            x_input = list(x_input.values())

            gini = predict_gini(np.array(x_input), describe=np.array(describe), weights=np.array(weights), model="logistic")

            gini_values.append(gini)

        output = {}
        output["x_values"] = x_values.tolist()
        output["predictions"] = gini_values
        output["x_axis"] = FEATURE_MAP[x_axis]

        current_app.logger.info(output)

        return jsonify(output)
    except Exception as e:
        current_app.logger.error(f"Error in gini_plot: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# DNN function! abstracted prediction function for routes that use Deep Neural Network model.
# takes in a list of feature values and output a jsonified set of outputs
def predict_from_features_deep_neural_network(row):
    try:
        # get XAxis and range
        x_axis = row["XAxis"]
        x_min = row["XMin"]
        x_max = row["XMax"]
        num_steps = int(row["XStep"])  
        x_values = np.linspace(x_min, x_max, num_steps)

        unemployment_values = []

        current_app.logger.info(f"Predicting unemployment for {len(x_values)} points using DNN")

        for x_val in x_values:
            x_input = row.copy()

            x_input[x_axis] = x_val
            
            # Remove graph configuration parameters
            x_input.pop("XAxis", None)
            x_input.pop("XMin", None)
            x_input.pop("XMax", None)
            x_input.pop("XStep", None)

            # Use the DNN prediction function
            unemployment = predict_unemployment_rate(x_input)
            # Ensure it's a standard Python float for JSON serialization
            unemployment_values.append(float(unemployment))

        output = {}
        output["x_values"] = x_values.tolist()
        output["predictions"] = unemployment_values
        output["x_axis"] = FEATURE_MAP[x_axis]

        current_app.logger.info(f"DNN prediction complete. Generated {len(unemployment_values)} predictions")

        return jsonify(output)
        
    except Exception as e:
        current_app.logger.error(f"Error in deep neural network prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500