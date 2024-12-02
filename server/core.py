import socket
import threading
import os
import queue
from datetime import datetime


class FullDuplex:
    """
    A class to handle full-duplex communication between a client and server.


    1. Once instantiated, starts a separate thread (listen_for_messages) to
       continuously listen for incoming messages from a remote address and
       save them to a message queue, as well as automatically save files.
    2. Sends various types of messages, including local files and images,
       via fixed request formats.

    Args:
        own (tuple): A tuple containing the IP address and port number of the local machine.
        peer (tuple): A tuple containing the IP address and port number of the remote peer.
        nick_name (str, optional): A nickname for the user. Defaults to an empty string.
        interface_socket (socket.socket): The pre-created socket object to use for communication.
                                          (This is passed from the client.)
        files (str, optional): The directory where received files are saved. Defaults to "./files/files/".
        imgs (str, optional): The directory where received images are saved. Defaults to "./files/imgs/".
        debug (bool, optional): Whether to print debug messages. Defaults to False.

    Example:
        # Server-side
        !!! The server must pass in an already created socket object, typically
        !!! the one returned by server_socket.accept().
        ```python
        # Server code
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", 12345))
        server_socket.listen(5)
        print(f"[*] Server is listening on {host}:{port}")

        client_socket, client_address = server_socket.accept()
        duplex = FullDuplex(
            ("0.0.0.0", 12345),
            client_address,
            client_socket=client_socket)
        ```

        # Client-side
        !!! The client does not pass in a pre-created socket object. This class
        !!! will create it automatically.
        ```python
        # Client code
        duplex = FullDuplex(
            ("0.0.0.0", 12345),
            ("127.0.0.1", 12345))
        ```

        # Getting messages from the queue
        ```python
        while duplex.running:
            message = duplex.get_message()  # Get message
            if message:  # Check if message is not None
                # Process message
        ```

        # Sending a message
        ```python
        duplex.send_message({
            'type': 1,  # Message type
            'source': 'Alice',  # Sender's nickname
            'target': 'Bob',  # Receiver's nickname
            'timestamp': FullDuplex.generate_timestamp(),  # Timestamp
            'message_type': "single",  # "single" or "group"
            'content': "Hello, Bob!"  # Message content
        })
        ```
    """

    class ProtocalHead:
        """
        FileType ProtocalHead
        """

        TEXT = 1
        FILE = 2
        IMAGE = 3
        CMD = 4

    TIME_LENGTH = 19

    @staticmethod
    def generate_timestamp():
        """
        Generate a timestamp in the format '2024.12.03-23:33:00' using the current time.
        """

        current_time = datetime.now()
        # 格式化时间为 'yyyy.MM.dd-HH:mm:ss'
        return current_time.strftime("%Y.%m.%d-%H:%M:%S")

    def __init__(self, own: tuple, peer: tuple,
                 nick_name: str = "",
                 interface_socket: socket.socket = None,
                 files: str = "./files/files/",
                 imgs: str = "./files/imgs",
                 debug: bool = False):
        """
        Initializes a FullDuplex object for full-duplex communication.

        Args:
            own (tuple): A tuple representing the local socket address, containing (IP address, port).
            peer (tuple): A tuple representing the peer socket address, containing (IP address, port).
            nick_name (str, optional): The nickname of the user. Defaults to an empty string.
            interface_socket (socket.socket, optional): An already created socket object passed from the client. Defaults to None.
            files (str, optional): The local path where received files will be saved. Defaults to './files/files/'.
            imgs (str, optional): The local path where received images will be saved. Defaults to './files/imgs/'.
            debug (bool, optional): Whether to print debug messages. Defaults to False.
        """

        self.own = own
        self.peer = peer
        self.nick_name = nick_name
        self.message_queue = queue.Queue()  # 存储接收到的消息
        self.running = True  # 控制通信状态
        self.interface_socket = interface_socket

        self.files_dir = files
        self.imgs_dir = imgs
        self.whoami = "client"
        self.debug = debug

        if not self.interface_socket:
            # 如果是客户端，创建本地接口，连接到服务器
            self.interface_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.interface_socket.bind(own)
            self.interface_socket.connect((self.peer[0], self.peer[1]))
            print(f"[*] Connected to {self.peer[0]}:{self.peer[1]}")
        else:
            # 如果是服务器端，直接打印出对方进程
            self.whoami = "server"
            print(f"[*] Connected to {self.peer[0]}:{self.peer[1]}")

        # 创建并启动接收消息线程
        self.recv_thread = threading.Thread(target=self.listen_for_messages)
        self.recv_thread.daemon = True
        self.recv_thread.start()

    def listen_for_messages(self):
        """Listens for messages from the peer and stores them in the message queue."""

        try:
            while self.running:
                # 接收消息类型（1字节）
                data_type = int.from_bytes(self.interface_socket.recv(1), 'big')
                if not data_type:
                    self.stop()
                    print(f"[*]  Peer Stoped Connection: {self.peer[0]}:{self.peer[1]}")
                    break

                # 接收元数据：source、target、timestamp 和 message_type, 大端序
                source_len = int.from_bytes(self.interface_socket.recv(1), 'big')
                source = self.interface_socket.recv(source_len).decode()

                target_len = int.from_bytes(self.interface_socket.recv(1), 'big')
                target = self.interface_socket.recv(target_len).decode()

                timestamp = self.interface_socket.recv(FullDuplex.TIME_LENGTH).decode()

                message_type_len = int.from_bytes(self.interface_socket.recv(1), 'big')
                message_type = self.interface_socket.recv(message_type_len).decode()

                # 处理接收到的消息类型
                if data_type == FullDuplex.ProtocalHead.TEXT:
                    # 接收文本消息
                    text_len = int.from_bytes(self.interface_socket.recv(4), 'big')  # 接收字符串长度
                    text_data = self.interface_socket.recv(text_len).decode()  # 接收字符串内容
                    msg_json = {
                        "type": FullDuplex.ProtocalHead.TEXT,
                        "source": source,
                        "target": target,
                        "timestamp": timestamp,
                        "message_type": message_type,
                        "content": text_data
                    }
                    self.message_queue.put(msg_json)  # 存入消息队列
                    if self.debug:
                        print(f"[*] 󰭻 Received text message: {text_data}")

                elif data_type == FullDuplex.ProtocalHead.FILE:
                    # 接收文件
                    file_size = int.from_bytes(self.interface_socket.recv(8), 'big')  # 8字节表示文件大小
                    file_name_len = int.from_bytes(self.interface_socket.recv(2), 'big')  # 2字节表示文件名长度
                    file_name = self.interface_socket.recv(file_name_len).decode()  # 接收文件名

                    if self.debug:
                        print(f"[*]  Receiving file: {file_name} of size {file_size} bytes")

                    # 接收文件内容
                    file_data = b""
                    while len(file_data) < file_size:
                        chunk = self.interface_socket.recv(min(1024, file_size - len(file_data)))  # 分块接收文件
                        file_data += chunk

                    # 保存文件
                    save_path = os.path.join(self.files_dir, file_name)
                    if not os.path.exists(os.path.dirname(save_path)):
                        os.makedirs(os.path.dirname(save_path))
                    with open(save_path, 'wb') as f:
                        f.write(file_data)
                    msg_json = {
                        "type": data_type,
                        "source": source,
                        "target": target,
                        "timestamp": timestamp,
                        "message_type": message_type,
                        "content": save_path
                    }
                    self.message_queue.put(msg_json)  # 存入消息队列
                    if self.debug:
                        print(f"[*]  File saved as: {save_path}")

                elif data_type == FullDuplex.ProtocalHead.IMAGE:
                    # 接收图片
                    file_size = int.from_bytes(self.interface_socket.recv(8), 'big')  # 8字节表示文件大小
                    file_name_len = int.from_bytes(self.interface_socket.recv(2), 'big')  # 2字节表示文件名长度
                    file_name = self.interface_socket.recv(file_name_len).decode()  # 接收文件名

                    if self.debug:
                        print(f"[*]  Receiving image: {file_name} of size {file_size} bytes")

                    # 接收图片内容
                    file_data = b""
                    while len(file_data) < file_size:
                        chunk = self.interface_socket.recv(min(1024, file_size - len(file_data)))  # 分块接收文件
                        file_data += chunk

                    # 保存图片
                    save_path = os.path.join(self.imgs_dir, file_name)
                    if not os.path.exists(os.path.dirname(save_path)):
                        os.makedirs(os.path.dirname(save_path))
                    with open(save_path, 'wb') as f:
                        f.write(file_data)
                    msg_json = {
                        "type": data_type,
                        "source": source,
                        "target": target,
                        "timestamp": timestamp,
                        "message_type": message_type,
                        "content": save_path
                    }
                    self.message_queue.put(msg_json)  # 存入消息队列
                    if self.debug:
                        print(f"[*]  Image saved as: {save_path}")

                elif data_type == FullDuplex.ProtocalHead.CMD:
                    # 接收命令
                    # TODO: #1 改成枚举类，固定命令种类
                    command_len = int.from_bytes(self.interface_socket.recv(2), 'big')  # 2字节表示命令长度
                    command = self.interface_socket.recv(command_len).decode()  # 接收命令

                    args = []
                    args_len = int.from_bytes(self.interface_socket.recv(2), 'big')  # 2字节表示参数长度
                    while args_len > 0:
                        args_len -= 1
                        arg_len = int.from_bytes(self.interface_socket.recv(1), 'big')  # 1字节表示参数长度
                        arg = self.interface_socket.recv(arg_len).decode()  # 接收参数
                        args.append(arg)

                    msg_json = {
                        "type": data_type,
                        "source": source,
                        "target": target,
                        "timestamp": timestamp,
                        "message_type": message_type,
                        "content": {
                            "command": command,
                            "args": args
                        }
                    }
                    self.message_queue.put(msg_json)  # 存入消息队列
                    if self.debug:
                        print(f"[*]  Received command: {command} with args: {args}")

                else:
                    # pass
                    print(f"[!] Unknown data type received: {data_type}")

        except Exception as e:
            print(f"[!] Error receiving message: {e}")
        finally:
            self.stop()
            print(f"[*] 󰩈 Connection closed with {self.peer[0]}:{self.peer[1]}")

    def send_message(self, message_dict: dict):
        """
        Sends a message, supporting text, files, and images.

        When sending a message, the metadata (such as type, file name, file size, etc.)
        is sent first, followed by the message content (such as text or file data).
        The Message Packge Looks like:
        | type: 1 byte | source_len: 1 byte | source: source_len < 50 bytes | target_len: 1 byte | target: target_len < 50 bytes | timestamp: timestamp_len = 19 bytes | message_type_len: 1 byte | message_type: message_type_len bytes | content_len: 8 bytes | content: content_len bytes |

        Args:
            message_dict (dict): The dictionary containing the message details with the following keys:

            {
                'type' (int):
                    The message type, where:
                    1 - Text: FullDuplex.ProtocalHead.TEXT
                    2 - File: FullDuplex.ProtocalHead.FILE
                    3 - Image: FullDuplex.ProtocalHead.IMAGE
                    4 - Command: FullDuplex.ProtocalHead.CMD
                'source' (str):
                    The sender's nickname or group name.
                'target' (str):
                    The receiver's nickname or group name.
                'timestamp' (str):
                    The formatted timestamp, which must be generated using `get_timestamp()` method.
                'message_type' (str):
                    Either "single" or "group", indicating whether the message is sent to one recipient or multiple.
                'content' (str | dict):
                    The message content, as follows:
                    - If 'type' == 1 (text), 'content' should be the text message (string).
                    - If 'type' == 2 (file) or 'type' == 3 (image), 'content' should be a dictionary containing:
                    {
                        'file_name' (str): The name of the file or image.
                        'file_path' (str): The path to the file or image.
                    }
                    - If 'type' == 4 (command), 'content' should be a dictionary containing:
                    {
                        'command' (str): The command to be executed.
                        'args' (list): A list of arguments for the command.
                    }
            }

        Example:
            # Sending a text message
            ```python
            message_dict = {
                'type': 1,  # Message type, 1 means text
                'source': 'Alice',  # Sender's nickname
                'target': 'Bob',  # Receiver's nickname
                'timestamp': FullDuplex.get_timestamp(),  # Timestamp
                'message_type': "single",  # "single" or "group"
                'content': "Hello, world!"  # Text message content
            }
            send_message(message_dict)
            ```

            # Sending a file
            ```python
            message_dict = {
                'type': 2,  # Message type, 2 means file
                'source': 'Alice',  # Sender's nickname
                'target': 'Bob',  # Receiver's nickname
                'timestamp': FullDuplex.get_timestamp(),  # Timestamp
                'message_type': "single",  # "single" or "group"
                'content': {
                    'file_name': 'file.txt',  # File name
                    'file_path': './files/files/file.txt'  # File path
                }
            }
            send_message(message_dict)
            ```

            # Sending an image
            ```python
            message_dict = {
                'type': 3,  # Message type, 3 means image
                'source': 'Alice',  # Sender's nickname
                'target': 'Bob',  # Receiver's nickname
                'timestamp': FullDuplex.get_timestamp(),  # Timestamp
                'message_type': "single",  # "single" or "group"
                'content': {
                    'file_name': 'image.jpg',  # Image name
                    'file_path': './files/imgs/image.jpg'  # Image path
                }
            }
            send_message(message_dict)
            ```

            # Sending a command
            ```python
            message_dict = {
                'type': 4,  # Message type, 4 means command
                'source': 'Alice',  # Sender's nickname
                'target': 'Bob',  # Receiver's nickname
                'timestamp': FullDuplex.get_timestamp(),  # Timestamp
                'message_type': "single",  # "single" or "group"
                'content': {
                    'command': 'ls',  # Command to be executed
                    'args': []  # Arguments for the command
                }
            }
            send_message(message_dict)
            ```
        """

        try:
            if self.interface_socket.fileno() == -1:  # 检查套接字是否已经关闭
                print("[!] Cannot send message, socket is closed.")
                return

            message_type = message_dict.get('type')
            source = message_dict.get('source')
            target = message_dict.get('target')
            timestamp = message_dict.get('timestamp')
            msg_type = message_dict.get('message_type')  # 获取 message_type，单发或群发

            # 发送元数据：message_type, source, target, timestamp
            self.interface_socket.send(message_type.to_bytes(1, 'big'))  # 发送消息类型
            self.interface_socket.send(len(source).to_bytes(1, 'big'))  # 发送 source 的长度
            self.interface_socket.send(source.encode())  # 发送 source 名称

            self.interface_socket.send(len(target).to_bytes(1, 'big'))  # 发送 target 的长度
            self.interface_socket.send(target.encode())  # 发送 target 名称

            self.interface_socket.send(timestamp.encode())  # 发送 timestamp 内容

            self.interface_socket.send(len(msg_type).to_bytes(1, 'big'))  # 发送 message_type 的长度
            self.interface_socket.send(msg_type.encode())  # 发送 message_type 内容

            # 发送具体内容
            if message_type == FullDuplex.ProtocalHead.TEXT:
                # 发送文本消息
                text_data = message_dict.get('content')
                if not isinstance(text_data, str):
                    raise ValueError("[!] Text message content must be a string.")
                text_len = len(text_data)
                self.interface_socket.send(text_len.to_bytes(4, 'big'))  # 发送字符串长度
                self.interface_socket.send(text_data.encode())  # 发送文本内容
                if self.debug:
                    print(f"[*] 󰭻 Sent text message: {text_data}")

            elif message_type == FullDuplex.ProtocalHead.FILE or message_type == FullDuplex.ProtocalHead.IMAGE:
                # 发送文件或图片
                file_info = message_dict.get('content')
                if not isinstance(file_info, dict):
                    raise ValueError("[!] File content must be a dictionary with 'file_name' and 'file_path'.")
                file_name = file_info.get('file_name')
                file_path = file_info.get('file_path')

                if not file_name or not file_path or not os.path.exists(file_path):
                    raise ValueError("[!] Invalid file path or file name.")

                file_size = os.path.getsize(file_path)
                file_name_len = len(file_name)

                # 发送文件元数据
                self.interface_socket.send(file_size.to_bytes(8, 'big'))  # 8字节表示文件大小
                self.interface_socket.send(file_name_len.to_bytes(2, 'big'))  # 2字节表示文件名长度
                self.interface_socket.send(file_name.encode())  # 发送文件名

                # 发送文件内容
                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(1024)  # 分块读取文件
                        if not chunk:
                            break
                        self.interface_socket.send(chunk)  # 发送文件块

                if self.debug:
                    if message_type == FullDuplex.ProtocalHead.FILE:
                        print(f"[*]  Sent file: {file_path}")
                    else:
                        print(f"[*]  Sent file: {file_path}")

            elif message_type == FullDuplex.ProtocalHead.CMD:
                # 发送命令
                cmd_info = message_dict.get('content')
                if not isinstance(cmd_info, dict):
                    raise ValueError("[!] Command content must be a dictionary with 'command' and 'args'.")
                command = cmd_info.get('command')
                args = cmd_info.get('args')

                if not command:
                    raise ValueError("[!] Command is required.")

                command_len = len(command)
                # TODO: #1 改成枚举，固定命令种类，变成静态属性
                self.interface_socket.send(command_len.to_bytes(1, 'big'))  # 发送命令长度
                self.interface_socket.send(command.encode())  # 发送命令

                self.interface_socket.send(len(args).to_bytes(1, 'big'))  # 发送参数长度
                if args:
                    args_len = len(args)
                    self.interface_socket.send(args_len.to_bytes(1, 'big'))  # 发送参数长度
                    self.interface_socket.send(args.encode())  # 发送参数

                if self.debug:
                    print(f"[*]  Sent command: {command}")

            else:
                raise ValueError("[!] Unsupported message type.")

        except Exception as e:
            print(f"[!] Error sending message: {e}")

    def get_message(self):
        """
        Get a message from the message queue.

        Returns:
            dict: The message dictionary, or None if the queue is empty.
        """

        if not self.message_queue.empty():
            return self.message_queue.get()
        else:
            return None

    def stop(self):
        """Stop the communication and close the socket."""

        self.running = False
        self.interface_socket.close()
