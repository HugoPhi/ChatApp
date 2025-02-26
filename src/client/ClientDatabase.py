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
                "timestamp",
                "source",
                "target",
                "type",
                "content",
                "message_type",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()  # write in table title

        print(f"[*] Database initialized {dbpath}")

    def __del__(self):
        pass

    def write_message(self, message):
        with open(self.message_table, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                "timestamp",
                "source",
                "target",
                "type",
                "content",
                "message_type",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            type_i2str = {
                1: "text",
                2: "file",
                3: "image"
            }

            fmt_message = {field: message.get(field, "") for field in fieldnames}

            fmt_message["type"] = type_i2str[message.get("type", 1)]

            writer.writerow(fmt_message)

    def insert_user(self, user_name):
        with open(self.users_table, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                "name"
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow({"name": user_name})

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
