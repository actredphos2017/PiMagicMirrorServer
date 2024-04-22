import time

from pipe import Pipe

notifyPipe = None


def main(pipe: Pipe):
    global notifyPipe
    notifyPipe = pipe

    notifyPipe.send('FACIAL', 'FACIAL RECOGNITION START!')

    # Code Here
    while True:
        time.sleep(5)
        notifyPipe.send('FACIAL', 'Hello World')


