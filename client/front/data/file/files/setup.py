from flask import Flask, send_from_directory, request, jsonify
import csv
import webbrowser
import os
from datetime import datetime

app = Flask(__name__, static_folder='front')
MESSAGE_QUEUE_FILE = 'front/data/message.csv'
FILE_UPLOAD_FOLDER = 'front/data/file/files'
PICTURE_UPLOAD_FOLDER = 'front/data/picture/pictures'

# 确保文件夹存在
os.makedirs(FILE_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PICTURE_UPLOAD_FOLDER, exist_ok=True)


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
    print(f'login on server: {data.get("server_ip")}:{data.get("server_port")}')

    '''
    这里写一个：发送请求到服务器，然后接受服务器的数据包。
    '''

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
    write_message_to_csv(message_record)
    print(f"Simulated message send to server: {message_record}")
    return jsonify({"status": "success"})


# 上传文件处理函数
@app.route('/send_file', methods=['POST'])
def send_file():
    return handle_file_upload("file")


@app.route('/send_picture', methods=['POST'])
def send_picture():
    return handle_file_upload("picture")


def handle_file_upload(file_type):
    upload_folder = FILE_UPLOAD_FOLDER if file_type == "file" else PICTURE_UPLOAD_FOLDER
    uploaded_file = request.files['file']
    file_path = os.path.join(upload_folder, uploaded_file.filename)
    uploaded_file.save(file_path)

    # 写入消息队列
    message_record = {
        "timestamp": datetime.now().isoformat(),
        "source": request.form.get("source", verify=False),  # you can open verify when put into use to increse safty.
        "target": request.form.get("target", verify=False),
        "type": file_type,
        "content": f"./{file_path}",  # 相对路径用于前端访问
        "message_type": request.form.get("message_type", verify=False),
    }
    write_message_to_csv(message_record)

    '''
    模拟将消息发送到服务器
    '''

    print(f"Simulated {file_type} send to server: {message_record}")

    return jsonify({"status": "success"})


def write_message_to_csv(message):
    """将消息写入到 message.csv 文件，并根据消息类型格式化内容路径"""
    file_exists = os.path.isfile(MESSAGE_QUEUE_FILE)

    # 如果消息类型是 picture 或 file，格式化 content 路径
    if message["type"] == "picture":
        # 保证路径为 ./pictures/filename 的格式
        filename = os.path.basename(message["content"])  # 提取文件名
        message["content"] = f"./pictures/{filename}"
        if message["message_type"] == "user":
            message["message_type"] = "personal"
    elif message["type"] == "file":
        # 保证路径为 ./files/filename 的格式
        filename = os.path.basename(message["content"])
        message["content"] = f"./files/{filename}"
        if message["message_type"] == "user":
            message["message_type"] = "personal"

    # 打开文件并追加写入消息
    with open(MESSAGE_QUEUE_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["timestamp", "source", "target", "type", "content", "message_type"]
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n'
        )

        # 如果文件不存在，则写入表头
        if not file_exists:
            writer.writeheader()

        # 确保所有值都被转换为字符串，并写入消息记录
        message_formatted = {k: str(v) if v is not None else "" for k, v in message.items()}
        writer.writerow(message_formatted)


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
