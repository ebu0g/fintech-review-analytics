"""Preprocessing helpers for Google Play review data."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

import pandas as pd

REQUIRED_COLUMNS = ["review", "rating", "date", "bank", "source"]


def _first_present(row: pd.Series, candidates: Iterable[str]):
    for candidate in candidates:
        if candidate in row and pd.notna(row[candidate]):
            return row[candidate]
    return None


def normalize_review_record(record: dict, bank_name: str, source: str = "Google Play") -> dict:
    """Normalize a raw scraper record into the standard schema."""

    review_text = record.get("review") or record.get("content") or record.get("text")
    rating = record.get("rating") or record.get("score")
    raw_date = record.get("date") or record.get("at") or record.get("review_date")

    normalized_date = pd.to_datetime(raw_date, errors="coerce")
    date_value = normalized_date.strftime("%Y-%m-%d") if pd.notna(normalized_date) else None

    return {
        "review": review_text.strip() if isinstance(review_text, str) else review_text,
        "rating": rating,
        "date": date_value,
        "bank": bank_name,
        "source": source,
    }


def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize a review dataframe."""

    frame = df.copy()

    rename_map = {
        "content": "review",
        "text": "review",
        "score": "rating",
        "at": "date",
        "review_date": "date",
        "app": "bank",
    }
    frame = frame.rename(columns={column: rename_map[column] for column in frame.columns if column in rename_map})

    for column in REQUIRED_COLUMNS:
        if column not in frame.columns:
            frame[column] = pd.NA

    frame["review"] = frame["review"].astype("string").str.strip()
    frame["bank"] = frame["bank"].astype("string").str.strip()
    frame["source"] = frame["source"].fillna("Google Play").astype("string").str.strip()
    frame["rating"] = pd.to_numeric(frame["rating"], errors="coerce")
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    before_rows = len(frame)
    frame = frame.dropna(subset=["review", "rating"])
    frame = frame[frame["review"].str.len() > 0]
    frame = frame.drop_duplicates(subset=["review", "rating", "date", "bank"])
    frame = frame.sort_values(["bank", "date", "rating"], na_position="last").reset_index(drop=True)

    return frame[[column for column in REQUIRED_COLUMNS if column in frame.columns]]


def summarize_reviews(df: pd.DataFrame) -> dict:
    """Return lightweight data quality summary metrics."""

    total = len(df)
    missing_review = int(df["review"].isna().sum()) if "review" in df else total
    missing_rating = int(df["rating"].isna().sum()) if "rating" in df else total
    missing_any = missing_review + missing_rating
    return {
        "total_rows": total,
        "missing_review": missing_review,
        "missing_rating": missing_rating,
        "missing_any_rate": round((missing_any / total) * 100, 2) if total else 0.0,
    }
