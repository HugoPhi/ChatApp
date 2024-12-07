import os
import csv


class dops:

    def __init__(self, dbpath="./db/"):
        if not os.path.exists(dbpath):
            os.mkdir(dbpath)

        self.gourps_table = dbpath + "groups.csv"
        self.current_groups_table = dbpath + "current_groups.csv"
        self.users_table = dbpath + "users.csv"
        self.message_table = dbpath + "message.csv"

        if os.path.exists(self.gourps_table):
            raise Exception("[!] Gourp File exists.")

        if os.path.exists(self.users_table):
            raise Exception("[!] User File exists.")

        if os.path.exists(self.message_table):
            raise Exception("[!] Message File exists.")

        if os.path.exists(self.current_groups_table):
            raise Exception("[!] Current Groups File exists.")

        with open(self.users_table, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                "name"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # write in table title

        with open(self.gourps_table, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                "name",
                "owner"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # write in table title

        with open(self.current_groups_table, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                "name",
                "type"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # write in table title

        with open(self.message_table, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                "type",
                "source",
                "target",
                "timestamp"
                "message_type",
                "content"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # write in table title

        print(f"[*] Database initialized {dbpath}")

    def __del__(self):
        pass

    def write_message(self, message):
        """
            {
                'type' (int):
                    The message type, where:
                    1 - Text: FullDuplex.ProtocalHead.TEXT
                    2 - File: FullDuplex.ProtocalHead.FILE
                    3 - Image: FullDuplex.ProtocalHead.IMAGE
                    4 - Command: FullDuplex.ProtocalHead.CMD
                'source' (str):
                    The sender's nickname or group name. Or 'Server'  # TODO
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
            }
        """

        with open(self.message_table, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                "type",
                "source",
                "target",
                "timestamp",
                "message_type",
                "content"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow(message)

    def insert_user(self):
        pass

    def delete_usr(self):
        pass

    def insert_group(self):
        pass

    def delete_group(self):
        pass

    def move_to(self):
        '''
        you or other
        '''
        pass
