import requests
import time
import threading
import random
from datetime import datetime

# 配置客户端的 URL 和发送间隔
CLIENT_URL = "http://localhost:8000/receive_data"  # 客户端的接收数据接口
MESSAGE_INTERVAL = 10  # 默认每 10 秒发送一条消息

# 模拟消息数据
SAMPLE_MESSAGES = [
    {"source": "ServerBot", "target": "Mike Ross", "type": "text", "content": "Hello Mike!", "message_type": "personal"},
    {"source": "ServerBot", "target": "Legal Team", "type": "text", "content": "Don't forget to review the case.", "message_type": "group"},
    {"source": "ServerBot", "target": "Project X", "type": "text", "content": "New update on Project X.", "message_type": "group"},
    {"source": "ServerBot", "target": "Client Discussions", "type": "picture", "content": "./pictures/project_chart.png", "message_type": "group"},
    {"source": "ServerBot", "target": "Mike Ross", "type": "file", "content": "./files/client_contract.pdf", "message_type": "personal"}
]


# 发送模拟消息到客户端
def send_mock_message():
    # 随机选择一条样例消息
    message = random.choice(SAMPLE_MESSAGES)
    message["timestamp"] = datetime.now().isoformat()

    # 发送 POST 请求到客户端
    try:
        response = requests.post(CLIENT_URL, json=message)
        if response.status_code == 200:
            print(f"Sent message: {message}")
        else:
            print(f"Failed to send message: {response.status_code}")
    except Exception as e:
        print(f"Error sending message: {e}")


# 定期发送消息的线程
def message_sender(interval):
    while True:
        send_mock_message()
        time.sleep(interval)


# 启动模拟器
def start_simulator(interval=MESSAGE_INTERVAL):
    print(f"Starting simulator with message interval {interval} seconds.")
    threading.Thread(target=message_sender, args=(interval,), daemon=True).start()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Start the server message simulator.")
    parser.add_argument("--interval", type=int, default=MESSAGE_INTERVAL, help="Interval (in seconds) between messages")
    args = parser.parse_args()

    start_simulator(args.interval)

    # 保持主线程运行
    while True:
        time.sleep(1)
