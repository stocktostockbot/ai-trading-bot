import schedule
import time
from datetime import datetime
from config import *
from angel_api import AngelSession
from ai_signals import generate_signal
from telegram_alerts import send_telegram_alert

# Create Angel API session and login
angel = AngelSession(API_KEY, CLIENT_CODE, PASSWORD, TOTP_SECRET)
angel.login()


# Define main bot logic
def run_bot():
    now = datetime.now().strftime("%H:%M")
    if now >= "15:30":
        print("📴 Market closed. Stopping bot.")
        exit()

    print(f"⏰ Checking signal at {now}...")

    signal = generate_signal()
    if signal:
        send_telegram_alert(f"📈 Trade Signal: {signal}")
        if LIVE_TRADING:
            angel.place_order(signal)


# Run once immediately
run_bot()

# Schedule every 5 minutes
schedule.every(5).minutes.do(run_bot)

# Infinite loop
while True:
    schedule.run_pending()
    time.sleep(1)
