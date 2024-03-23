import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from joblib import dump

# Load your data
df = pd.read_csv('data\Merged_File.csv')

# Replace '-' with NaN for numerical columns and 'None' for categorical
df['Task Completed'] = pd.to_numeric(df['Task Completed'], errors='coerce')
df['Imposter Kills'] = pd.to_numeric(df['Imposter Kills'], errors='coerce')
df['Game Length'] = df['Game Length'].apply(lambda x: int(x.split('m')[0]) * 60 + int(x.split(' ')[1].split('s')[0]) if isinstance(x, str) and 'm' in x else None)
df.replace({'-': None, 'No': 0, 'Yes': 1}, inplace=True)

# Label encode categorical columns. Now 'Team' is included as a feature, not a target.
label_encoders = {}
for column in ['Team', 'Ejected']:
    label_encoder = LabelEncoder()
    df[column] = label_encoder.fit_transform(df[column])
    label_encoders[column] = label_encoder

# Since 'Outcome' is our target, we also need to encode it
outcome_label_encoder = LabelEncoder()
df['Outcome'] = outcome_label_encoder.fit_transform(df['Outcome'])
label_encoders['Outcome'] = outcome_label_encoder

# Updated feature columns - 'Outcome' is removed, 'Team' is included
features = ['Team', 'Task Completed', 'Murdered', 'Imposter Kills', 'Game Length', 'Ejected']

# Handle missing values appropriately
df[features] = df[features].fillna(0)

# Target variable is 'Outcome'
target = 'Outcome'

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# Initialize and train the classifier
random_forest = RandomForestClassifier(n_estimators=100, random_state=42)
random_forest.fit(X_train, y_train)

# Predict and evaluate
y_pred = random_forest.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy}')

# Save the model and label encoders
model_filename = 'outcome_prediction_with_team_model.joblib'
dump(random_forest, model_filename)
print(f'Trained model saved to {model_filename}')

for column, encoder in label_encoders.items():
    encoder_filename = f'{column}_label_encoder.joblib'
    dump(encoder, encoder_filename)
    print(f'LabelEncoder for {column} saved to {encoder_filename}')
