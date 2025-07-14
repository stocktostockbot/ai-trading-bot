from flask import Flask, render_template
from ai_signals import generate_signal
from telegram_alerts import send_telegram_alert
import datetime

app = Flask(__name__)
signal_history = []

@app.route('/')
def index():
    signal = generate_signal()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Send Telegram alert
    telegram_status = "✅ Sent"
    try:
        send_telegram_alert(f"📈 AI Web Signal: {signal}")
    except Exception as e:
        telegram_status = f"❌ Failed ({e})"

    # Store signal history
    signal_history.append({
        "signal": signal,
        "time": now,
        "status": telegram_status
    })

    # Limit history to last 5
    if len(signal_history) > 5:
        signal_history.pop(0)

    return render_template("index.html", signal=signal, now=now, history=signal_history[::-1], telegram_status=telegram_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
