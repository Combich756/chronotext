from pathlib import Path
import csv
import re


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
METADATA_PATH = DATA_DIR / "metadata.csv"

LABEL_PATTERN = re.compile(r"_(1600|1700|1800|1900)\.txt$")

rows = []

VALID_LABELS = {"1600", "1700", "1800", "1900"}

for file_path in sorted(DATA_DIR.glob("*.txt")):
    match = LABEL_PATTERN.search(file_path.name)

    if match is not None:
        label = int(match.group(1))

    else:
        # Старый формат: label находится в первой строке файла
        with file_path.open("r", encoding="utf-8") as file:
            first_line = file.readline().strip()

        if first_line not in VALID_LABELS:
            print(
                f"[ERROR] Не удалось определить label: "
                f"{file_path.name}, first_line={first_line!r}"
            )
            continue

        label = int(first_line)

        print(
            f"[INFO] Label взят из первой строки: "
            f"{file_path.name} -> {label}"
        )

    rows.append({
        "filename": file_path.name,
        "label": label
    })


print(f"Created: {METADATA_PATH}")
print(f"Number of texts: {len(rows)}")