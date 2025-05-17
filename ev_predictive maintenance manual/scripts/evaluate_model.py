import pandas as pd
from sklearn.metrics import classification_report
import joblib

# Load preprocessed data and model
data = pd.read_csv('data/battery_data_preprocessed.csv')
X = data.drop('target', axis=1)
y = data['target']
model = joblib.load('models/battery_health_model.pkl')

# Predict and evaluate
y_pred = model.predict(X)
report = classification_report(y, y_pred)
print(report)
