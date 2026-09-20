from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd

app = Flask(__name__, static_folder="..", static_url_path="")

# Load the trained ML model
model = joblib.load("crowd_model.pkl")

# Load destination tourism data
destination_data = pd.read_csv("destinaion_data.csv")

# Load our prototype crowd-score dataset
score_data = pd.read_csv("destination_dataset.csv")


@app.route("/")
def home():
    return send_from_directory("..", "index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    destination = data["destination"]

    # Find destination
    destination_row = destination_data[
        destination_data["destination"].str.lower()
        == destination.lower()
    ]

    if destination_row.empty:
        return jsonify({
            "prediction": "Unknown",
            "destination": destination,
            "annual_visitors": None,
            "crowd_score": None,
            "destination_found": False
        })

    # Get destination information
    actual_destination = destination_row.iloc[0]["destination"]
    annual_visitors = int(destination_row.iloc[0]["annual_visitors"])

    # ML model input
    input_data = pd.DataFrame([{
        "destination": actual_destination,
        "annual_visitors": annual_visitors,
        "day": data["day"],
        "weather": data["weather"],
        "holiday": data["holiday"],
        "festival": data["festival"]
    }])

    # Predict crowd category
    prediction = model.predict(input_data)[0]

    # Find corresponding crowd score
    score_row = score_data[
        (score_data["destination"] == actual_destination)
        & (score_data["day"] == data["day"])
        & (score_data["weather"] == data["weather"])
        & (score_data["holiday"] == data["holiday"])
        & (score_data["festival"] == data["festival"])
    ]

    if not score_row.empty:
        crowd_score = float(score_row.iloc[0]["crowd_score"])
    else:
        crowd_score = None

    return jsonify({
        "prediction": prediction,
        "destination": actual_destination,
        "annual_visitors": annual_visitors,
        "crowd_score": crowd_score,
        "destination_found": True
    })


if __name__ == "__main__":
    app.run(debug=True)
