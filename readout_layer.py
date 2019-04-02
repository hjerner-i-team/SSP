from CREPE.communication.queue_service import QueueService
import random


class ReadoutLayer(QueueService):
    def __init__(self, queue_out, queue_in):
        QueueService.__init__(self, name="READOUTLAYER" , queue_out=queue_out, queue_in=queue_in)

    def run(self):
        i = 0
        while True:
            data = self.get()
            rnd = random.randint(0,4)
            self.put(rnd)


