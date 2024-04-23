import time
import pyaudio, wave
from datetime import datetime
from typing import Callable

from pipe import Pipe, Notification

notifyPipe: Pipe
log: Callable


def init_module(pipe: Pipe):
    # 模块初始化
    global notifyPipe, log
    notifyPipe = pipe
    log = Notification.create_notifier(pipe, "语音助手")


def simulation_assistant():
    log("模拟开始语音助手")
    notifyPipe.send("ASSISTANT_BEGIN")

    time.sleep(1)

    log("模拟语音识别过程")
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今",
        "end": False
    })
    time.sleep(0.2)
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今天",
        "end": False
    })
    time.sleep(0.2)
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今天天气",
        "end": False
    })
    time.sleep(0.2)
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今天天气怎么",
        "end": False
    })
    time.sleep(0.2)
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今天天气怎么样",
        "end": False
    })
    time.sleep(0.5)
    notifyPipe.send("ASSISTANT_ASK", {
        "content": "今天天气怎么样",
        "end": True
    })

    time.sleep(2)

    log("模拟语音助手回应")
    notifyPipe.send("ASSISTANT_ANSWER", {
        "content": "杭州市今天天气小雨转阴，气温13到20摄氏度，出门注意带伞哦",
    })

    time.sleep(5)

    log("模拟结束语音助手")
    notifyPipe.send("ASSISTANT_CLOSE")


def usage():
    log("设置便签")
    notifyPipe.send("ASSISTANT_SET_NOTE", {
        "content": "购买西红柿"
    })
    log("添加日程")
    notifyPipe.send("ASSISTANT_ADD_SCHEDULE", {
        "content": "开会",
        "time": "2025-07-21T14:00:00",
        "prompt": "下午"
    })


def demo():
    # 实例化一个PyAudio对象
    pa = pyaudio.PyAudio()
    # 打开声卡，设置 采样深度为16位、声道数为2、采样率为16、输入、采样点缓存数量为2048
    stream = pa.open(format=pyaudio.paInt16, channels=2, rate=16000, input=True, frames_per_buffer=2048)
    # 打开声卡，设置 采样深度为16位、声道数为2、采样率为16、输入、采样点缓存数量为2048
    stream = pa.open(format=pyaudio.paInt16, channels=2, rate=16000, input=True, frames_per_buffer=2048)
    # 新建一个列表，用来存储采样到的数据
    record_buf = []
    count = 0
    while count < 8 * 5:
        audio_data = stream.read(2048)  # 读出声卡缓冲区的音频数据
        record_buf.append(audio_data)  # 将读出的音频数据追加到record_buf列表
        count += 1
        print('*')
    wf = wave.open('01.wav', 'wb')  # 创建一个音频文件，名字为“01.wav"
    wf.setnchannels(2)  # 设置声道数为2
    wf.setsampwidth(2)  # 设置采样深度为
    wf.setframerate(16000)  # 设置采样率为16000
    # 将数据写入创建的音频文件
    wf.writeframes("".encode().join(record_buf))
    # 写完后将文件关闭
    wf.close()
    # 停止声卡
    stream.stop_stream()
    # 关闭声卡
    stream.close()
    # 终止pyaudio
    pa.terminate()


def main(pipe: Pipe):
    init_module(pipe)
    log('启动！')
    demo()
    # 主代码从这里开始
    # while True:
    #     time.sleep(3)
    #     模拟魔镜输出
    # simulation_assistant()
