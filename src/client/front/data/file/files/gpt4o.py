#!/usr/bin/env python
from PIL import Image
import rospy
import numpy as np
from sensor_msgs.msg import Image as ROSImage
from geometry_msgs.msg import Point
import time
import requests
import json
import base64
import re
import threading

# Initialize global variables
i = 0
last_time = 0


arr = [0] * 9
gpt_sent = 0
gpt_recive = 0


# openrouter gpt4o
gpt4o = {
    'API_Key': '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',
    'URL': 'https://openrouter.ai/api/v1/chat/completions',
    'model': 'openai/gpt-4o-2024-08-06',
    'temperature': 0.3,
    'max_tokens': 500
}


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def find_last_multi_digit_number(s):
    # 使用正则表达式从后往前查找所有连续数字
    # \d+ 匹配一个或多个数字
    # reversed(s) 是将字符串反转，以便从后往前搜索
    matches = re.findall(r'\d+', s[::-1])

    # print(s)
    # 如果找到了匹配项，返回第一个多位数字（即最先出现的多位数字）
    for match in matches:
        if len(match) >= 1:  # 判断是否是多位数
            res = match[::-1]
            res = int(res)
            # print(f'res in RE before is:{res}')
            if res not in [-1] + [x for x in range(1, 9)]:
                res = -1

            # print(f'res in RE after is:{res}')
            return res

    return -1   # 如果没有找到多位数返回 None


def generate_response_with_image(image_path, config):
    base64_image = image_to_base64(image_path)
    url = config['URL']
    api_key = config['API_Key']

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    # 创建请求数据
    data = {
        "model": config['model'],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",  # 使用base64编码的图片
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "slove the mathematical formula in the picture. Give only a short solution to the problem.",
                    }
                ]
            }
        ]
    }

    # 发送请求
    global gpt_sent
    gpt_sent += 1
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 解析返回结果
    if response.status_code == 200:
        result = response.json()
        res = result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
        return find_last_multi_digit_number(res)
    else:
        return f"Error: {response.status_code}, {response.text}"


# 第一个函数：更新数组并计数, 改模型在这里
def count_number(image_path, stop_event):
    global arr
    cnt = 0
    while not stop_event.is_set():  # 检查事件标志，如果被设置为True，则退出循环
        # 随机从0, 1, 2, ..., 8 中选择一个数字
        cnt += 1
        input_num = generate_response_with_image(image_path, gpt4o)
        global gpt_recive
        gpt_recive += 1
        # print(input_num)
        input_num = int(input_num)
        if input_num == -1:
            arr[0] += 1
        else:
            arr[input_num] += 1

    print(cnt)


# 第二个函数：获取可能性最高的数字
def get_most_frequent():
    max = 0
    max_id = 0
    for i in range(9):
        if arr[i] > max:
            max = arr[i]
            max_id = i

    if max_id == 0:
        max_id = -1

    return max_id


# 重置数组为全1
def reset_array():
    global arr
    arr = [0] * 9


# 主线程：计时9秒并控制线程
def main(image_path):
    global stop_event
    reset_array()
    stop_event = threading.Event()  # 事件标志，用于控制线程的停止

    # 启动计数线程: gpt4o: 8, wwu: 8, 12一个都没回来
    for _ in range(10):
        count_thread = threading.Thread(target=count_number, args=(image_path, stop_event, ), daemon=True)
        count_thread.start()

    # 主线程等待9秒
    time.sleep(7)

    # 9秒后，通知计数线程停止
    stop_event.set()  # 设置事件标志，计数线程将停止

    # 获取数组中可能性最高的数字
    most_frequent = get_most_frequent()
    print(f'{arr}')
    print(f'{[-1] + [x for x in range(1, 9)]}')
    print(f"最可能的数字是: {most_frequent}")
    return most_frequent


# call when stopped
def call_with_local_file(rgb_array):
    img = Image.fromarray(rgb_array)
    img.save('./input_image.jpg')
    res = main('./input_image.jpg')
    return res


# Callback function for image processing
def callback(data):
    global last_time
    current_time = time.time()
    if current_time - last_time < 1:  # Reduce interval to 1 second for faster updates
        return
    last_time = current_time

    # Convert ROS image data to numpy array
    n_channels = 3 if data.encoding in ['rgb8', 'bgr8'] else 1
    dtype = np.uint8
    image_np = np.frombuffer(data.data, dtype=dtype).reshape(data.height, data.width, n_channels)
    if data.encoding == 'bgr8':
        image_np = image_np[:, :, ::-1]  # Convert BGR to RGB if needed

    global i
    i += 1
    print(image_np.shape, i)
    result = call_with_local_file(image_np)

    # Publish the result
    point = Point(x=float(data.width) / 2, y=float(data.height) / 2, z=float(result))
    print(result)
    pub.publish(point)


# ROS listener initialization
def listener():
    rospy.init_node('numpy_image_listener', anonymous=True)
    rospy.Subscriber("/usb_cam/image_raw", ROSImage, callback)
    global pub
    pub = rospy.Publisher('/gpt_result', Point, queue_size=10)
    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
