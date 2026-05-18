import pandas as pd

from src.nlp import aggregate_sentiment_by_bank, identify_theme, tokenize_text


def test_tokenize_text_extracts_words():
    tokens = tokenize_text("Love the UI, but it crashes often!")
    assert tokens == ["love", "the", "ui", "but", "it", "crashes", "often"]


def test_identify_theme_maps_login_issue():
    assert identify_theme("Login error and OTP not received") == "Account Access Issues"


def test_aggregate_sentiment_by_bank_returns_summary():
    frame = pd.DataFrame(
        [
            {"review_id": 1, "bank": "CBE", "sentiment_label": "positive", "sentiment_score": 0.9, "rating": 5},
            {"review_id": 2, "bank": "CBE", "sentiment_label": "negative", "sentiment_score": -0.7, "rating": 1},
        ]
    )
    summary = aggregate_sentiment_by_bank(frame)
    assert list(summary["bank"]) == ["CBE"]
    assert summary.iloc[0]["review_count"] == 2
