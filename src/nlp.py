"""Sentiment and thematic analysis helpers for review text."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer

try:
    from transformers import pipeline
except Exception:  # pragma: no cover - optional dependency handling
    pipeline = None

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except Exception:  # pragma: no cover - optional dependency handling
    SentimentIntensityAnalyzer = None

THEME_KEYWORDS = {
    "Account Access Issues": {
        "login",
        "log in",
        "sign in",
        "otp",
        "password",
        "pin",
        "verify",
        "authentication",
        "access",
    },
    "Transaction Performance": {
        "transfer",
        "slow",
        "delay",
        "pending",
        "failed",
        "stuck",
        "processing",
        "transaction",
    },
    "UI & Navigation": {
        "ui",
        "interface",
        "design",
        "easy",
        "menu",
        "navigate",
        "user friendly",
        "layout",
    },
    "Customer Support": {
        "support",
        "help",
        "service",
        "contact",
        "response",
        "call",
    },
    "Feature Requests": {
        "fingerprint",
        "budget",
        "dark mode",
        "statement",
        "history",
        "notification",
        "biometric",
        "loan",
    },
    "Stability & Errors": {
        "crash",
        "error",
        "bug",
        "freeze",
        "hang",
        "not working",
        "close",
        "loading",
    },
}

TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z']+")


def tokenize_text(text: str) -> list[str]:
    """Tokenize text using a simple regex-based strategy."""

    if not isinstance(text, str):
        return []
    return TOKEN_PATTERN.findall(text.lower())


def remove_stop_words(tokens: Iterable[str]) -> list[str]:
    """Remove stop words using scikit-learn's built-in English stop word list."""

    return [token for token in tokens if token not in ENGLISH_STOP_WORDS]


def lemmatize_tokens(tokens: Iterable[str]) -> list[str]:
    """Optional light lemmatization using NLTK when available."""

    try:
        from nltk.stem import WordNetLemmatizer
    except Exception:  # pragma: no cover - optional dependency handling
        return list(tokens)

    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def prepare_text(text: str, use_lemmatization: bool = False) -> str:
    """Normalize text before TF-IDF and theme extraction."""

    tokens = tokenize_text(text)
    tokens = remove_stop_words(tokens)
    if use_lemmatization:
        tokens = lemmatize_tokens(tokens)
    return " ".join(tokens)


@lru_cache(maxsize=1)
def _load_transformer_pipeline():
    if pipeline is None:
        raise ImportError("transformers is not available in this environment")
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


@lru_cache(maxsize=1)
def _load_vader():
    if SentimentIntensityAnalyzer is None:
        raise ImportError("vaderSentiment is not available in this environment")
    return SentimentIntensityAnalyzer()


def classify_sentiment(text: str, threshold: float = 0.15) -> dict:
    """Return a sentiment label and signed confidence score.

    The preferred path uses the DistilBERT SST-2 model. If that is not
    available, the function falls back to VADER.
    """

    normalized_text = text.strip() if isinstance(text, str) else ""
    if not normalized_text:
        return {"sentiment_label": "neutral", "sentiment_score": 0.0, "sentiment_source": "empty"}

    try:
        predictor = _load_transformer_pipeline()
        result = predictor(normalized_text[:512])[0]
        label = result["label"].lower()
        confidence = float(result["score"])
        signed_score = (confidence * 2) - 1 if label == "positive" else 1 - (confidence * 2)
        if abs(signed_score) < threshold:
            return {"sentiment_label": "neutral", "sentiment_score": round(signed_score, 4), "sentiment_source": "distilbert"}
        return {
            "sentiment_label": "positive" if signed_score > 0 else "negative",
            "sentiment_score": round(signed_score, 4),
            "sentiment_source": "distilbert",
        }
    except Exception:
        analyzer = _load_vader()
        compound = float(analyzer.polarity_scores(normalized_text)["compound"])
        if compound >= threshold:
            label = "positive"
        elif compound <= -threshold:
            label = "negative"
        else:
            label = "neutral"
        return {"sentiment_label": label, "sentiment_score": round(compound, 4), "sentiment_source": "vader"}


def identify_theme(text: str) -> str:
    """Assign a business theme to a review based on keyword matches."""

    normalized = text.lower() if isinstance(text, str) else ""
    for theme, keywords in THEME_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return theme
    return "Other"


def analyze_reviews(df: pd.DataFrame, use_lemmatization: bool = False) -> pd.DataFrame:
    """Run sentiment and theme analysis for a cleaned review dataframe."""

    frame = df.copy()
    if frame.empty:
        return frame.assign(
            review_id=pd.Series(dtype="int64"),
            review_text=pd.Series(dtype="string"),
            sentiment_label=pd.Series(dtype="string"),
            sentiment_score=pd.Series(dtype="float64"),
            identified_theme=pd.Series(dtype="string"),
        )

    if "review" not in frame.columns:
        raise KeyError("Expected a review column in the cleaned dataframe")

    frame = frame.reset_index(drop=True)
    frame["review_id"] = frame.index + 1
    frame["review_text"] = frame["review"].astype(str)
    frame["processed_text"] = frame["review_text"].apply(lambda value: prepare_text(value, use_lemmatization=use_lemmatization))

    sentiments = frame["review_text"].apply(classify_sentiment)
    frame["sentiment_label"] = sentiments.apply(lambda item: item["sentiment_label"])
    frame["sentiment_score"] = sentiments.apply(lambda item: item["sentiment_score"])
    frame["sentiment_source"] = sentiments.apply(lambda item: item["sentiment_source"])
    frame["identified_theme"] = frame["review_text"].apply(identify_theme)

    return frame


def aggregate_sentiment_by_bank(frame: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sentiment scores by bank."""

    return (
        frame.groupby("bank", dropna=False)
        .agg(
            review_count=("review_id", "count"),
            mean_sentiment=("sentiment_score", "mean"),
            positive_share=("sentiment_label", lambda values: (values == "positive").mean()),
            negative_share=("sentiment_label", lambda values: (values == "negative").mean()),
            neutral_share=("sentiment_label", lambda values: (values == "neutral").mean()),
        )
        .reset_index()
        .sort_values("bank")
    )


def aggregate_sentiment_by_rating(frame: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sentiment scores by star rating."""

    return (
        frame.groupby("rating", dropna=False)
        .agg(
            review_count=("review_id", "count"),
            mean_sentiment=("sentiment_score", "mean"),
        )
        .reset_index()
        .sort_values("rating")
    )


def extract_theme_keywords(frame: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Extract TF-IDF n-grams to support the thematic analysis."""

    if frame.empty:
        return pd.DataFrame(columns=["term", "score"])

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
    matrix = vectorizer.fit_transform(frame["processed_text"].fillna(""))
    scores = matrix.mean(axis=0).A1
    terms = vectorizer.get_feature_names_out()
    ranking = (
        pd.DataFrame({"term": terms, "score": scores})
        .sort_values("score", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return ranking
