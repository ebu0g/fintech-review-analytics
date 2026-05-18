"""Database helpers for PostgreSQL persistence."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

try:
    from sqlalchemy import create_engine, text
except Exception:  # pragma: no cover - optional dependency handling
    create_engine = None
    text = None


@dataclass
class DatabaseConfig:
    url: str


def get_engine(database_url: str):
    if create_engine is None:
        raise ImportError("sqlalchemy is required for PostgreSQL loading. Install the project dependencies first.")
    return create_engine(database_url)


def create_schema(engine, schema_path: str | Path = "schema.sql") -> None:
    schema_file = Path(schema_path)
    if not schema_file.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_file}")
    sql_text = schema_file.read_text(encoding="utf-8")
    with engine.begin() as connection:
        for statement in [part.strip() for part in sql_text.split(";") if part.strip()]:
            connection.exec_driver_sql(f"{statement};")


def load_banks(engine, banks: Iterable[dict]) -> None:
    bank_frame = pd.DataFrame(list(banks))
    if bank_frame.empty:
        return
    bank_frame.to_sql("banks", engine, if_exists="append", index=False)


def load_reviews(engine, reviews: pd.DataFrame) -> None:
    if reviews.empty:
        return
    reviews.to_sql("reviews", engine, if_exists="append", index=False)


def verify_database(engine) -> pd.DataFrame:
    query = text(
        """
        SELECT
            b.bank_name,
            COUNT(r.review_id) AS review_count,
            AVG(r.rating) AS average_rating
        FROM banks b
        LEFT JOIN reviews r ON r.bank_id = b.bank_id
        GROUP BY b.bank_name
        ORDER BY b.bank_name;
        """
    )
    with engine.begin() as connection:
        result = connection.execute(query)
        return pd.DataFrame(result.fetchall(), columns=result.keys())
