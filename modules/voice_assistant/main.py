import time

from pipe import Pipe

notifyPipe = None


def main(p: Pipe):
    print('VOICE ASSISTANT START!')
    global notifyPipe
    notifyPipe = p

    while True:
        time.sleep(3)
        notifyPipe.send('ASSISTANT', 'Hello World')
