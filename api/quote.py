import yfinance as yf
import json

def handler(request):
    symbol = request.args.get('symbol', '')
    if not symbol:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'symbol' parameter"})
        }

    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d")
    if hist.empty:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": f"No data found for symbol {symbol}"})
        }

    latest_value = hist["Close"].iloc[-1]
    return {
        "statusCode": 200,
        "body": json.dumps({
            "symbol": symbol,
            "value": round(float(latest_value), 2)
        }),
        "headers": {
            "Content-Type": "application/json"
        }
    }