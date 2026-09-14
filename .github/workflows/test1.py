import time
import requests
import yfinance as yf
import os

# 從 GitHub Secrets 取得 Telegram Token 和 Chat ID
token = os.environ["TELEGRAM_TOKEN"]
chat_id = os.environ["CHAT_ID"]

# 設定要查詢的股票
stocks = ["1101.TW", "2330.TW"]

# 依序取得股價並發送 Telegram 訊息
for stock_id in stocks:
    try:
        # 使用 yfinance 抓取資料
        ticker = yf.Ticker(stock_id)
        todays_data = ticker.history(period="1d")

        if not todays_data.empty:
            price = todays_data["Close"].iloc[-1]
            message = f"股票 {stock_id} 即時股價為 {price:.2f}"
        else:
            message = f"股票 {stock_id} 目前無法取得資料"

    except Exception as e:
        message = f"股票 {stock_id} 查詢發生錯誤：{e}"

    # 發送到 Telegram
    telegram_url = f"https://api.telegram.org/bot{token}/sendMessage"

    requests.get(
        telegram_url,
        params={
            "chat_id": chat_id,
            "text": message
        }
    )

    time.sleep(2)
