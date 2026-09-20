import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load destination-aware dataset
data = pd.read_csv("backend/destination_dataset.csv")

# Features
X = data[
    [
        "destination",
        "annual_visitors",
        "day",
        "weather",
        "holiday",
        "festival"
    ]
]

# Target
y = data["crowd"]

# Categorical features
categorical_columns = [
    "destination",
    "day",
    "weather",
    "holiday",
    "festival"
]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        )
    ],
    remainder="passthrough"
)

# Random Forest model
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=100,
                random_state=42
            )
        )
    ]
)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train
model.fit(X_train, y_train)

# Test accuracy
accuracy = model.score(X_test, y_test)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "backend/crowd_model.pkl")

print("Final destination-aware model trained and saved successfully!")