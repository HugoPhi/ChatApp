import socket
import sys
import os
from rich import print
from rich.console import Console
from rich.table import Table
from questionary import select, text
from questionary import Validator, ValidationError

# 创建 Rich 控制台实例
console = Console()

# 自定义验证器，确保端口号为整数且大于1024


class PortValidator(Validator):
    def validate(self, document):
        try:
            port = int(document.text)
            if port <= 1024 or port > 65535:
                raise ValidationError(
                    message="端口号必须是大于1024且小于65536的数字。",
                    cursor_position=len(document.text))  # 将光标放在输入的末尾
        except ValueError:
            raise ValidationError(
                message="请输入一个有效的数字。",
                cursor_position=len(document.text))


def get_local_ip():
    """获取本地IP地址"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到一个不存在的IP地址，仅用于获取本地IP
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def setup_server(port):
    """
    配置服务器的逻辑。
    这里是一个示例实现，你需要根据实际需求进行修改。
    """
    # 示例逻辑：启动服务器（此处仅打印信息）
    console.print(f"[bold green]服务器已启动，监听端口 {port}[/bold green]")


def setup_client(port, use_existing_db=False):
    """
    配置客户端的逻辑。
    这里是一个示例实现，你需要根据实际需求进行修改。

    :param port: 客户端连接的端口号
    :param use_existing_db: 是否使用已有的数据库
    """
    db_status = "使用已有的数据库" if use_existing_db else "使用新的数据库"
    console.print(f"[bold green]客户端已配置，连接端口 {port}，{db_status}[/bold green]")


def run_setup_script():
    """
    如果你有其他需要在配置后运行的脚本，可以在这里调用。
    例如：调用其他 Python 脚本或执行系统命令。
    """
    # 示例：打印一条信息
    console.print("[bold blue]执行额外的设置脚本...[/bold blue]")
    # 你可以在这里添加实际的脚本调用逻辑
    # 例如：subprocess.run(["python", "other_script.py"])
    pass


def display_server_info(ip, port):
    table = Table(title="服务器信息")

    table.add_column("IP 地址", style="cyan", no_wrap=True)
    table.add_column("端口号", style="magenta")

    table.add_row(ip, str(port))

    console.print(table)


def display_client_info(ip, port, db_status):
    table = Table(title="客户端信息")

    table.add_column("IP 地址", style="cyan", no_wrap=True)
    table.add_column("端口号", style="magenta")
    table.add_column("数据库状态", style="yellow")

    table.add_row(ip, str(port), db_status)

    console.print(table)


def main():
    console.print("[bold cyan]欢迎使用开放式聊天室！[/bold cyan]\n")

    # 选择类型：Server 或 Client
    choice = select(
        "请选择类型：",
        choices=["Server", "Client"]
    ).ask()

    if choice == "Server":
        # 输入端口号
        port_input = text(
            "请输入端口号（大于1024）：",
            validate=PortValidator
        ).ask()

        port = int(port_input)

        # 运行服务器配置函数
        setup_server(port)

        # 获取本地IP
        ip = get_local_ip()

        # 输出服务器信息
        display_server_info(ip, port)

        # 运行额外的设置脚本（如果需要）
        run_setup_script()

    elif choice == "Client":
        # 输入端口号
        port_input = text(
            "请输入端口号（大于1024）：",
            validate=PortValidator
        ).ask()

        port = int(port_input)

        # 输入数据库选项
        db_choice = text(
            "请输入数据库名称（留空使用新的数据库，输入名称使用已有的数据库）：",
            default=""
        ).ask()

        # 根据数据库选择设置参数
        if db_choice.strip() == "":
            use_existing_db = False
            db_status = "使用新的数据库"
            console.print(f"[bold yellow]{db_status}。[/bold yellow]")
        else:
            # 检查 ./client/data/{db_choice} 是否存在
            db_path = os.path.join('.', 'client', 'data', db_choice)
            if os.path.isdir(db_path):
                use_existing_db = True
                db_status = f"使用已有的数据库：{db_choice}"
                console.print(f"[bold yellow]{db_status}。[/bold yellow]")
            else:
                console.print(f"[bold red]错误：没有已知数据库 '{db_choice}'。[/bold red]")
                sys.exit(1)

        # 运行客户端配置函数
        setup_client(port, use_existing_db=use_existing_db)

        # 获取本地IP
        ip = get_local_ip()

        # 输出客户端信息
        display_client_info(ip, port, db_status)

        # 运行额外的设置脚本（如果需要）
        run_setup_script()

    else:
        console.print("[red]无效的选择。程序退出。[/red]")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]用户中断程序。[/red]")
        sys.exit(0)
