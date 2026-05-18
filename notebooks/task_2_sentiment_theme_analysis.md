# Task 2: Sentiment and Thematic Analysis

## Objective

Classify review sentiment and identify recurring themes that explain what users praise and what frustrates them across the three bank apps.

## Method Choice

The analysis pipeline prefers the DistilBERT SST-2 transformer model because it is strong on short review text and better captures context than a simple lexicon approach. If the transformer stack is unavailable in the execution environment, the code falls back to VADER so the pipeline still runs end-to-end.

## Theme Grouping Logic

Themes are assigned using repeated business-relevant keyword patterns:

- Account Access Issues
- Transaction Performance
- UI & Navigation
- Customer Support
- Feature Requests
- Stability & Errors

These themes are broad enough to compare banks consistently while still mapping to concrete product issues.

## Output Files

- `data/raw/playstore_reviews_analyzed.csv`
- `data/raw/sentiment_summary_by_bank.csv`
- `data/raw/sentiment_summary_by_rating.csv`
- `data/raw/top_theme_keywords.csv`
