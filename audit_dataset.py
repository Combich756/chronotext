from pathlib import Path
import csv
import hashlib
from collections import Counter, defaultdict


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
METADATA_PATH = DATA_DIR / "metadata.csv"

MIN_CHARS = 1000

errors = []
warnings = []

labels = []
seen_files = set()
hash_to_files = defaultdict(list)


with METADATA_PATH.open("r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        filename = row["filename"]
        label = row["label"]

        labels.append(label)

        # Повторяющийся filename в metadata
        if filename in seen_files:
            errors.append(f"Duplicate metadata entry: {filename}")

        seen_files.add(filename)

        file_path = DATA_DIR / filename

        # Файл существует?
        if not file_path.exists():
            errors.append(f"Missing file: {filename}")
            continue

        text = file_path.read_text(encoding="utf-8").strip()

        # Файл пустой?
        if not text:
            errors.append(f"Empty file: {filename}")
            continue

        # Подозрительно короткий текст
        if len(text) < MIN_CHARS:
            warnings.append(
                f"Short text: {filename} ({len(text)} chars)"
            )

        # Не остался ли старый label первой строкой
        first_line = text.splitlines()[0].strip()

        if first_line in {"1600", "1700", "1800", "1900"}:
            errors.append(
                f"Possible leaked label in {filename}: {first_line}"
            )

        # Хэш для поиска полных дубликатов
        text_hash = hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

        hash_to_files[text_hash].append(filename)


# Все txt-файлы на диске
all_txt_files = {
    path.name
    for path in DATA_DIR.glob("*.txt")
}


# Файлы существуют, но отсутствуют в metadata
extra_files = all_txt_files - seen_files

for filename in sorted(extra_files):
    errors.append(
        f"File not present in metadata: {filename}"
    )


# Полностью одинаковые тексты
for files in hash_to_files.values():
    if len(files) > 1:
        errors.append(
            f"Duplicate texts: {files}"
        )


print("=== Dataset summary ===")
print(f"Metadata rows: {len(labels)}")
print(f"Text files: {len(all_txt_files)}")
print(f"Class distribution: {Counter(labels)}")

print()

print("=== Errors ===")
if errors:
    for error in errors:
        print("[ERROR]", error)
else:
    print("No errors")

print()

print("=== Warnings ===")
if warnings:
    for warning in warnings:
        print("[WARNING]", warning)
else:
    print("No warnings")

print()

print(f"Errors: {len(errors)}")
print(f"Warnings: {len(warnings)}")