# Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report


# Preprocessing
df = pd.read_csv('maternal_health_risk_dataset.csv')
df.replace({'RiskLevel': {'low risk': 0, 'mid risk': 1, 'high risk': 2}}, inplace=True)

# Model Training
X = df.drop(columns='RiskLevel')
y = df['RiskLevel']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

# Model Evaluation
print(classification_report(y_test, y_pred, target_names=['low risk', 'mid risk', 'high risk']))

skf = StratifiedKFold(n_splits=5)
scores = cross_val_score(clf, X, y, cv=skf)
print("CV scores:", scores)
print("Mean:", scores.mean(), "Std:", scores.std())

# See Feature Weighting
importances = pd.Series(clf.feature_importances_, index=X.columns)
importances.sort_values().plot(kind='barh')
plt.title('Feature Importances')
plt.xlabel('Importance')
plt.tight_layout()
plt.show()

# Predict w/ an actual patient
# print(X.columns.tolist())

patient = pd.DataFrame([{
    'Age': 25,
    'SystolicBP': 120,
    'DiastolicBP': 80,
    'BS': 6.5,
    'BodyTemp': 98.6,
    'HeartRate': 76
}])

# prediction = clf.predict(patient)
# risk_names = {0: 'low risk', 1: 'mid risk', 2: 'high risk'}
# print("Predicted risk level:", risk_names[prediction[0]])

import pickle

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)

# Load the model
with open("model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

# Make predictions with the loaded model
print(loaded_model.predict(patient))