import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

df = pd.read_csv(
    "../data/processed/cleaned_quality_data.csv"
)

features = [
    "Production_Line",
    "Component_Type",
    "Temperature",
    "Humidity",
    "Voltage",
    "Current",
    "Machine_Age",
    "Inspection_Score",
    "Shift",
    "Downtime"
]

X = df[features]
y = df["Defect"]

categorical_features = [
    "Production_Line",
    "Component_Type",
    "Shift"
]

numerical_features = [
    "Temperature",
    "Humidity",
    "Voltage",
    "Current",
    "Machine_Age",
    "Inspection_Score",
    "Downtime"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            SimpleImputer(strategy="median"),
            numerical_features
        ),
        (
            "categorical",
            Pipeline([
                (
                    "imputer",
                    SimpleImputer(
                        strategy="most_frequent"
                    )
                ),
                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    )
                )
            ]),
            categorical_features
        )
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Logistic Regression

logistic_model = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "model",
        LogisticRegression(
            max_iter=1000
        )
    )
])

logistic_model.fit(
    X_train,
    y_train
)

logistic_pred = logistic_model.predict(X_test)

logistic_probability = (
    logistic_model.predict_proba(X_test)[:, 1]
)


# Random Forest

random_forest_model = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "model",
        RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced"
        )
    )
])

random_forest_model.fit(
    X_train,
    y_train
)

rf_pred = random_forest_model.predict(X_test)

rf_probability = (
    random_forest_model.predict_proba(X_test)[:, 1]
)


def evaluate_model(
    model_name,
    y_true,
    predictions,
    probabilities
):

    print("\n====================================")
    print(model_name)
    print("====================================")

    print(
        "Accuracy:",
        round(
            accuracy_score(
                y_true,
                predictions
            ),
            4
        )
    )

    print(
        "Precision:",
        round(
            precision_score(
                y_true,
                predictions,
                zero_division=0
            ),
            4
        )
    )

    print(
        "Recall:",
        round(
            recall_score(
                y_true,
                predictions,
                zero_division=0
            ),
            4
        )
    )

    print(
        "F1 Score:",
        round(
            f1_score(
                y_true,
                predictions,
                zero_division=0
            ),
            4
        )
    )

    print(
        "ROC-AUC:",
        round(
            roc_auc_score(
                y_true,
                probabilities
            ),
            4
        )
    )

    print("\nClassification Report:")

    print(
        classification_report(
            y_true,
            predictions,
            zero_division=0
        )
    )


evaluate_model(
    "Logistic Regression",
    y_test,
    logistic_pred,
    logistic_probability
)

evaluate_model(
    "Random Forest",
    y_test,
    rf_pred,
    rf_probability
)


# Confusion matrix

cm = confusion_matrix(
    y_test,
    rf_pred
)

plt.figure(figsize=(7, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=[
        "Non-Defective",
        "Defective"
    ],
    yticklabels=[
        "Non-Defective",
        "Defective"
    ]
)

plt.title(
    "Random Forest Confusion Matrix"
)

plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(
    "../images/confusion_matrix.png",
    dpi=300
)

plt.show()


# Save predictions

prediction_results = X_test.copy()

prediction_results["Actual_Defect"] = y_test.values

prediction_results["Predicted_Defect"] = rf_pred

prediction_results["Defect_Probability"] = rf_probability

prediction_results.to_csv(
    "../data/processed/prediction_results.csv",
    index=False
)

print(
    "Prediction results saved successfully."
)
