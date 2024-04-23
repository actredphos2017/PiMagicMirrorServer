import threading

from modules.facial_recognition.main import main as facial_recognition
from modules.master.main import main as manager
from modules.messanger.main import main as messanger
from modules.voice_assistant.main import main as voice_assistant
from pipe import Pipe, Event, Subscriber

registered_modules = [
    voice_assistant,
    facial_recognition,
    messanger,
    manager
]


def logger(n: Event):
    print(n.stamp.strftime("%Y-%m-%d %H:%M:%S"), n.data['sender'], n.data['msg'])


if __name__ == '__main__':
    pipe = Pipe()
    pipe.subscribe(Subscriber("LOG", logger))
    for module in registered_modules:
        threading.Thread(target=lambda: module(pipe)).start()
    pipe.hold()
