from flask import Flask, render_template, request, redirect, session
from ai_signals import generate_signal
from telegram_alerts import send_telegram_alert
import datetime

app = Flask(__name__)
app.secret_key = "your-secret-key"  # change this to something secure

# login credentials
USERNAME = "admin"
PASSWORD = "tradingbot123"from flask import Flask, render_template, redirect, url_for, request, session
import os
from ai_signals import generate_signal

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecret")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == os.getenv("DASHBOARD_PASSWORD", "1234"):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid password")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    signal = generate_signal()
    return render_template('dashboard.html', signal=signal)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)


signal_history = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect('/')

    signal = generate_signal()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        send_telegram_alert(f"📈 AI Web Signal: {signal}")
        telegram_status = "✅ Sent"
    except Exception as e:
        telegram_status = f"❌ Failed ({e})"

    signal_history.append({
        "signal": signal,
        "time": now,
        "status": telegram_status
    })

    if len(signal_history) > 5:
        signal_history.pop(0)

    return render_template("index.html", signal=signal, now=now, history=signal_history[::-1], telegram_status=telegram_status)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')
