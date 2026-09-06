from pathlib import Path
import csv
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_validate,
)
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)


BASE_DIR = Path(__file__).resolve().parents[1]

TEXTS_DIR = BASE_DIR / "data"
METADATA_PATH = TEXTS_DIR / "metadata.csv"

REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

LABELS = [1600, 1700, 1800, 1900]


def load_dataset(data_dir, metadata_path):
    texts = []
    labels = []

    with metadata_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            filename = row["filename"]
            label = int(row["label"])

            file_path = data_dir / filename

            if not file_path.exists():
                raise FileNotFoundError(
                    f"File from metadata not found: {filename}"
                )

            text = file_path.read_text(
                encoding="utf-8"
            ).strip()

            if not text:
                raise ValueError(
                    f"Empty text file: {filename}"
                )

            texts.append(text)
            labels.append(label)

    return texts, labels


def create_pipeline():
    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 1),
                min_df=2,
                max_features=50_000,
                dtype=np.float32,
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
            ),
        ),
    ])


texts, labels = load_dataset(
    TEXTS_DIR,
    METADATA_PATH,
)

print("=== Dataset ===")
print(f"Texts: {len(texts)}")
print(f"Class distribution: {Counter(labels)}")
print()


# =========================================================
# 1. FIXED TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels,
)

model = create_pipeline()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)


print("=== Fixed train/test split ===")
print(f"Train size: {len(X_train)}")
print(f"Test size: {len(X_test)}")
print()

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0,
    )
)


# =========================================================
# CONFUSION MATRIX
# =========================================================

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=LABELS,
)

print("Confusion matrix:")
print(cm)
print()


disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=LABELS,
)

fig, ax = plt.subplots(figsize=(7, 6))

disp.plot(
    ax=ax,
    values_format="d",
)

ax.set_title(
    "ChronoText Baseline Confusion Matrix"
)

fig.tight_layout()

confusion_matrix_path = (
    REPORTS_DIR / "confusion_matrix.png"
)

fig.savefig(
    confusion_matrix_path,
    dpi=200,
    bbox_inches="tight",
)

plt.close(fig)

print(
    f"Confusion matrix saved to: "
    f"{confusion_matrix_path}"
)
print()


# =========================================================
# 2. 5-FOLD CROSS-VALIDATION
# =========================================================

print("=== 5-fold cross-validation ===")

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)

cv_model = create_pipeline()

scores = cross_validate(
    estimator=cv_model,
    X=texts,
    y=labels,
    cv=cv,
    scoring={
        "accuracy": "accuracy",
        "macro_f1": "f1_macro",
        "weighted_f1": "f1_weighted",
    },
    n_jobs=1,
)


accuracy_scores = scores["test_accuracy"]
macro_f1_scores = scores["test_macro_f1"]
weighted_f1_scores = scores["test_weighted_f1"]


print("Accuracy per fold:")
print(accuracy_scores)

print("Macro F1 per fold:")
print(macro_f1_scores)

print("Weighted F1 per fold:")
print(weighted_f1_scores)

print()


print(
    "Accuracy: "
    f"{accuracy_scores.mean():.3f} "
    f"± {accuracy_scores.std():.3f}"
)

print(
    "Macro F1: "
    f"{macro_f1_scores.mean():.3f} "
    f"± {macro_f1_scores.std():.3f}"
)

print(
    "Weighted F1: "
    f"{weighted_f1_scores.mean():.3f} "
    f"± {weighted_f1_scores.std():.3f}"
)
