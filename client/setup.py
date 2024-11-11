from flask import Flask, send_from_directory, request, jsonify
import webbrowser
import argparse


app = Flask(__name__, static_folder='front')  # 指定静态文件文件夹为 front


# 路由：指向 index.html
@app.route('/')
def serve_index():
    return send_from_directory('front', 'index.html')


# 路由：支持直接访问其他静态文件（例如 /index.html）
@app.route('/<path:filename>')
def serve_static_file(filename):
    return send_from_directory('front', filename)


# 自动打开浏览器
def open_browser(port):
    webbrowser.open(f"http://localhost:{port}")


# 接收来自前端的消息
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()  # 获取前端发送的 JSON 数据
    message = data.get("message", "")
    print("Received message:", message)  # 打印收到的消息
    return jsonify({"status": "success", "message": message})  # 返回 JSON 响应


# 主函数
def run_server(port):
    # threading.Timer(1, open_browser).start()
    open_browser(port)
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Run a Flask client.")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the Flask server on.")
    args = parser.parse_args()

    # 获取本机 IP 地址

    # 启动服务器
    run_server(args.port)
