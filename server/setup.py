import socket
import threading
import json
import csv
import os

# 服务器配置
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8000

# 数据存储位置
MESSAGE_QUEUE_FILE = 'server_data/message_queue.csv'
os.makedirs(os.path.dirname(MESSAGE_QUEUE_FILE), exist_ok=True)

# 在线用户字典 (用户名 -> IP)
user_socket_dict = {}

# 组名 -> 组成员列表
group_dict = {}


def write_message_to_csv(message):
    file_exists = os.path.isfile(MESSAGE_QUEUE_FILE)

    with open(MESSAGE_QUEUE_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["timestamp", "source", "target", "type", "content", "message_type", "appendix"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

        if not file_exists:
            writer.writeheader()  # 写入表头

        # 确保所有值都被转换为字符串，并写入消息记录
        message_formatted = {k: str(v) if v is not None else "" for k, v in message.items()}
        writer.writerow(message_formatted)


# 处理每个客户端的连接
def handle_client(client_socket, client_address):
    try:
        # 接收登录请求，提取用户信息
        data = client_socket.recv(1024).decode('utf-8')
        login_request = json.loads(data)

        username = login_request.get('username')
        ip, port = client_address

        print(f"User {username} logged in from {ip}")

        # 更新用户-IP字典
        user_socket_dict[username] = (client_socket, (ip, port))
        print(user_socket_dict)

        # 向客户端发送在线用户列表
        online_users = list(user_socket_dict.keys())
        for v in user_socket_dict.values():
            cs = v[0]
            response = {
                "status": "success",
                "users": online_users
            }
            cs.send(json.dumps(response).encode('utf-8'))

        # 进入消息接收循环
        while True:
            message_data = client_socket.recv(1024).decode('utf-8')
            if not message_data:
                continue

            # 解析接收到的消息
            message = json.loads(message_data)
            print(f"Received message: {message}")
            '''
            这里实现信息的转发以及群组创建信息的转发(TODO)。
            '''
            # 如果消息类型是群组消息，则转发给群组成员
            if message["type"] == "group":
                group_name = message.get("group_name")
                if group_name in group_dict:
                    # 群组存在，转发消息给群组成员
                    for member in group_dict[group_name]:
                        # 如果该成员在线，发送消息
                        if member in user_socket_dict:
                            user_socket_dict[member][0].send(json.dumps(message).encode('utf-8'))
                            print(f"Sent group message to {member}")

                else:
                    print(f"Group {group_name} does not exist.")

            # 如果是普通消息，转发给目标用户
            else:
                target_user = message.get("target")
                if target_user in user_socket_dict:
                    # 如果目标用户在线，发送消息
                    user_socket_dict[target_user][0].send(json.dumps(message).encode('utf-8'))
                    print(f"Sent message to {target_user}")
                else:
                    print(f"Target user {target_user} is not online.")

            # 写入消息队列
            write_message_to_csv(message)

            # 向客户端回复成功响应
            client_socket.send(json.dumps({"status": "success", "message": "Message received and saved"}).encode('utf-8'))

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        # 关闭连接
        client_socket.close()

        # 从用户字典中删除已断开连接的客户端
        username_to_remove = None
        for username, (client_ip, client_port) in user_socket_dict.items():
            if (client_ip, client_port) == (client_address[0], client_address[1]):
                username_to_remove = username
                break

        if username_to_remove:
            del user_socket_dict[username_to_remove]
            print(f"User {username_to_remove} disconnected. Current users: {user_socket_dict}")


# 启动服务器并监听客户端连接
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}...")

    while True:
        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        # 启动新线程处理该客户端
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


# 启动服务器
if __name__ == "__main__":
    start_server()
