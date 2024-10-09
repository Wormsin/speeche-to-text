from flask import Flask, request, jsonify
import subprocess
import threading

app = Flask(__name__)
recording_process = None


@app.route('/start', methods=['POST'])
def start():
    global recording_process
    if recording_process is None:
        # Запускаем скрипт записи в отдельном процессе
        recording_process = subprocess.Popen(['python', 'audio.py', "start"])
        return jsonify({"status": "recording started"})
    return jsonify({"status": "already recording"})

@app.route('/stop', methods=['POST'])
def stop():
    global recording_process
    if recording_process is not None:
        # Создаем файл-сигнал, чтобы остановить запись
        with open("stop_signal.txt", "w") as f:
            f.write("stop")
        recording_process = None
        return jsonify({"status": "recording stopped"})
    return jsonify({"status": "not recording"})

@app.route('/get_json', methods=['GET'])
def get_json():
    subprocess.Popen(['python', 'log2json.py'])
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
