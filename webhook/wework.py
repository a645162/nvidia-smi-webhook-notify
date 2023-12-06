import os

import requests
import json

from utils import my_time


def get_wework_url():
    wework_env = os.environ.get('GPU_MONITOR_WEBHOOK_WEWORK')
    if not wework_env:
        # print("GPU_MONITOR_WEBHOOK_WEWORK Not Set!")
        return None
    webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + wework_env
    return webhook_url


def send_text(msg):
    webhook_url = get_wework_url()

    if not webhook_url:
        print("GPU_MONITOR_WEBHOOK_WEWORK Not Set!")
        return

    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }
    r = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    print("WeWork", "text", r.text)


def send_markdown(content):
    webhook_url = get_wework_url()

    if not webhook_url:
        print("GPU_MONITOR_WEWORK 环境变量未设置")
        return

    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "GPU Monitor",
            "content": content
        }
    }
    r = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    print("WeWork", "MarkDown", r.text)


if __name__ == '__main__':
    import socket

    # 获取当前机器的名称
    machine_name = socket.gethostname()
    print("当前机器名称:", machine_name)

    formatted_time = my_time.get_now_time()
    print("当前时间:", formatted_time)

    # 发送测试数据
    send_text(
        f"GPU Monitor\n"
        f"\tMachine Name: {machine_name}\n"
        f"\tTime: {formatted_time}\n"
        f"Test Pass!\n"
    )

    send_markdown(
        f"# GPU Monitor\n"
        f"## Machine Name\n{machine_name}\n"
        f"## Time\n{formatted_time}\n"
        f"# Test Pass!\n"
    )
