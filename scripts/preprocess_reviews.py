"""Preprocess raw review CSV files into the final analysis-ready dataset."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing import clean_reviews, summarize_reviews


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean Google Play review data")
    parser.add_argument("--input", default="data/raw/playstore_reviews_raw.csv", help="Input CSV path")
    parser.add_argument("--output", default="data/raw/playstore_reviews_clean.csv", help="Output CSV path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    raw_df = pd.read_csv(input_path)
    cleaned_df = clean_reviews(raw_df)
    cleaned_df.to_csv(output_path, index=False)

    summary = summarize_reviews(cleaned_df)
    print(f"Saved {len(cleaned_df)} cleaned reviews to {output_path}")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
