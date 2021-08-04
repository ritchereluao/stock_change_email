import requests
import smtplib
from email.message import EmailMessage
from email.header import Header
from email.utils import formataddr

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = ""

stock_watchlist = ["AAPL", "GOOGL", "JPM", "TSLA", "JNJ", "KO", "AMZN", "FB"]
ticker_changes = []

for each_ticker in stock_watchlist:
    try:
        stock_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": each_ticker,
            "apikey": STOCK_API_KEY,
        }
        stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
        stock_response.raise_for_status()
        data = stock_response.json()["Time Series (Daily)"]
        data_to_list = [value for key, value in data.items()]

        closing_price_latest = float(data_to_list[0]["4. close"])
        closing_price_prev = float(data_to_list[1]["4. close"])
        percent_diff = round(((closing_price_prev - closing_price_latest) / closing_price_latest) * 100, 4)

        up_down_emoji = None
        if percent_diff > 0:
            up_down_emoji = "🔺+"
        else:
            up_down_emoji = "🔻"

        ticker_changes.append(f"{up_down_emoji}{percent_diff}")

    except KeyError:
        pass

data_in_dict = dict(zip(stock_watchlist, ticker_changes))
print(data_in_dict)

MY_EMAIL = "@gmail.com"
MY_PASSWORD = ""

msg = EmailMessage()
msg["Subject"] = "Stock Updates"
msg["From"] = formataddr((str(Header(" ", "utf-8")), MY_EMAIL))
msg["To"] = "@yahoo.com"
msg.set_content(f"{data_in_dict}")

with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.send_message(msg)

    # connection.sendmail(
    #     from_addr=MY_EMAIL,
    #     to_addrs="@yahoo.com",
    #     msg=f"Subject:Stock Updates!\n\n{ticker_changes}"
    # )
