# fintech-review-analytics

Customer Experience Analytics for Fintech Apps is a data engineering and NLP project that scrapes Google Play Store reviews for three Ethiopian banks, cleans the data, analyzes sentiment and themes, and stores the processed results in PostgreSQL.

## Project Scope

Banks in scope:
- Commercial Bank of Ethiopia
- Bank of Abyssinia
- Dashen Bank

Target dataset fields:
- review
- rating
- date
- bank
- source

## Repository Structure

- `.github/workflows/unittests.yml` - CI workflow
- `scripts/` - command-line entry points for scraping and preprocessing
- `src/` - reusable pipeline code
- `tests/` - unit tests
- `notebooks/` - analysis notebooks
- `data/raw/` - local raw outputs, ignored by Git

## Task 1 Methodology

1. Scrape reviews from Google Play Store using `google_play_scraper`.
2. Normalize each record to the fields required for analysis.
3. Remove duplicate rows.
4. Drop rows with missing review text or rating.
5. Standardize dates to `YYYY-MM-DD`.
6. Save a clean CSV containing only the required columns.

## Scraping Notes

The scraper is designed to accept bank metadata from a config object or CLI arguments. If Google Play returns fewer than 400 reviews per bank, expand the date range and rerun the extraction.

## Data Quality Rules

- Drop duplicate reviews.
- Drop rows missing review text or rating.
- Keep `source` fixed as `Google Play`.
- Preserve bank metadata for later aggregation.

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Scrape reviews:

```bash
python scripts/scrape_reviews.py --output data/raw/playstore_reviews_raw.csv
```

Preprocess reviews:

```bash
python scripts/preprocess_reviews.py --input data/raw/playstore_reviews_raw.csv --output data/raw/playstore_reviews_clean.csv
```

## Notes and Limitations

- App IDs for the bank apps may need to be confirmed from Google Play before scraping.
- Rate limits or unavailable review history may reduce the number of reviews collected.
- The final report should document the exact date range and scrape counts used.
