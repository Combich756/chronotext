from pathlib import Path
import csv


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
METADATA_PATH = DATA_DIR / "metadata.csv"

ok_count = 0
error_count = 0


with METADATA_PATH.open("r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        filename = row["filename"]
        expected_label = row["label"]

        file_path = DATA_DIR / filename

        if not file_path.exists():
            print(f"[ERROR] Missing file: {filename}")
            error_count += 1
            continue

        with file_path.open("r", encoding="utf-8") as text_file:
            first_line = text_file.readline().strip()

        if first_line != expected_label:
            print(
                f"[ERROR] {filename}: "
                f"metadata={expected_label}, "
                f"first_line={first_line!r}"
            )
            error_count += 1
        else:
            ok_count += 1


print(f"Correct files: {ok_count}")
print(f"Problems: {error_count}")