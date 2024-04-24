import threading

from pipe import Pipe, Notification
from utils.caiyun_weather import request_for_comprehensive


def to_update_weather(_, pipe: Pipe):
    log = Notification.create_notifier(pipe, "天气之子")

    def update_weather():
        updateResponse = request_for_comprehensive()
        log("天气获取结果:", updateResponse if isinstance(updateResponse, int) else "SUCCESS")
        pipe.send("WEATHER_UPDATE", {
            "available": isinstance(updateResponse, dict),
            "result": updateResponse
        })

    threading.Thread(target=update_weather).start()


def init_call_event_handler(pipe: Pipe):
    pipe.on("VIEW_UPDATE_WEATHER", to_update_weather)
