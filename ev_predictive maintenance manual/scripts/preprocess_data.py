import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load data
data = pd.read_csv('data/battery_data.csv')

# Preprocessing steps
# For example: Drop missing values and standardize features
data.dropna(inplace=True)

# Feature engineering (e.g., create new features if needed)
# data['new_feature'] = ...

# Standardize features
features = ['voltage', 'current', 'temperature', 'state_of_charge']
X = data[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save preprocessed data
preprocessed_data = pd.DataFrame(X_scaled, columns=features)
preprocessed_data['target'] = data['target']  # Assuming target is a column in your data
preprocessed_data.to_csv('data/battery_data_preprocessed.csv', index=False)

# Save scaler
import joblib
joblib.dump(scaler, 'models/scaler.pkl')
