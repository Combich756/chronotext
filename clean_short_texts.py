from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
DATA_DIR = BASE_DIR / "data"

START_GUTENBERG = "*** START OF THE PROJECT GUTENBERG EBOOK"
END_GUTENBERG = "*** END OF THE PROJECT GUTENBERG EBOOK"


BOOKS = [
    {
        "input": "mary_barton.txt",
        "output": "mary_barton_1800.txt",
        "start": "CHAPTER I.",
        "occurrence": 1,
    },
    {
        "input": "barchester_towers.txt",
        "output": "barchester_towers_1800.txt",
        "start": "CHAPTER I",
        "occurrence": 1,
    },
    {
        "input": "the_last_chronicle_of_barset.txt",
        "output": "the_last_chronicle_of_barset_1800.txt",
        "start": "CHAPTER I.",
        "occurrence": 1,
    },
    {
        "input": "the_phoenix_and_the_carpet.txt",
        "output": "the_phoenix_and_the_carpet_1900.txt",
        "start": "CHAPTER 1. THE EGG",
        "occurrence": 1,
    },
    {
        "input": "the_small_house_at_allington.txt",
        "output": "the_small_house_at_allington_1800.txt",
        "start": "CHAPTER I.",
        "occurrence": 1,
    },
    {
        "input": "this_side_of_paradise.txt",
        "output": "this_side_of_paradise_1900.txt",
        "start": "CHAPTER 1. Amory, Son of Beatrice",
        "occurrence": 2,
    },
]


def find_nth(text, marker, occurrence, start_pos=0):
    """
    Возвращает позицию occurrence-го вхождения marker в text,
    начиная поиск с start_pos.

    Например occurrence=2 означает:
    найти второе вхождение marker.
    """

    position = start_pos

    for _ in range(occurrence):
        position = text.find(marker, position)

        if position == -1:
            return -1

        position += len(marker)

    return position - len(marker)


def clean_book(book):
    raw_path = RAW_DIR / book["input"]
    output_path = DATA_DIR / book["output"]

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Raw file not found: {raw_path}"
        )

    text = raw_path.read_text(encoding="utf-8")

    gutenberg_start = text.find(START_GUTENBERG)

    if gutenberg_start == -1:
        raise ValueError(
            f"Gutenberg start marker not found: "
            f"{book['input']}"
        )

    start = find_nth(
        text=text,
        marker=book["start"],
        occurrence=book["occurrence"],
        start_pos=gutenberg_start,
    )

    if start == -1:
        raise ValueError(
            f"Could not find occurrence "
            f"{book['occurrence']} of marker "
            f"{book['start']!r} "
            f"in {book['input']}"
        )

    end = text.find(
        END_GUTENBERG,
        start
    )

    if end == -1:
        raise ValueError(
            f"Gutenberg end marker not found: "
            f"{book['input']}"
        )

    if start >= end:
        raise ValueError(
            f"Invalid boundaries: {book['input']}"
        )

    clean_text = text[start:end].strip()

    if len(clean_text) < 10_000:
        raise ValueError(
            f"Cleaned text is suspiciously short: "
            f"{book['input']} -> "
            f"{len(clean_text)} chars"
        )

    output_path.write_text(
        clean_text,
        encoding="utf-8"
    )

    print(
        f"{book['input']}: "
        f"{len(text):,} -> "
        f"{len(clean_text):,} chars"
    )


for book in BOOKS:
    clean_book(book)