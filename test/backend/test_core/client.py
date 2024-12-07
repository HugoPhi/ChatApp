import argparse
import core


def parse_args():
    # 创建解析器对象
    parser = argparse.ArgumentParser(description="Server or Client PORT Parser")

    # 添加命令行参数
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=8001,  # 默认端口
        help="Port number to bind/connect to (default: 8001)"
    )

    # 解析命令行参数
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    # 这里传入自己的 IP 和端口，和目标服务器的 IP 和端口

    args = parse_args()
    fd = core.FullDuplex(
        ("127.0.0.1", args.port),
        ("127.0.0.1", 8000)
    )

    # 发送消息
    fd.send_message({
        'type': core.FullDuplex.ProtocalHead.TEXT,  # Message type
        'source': 'Alice',  # Sender's nickname
        'target': 'Bob',  # Receiver's nickname
        'timestamp': core.FullDuplex.generate_timestamp(),  # Timestamp
        'message_type': "single",  # "single" or "group"
        'content': "User Login"
    })

    # 接收并打印服务器的回复
    while True:
        input_str = input("T: Enter to send a GET request...\n> ")
        if input_str == "text":
            print("[*] Sent a text message to the server.")
            fd.send_message({
                'type': core.FullDuplex.ProtocalHead.TEXT,  # Message type
                'source': 'Alice',  # Sender's nickname
                'target': 'Bob',  # Receiver's nickname
                'timestamp': core.FullDuplex.generate_timestamp(),  # Timestamp
                'message_type': "single",  # "single" or "group"
                'content': "Hello, Bob!"  # Message content
            })
        elif input_str == "file":
            print("[*] Sent a file to the server.")
            fd.send_message({
                'type': core.FullDuplex.ProtocalHead.FILE,  # Message type
                'source': 'Alice',  # Sender's nickname
                'target': 'Bob',  # Receiver's nickname
                'timestamp': core.FullDuplex.generate_timestamp(),  # Timestamp
                'message_type': "single",  # "single" or "group"
                'content': {
                    'file_name': "test.txt",  # File name
                    'file_path': "./test.txt"  # File path
                }
            })
        elif input_str == "img":
            print("[*] Sent an image to the server.")
            fd.send_message({
                'type': core.FullDuplex.ProtocalHead.IMAGE,  # Message type
                'source': 'Alice',  # Sender's nickname
                'target': 'Bob',  # Receiver's nickname
                'timestamp': core.FullDuplex.generate_timestamp(),  # Timestamp
                'message_type': "single",  # "single" or "group"
                'content': {
                    'file_name': "test.png",  # File name
                    'file_path': "./test.png"  # File path
                }
            })
        elif input_str == "cmd":
            print("[*] Sent a command to the server.")
            fd.send_message({
                'type': core.FullDuplex.ProtocalHead.CMD,  # Message type
                'source': 'Alice',  # Sender's nickname
                'target': 'Bob',  # Receiver's nickname
                'timestamp': core.FullDuplex.generate_timestamp(),  # Timestamp
                'message_type': "single",  # "single" or "group"
                'content': {
                    'cmd': "ls",  # Command name
                    'args': ["arg1", "arg2", "arg3"]
                }
            })
        elif input_str == "get":
            print("[*] Sent a GET request to the server.")
            while not fd.message_queue.empty():
                print(fd.message_queue.get())

        elif input_str == "exit":
            print("[*] Exiting...")
            break
        else:
            print("[!] Invalid input, please enter 'text', 'file', 'img', or 'cmd'.")

    fd.stop()
