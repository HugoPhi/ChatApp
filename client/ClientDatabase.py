import os
import csv


class dops:

    def __init__(self, dbpath="./db/"):
        if not os.path.exists(dbpath):
            os.mkdir(dbpath)

        self.gourps_table = dbpath + "groups.csv"
        self.users_table = dbpath + "users.csv"
        self.message_table = dbpath + "message.csv"

        if os.path.exists(self.gourps_table):
            raise Exception("[!] Gourp File exists.")

        if os.path.exists(self.users_table):
            raise Exception("[!] User File exists.")

        if os.path.exists(self.message_table):
            raise Exception("[!] Message File exists.")

        self.users = {
            "name": []
        }
        self.groups = {
            "name": [],
            "created_by_user": []  # true, or false, lowercase only
        }

        with open(self.users_file, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = list(self.users.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # write in table title
            writer.writerow()  # write a blank line

        with open(self.gourps_file, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = list(self.groups.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # write in table title
            writer.writerow()  # write a blank line

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
            writer.writerow()  # write a blank line

        print("[*] Database initialized.")

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

        pass

    def update_usrs(self):
        pass

    def update_groups(self):
        pass

    def get_usrs(self):
        pass

    def get_groups(self):
        pass
