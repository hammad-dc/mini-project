import pandas as pd
import numpy as np
import time
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
import matplotlib.pyplot as plt
import os
from imblearn.over_sampling import SMOTE

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), "Blinkit_Master_Data.csv")
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

initial_count = len(df)
# --- 📍 FIX 1: DATA CLEANING (Put this immediately after loading) ---
# This removes "Noise" by dropping rows with missing values and extreme outliers
df = df.dropna(subset=['distance_km', 'delay_minutes', 'area', 'category'])
df = df[df['delay_minutes'] < 120]  # Remove impossible delays
df = df[df['distance_km'] < 30]    # Remove impossible distances

rows_removed = initial_count - len(df)

# --- 📍 DATA QUALITY REPORT ---
print("-" * 30)
print(f"Initial rows: {initial_count}")
print(f"Cleaned rows: {len(df)}")
print(f"Noise removed: {rows_removed} rows")
print("-" * 30)

# Target: is_late (Delay > 5 min)

delay_col = None
for c in ["delay_minutes", "actual_delivery_time", "delivery_time_minutes"]:
    if c in df.columns:
        delay_col = c
        break
if not delay_col:
    raise Exception("No delay column found.")
df["is_late"] = (df[delay_col] > 5).astype(int)

# Features
area_col = None
for c in ["area", "location", "city", "zone", "region", "delivery_area"]:
    if c in df.columns:
        area_col = c
        break
category_col = None
for c in ["category", "product_category", "item_category"]:
    if c in df.columns:
        category_col = c
        break
time_col = None
for c in ["order_time", "order_date", "delivery_date", "date"]:
    if c in df.columns:
        time_col = c
        break
distance_col = None
for c in ["distance_km", "distance", "delivery_distance"]:
    if c in df.columns:
        distance_col = c
        break
stock_col = None
for c in ["stock_received", "stock", "quantity"]:
    if c in df.columns:
        stock_col = c
        break

# Extract hour_of_day
if time_col:
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
    df["hour_of_day"] = df[time_col].dt.hour
else:
    df["hour_of_day"] = 0

# Grouping hours into slots helps the model see "Rush Hour" vs "Night"
def get_time_slot(hour):
    if 6 <= hour < 11: return 1  # Morning
    if 11 <= hour < 17: return 2 # Afternoon
    if 17 <= hour < 22: return 3 # Evening
    return 4                     # Night

df["time_slot"] = df["hour_of_day"].apply(get_time_slot)

# Prepare features
features = [area_col, category_col, "time_slot", distance_col, stock_col]
features = [f for f in features if f]
X = df[features].copy()

# --- REPLACE OLD ENCODING WITH THIS ---
# One-Hot Encoding: Creates separate 0/1 columns for each Area and Category
X = pd.get_dummies(X, columns=[area_col, category_col], drop_first=True)
# ------------------
# --- 📍 COLUMN VERIFICATION ---
print(f"Total features after encoding: {len(X.columns)}")
print("First 10 features:", list(X.columns)[:10])
print("-" * 30)

# Fill missing
y = df["is_late"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



# Model
clf = RandomForestClassifier(
    n_estimators=150, 
    max_depth=8,         # Prevents the model from "memorizing" noise
    min_samples_leaf=10,    # Ensures rules are based on at least 5 examples
    class_weight='balanced', # Automatically handles the 0 vs 1 imbalance
    random_state=42
)

print("🚀 Training the Intelligence Model... Please wait.")
# Simple manual progress bar for the console
for i in range(10):
    time.sleep(0.1) # Simulates work
    sys.stdout.write(f"\r[{'=' * i}{' ' * (10-i)}] {i*10}% Complete")
    sys.stdout.flush()
print("\n✅ Training Finished!\n")
# ----------------------------------
clf.fit(X_train, y_train)



# Custom threshold for late prediction
threshold = 0.5
y_proba = clf.predict_proba(X_test)[:,1]
y_pred_thresh = (y_proba > threshold).astype(int)

# Evaluation
print("Classification Report (threshold=0.4):")
print(classification_report(y_test, y_pred_thresh))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_thresh))

# Feature importance
importances = clf.feature_importances_
feat_names = X.columns
plt.figure(figsize=(8,4))
plt.barh(feat_names, importances, color="#2d9cdb")
plt.xlabel("Importance")
plt.title("Feature Importance for Late Delivery Prediction")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()

# Export model
joblib.dump(clf, "late_delivery_rf.joblib")
print("Model exported as late_delivery_rf.joblib")
