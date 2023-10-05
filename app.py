from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import plot_cross_validation_metric
import pickle
import logging
from prophet import Prophet
logging.basicConfig(level=logging.DEBUG)
import os 



app = Flask(__name__)

db_path = "sales_data.db"

@app.route('/')
def index():
    return render_template('forecast.html')


MODEL_MAP = {
    4: "prophet_model_4.pkl",
    219: "prophet_model_219.pkl",
    676: "prophet_model_676.pkl",
    1066: "prophet_model_1066.pkl",
    1098: "prophet_model_1098.pkl",

}

def load_model(store_id):

    """
    Load the pretrained model for the given store ID.
    """
    model_path = MODEL_MAP.get(store_id)
    if model_path is None:
        raise ValueError(f"No model found for store {store_id}")
    
    absolute_path = os.path.abspath(model_path)
    print(f"Trying to open model from: {absolute_path}")

    with open(absolute_path, 'rb') as f:
        try:
            model = pickle.load(f)
            if not isinstance(model, Prophet):  # Check if it's a Prophet model
                raise TypeError(f"Loaded model is not a Prophet model. It's of type: {type(model)}")

            return model
        except Exception as e:
            raise RuntimeError(f"Error loading model: {str(e)}")

@app.route('/forecast', methods=['GET','POST'])
def forecast():

    try:

        if request.method == 'POST':

            # Get data from POST request
            store_id = int(request.form.get('store_id'))
            number_of_days = int(request.form.get('number_of_days'))

            # Load the appropriate model
            model = load_model(store_id)

            # Create future dataframe and predict
            future = model.make_future_dataframe(periods=number_of_days)
            forecast = model.predict(future)

            # Extract the predicted values and seasonal components for the specified number of days
            predicted_values = forecast['yhat'][-number_of_days:].values.tolist()
            trend = forecast['trend'][-number_of_days:].values.tolist()
            yearly = forecast['yearly'][-number_of_days:].values.tolist()
            weekly = forecast['weekly'][-number_of_days:].values.tolist()
            # If you have daily seasonality, extract it as well
            daily = forecast.get('daily', [])[-number_of_days:].values.tolist() if 'daily' in forecast else []

            # Return prediction and seasonal components as JSON response
            return jsonify(
                prediction=predicted_values,
                trend=trend,
                yearly=yearly,
                weekly=weekly,
                daily=daily
            )

        return render_template('forecast.html')

    except Exception as e:
        print("Error:", str(e)) 
        return jsonify(error=f"Error: {str(e)}"), 500

if __name__ == "__main__":
    app.run(debug=True)









