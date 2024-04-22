import threading

from modules.facial_recognition.main import main as facial_recognition
from modules.voice_assistant.main import main as voice_assistant
from pipe import Pipe

registered_modules = [
    voice_assistant,
    facial_recognition
]

if __name__ == '__main__':
    pipe = Pipe(lambda n: print(n.stamp.strftime("%Y-%m-%d %H:%M:%S"), n.flag, n.msg))
    for module in registered_modules:
        threading.Thread(target=lambda: module(pipe)).start()
    pipe.hold()
