from src.preprocessing import clean_reviews

import pandas as pd


def test_clean_reviews_drops_missing_and_duplicates():
    raw = pd.DataFrame(
        [
            {"content": "Great app", "score": 5, "at": "2026-05-17", "bank": "CBE", "source": "Google Play"},
            {"content": "Great app", "score": 5, "at": "2026-05-17", "bank": "CBE", "source": "Google Play"},
            {"content": None, "score": 1, "at": "2026-05-16", "bank": "BOA", "source": "Google Play"},
            {"content": "Login issue", "score": None, "at": "2026-05-15", "bank": "Dashen", "source": "Google Play"},
        ]
    )

    cleaned = clean_reviews(raw)

    assert len(cleaned) == 1
    assert list(cleaned.columns) == ["review", "rating", "date", "bank", "source"]
    assert cleaned.iloc[0]["review"] == "Great app"
    assert cleaned.iloc[0]["date"] == "2026-05-17"


def test_clean_reviews_standardizes_dates():
    raw = pd.DataFrame(
        [
            {"content": "Okay", "score": 3, "at": "17 May 2026", "bank": "CBE", "source": "Google Play"},
        ]
    )

    cleaned = clean_reviews(raw)

    assert cleaned.iloc[0]["date"] == "2026-05-17"
