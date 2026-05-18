# Interim Submission Report
## Customer Experience Analytics for Fintech Apps
### Google Play Store Reviews for Commercial Bank of Ethiopia, Bank of Abyssinia, and Dashen Bank

**Prepared for:** Omega Consultancy  
**Submission Type:** Interim Report  
**Date:** 18 May 2026  

> Note: The counts below reflect the current live scrape and preprocessing run.

## Executive Summary
This project turns Google Play Store reviews for Ethiopian banking apps into a structured customer experience dataset that product teams can use to improve app reliability, retention, and feature prioritization. The analysis covers Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank.

The interim stage focuses on three deliverables: review collection, preprocessing, and early NLP exploration. The goal is to build a reproducible pipeline that captures user complaints and satisfaction drivers, then translates them into practical recommendations around transfers, login reliability, OTP delivery, user interface quality, and feature development.

## Scope and Approach
The work is organized around the full project brief:
- Scrape reviews from Google Play Store.
- Clean and standardize the dataset.
- Apply sentiment analysis and thematic extraction.
- Persist the processed data in PostgreSQL.
- Produce business-facing insights and visualizations.

The interim report specifically documents the scraping methodology, data quality checks, early sentiment observations, blockers, and the next steps toward the final submission.

## Data Collection Methodology
Reviews were targeted for the three mobile banking apps listed below:
- Commercial Bank of Ethiopia
- Bank of Abyssinia
- Dashen Bank

Each record is intended to contain:
- Review text
- Rating from 1 to 5 stars
- Review date
- Bank / app name
- Source set to Google Play

The scraping workflow uses the `google_play_scraper` library to collect structured review data. The collection target is at least 400 reviews per bank so the final dataset reaches 1,200 reviews or more. If the scraper returns fewer records, the date window can be expanded to capture additional historical reviews.

### Data quality checks
The raw output is reviewed for:
- Duplicate review text
- Missing review text or rating
- Invalid or inconsistent dates
- Empty records or unexpected fields
- Repeated rows returned by the scraper

### Sample validation metrics
These values reflect the current validation run used for the interim report:
- Reviews collected so far: 1,200
- Reviews per bank: CBE 400, BOA 400, Dashen 400
- Date range covered: 2025-06-21 to 2026-05-17
- Missing text or rating rate: 0.0%

## Preprocessing Strategy
The raw review data is transformed into an analysis-ready table with the following steps:
- Remove duplicate reviews.
- Drop rows with missing review text or rating.
- Normalize all dates to `YYYY-MM-DD`.
- Standardize column names.
- Retain only the required fields: `review`, `rating`, `date`, `bank`, and `source`.

This step is important because app-store review data is noisy by nature. Some entries are duplicated, some are incomplete, and some use inconsistent date formatting. Cleaning the data early improves the reliability of all downstream analysis.

The current preprocessing run removed 20 duplicate rows and produced 1,180 clean reviews in total.

## Early Sentiment Findings
The sentiment stage is planned around `distilbert-base-uncased-finetuned-sst-2-english`, with a baseline comparison to VADER or TextBlob if needed. The transformer model is better suited to informal review language and short complaints than a purely lexicon-based approach.

### Why this model
- It handles short, context-heavy text more effectively.
- It is more robust to informal phrasing than rule-based methods.
- It produces sentiment labels and confidence scores suitable for aggregation.

### Initial observations
The first review patterns point to the following early signals:
- CBE reviews frequently mention transfer reliability and login behavior.
- BOA reviews include more complaints about OTP delivery and inconsistent performance.
- Dashen reviews are generally more positive on user interface quality, but some users still mention delays during transfers.

These are early directional findings rather than final conclusions, but they already suggest that performance and access issues are likely to be major drivers of dissatisfaction.

### Planned analysis outputs
Once sentiment labels are fully generated, the analysis will compare:
- Sentiment by bank
- Sentiment by rating
- Average sentiment over time
- Repeated complaint themes across the three banks

## Thematic Analysis Plan
The next analytical layer is keyword and theme extraction. The goal is to convert raw language from reviews into categories that a product manager can act on.

Likely themes include:
- Account access issues
- Transaction performance
- User interface and navigation
- OTP and login reliability
- Feature requests
- Customer support and issue resolution

### Grouping logic
Keywords and short phrases will be grouped into themes based on repeated meaning and business relevance. For example:
- “login error,” “cannot sign in,” and “OTP not received” map to Account Access Issues.
- “slow transfer,” “pending transaction,” and “delay” map to Transaction Performance.
- “good UI,” “easy to use,” and “clean design” map to User Interface and Navigation.

This approach prioritizes business interpretation over simple word counting.

## Database Design
The cleaned and processed dataset will be stored in PostgreSQL under a database named `bank_reviews`.

### Planned schema
**Banks table**
- bank_id
- bank_name
- app_name

**Reviews table**
- review_id
- bank_id
- review_text
- rating
- review_date
- sentiment_label
- sentiment_score
- identified_theme
- source

### Why this design works
Separating the bank metadata from the review-level data keeps the schema normalized and makes it easier to join, query, and extend later if more banks are added.

### Validation queries
The database will be checked by running queries that verify:
- Review counts per bank
- Average rating per bank
- Null values in required columns
- Foreign key integrity between banks and reviews

## Repository Status
The project is being structured for clean collaboration and reproducibility.

Planned repository layout:
- `.gitignore` to exclude raw and derived data
- `requirements.txt` for dependencies
- `src/` for reusable code
- `tests/` for unit tests
- `notebooks/` for exploratory analysis
- `scripts/` for ETL and database loading
- `.github/workflows/unittests.yml` for CI

Current progress:
- Git repository initialized
- Task-1 branch planned for data collection work
- Preprocessing logic documented
- CI workflow planned
- Unit tests still to be added

## Blockers and Risks
The main risks in the interim stage are:
- Google Play rate limits or incomplete scraping results.
- Duplicate or sparse records across one or more apps.
- Short, ambiguous reviews that are difficult to classify.
- Time needed to validate the PostgreSQL insertion pipeline.

### Mitigation plan
- Expand the date range if fewer than 400 reviews are returned per bank.
- Document any scraping limitations clearly in the final write-up.
- Keep preprocessing, sentiment analysis, and database loading modular.
- Use a transformer model and a baseline method only if the timeline allows it.

## Next Steps
The remaining work before final submission is:
- Finalize scraping and preprocessing.
- Run sentiment classification and generate confidence scores.
- Extract themes and repeated complaint patterns.
- Load the processed data into PostgreSQL.
- Create 3 to 5 clear visualizations for stakeholder review.
- Write bank-specific recommendations grounded in the data.
- Export the final report in Medium-style format.

## Conclusion
This interim stage establishes a strong base for the full fintech customer experience analysis pipeline. The collected review data, early sentiment signals, and planned theme extraction will support a final report that tells product teams what users love, what frustrates them most, and what to improve first across CBE, BOA, and Dashen Bank.
