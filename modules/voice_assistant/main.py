import time
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



def main(pipe: Pipe):
    init_module(pipe)
    log('启动！')

    # 主代码从这里开始
    while True:
        time.sleep(3)

        # 模拟魔镜输出
        simulation_assistant()
