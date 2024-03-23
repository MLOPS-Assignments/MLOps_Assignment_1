import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from joblib import dump

# Load your data
df = pd.read_csv(r'data\Merged_File.csv')

# Replace '-' with NaN for numerical columns and 'None' for categorical
df['Task Completed'] = pd.to_numeric(df['Task Completed'], errors='coerce')
df['Imposter Kills'] = pd.to_numeric(df['Imposter Kills'], errors='coerce')


def convert_game_length(x):
    """Converts game length from 'xm ys' format to total seconds."""
    if isinstance(x, str) and 'm' in x:
        minutes, seconds = x.replace('s', '').split('m')
        return int(minutes) * 60 + int(seconds)
    return None


df['Game Length'] = df['Game Length'].apply(convert_game_length)
df.replace({'-': None, 'No': 0, 'Yes': 1}, inplace=True)

# Label encode categorical columns. Now 'Team' is included as a feature.
label_encoders = {}
for column in ['Team', 'Ejected']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Since 'Outcome' is our target, we also need to encode it
outcome_le = LabelEncoder()
df['Outcome'] = outcome_le.fit_transform(df['Outcome'])
label_encoders['Outcome'] = outcome_le

# Define feature columns - 'Outcome' is removed, 'Team' is included
features = ['Team', 'Task Completed', 'Murdered', 'Imposter Kills',
            'Game Length', 'Ejected']

# Handle missing values
df[features] = df[features].fillna(0)

# Define the target variable
target = 'Outcome'

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    df[features], df[target], test_size=0.2, random_state=42)

# Initialize and train the classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Predict and evaluate
y_pred = rf_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy}')

# Save the model and label encoders
model_filename = 'outcome_prediction_with_team_model.joblib'
dump(rf_classifier, model_filename)
print(f'Trained model saved to {model_filename}')

for col, encoder in label_encoders.items():
    encoder_filename = f'{col}_label_encoder.joblib'
    dump(encoder, encoder_filename)
    print(f'LabelEncoder for {col} saved to {encoder_filename}')
