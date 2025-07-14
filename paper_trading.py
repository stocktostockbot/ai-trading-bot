import json
import os
from datetime import datetime
from telegram_alerts import send_telegram_alert

DATA_FILE = "paper_trades.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"balance": 100000, "trades": []}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)

def record_trade(signal, price):
    data = load_data()
    trades = data["trades"]
    balance = data["balance"]
    now = datetime.now().strftime("%H:%M:%S")

    # Find open trade
    open_trade = None
    for t in reversed(trades):
        if "exit_price" not in t:
            open_trade = t
            break

    if open_trade:
        # Same direction → do nothing
        if open_trade["type"] == signal:
            return
        else:
            # Opposite direction → close current
            exit_price = price
            entry_price = open_trade["price"]
            qty = open_trade["qty"]
            pnl = (exit_price - entry_price) * qty if open_trade["type"] == "BUY" else (entry_price - exit_price) * qty

            open_trade["exit_price"] = exit_price
            open_trade["exit_datetime"] = str(datetime.now())
            open_trade["pnl"] = round(pnl, 2)
            data["balance"] += pnl

            send_telegram_alert(
                f"💼 Trade Closed\nType: {open_trade['type']}\nExit Price: {exit_price}\nQty: {qty}\nP&L: ₹{round(pnl, 2)}\nTime: {now}"
            )

    # New trade entry
    qty = int(balance // price)
    if qty == 0:
        send_telegram_alert("❌ Not enough balance to take a new position.")
        save_data(data)
        return

    new_trade = {
        "type": signal,
        "price": price,
        "qty": qty,
        "datetime": str(datetime.now())
    }
    trades.append(new_trade)
    send_telegram_alert(
        f"✅ New Trade Executed\nType: {signal}\nEntry Price: {price}\nQty: {qty}\nTime: {now}"
    )

    save_data(data)

def get_summary():
    data = load_data()
    trades = data["trades"]
    total_trades = len(trades)
    correct = 0
    wrong = 0

    for t in trades:
        if "pnl" in t:
            if t["pnl"] > 0:
                correct += 1
            elif t["pnl"] < 0:
                wrong += 1

    accuracy = (correct / (correct + wrong) * 100) if (correct + wrong) > 0 else 0

    return {
        "balance": round(data["balance"], 2),
        "total_trades": total_trades,
        "total_pnl": round(sum(t.get("pnl", 0) for t in trades), 2),
        "correct": correct,
        "wrong": wrong,
        "accuracy": round(accuracy, 2),
        "trades": trades
    }
