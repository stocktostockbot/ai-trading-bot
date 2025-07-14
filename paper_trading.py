import json
import os
from datetime import datetime
from telegram_alerts import send_telegram_alert
from datetime import datetime


DATA_FILE = "paper_trades.json"
START_BALANCE = 100000  # ₹1 Lakh initial

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"balance": START_BALANCE, "trades": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def record_trade(signal, price):
    data = load_data()

    quantity = 15  # lot size, can be dynamic later
    pnl = 0

    if signal == "BUY":
        entry = {
            "type": "BUY",
            "price": price,
            "qty": quantity,
            "datetime": str(datetime.now())
        }
        data["trades"].append(entry)

    elif signal == "SELL":
        # Assume selling the last BUY
        for t in reversed(data["trades"]):
            if t["type"] == "BUY" and "exit_price" not in t:
                pnl = (price - t["price"]) * quantity
                t["exit_price"] = price
                t["exit_datetime"] = str(datetime.now())
                t["pnl"] = pnl
                data["balance"] += pnl
                break

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


def record_trade(signal, price):
    data = load_data()
    quantity = 15  # lot size
    pnl = 0
    now = datetime.now().strftime("%H:%M:%S")

    if signal == "BUY":
        entry = {
            "type": "BUY",
            "price": price,
            "qty": quantity,
            "datetime": str(datetime.now())
        }
        data["trades"].append(entry)
        send_telegram_alert(
            f"✅ Paper Trade Executed\nType: BUY\nQty: {quantity}\nPrice: {price}\nTime: {now}"
        )

    elif signal == "SELL":
        for t in reversed(data["trades"]):
            if t["type"] == "BUY" and "exit_price" not in t:
                pnl = (price - t["price"]) * quantity
                t["exit_price"] = price
                t["exit_datetime"] = str(datetime.now())
                t["pnl"] = pnl
                data["balance"] += pnl
                send_telegram_alert(
                    f"✅ Paper Trade Closed\nType: SELL\nQty: {quantity}\nSell Price: {price}\nP&L: ₹{round(pnl, 2)}\nTime: {now}"
                )
                break

    save_data(data)

