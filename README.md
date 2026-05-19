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

## Task 2 Methodology

Task 2 extends the cleaned review data with sentiment labels and recurring themes.

### Sentiment approach

The analysis uses the DistilBERT SST-2 model as the primary classifier. The code converts the transformer output into a signed sentiment score and labels each review as positive, negative, or neutral. If the transformer stack is unavailable in the environment, the pipeline falls back to VADER so the workflow still runs end-to-end.

### Thematic approach

Thematic analysis uses keyword rules and TF-IDF n-grams to surface recurring complaint patterns and feature requests. The main theme buckets are:

- Account Access Issues
- Transaction Performance
- UI & Navigation
- Customer Support
- Feature Requests
- Stability & Errors

### Output files

- `data/raw/playstore_reviews_analyzed.csv`
- `data/raw/sentiment_summary_by_bank.csv`
- `data/raw/sentiment_summary_by_rating.csv`
- `data/raw/top_theme_keywords.csv`

## Scraping Notes

The scraper uses the following official Google Play package IDs:

- Commercial Bank of Ethiopia: `com.combanketh.mobilebanking`
- Bank of Abyssinia: `com.boa.boaMobileBanking`
- Dashen Bank: `com.dashen.dashensuperapp`

If Google Play returns fewer than 400 reviews per bank, expand the date range and rerun the extraction.

## Task 1 Results

Current validated scrape results:

- Raw reviews collected: 1,200
- Reviews per bank: CBE 400, BOA 400, Dashen 400
- Clean reviews after preprocessing: 1,180
- Duplicate rows removed: 20
- Missing review text or rating rate in raw data: 0.0%
- Date range covered: 2025-06-21 to 2026-05-17

The final clean CSV contains only the required columns: `review`, `rating`, `date`, `bank`, and `source`.

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
- The final cleaned CSV should include only `review`, `rating`, `date`, `bank`, and `source`.
