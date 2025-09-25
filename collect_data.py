# 功能：通过MPU6050采集数据集，目前采集4组，circle是划圆，cross是划十字，左右就是向左砍和向右砍
# 目标；帮老黄的金箍棒灯效采集数据
# Editor： 漂移菌 
# 串口数据来自接入的ESP32

import serial 
import time 
import csv
import os 


GESTURES = ["circle", "cross", "left", "right"] 
SAMPLES_PER_GESTURE = 30 # 每种手势采集30条
SAMPLE_DURATION = 2.0    # 每条样本2秒
SAMPLE_RATE = 50         # 50HZ
TOTAL_READS = int(SAMPLE_RATE * SAMPLE_DURATION)

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
time.sleep(2)

def collect_gesture(gesture_name, index):
    filename = f"{gesture_name}/{gesture_name}_{index:03d}.csv"
    print(f"准备采集: {filename}, 请在2秒内完成动作...")
    time.sleep(2)
    data = [] 
    try:
        while len(data) < TOTAL_READS:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(line)
                parts = line.split(',')
                if len(parts) == 3:
                    try:
                        yaw, pitch, roll = map(float, parts)
                        data.append([yaw, pitch, roll])
                        print(f"✅\r已采集: {len(data)}条数据", end='\n')
                    except ValueError:
                        print("跳过坏数据:", line)

        print(f"✅ 采集完成：{filename}, 共{len(data)}条数据")
    except KeyboardInterrupt:
        print(f"✅ 手动结束采集：{filename}, 共{len(data)}条数据")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["yaw", "pitch", "roll"])
        writer.writerows(data) 

if __name__ == "__main__":
    for gesture in GESTURES:
        os.makedirs(gesture, exist_ok=True)
        for i in range(1, SAMPLES_PER_GESTURE+1):
            input(f"\n按下回车开始采集{gesture}第{i}条...")
            collect_gesture(gesture, i)

