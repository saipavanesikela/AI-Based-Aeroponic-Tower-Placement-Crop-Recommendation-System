import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, f1_score
import joblib

# Load dataset
df = pd.read_csv("aeroponic_crop_placement_dataset.csv")

# Encode crop_type
le = LabelEncoder()
df["crop_type"] = le.fit_transform(df["crop_type"])

# Features and target
X = df.drop("yield_score", axis=1)
y = df["yield_score"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation (percentage format)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

print(f"Model Accuracy: {accuracy * 100:.2f}%")
print(f"Weighted F1-Score: {f1 * 100:.2f}%")

# ⬇⬇⬇ THIS LINE FIXES THE WARNING ⬇⬇⬇
print(
    "\nClassification Report:\n",
    classification_report(y_test, y_pred, zero_division=0)
)

# Save model
joblib.dump(model, "placement_model.pkl")
joblib.dump(le, "crop_encoder.pkl")

print("Model and encoder saved successfully")
