from flask import Flask, send_from_directory, request, jsonify
import csv
import webbrowser
import os
from datetime import datetime

app = Flask(__name__, static_folder='front')
MESSAGE_QUEUE_FILE = 'front/data/message.csv'


@app.route('/')
def serve_index():
    return send_from_directory('front', 'index.html')


@app.route('/<path:filename>')
def serve_static_file(filename):
    return send_from_directory('front', filename)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"Attempting login for user: {data.get('username')}")
    return jsonify({"status": "success", "message": "Login successful"})


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message_record = {
        "timestamp": datetime.now().isoformat(),
        "source": data.get("source"),
        "target": data.get("target"),
        "type": data.get("type"),
        "content": data.get("message"),
        "message_type": data.get("message_type"),
    }

    # 写入消息队列
    write_message_to_csv(message_record)

    # 模拟将消息发送到服务器
    print(f"Simulated message send to server: {message_record}")

    # 返回成功响应，通知前端刷新
    return jsonify({"status": "success"})


def write_message_to_csv(message):
    """将消息写入到 message.csv 文件"""
    file_exists = os.path.isfile(MESSAGE_QUEUE_FILE)
    with open(MESSAGE_QUEUE_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["timestamp", "source", "target", "type", "content", "message_type"]
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL
        )
        if not file_exists:
            writer.writeheader()  # 如果文件不存在则写入表头
        writer.writerow(message)  # 写入消息记录


# 自动打开浏览器
def open_browser(port):
    webbrowser.open(f"http://localhost:{port}")


def run_server(port):
    open_browser(port)
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run a Flask client.")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the Flask server on.")
    args = parser.parse_args()
    run_server(args.port)
