from config import *
from angel_api import AngelSession
from ai_signals import generate_signal
from telegram_alerts import send_telegram_alert
import schedule
import time
from paper_trading import record_trade


angel = AngelSession(API_KEY, CLIENT_CODE, PASSWORD, TOTP_SECRET)
angel.login()

def run_bot():
    signal = generate_signal()
    if signal:
        send_telegram_alert(f"📈 Trade Signal: {signal}")
        if LIVE_TRADING:
            angel.place_order(signal)

# Run every 1 minute
schedule.every(1).minutes.do(run_bot)

if __name__ == "__main__":
    print("🔁 AI Trading Bot is running on schedule...")
    while True:
        schedule.run_pending()
        time.sleep(5)

def run_bot():
    signal = generate_signal()
    if signal:
        send_telegram_alert(f"📈 Trade Signal: {signal}")
        if LIVE_TRADING:
            angel.place_order(signal)
        else:
            price = angel.get_ltp("NSE:NIFTY")  # or BANKNIFTY
            record_trade(signal, price)
