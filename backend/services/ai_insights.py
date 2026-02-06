import os


def generate_insight(metrics: dict) -> str:
    """
    Replace this with real LLM call.
    """

    if metrics["profit"] < 0:
        health = "The business is currently running at a loss."
    else:
        health = "The business is profitable."

    if metrics["current_ratio"] < 1:
        liquidity = "Liquidity risk detected."
    else:
        liquidity = "Healthy short‑term liquidity."

    return f"{health} {liquidity} Consider reducing expenses and improving cash flow."