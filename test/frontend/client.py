from flask import Flask, send_from_directory, request, jsonify
import threading
import time
import socket
import json
import csv
import webbrowser
import os
from datetime import datetime

app = Flask(__name__, static_folder='front')
MESSAGE_QUEUE_FILE = 'front/data/message.csv'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_FILE_EXTENSIONS = {'txt', 'pdf', 'docx', 'zip', 'csv'}  # 可上传的文件类型
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}  # 可上传的图片类型
FILE_UPLOAD_FOLDER = 'front/data/file/files'
PICTURE_UPLOAD_FOLDER = 'front/data/picture/pictures'
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8888

sent_socket = None
recive_socket = None


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
    def send_login_request(username):
        """通过 socket 发送登录请求到服务器，并处理服务器的 JSON 响应"""
        login_data = {
            "username": username,
            "server_ip": SERVER_IP,
            "server_port": SERVER_PORT
        }

        try:
            # 创建 socket 连接
            global sent_socket
            sent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 连接到服务器
            sent_socket.connect((SERVER_IP, SERVER_PORT))

            # 将 login_data 转换为 JSON 字符串并发送
            login_data_str = json.dumps(login_data)
            sent_socket.sendall(login_data_str.encode('utf-8'))
            print(f"Login data sent to server: {login_data_str}")

            # 接收服务器的响应
            response_data = sent_socket.recv(1024).decode('utf-8')  # 接收服务器返回的数据
            print(f"Response received: {response_data}")

            # 解析服务器返回的 JSON 响应
            response_json = json.loads(response_data)
            print(response_json)

            # 假设服务器返回的 JSON 包含 status 字段来表示登录是否成功
            if response_json.get('status') == 'success':
                print(f"Login successful for {username}")
                '''
                这里实现本地三个文件的初始化，同时用户列表是需要写入的，而其他的只需要新建。(TODO)
                '''
                return True
            else:
                print(f"Login failed: {response_json.get('message')}")
                return False
        except Exception as e:
            print(f"Error during login request: {str(e)}")
            return False

    # 创建并保存在线用户到 users.csv
    def save_users_to_csv(users):
        # 文件路径
        users_file = './front/data/users.csv'

        # 写入用户数据
        with open(users_file, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # writer.writeheader()  # 写入表头
            for user in users:
                writer.writerow({'name': user})

        print(f"Users saved to {users_file}")

    def listen_for_server_responses():
        """通过 socket 监听服务器请求，并处理接收到的消息"""
        try:
            # 创建 socket 连接
            global recive_socket
            recive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 连接到服务器
            recive_socket.connect((SERVER_IP, SERVER_PORT))

            print("Listening for messages from server...")

            while True:
                # 接收服务器发送的消息
                response_data = recive_socket.recv(1024).decode('utf-8')  # 1024 是缓冲区大小，适当调整

                if response_data:
                    print(f"Received message from server: {response_data}")

                    # 解析 JSON 格式的响应数据
                    try:
                        message = json.loads(response_data)
                        print(f"Processed message: {message}")
                        '''
                        这里实现把服务器数据写入后端
                        '''
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON message: {e}")
                else:
                    print("No data received from server. Closing connection.")
                    break

                time.sleep(1)  # 每1秒检查一次是否有新消息

        except Exception as e:
            print(f"Error while listening to server: {str(e)}")

    data = request.get_json()
    username = data.get('username')
    SERVER_IP = data.get('server_ip')
    SERVER_PORT = data.get('server_port')
    SERVER_PORT = int(SERVER_PORT)
    print(f"Attempting login for user: {username}")
    print(f'login on server: {SERVER_IP}:{SERVER_PORT}')

    '''
    这里实现：发送请求到服务器，然后接受服务器的数据包。
    '''
    if send_login_request(username):
        save_users_to_csv([username])
        # 登录成功后，开启线程监听服务器的请求
        listener_thread = threading.Thread(target=listen_for_server_responses, args=(SERVER_IP, SERVER_PORT,))
        listener_thread.daemon = True  # 设置为守护线程，主程序结束时线程也结束
        listener_thread.start()

        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "error", "message": "Login failed"}), 400


@app.route('/send_message', methods=['POST'])
def send_message():
    def send_message_to_server(message):
        try:
            if sent_socket:
                # 将消息转换为JSON格式并编码成字节发送
                message_json = json.dumps(message).encode('utf-8')
                sent_socket.sendall(message_json)
                print(f"Message successfully sent to server: {message}")
                return True
            else:
                print("No connection to server.")
                return False
        except Exception as e:
            print(f"Failed to send message to server: {str(e)}")
            return False

    data = request.get_json()
    message_record = {
        "timestamp": datetime.now().isoformat(),
        "source": data.get("source"),
        "target": data.get("target"),
        "type": data.get("type"),
        "content": data.get("message"),
        "message_type": data.get("message_type"),
    }
    '''
    模拟发送到服务器
    '''
    if send_message_to_server(message_record):
        write_message_to_csv(message_record)
        return jsonify({"status": "success"})
    else:
        print('Error Sent Message')
        return jsonify({"status": "error", "message": "Failed to send message"})


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
        # "source": request.form.get("source", verify=False),  # you can open verify when put into use to increse safty.
        "source": request.form.get("source"),
        "target": request.form.get("target"),
        "type": file_type,
        "content": f"./{file_path}",  # 相对路径用于前端访问
        "message_type": request.form.get("message_type"),
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
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run a Flask client.")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the Flask server on.")
    args = parser.parse_args()
    run_server(args.port)
