import json
import threading

from utils.orm import LocalStorage, RuntimeCache
from utils.pipe import Pipe, Notification
from utils.caiyun_weather import get_weather


def to_update_weather(_, pipe: Pipe):
    log = Notification.create_notifier(pipe, "WEATHER")

    def update_weather():
        updateResponse = get_weather()
        log("天气获取结果:", updateResponse if isinstance(updateResponse, int) else "SUCCESS")
        pipe.send("WEATHER_UPDATE", {
            "available": isinstance(updateResponse, dict),
            "result": updateResponse
        })

    threading.Thread(target=update_weather).start()


def check_environment(_, pipe: Pipe):
    environment = LocalStorage.get("environment")
    if environment is not None and environment == "active":
        pipe.send("ENVIRONMENT_ACTIVE")
    else:
        pipe.send("ENVIRONMENT_SILENT")

    bluetooth_advertise_info = RuntimeCache.get("bluetooth_advertise_info")
    if bluetooth_advertise_info is not None:
        pipe.send("BLUETOOTH_ADVERTISE_INFO", json.loads(bluetooth_advertise_info))


def init_functional_event_handler(pipe: Pipe):
    pipe.on("VIEW_UPDATE_WEATHER", to_update_weather)
    pipe.on("VIEW_CHECK_ENVIRONMENT", check_environment)
