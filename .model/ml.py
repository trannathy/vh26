import joblib
# import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
# from sklearn.metrics import classification_report


def train_model():
    # Preprocessing
    df = pd.read_csv('maternal_health_risk_dataset.csv')
    df.replace({'RiskLevel': {'low risk': 0, 'mid risk': 1, 'high risk': 2}}, inplace=True)

    # Model Training
    X = df.drop(columns='RiskLevel')
    y = df['RiskLevel']

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)

    joblib.dump(clf, 'maternal_health_model.pkl')
    print("Model saved.")

def predict_patient(age, systolic, diastolic, sugar, heartrate):
    clf = joblib.load('maternal_health_model.pkl')

    patient = pd.DataFrame([{
        'Age': age,
        'SystolicBP': systolic,
        'DiastolicBP': diastolic,
        'BS': sugar,
        'BodyTemp': 98.6,
        'HeartRate': heartrate
    }])

    prediction = clf.predict(patient)
    risk_names = {0: 'Low', 1: 'Medium', 2: 'High'}
    return risk_names[prediction[0]]