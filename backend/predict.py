from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from joblib import load

app = Flask(__name__)
CORS(app)  # Enable CORS on the Flask app

# Load the trained Random Forest model for predicting Outcome
model_filename = 'backend/outcome_prediction_with_team_model.joblib'
random_forest_model = load(model_filename)

# Load the LabelEncoders
label_encoders = {}
for column in ['Team', 'Ejected']:
    le_filename = f'backend/{column}_label_encoder.joblib'
    label_encoders[column] = load(le_filename)

# Outcome's LabelEncoder for decoding the prediction
outcome_label_encoder = load('backend/Outcome_label_encoder.joblib')


@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()
    X_new = pd.DataFrame([input_data])

    X_new['Task Completed'] = pd.to_numeric(X_new['Task Completed'], 
                                            errors='coerce')
    X_new['Imposter Kills'] = pd.to_numeric(X_new['Imposter Kills'], 
                                            errors='coerce')

    def process_game_length(gl):
        if isinstance(gl, str) and 'm' in gl:
            parts = gl.replace('s', '').split('m')
            return int(parts[0]) * 60 + int(parts[1])
        return None

    X_new['Game Length'] = X_new['Game Length'].apply(process_game_length)
    X_new.replace({'No': 0, 'Yes': 1}, inplace=True)

    for column in ['Team', 'Ejected']:
        X_new[column] = label_encoders[column].transform(X_new[column])

    X_new.fillna(0, inplace=True)

    new_prediction = random_forest_model.predict(X_new)
    predicted_outcome = outcome_label_encoder.inverse_transform(new_prediction)

    return jsonify({'predicted_outcome': predicted_outcome[0]})


if __name__ == '__main__':
    app.run(debug=True)