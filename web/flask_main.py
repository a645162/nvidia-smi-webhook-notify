from flask import Flask, render_template
from flask_socketio import SocketIO

import subprocess
import html
import time

import threading

from config import config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
async_mode = 'threading'
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    # return redirect('/nvidiasmi')
    return render_template('index.html')


@app.route('/nvidiasmi')
def nvidiasmi():
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        output = result.stdout.strip()
        escaped_output = html.escape(output)
        formatted_output = f'<pre>{escaped_output}</pre>'
        return formatted_output
    except Exception as e:
        return str(e), 500


@app.route('/nvitop')
def nvitop1():
    try:
        result = subprocess.run(
            ['nvitop', '-1'],
            capture_output=True, text=True
        )
        output = result.stdout.strip()
        escaped_output = html.escape(output)
        formatted_output = f'<pre>{escaped_output}</pre>'
        # print(formatted_output)
        return formatted_output
    except Exception as e:
        return str(e), 500


running = False


def run_nvitop():
    while running:
        try:
            process = subprocess.Popen(
                ['nvitop', '-1'],
                stdout=subprocess.PIPE, universal_newlines=True
            )

            output = process.stdout.read().strip()
            socketio.emit('nvitop_output', {'output': output})
        except Exception as e:
            socketio.emit('nvitop_output', {'output': str(e)})

        time.sleep(1)


@app.route('/nvitop')
def nvitop():
    return render_template('nvitop.html')


@socketio.on('connect')
def handle_connect():
    global running
    if not running:
        running = True
        print('Client connected.')
        threading.Thread(target=run_nvitop).start()


@socketio.on('disconnect')
def handle_disconnect():
    global running
    print('Client disconnected.')
    running = False


def start_web_server():
    app.run(host=config.web_server_host, port=config.web_server_port)


if __name__ == '__main__':
    start_web_server()
