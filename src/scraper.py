"""Google Play scraping helpers for bank app reviews."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from .banks import BANK_SPECS
from .preprocessing import normalize_review_record

try:
    from google_play_scraper import Sort, reviews as gp_reviews
except Exception:  # pragma: no cover - import handled at runtime
    Sort = None
    gp_reviews = None


@dataclass
class BankApp:
    bank_name: str
    app_name: str
    app_id: str


DEFAULT_BANKS = [BankApp(**spec) for spec in BANK_SPECS]


def scrape_bank_reviews(bank: BankApp, target_count: int = 400, lang: str = "en", country: str = "et") -> pd.DataFrame:
    """Scrape reviews for a single bank app."""

    if not bank.app_id or bank.app_id.startswith("REPLACE_WITH"):
        raise ValueError(f"Missing Google Play app_id for {bank.bank_name}. Update src/banks.py before scraping.")
    if gp_reviews is None:
        raise ImportError("google_play_scraper is not installed. Install requirements first.")

    collected: list[dict] = []
    token = None

    while len(collected) < target_count:
        batch_size = min(200, target_count - len(collected))
        batch, token = gp_reviews(
            bank.app_id,
            lang=lang,
            country=country,
            sort=Sort.NEWEST if Sort is not None else 0,
            count=batch_size,
            continuation_token=token,
        )

        if not batch:
            break

        for item in batch:
            collected.append(normalize_review_record(item, bank.bank_name))

        if token is None:
            break

    frame = pd.DataFrame(collected)
    if not frame.empty:
        frame["app_name"] = bank.app_name
        frame["bank"] = bank.bank_name
    return frame


def scrape_all_banks(banks: Iterable[BankApp] = DEFAULT_BANKS, target_count: int = 400) -> pd.DataFrame:
    """Scrape all configured banks and combine results."""

    frames = []
    for bank in banks:
        frame = scrape_bank_reviews(bank, target_count=target_count)
        if not frame.empty:
            frames.append(frame)

    if not frames:
        return pd.DataFrame(columns=["review", "rating", "date", "bank", "source", "app_name"])

    return pd.concat(frames, ignore_index=True)
