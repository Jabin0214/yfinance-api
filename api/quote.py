import yfinance as yf
import json

def handler(event, context):
    params = event.get("queryStringParameters") or {}
    symbol = params.get("symbol", "")

    if not symbol:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing symbol"})
        }

    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")

        if hist.empty:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"No data found for symbol {symbol}"})
            }

        value = round(float(hist["Close"].iloc[-1]), 2)
        return {
            "statusCode": 200,
            "body": json.dumps({"symbol": symbol, "value": value}),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }