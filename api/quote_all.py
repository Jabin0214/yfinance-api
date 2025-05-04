import yfinance as yf
import json

indices = [
    {"symbol": "^GSPC", "name": "S&P 500", "market": "USA"},
    {"symbol": "^IXIC", "name": "Nasdaq", "market": "USA"},
    {"symbol": "^DJI", "name": "Dow Jones", "market": "USA"},
    {"symbol": "^HSI", "name": "Hang Seng", "market": "Hong Kong"},
    {"symbol": "NI225.T", "name": "Nikkei 225", "market": "Japan"},
    {"symbol": "AXJO.AX", "name": "ASX 200", "market": "Australia"},
    {"symbol": "^NZ50", "name": "NZX 50", "market": "New Zealand"}
]

def handler(event, context):
    result = []
    for index in indices:
        try:
            ticker = yf.Ticker(index["symbol"])
            hist = ticker.history(period="1d")
            value = round(float(hist["Close"].iloc[-1]), 2) if not hist.empty else None
            result.append({
                "symbol": index["symbol"],
                "name": index["name"],
                "market": index["market"],
                "value": value
            })
        except Exception as e:
            result.append({
                "symbol": index["symbol"],
                "name": index["name"],
                "market": index["market"],
                "value": None,
                "error": str(e)
            })

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }