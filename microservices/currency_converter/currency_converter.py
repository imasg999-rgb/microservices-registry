import os
import sys
import logging

import requests

EXCHANGE_API_URL = os.getenv(
    "EXCHANGE_API_URL",
    "https://api.apilayer.com/exchangerates_data/convert",
)
# API requests are limited for me so need to kepe that into consideration
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


class CurrencyConversionError(Exception):
    pass


class CurrencyProviderError(CurrencyConversionError):
    pass


def convert_currency(from_currency: str, to_currency: str, amount: float) -> dict:
    if not EXCHANGE_API_KEY:
        raise ValueError("Currency provider is not configured (missing API key).")

    if amount < 0:
        raise ValueError("Amount must be non-negative.")
    headers = {"apikey": EXCHANGE_API_KEY}

    params = {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount,
    }

    resp = requests.get(
        EXCHANGE_API_URL,
        headers=headers,
        params=params,
        timeout=5,
    )

    if resp.status_code != 200:
        logger.error(
            "Currency provider HTTP error: %s - body: %s",
            resp.status_code,
            resp.text,
        )
        raise CurrencyProviderError("Currency provider HTTP error.")

    data = resp.json()

    if not data.get("success", False):
        error_obj = data.get("error")
        provider_message = None
        if isinstance(error_obj, dict):
            provider_message = error_obj.get("info") or error_obj.get("type")

        logger.error("Currency provider returned error: %s", error_obj)
        raise CurrencyProviderError(
            provider_message or "Conversion failed at provider."
        )

    result = data.get("result")
    info = data.get("info", {}) or {}
    rate = info.get("rate")

    if result is None:
        logger.error("Provider returned no 'result' field: %s", data)
        raise CurrencyProviderError("Provider returned no result.")

    if rate is None and amount:
        rate = result / amount
    return {
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "amount": amount,
        "converted_amount": result,
        "rate": rate,
    }
