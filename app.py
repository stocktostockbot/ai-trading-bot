from flask import Flask, render_template, redirect, url_for, request, session
import os
from ai_signals import generate_signal
from paper_trading import get_summary
from flask import send_file

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
    summary = get_summary()
    return render_template('dashboard.html', signal=signal, summary=summary)



@app.route('/download')
def download_log():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return send_file("signals_log.csv", as_attachment=True)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
