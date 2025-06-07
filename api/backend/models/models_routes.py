from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error
import numpy as np
from backend.ml_models.logistic import predict_gini

# OLD_FULL_FEATURES = """Population, GDP_per_capita, Trade_union_density, Unemployment_rate,
#                        Health, Education, Housing, Community_development, Real_interest_rates,
#                        Productivity, Corporate_tax_rate, Inflation, Personal_property_tax, IRLT,
#                        Region_East_Asia_and_Pacific, 
#                        Region_Europe_and_Central_Asia, Region_Latin_America_and_Caribbean, 
#                        Region_Middle_East_and_North_Africa"""

FEATURES = """Population, GDP_per_capita, Trade_union_density, Corporate_tax_rate, Education, 
                       Health, Housing, Community_development, IRLT, Unemployment_rate,
                       Inflation, 
                       Region_East_Asia_and_Pacific, 
                       Region_Europe_and_Central_Asia, Region_Latin_America_and_Caribbean, 
                       Region_Middle_East_and_North_Africa"""

# Features which are broken or didn't train properly in the model: Real_interest_rates, Productivity, Personal_property_tax,

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
        cursor.execute(f"""SELECT XAxis, XMin, XMax, XStep, {FEATURES} FROM Graphs WHERE GraphID = %s""", (graphID,))
        row = cursor.fetchone()
        current_app.logger.info(row)

        if row is None:
            return jsonify({"error": "Graph not found"}), 404

        # get weights of graph
        cursor.execute(f"""SELECT {FEATURES} 
                       FROM ModelWeights WHERE ModelName = 'Logistic Regression'""")
        weights = list(cursor.fetchone().values())
        current_app.logger.info(weights)

        # get describe metrics
        cursor.execute(f"""SELECT {FEATURES} FROM PredictMetrics ORDER BY Metric""")
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
        x_step = row["XStep"]
        x_values = np.arange(x_min, x_max + x_step, x_step)

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
        output["x_axis"] = x_axis

        current_app.logger.info(output)

        return jsonify(output)
        
    except Exception as e:
        current_app.logger.error(f"Error in gini_plot: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# POST request to get a plotly prediction graph for the data playground
@models.route("/playground/predict", methods=["POST"])
def get_playground_predictions():
    try:
        cursor = db.get_db().cursor()

        row = request.get_json()

        # NOTE: The model was trained with only 15 features (excluding Real_interest_rates, 
        # Productivity, Personal_property_tax which had problematic training data).
        # We filter these out before prediction but keep them in the frontend/database
        # for future use when the model is retrained.
        
        # get weights of graph (only for working features)
        cursor.execute(f"""SELECT {FEATURES} 
                       FROM ModelWeights WHERE ModelName = 'Logistic Regression'""")
        weights = list(cursor.fetchone().values())
        current_app.logger.info(weights)

        # get describe metrics (only for working features)
        cursor.execute(f"""SELECT {FEATURES} FROM PredictMetrics ORDER BY Metric""")
        rows = cursor.fetchall()
        
        cursor.close()

        columns = [col for col in rows[0].keys() if col != 'Metric']

        describe = [
            [row[col] for col in columns] for row in rows
            ]

        current_app.logger.info("describe")
        current_app.logger.info(describe)

        # get XAxis and range
        x_axis = row["XAxis"]
        x_min = row["XMin"]
        x_max = row["XMax"]
        num_steps = int(row["XStep"])  # XStep is actually num steps not stepsize
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

            # IMPORTANT: Filter out broken features before calling the ML model
            # Remove Real_interest_rates, Productivity, Personal_property_tax temporarily
            x_input.pop("Real_interest_rates", None)
            x_input.pop("Productivity", None) 
            x_input.pop("Personal_property_tax", None)

            x_input = list(x_input.values())

            gini = predict_gini(np.array(x_input), describe=np.array(describe), weights=np.array(weights), model="logistic")

            gini_values.append(gini)

        output = {}
        output["x_values"] = x_values.tolist()
        output["predictions"] = gini_values
        output["x_axis"] = x_axis


        return jsonify(output)

    except Exception as e:
        current_app.logger.error(f"Error in gini_plot: {str(e)}")
        return jsonify({"error": str(e)}), 500
