from CREPE import QueueService
import random


class ReadoutLayer(QueueService):
    def __init__(self, **kwargs):
        QueueService.__init__(self, name="READOUTLAYER" , **kwargs)

    def run(self):
        i = 0
        while True:
            data = self.get()
            if data is False:
                self.end()
                return
            rnd = random.randint(0,4)
            self.put(rnd)


