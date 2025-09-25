#!/usr/bin/env python3
import paho.mqtt.publish as publish
import socket
import subprocess
import time

# 连接参数
broker_ip   = "192.168.3.66"   # 改成你的 Broker 地址
broker_port = 1883
auth = None                     # 若 Broker 无认证可留空
# auth = {'username': 'user', 'password': 'pass'}  # 有认证时打开

topic = "esp32sensor/status"        # 统一主题，可自行更改

def get_serial():
    with open('/proc/cpuinfo') as f:
        for line in f:
            if line.startswith('Serial'):
                return line.split(':')[1].strip()
    return "unknown"

def get_hostname():
    return socket.gethostname()

def get_time():
    return time.strftime('%Y-%m-%d %H-%M-%S')

def get_temp():
    out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
    # 输出形如 "temp=45.2'C\n"
    return out.split("=")[1].split("'")[0]

while True:
    payload = {
        "serial":  get_serial(),
        "timestamp": get_time(),
        "hostname": get_hostname(),
        "temp":     float(get_temp())
    }
    publish.single(
        topic,
        payload=str(payload),
        hostname=broker_ip,
        port=broker_port,
        auth=auth
    )
    time.sleep(5)  # 每 5 秒发一次
