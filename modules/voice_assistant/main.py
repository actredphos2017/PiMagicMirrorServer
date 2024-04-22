import time

from pipe import Pipe

notifyPipe: Pipe | None = None


def main(pipe: Pipe):
    global notifyPipe
    notifyPipe = pipe

    notifyPipe.send('ASSISTANT', 'VOICE ASSISTANT START!')

    # Code Here
    while True:
        time.sleep(3)
        notifyPipe.send('ASSISTANT', 'Hello World')
