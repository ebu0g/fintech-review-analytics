"""Load cleaned review data into PostgreSQL."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.banks import BANK_SPECS
from src.database import create_schema, get_engine, load_banks, load_reviews, verify_database


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load reviews into PostgreSQL")
    parser.add_argument("--input", default="data/raw/playstore_reviews_clean.csv", help="Clean CSV input path")
    parser.add_argument("--database-url", required=True, help="PostgreSQL SQLAlchemy connection string")
    parser.add_argument("--schema", default="schema.sql", help="Path to the SQL schema file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Clean CSV not found: {input_path}")
        return 1

    engine = get_engine(args.database_url)
    create_schema(engine, args.schema)

    review_frame = pd.read_csv(input_path)
    bank_frame = pd.DataFrame(BANK_SPECS)[["bank_name", "app_name"]].reset_index().rename(columns={"index": "bank_id"})
    bank_frame["bank_id"] = bank_frame["bank_id"] + 1
    load_banks(engine, bank_frame.to_dict(orient="records"))

    if "bank" not in review_frame.columns:
        print("The cleaned CSV must include a bank column so it can be linked to the banks table.")
        return 1

    review_frame = review_frame.merge(bank_frame[["bank_id", "bank_name"]], left_on="bank", right_on="bank_name", how="left")
    review_frame = review_frame.rename(columns={"review": "review_text", "date": "review_date"})
    review_frame["source"] = review_frame.get("source", "Google Play")

    for column in ["sentiment_label", "sentiment_score", "identified_theme"]:
        if column not in review_frame.columns:
            review_frame[column] = pd.NA

    review_frame = review_frame[[
        "bank_id",
        "review_text",
        "rating",
        "review_date",
        "sentiment_label",
        "sentiment_score",
        "identified_theme",
        "source",
    ]]

    load_reviews(engine, review_frame)
    verification = verify_database(engine)
    print(verification.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
