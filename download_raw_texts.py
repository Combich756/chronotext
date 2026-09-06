from pathlib import Path
from urllib.request import urlopen


BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


BOOKS = {
    "barchester_towers.txt": 3409,
    "mary_barton.txt": 2153,
    "the_last_chronicle_of_barset.txt": 3045,
    "the_phoenix_and_the_carpet.txt": 836,
    "the_small_house_at_allington.txt": 4599,
    "this_side_of_paradise.txt": 805,
    "little_dorrit.txt": 963,
    "dombey_and_son.txt": 821,
    "the_warden.txt": 619,
    "greenmantle.txt": 559,
}


for filename, ebook_id in BOOKS.items():
    url = (
        f"https://www.gutenberg.org/cache/epub/"
        f"{ebook_id}/pg{ebook_id}.txt"
    )

    print(f"Downloading {filename}...")

    with urlopen(url) as response:
        text = response.read().decode("utf-8-sig")

    output_path = RAW_DIR / filename
    output_path.write_text(text, encoding="utf-8")

    print(
        f"Saved {filename}: "
        f"{len(text):,} characters"
    )