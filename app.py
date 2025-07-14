from flask import Flask, render_template
from ai_signals import generate_signal

app = Flask(__name__)

@app.route('/')
def index():
    signal = generate_signal()
    return render_template('index.html', signal=signal)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
