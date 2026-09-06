from pathlib import Path
import csv


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
METADATA_PATH = DATA_DIR / "metadata.csv"

processed = 0


with METADATA_PATH.open("r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        filename = row["filename"]
        expected_label = row["label"]

        file_path = DATA_DIR / filename

        lines = file_path.read_text(encoding="utf-8").splitlines()

        if not lines:
            raise ValueError(f"Empty file: {filename}")

        first_line = lines[0].strip()

        # Защита от случайного удаления настоящего текста
        if first_line != expected_label:
            raise ValueError(
                f"Label mismatch in {filename}: "
                f"expected={expected_label}, "
                f"found={first_line!r}"
            )

        text_without_label = "\n".join(lines[1:]).lstrip()

        file_path.write_text(
            text_without_label,
            encoding="utf-8"
        )

        processed += 1


print(f"Removed labels from {processed} files")