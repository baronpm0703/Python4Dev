import numpy as np
import pandas as pd
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
    VotingClassifier,
)
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier


RANDOM_STATE = 50
TARGET_COLUMN = "target"
N_NEIGHBORS = 10
N_ESTIMATORS = 50


def parse_number(value):
    """Convert CSV values like '50.166.465...' back to numeric floats."""
    if not isinstance(value, str):
        return value

    value = value.strip()
    if value.count(".") <= 1:
        return float(value)

    sign = -1 if value.startswith("-") else 1
    digits = value.lstrip("-").replace(".", "")
    return sign * float(f"0.{digits}")


def clean_dataframe(df):
    df = df.copy()
    for column in df.columns:
        df[column] = df[column].map(parse_number)
    return df


def split_features_target(df):
    return df.drop(columns=TARGET_COLUMN), df[TARGET_COLUMN].astype(int)


def prediction_confidence(model, sample):
    probabilities = model.predict_proba(sample)[0]
    prediction = int(np.argmax(probabilities))
    confidence = float(np.max(probabilities))
    return prediction, confidence


def label_prediction(prediction):
    return "Heart Disease" if prediction == 1 else "No Heart Disease"


def minmax_to_minus_one_one(value, min_value, max_value):
    return 2 * ((value - min_value) / (max_value - min_value)) - 1


def patient_from_webapp_input(values, columns):
    """Map raw UI values from WebApp.png to the encoded feature scale in CSV."""
    encoded = {
        "age": minmax_to_minus_one_one(values["age"], 29, 77),
        "trestbps": minmax_to_minus_one_one(values["trestbps"], 94, 200),
        "chol": minmax_to_minus_one_one(values["chol"], 126, 564),
        "thalach": minmax_to_minus_one_one(values["thalach"], 71, 202),
        "oldpeak": minmax_to_minus_one_one(values["oldpeak"], 0, 6.2),
        "sex": values["sex"],
        "cp": (values["cp"] - 1) / 3,
        "fbs": values["fbs"],
        "restecg": values["restecg"] / 2,
        "exang": values["exang"],
        "slope": (values["slope"] - 1) / 2,
        "ca": values["ca"] / 3,
        "thal": {3: 0, 6: 0.5, 7: 1}[values["thal"]],
    }
    return pd.DataFrame([encoded], columns=columns)


def build_models():
    models = {
        "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE),
        "K-NN": KNeighborsClassifier(n_neighbors=N_NEIGHBORS),
        "Naive Bayes": GaussianNB(),
        "Random Forest": RandomForestClassifier(
            n_estimators=N_ESTIMATORS,
            random_state=RANDOM_STATE,
        ),
        "AdaBoost": AdaBoostClassifier(random_state=RANDOM_STATE),
        "Gradient Boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
        "XGBoost": XGBClassifier(
            n_estimators=N_ESTIMATORS,
            eval_metric="logloss",
            random_state=RANDOM_STATE,
        ),
    }

    models["Ensemble (Soft Voting)"] = VotingClassifier(
        estimators=[(name, model) for name, model in models.items()],
        voting="soft",
    )
    return models


def main():
    # Load data
    df_raw_train = pd.read_csv('data/raw_train.csv')
    df_raw_test = pd.read_csv('data/raw_test.csv')
    df_raw_val = pd.read_csv('data/raw_val.csv')

    # Clean data
    df_raw_train = clean_dataframe(df_raw_train)
    df_raw_test = clean_dataframe(df_raw_test)
    df_raw_val = clean_dataframe(df_raw_val)

    # Splitting axis
    x_train, y_train = split_features_target(df_raw_train)
    x_val, y_val = split_features_target(df_raw_val)
    x_test, y_test = split_features_target(df_raw_test)

    models = build_models()
    new_patient = patient_from_webapp_input(
        {
            "age": 107,
            "sex": 1,
            "cp": 2,
            "trestbps": 130,
            "chol": 250,
            "fbs": 0,
            "restecg": 1,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 1,
            "slope": 1,
            "ca": 0,
            "thal": 3,
        },
        x_train.columns,
    )

    results = []

    for model_name, model in models.items():
        model.fit(x_train, y_train)

        val_predictions = model.predict(x_val)
        test_predictions = model.predict(x_test)
        patient_prediction, patient_confidence = prediction_confidence(
            model,
            new_patient,
        )

        results.append(
            {
                "model": model_name,
                "val_accuracy": accuracy_score(y_val, val_predictions),
                "test_accuracy": accuracy_score(y_test, test_predictions),
                "patient_prediction": label_prediction(patient_prediction),
                "patient_confidence": patient_confidence,
            }
        )

    results_df = pd.DataFrame(results).sort_values(
        by=["val_accuracy", "patient_confidence"],
        ascending=False,
    )

    print("Model Predictions Overview")
    print(results_df.to_string(index=False, formatters={
        "val_accuracy": "{:.2%}".format,
        "test_accuracy": "{:.2%}".format,
        "patient_confidence": "{:.2%}".format,
    }))


if __name__ == "__main__":
    main()
