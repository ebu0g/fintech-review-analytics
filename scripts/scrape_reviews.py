"""Scrape Google Play Store reviews for the configured bank apps."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scraper import DEFAULT_BANKS, scrape_all_banks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape bank app reviews from Google Play Store")
    parser.add_argument("--output", default="data/raw/playstore_reviews_raw.csv", help="Path to save raw scraped reviews")
    parser.add_argument("--target-count", type=int, default=400, help="Target review count per bank")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    reviews_df = scrape_all_banks(DEFAULT_BANKS, target_count=args.target_count)
    if reviews_df.empty:
        print("No reviews were collected. Check the Google Play app IDs in src/banks.py.")
        return 1

    reviews_df.to_csv(output_path, index=False)
    print(f"Saved {len(reviews_df)} scraped reviews to {output_path}")
    print(reviews_df.groupby("bank").size().to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
