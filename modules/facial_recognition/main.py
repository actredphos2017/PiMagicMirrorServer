import time

from pipe import Pipe

notifyPipe = None


def main(p: Pipe):
    print('FACIAL RECOGNITION START!')
    global notifyPipe
    notifyPipe = p

    while True:
        time.sleep(5)
        notifyPipe.send('FACIAL', 'Hello World')


