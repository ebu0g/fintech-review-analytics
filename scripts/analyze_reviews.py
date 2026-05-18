"""Run sentiment and thematic analysis on the cleaned review dataset."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.nlp import aggregate_sentiment_by_bank, aggregate_sentiment_by_rating, analyze_reviews, extract_theme_keywords


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze cleaned review data")
    parser.add_argument("--input", default="data/raw/playstore_reviews_clean.csv", help="Clean CSV input path")
    parser.add_argument("--output", default="data/raw/playstore_reviews_analyzed.csv", help="Output CSV with analysis results")
    parser.add_argument("--summary-output", default="data/raw/sentiment_summary_by_bank.csv", help="Bank-level summary CSV")
    parser.add_argument("--rating-output", default="data/raw/sentiment_summary_by_rating.csv", help="Rating-level summary CSV")
    parser.add_argument("--themes-output", default="data/raw/top_theme_keywords.csv", help="Top TF-IDF keywords CSV")
    parser.add_argument("--lemmatize", action="store_true", help="Apply optional NLTK lemmatization")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    cleaned_df = pd.read_csv(input_path)
    analyzed_df = analyze_reviews(cleaned_df, use_lemmatization=args.lemmatize)
    analyzed_df[["review_id", "review_text", "sentiment_label", "sentiment_score", "identified_theme"]].to_csv(args.output, index=False)

    bank_summary = aggregate_sentiment_by_bank(analyzed_df)
    rating_summary = aggregate_sentiment_by_rating(analyzed_df)
    theme_keywords = extract_theme_keywords(analyzed_df)

    bank_summary.to_csv(args.summary_output, index=False)
    rating_summary.to_csv(args.rating_output, index=False)
    theme_keywords.to_csv(args.themes_output, index=False)

    print(f"Saved analyzed reviews to {args.output}")
    print(f"Saved bank summary to {args.summary_output}")
    print(f"Saved rating summary to {args.rating_output}")
    print(f"Saved theme keywords to {args.themes_output}")
    print(bank_summary.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
