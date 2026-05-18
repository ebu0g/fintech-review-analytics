CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name TEXT NOT NULL UNIQUE,
    app_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id BIGSERIAL PRIMARY KEY,
    bank_id INTEGER NOT NULL REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_date DATE NOT NULL,
    sentiment_label TEXT,
    sentiment_score NUMERIC(5, 4),
    identified_theme TEXT,
    source TEXT NOT NULL DEFAULT 'Google Play'
);

CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_review_date ON reviews(review_date);
