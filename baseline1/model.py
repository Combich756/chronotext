from pathlib import Path
import csv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from collections import Counter
from sklearn.metrics import classification_report, confusion_matrix


BASE_DIR = Path(__file__).resolve().parents[1]
TEXTS_DIR = BASE_DIR / "data"
METADATA_PATH = TEXTS_DIR / "metadata.csv"


def load_dataset(data_dir, metadata_path):
    texts = []
    labels = []

    with metadata_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            filename = row["filename"]
            label = int(row["label"])

            file_path = data_dir / filename

            if not file_path.exists():
                raise FileNotFoundError(
                    f"File from metadata not found: {filename}"
                )

            text = file_path.read_text(encoding="utf-8").strip()

            if not text:
                raise ValueError(
                    f"Empty text file: {filename}"
                )

            texts.append(text)
            labels.append(label)

    return texts, labels


train_texts, train_y = load_dataset(
    TEXTS_DIR,
    METADATA_PATH
)

print("Class distribution:", Counter(train_y))


X_train_texts, X_test_texts, y_train, y_test = train_test_split(
    train_texts,
    train_y,
    test_size=0.2,
    random_state=42,
    stratify=train_y
)

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 1),
    min_df=2,
    max_features=50_000
)

X_train = vectorizer.fit_transform(X_train_texts)
X_test = vectorizer.transform(X_test_texts)

clf = LogisticRegression(max_iter=1000)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("Confusion matrix:")
print(confusion_matrix(
    y_test,
    y_pred,
    labels=[1600, 1700, 1800, 1900]
))

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)
