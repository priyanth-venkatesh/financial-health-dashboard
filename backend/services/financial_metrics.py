def compute_metrics(data: dict):
    profit = data["revenue"] - data["expenses"]

    current_ratio = data["cash"] / data["debt"] if data["debt"] else 0

    return {
        "profit": profit,
        "current_ratio": current_ratio,
        "revenue": data["revenue"],
        "expenses": data["expenses"],
    }