import threading

from modules.facial_recognition.main import main as facial_recognition
from modules.voice_assistant.main import main as voice_assistant
from pipe import Pipe, Notification

registered_modules = [
    voice_assistant,
    facial_recognition
]


def logger(notification: Notification):
    print(notification.stamp.strftime("%Y-%m-%d %H:%M:%S"), notification.flag, notification.msg)


if __name__ == '__main__':
    pipe = Pipe(logger)
    threads = []
    for module in registered_modules:
        t = threading.Thread(target=lambda: module(pipe))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
