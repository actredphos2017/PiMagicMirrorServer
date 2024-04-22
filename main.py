import threading

from modules.facial_recognition.main import main as facial_recognition
from modules.voice_assistant.main import main as voice_assistant
from modules.messanger.main import main as messanger
from pipe import Pipe, Notification

registered_modules = [
    voice_assistant,
    facial_recognition,
    messanger
]


def logger(n: Notification):
    print(n.stamp.strftime("%Y-%m-%d %H:%M:%S"), n.flag, n.msg)


if __name__ == '__main__':
    pipe = Pipe(logger)
    for module in registered_modules:
        threading.Thread(target=lambda: module(pipe)).start()
    pipe.hold()
