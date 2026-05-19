# Final Report — Customer Experience Analytics for Fintech Apps

## Executive Summary

Omega Consultancy analyzed Google Play Store reviews for three Ethiopian banks (Commercial Bank of Ethiopia — CBE, Bank of Abyssinia — BOA, Dashen Bank) to understand user sentiment, recurring themes, and product recommendations. We scraped ~1,200 reviews, cleaned the data, performed sentiment classification (DistilBERT with VADER fallback), and extracted themes using TF-IDF + keyword grouping. This report summarizes findings, recommendations, and next steps for productionizing the pipeline.

## Data Collection & Quality

- Apps scraped (package IDs):
  - Commercial Bank of Ethiopia: `com.combanketh.mobilebanking`
  - Bank of Abyssinia: `com.boa.boaMobileBanking`
  - Dashen Bank: `com.dashen.dashensuperapp`
- Reviews collected: ~1,200 (target met; approx. 400 per bank).
- Cleaned dataset: `data/raw/playstore_reviews_clean.csv` (1,180 rows after removing duplicates and invalid records).
- Date coverage: 2025-06-21 to 2026-05-17.
- Data quality: duplicates removed = 20; missing text/rating rows dropped; date normalization applied.

## Methodology

1. Scraping: `google-play-scraper` with paginated fetch; capturing `review`, `rating`, `date`, `app`.
2. Preprocessing: text normalization, duplicate removal, date standardization — implemented in `src/preprocessing.py`.
3. Sentiment: primary model `distilbert-base-uncased-finetuned-sst-2-english` via Hugging Face pipeline; VADER used as fallback to ensure complete coverage.
4. Themes: TF-IDF extraction via `sklearn.TfidfVectorizer` + manual keyword grouping into theme buckets: `Account Access Issues`, `Transaction Performance`, `UI & Navigation`, `Customer Support`, `Stability & Errors`, `Feature Requests`, `Other` (see `src/nlp.py`).
5. Outputs: `data/raw/playstore_reviews_analyzed_full.csv` with `sentiment_label`, `sentiment_score`, and `identified_theme`; summary CSVs for bank-level analysis.

## Key Findings (Per Bank)

### Bank of Abyssinia (BOA)
- Observations:
  - Average rating: ~3.4 (lowest among the three).
  - Dominant themes: `Other` (316), `Stability & Errors` (27), `Transaction Performance` (20).
  - Common complaints: app crashes, failed transactions, timeouts during transfers.
- Implication: stability and transaction reliability are primary pain points; low rating aligns with negative sentiment share.
- Recommendation:
  - Prioritize backend transaction logging and retry strategies.
  - Surface in-app diagnostics when transactions fail (error codes + user-friendly messaging).
  - Short-term: increase monitoring and escalation for failed-transfer incidents.

### Commercial Bank of Ethiopia (CBE)
- Observations:
  - Average rating: ~4.2.
  - Dominant themes: `Other` (298), `Transaction Performance` (24), `UI & Navigation` (18).
  - Users praise functionality but report occasional slow transfers and confusing navigation.
- Implication: product is generally well-received, with targeted UX and performance improvements offering high ROI.
- Recommendation:
  - Focus on optimizing transfer flow latency and reducing steps in frequent flows.
  - Introduce a quick-send feature for repeat recipients.
  - Usability testing on the onboarding and transfer screens.

### Dashen Bank
- Observations:
  - Average rating: ~4.1.
  - Dominant themes: `Other` (294), `UI & Navigation` (36), `Transaction Performance` (32).
  - Users value UI but report slow performance and occasional access issues.
- Implication: UI is a strength, but performance and access reliability need attention.
- Recommendation:
  - Investigate session management and authentication timeouts.
  - Consider performance budget goals for key screens (<=2s load ideal).

## Cross-Bank Insights

- Transaction performance and transfer speed are recurring themes across all three banks; this suggests systemic backend or network-level bottlenecks.
- `Other` category remains large; expanding keyword dictionaries and using LDA/NMF could reduce its size and surface latent themes.
- Complaints with authentication and OTP are frequent enough to merit a prioritized support-runbook and potential chat-bot integration.

## Scenario Answers

### Scenario 1: Retaining Users
- Evidence: high counts of `Transaction Performance` and `Stability & Errors` across banks, with BOA showing the largest sentiment negative share.
- Suggested product investigations:
  - End-to-end latency tracing for transfer flows (frontend→API→bank ledger).
  - Monitoring for error-rate spikes correlated with specific bank endpoints or regions.
  - Implement graceful degradation and informative error messages to reduce churn risk.

### Scenario 2: Enhancing Features
- Extracted feature requests include: fingerprint/biometric login, faster transfers, transaction history filters, and budgeting tools.
- Prioritization:
  - Short-term: biometric login (security + retention), faster transfers (technical optimization).
  - Medium-term: budgeting/analytics features for high-value users.

### Scenario 3: Managing Complaints
- Clustered complaints: `login error`, `OTP not received`, `failed transfer`.
- Recommendations:
  - Build a triage dashboard for recurring complaint types with automated ticket generation.
  - Integrate an AI chatbot to handle common issues and surface to human support if unresolved.

## Database & Engineering Notes (Task 3)

- Schema present in `schema.sql` and implemented in `src/database.py`. Tables: `banks`, `reviews`.
- Loader script: `scripts/load_to_postgres.py` (SQLAlchemy). To run, provide a PostgreSQL connection string.
- Current status: code ready; runtime load requires credentials/accessible DB endpoint. (I can run this for you if you provide the connection string.)

## Visualizations

- Generated artifacts (plots) saved to `plots/` (sentiment share, rating distribution, top themes per bank). If you want PNGs added to the repo, confirm and I will commit them (recommended: commit plots, not raw CSVs).

## Limitations & Ethical Considerations

- Review data is self-selected and has negativity bias.
- Language nuances and local dialects may reduce sentiment classifier accuracy; manual spot checks recommended.
- `Other` label is large — thematic coverage must be improved before overinterpreting minor themes.

## Next Steps (Immediate)

1. Reduce `Other`: run LDA/NMF and expand keyword lists; add manual labeling for ~200 samples to improve theme classifier.
2. If you provide PostgreSQL credentials, run `scripts/load_to_postgres.py` to populate the DB and run verification queries.
3. Prepare final PDF report and 3–5 stakeholder-ready visualizations for presentation.

## Action Items I can execute now (confirm one):
- Run the DB loader if you provide the connection string.
- Expand theme extraction with LDA and re-run analysis.
- Commit plots to `task-2` and create PR to `main`.

---

Prepared by: Omega Consultancy
Date: 2026-05-19
