import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
    "enhanced"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ============================================================
# 2. SETTINGS
# ============================================================

SAMPLES_PER_CLASS = 800


# ============================================================
# 3. LOAD DATA
# ============================================================

print()
print("==============================================")
print("     ENHANCED HAND GESTURE MODEL TRAINING")
print("==============================================")
print()

dataframes = []


for filename in sorted(os.listdir(DATA_DIR)):

    if filename.endswith(".csv"):

        filepath = os.path.join(
            DATA_DIR,
            filename
        )

        gesture_name = filename.replace(
            ".csv",
            ""
        )

        print(
            f"Loading: {filename}"
        )

        df = pd.read_csv(
            filepath,
            header=None
        )

        # Remove completely empty rows
        df = df.dropna(
            how="all"
        )

        # Remove rows with missing values
        df = df.dropna()

        # Add gesture label if it isn't already present
        if df.shape[1] == 63:

            df["label"] = gesture_name

        elif df.shape[1] != 64:

            print(
                f"WARNING: {filename} has "
                f"{df.shape[1]} columns."
            )

        # Keep only the desired number of samples
        if len(df) > SAMPLES_PER_CLASS:

            df = df.sample(
                n=SAMPLES_PER_CLASS,
                random_state=42
            )

        print(
            f"  Using {len(df)} samples"
        )

        dataframes.append(df)


# ============================================================
# 4. COMBINE DATA
# ============================================================

data = pd.concat(
    dataframes,
    ignore_index=True
)


print()
print("----------------------------------------------")
print("DATASET INFORMATION")
print("----------------------------------------------")

print(
    f"Total samples: {len(data)}"
)

print(
    f"Total columns: {len(data.columns)}"
)


# ============================================================
# 5. FEATURES AND LABELS
# ============================================================

X = data.iloc[:, :-1].astype(float)

y = data.iloc[:, -1]


print()
print("----------------------------------------------")
print("GESTURE DISTRIBUTION")
print("----------------------------------------------")

print(
    y.value_counts()
)


# ============================================================
# 6. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print()
print("----------------------------------------------")
print("TRAIN / TEST SPLIT")
print("----------------------------------------------")

print(
    f"Training samples: {len(X_train)}"
)

print(
    f"Testing samples : {len(X_test)}"
)


# ============================================================
# 7. CREATE RANDOM FOREST
# ============================================================

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# 8. TRAIN
# ============================================================

print()
print("----------------------------------------------")
print("TRAINING MODEL")
print("----------------------------------------------")

model.fit(
    X_train,
    y_train
)

print(
    "Training completed!"
)


# ============================================================
# 9. PREDICT
# ============================================================

y_pred = model.predict(
    X_test
)


# ============================================================
# 10. ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print()
print("==============================================")
print(
    f"MODEL ACCURACY: {accuracy * 100:.2f}%"
)
print("==============================================")


# ============================================================
# 11. CLASSIFICATION REPORT
# ============================================================

print()
print("----------------------------------------------")
print("CLASSIFICATION REPORT")
print("----------------------------------------------")
print()

print(
    classification_report(
        y_test,
        y_pred
    )
)


# ============================================================
# 12. CONFUSION MATRIX
# ============================================================

labels = sorted(
    y.unique()
)

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print()
print("----------------------------------------------")
print("CONFUSION MATRIX")
print("----------------------------------------------")

print()
print("Labels:")
print(labels)

print()
print(cm)


# ============================================================
# 13. SAVE ENHANCED MODEL
# ============================================================

model_path = os.path.join(
    MODEL_DIR,
    "gesture_model_enhanced.pkl"
)

joblib.dump(
    model,
    model_path
)


print()
print("----------------------------------------------")
print("MODEL SAVED")
print("----------------------------------------------")

print(
    model_path
)

print()
print("Enhanced model training completed! 🎉")