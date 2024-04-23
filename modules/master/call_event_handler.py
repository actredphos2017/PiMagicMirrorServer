from pipe import Pipe, Notification
from utils.caiyun_weather import request_for_comprehensive


def to_update_weather(_, pipe: Pipe):
    updateResponse = request_for_comprehensive()
    Notification.create_notifier(pipe, "天气之子")("天气获取结果:", updateResponse)
    pipe.send("WEATHER_UPDATE", {
        "available": isinstance(updateResponse, dict),
        "result": updateResponse
    })


def init_call_event_handler(pipe: Pipe):
    pipe.on("VIEW_UPDATE_WEATHER", to_update_weather)
