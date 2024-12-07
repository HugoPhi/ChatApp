import threading
import socket
import core


user_dict = {}


def handle_client(client_socket, client_address):
    """处理客户端连接"""
    print(f"[*] Handling connection from {client_address}")

    # 创建 FullDuplex 类实例
    fd = core.FullDuplex(
        ("0.0.0.0", 8000),
        client_address,
        nick_name="Alice",
        interface_socket=client_socket,
        files="./files/files/",
        imgs="./files/imgs/"
    )

    user_dict[fd.nick_name] = fd

    try:
        while fd.running:
            msg = fd.get_message()
            if msg:
                # print(type(msg))
                # print(type(msg['type']))

                if msg['type'] == core.FullDuplex.ProtocalHead.TEXT:
                    print(f"[*] Message from {client_address}: {msg}")
                    fd.send_message({
                        'type': core.FullDuplex.ProtocalHead.TEXT,  # Message type
                        'source': 'Server',  # Sender's nickname
                        'target': 'Alice',  # Receiver's nickname
                        'timestamp': core.FullDuplex.generate_timestamp(),  # Timestamp
                        'message_type': "single",  # "single" or "group"
                        'content': "Server Get Message."  # Message content
                    })
                elif msg['type'] == core.FullDuplex.ProtocalHead.FILE:
                    print(f"[*] File from {client_address}: {msg}")
                    fd.send_message({
                        'type': core.FullDuplex.ProtocalHead.TEXT,  # Message type
                        'source': 'Server',  # Sender's nickname
                        'target': 'Alice',  # Receiver's nickname
                        'timestamp': core.FullDuplex.generate_timestamp(),  # Timestamp
                        'message_type': "single",  # "single" or "group"
                        'content': "Server Get File."  # Message content
                    })
                elif msg['type'] == core.FullDuplex.ProtocalHead.IMAGE:
                    print(f"[*] Image from {client_address}: {msg}")
                    fd.send_message({
                        'type': core.FullDuplex.ProtocalHead.TEXT,  # Message type
                        'source': 'Server',  # Sender's nickname
                        'target': 'Alice',  # Receiver's nickname
                        'timestamp': core.FullDuplex.generate_timestamp(),  # Timestamp
                        'message_type': "single",  # "single" or "group"
                        'content': "Server Get Image."  # Message content
                    })
                elif msg['type'] == core.FullDuplex.ProtocalHead.CMD:
                    print(f"[*] Command from {client_address}: {msg}")
                    fd.send_message({
                        'type': core.FullDuplex.ProtocalHead.TEXT,  # Message type
                        'source': 'Server',  # Sender's nickname
                        'target': 'Alice',  # Receiver's nickname
                        'timestamp': core.FullDuplex.generate_timestamp(),  # Timestamp
                        'message_type': "single",  # "single" or "group"
                        'content': "Server Get Command."  # Message content
                    })
                else:
                    print(f"[*] Unknown message type from {client_address}: {msg}")
    except Exception as e:
        print(f"[!] Error in communication: {e}")
    finally:
        fd.stop()
        print(f"[*] {client_address} has disconnected.")


def start_server(host, port):
    """服务器主函数"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Server is listening on {host}:{port}")

    while True:
        # 等待用户输入来启动监听
        # input("Press Enter to start listening for connections...")

        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address}")

        # 启动一个独立线程来处理该连接
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.daemon = True
        client_thread.start()


if __name__ == "__main__":
    start_server("0.0.0.0", 8000)
