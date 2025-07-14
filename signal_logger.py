import csv
from datetime import datetime
import os

CSV_FILE = "signals_log.csv"

def log_signal(signal):
    if not signal:
        return

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Signal"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), signal])
