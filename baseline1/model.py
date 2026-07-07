from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# model.py лежит в project/model/
# texts лежит в project/texts/
BASE_DIR = Path(__file__).resolve().parents[1]
TEXTS_DIR = BASE_DIR / "data"


def load_texts_from_folder(folder_path):
    texts = []
    labels = []

    for file_path in folder_path.glob("*.txt"):
        raw_text = file_path.read_text(encoding="utf-8").strip()

        if not raw_text:
            continue

        lines = raw_text.splitlines()

        if len(lines) < 2:
            continue

        date = lines[0].strip()
        text = "\n".join(lines[1:]).strip()

        if not text:
            continue

        labels.append(date)
        texts.append(text)

    return texts, labels


train_texts, train_y = load_texts_from_folder(TEXTS_DIR)




X_train_texts, X_test_texts, y_train, y_test = train_test_split(
    train_texts,
    train_y,
    test_size=0.2,
    random_state=42,
    stratify=train_y
)

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=1
)

X_train = vectorizer.fit_transform(X_train_texts)
X_test = vectorizer.transform(X_test_texts)

clf = LogisticRegression(max_iter=1000)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(classification_report(y_test, y_pred))
