from CREPE.communication.queue_service import QueueService
from CREPE.utils.growing_np_array import Array
import numpy as np

class MovingAvg(QueueService):
    def __init__(self, queue_out, queue_in, mov_avg_size=1000):
        QueueService.__init__(self, name="MOVINGAVG" , queue_out=queue_out, queue_in=queue_in)

        self.mov_avg_size = mov_avg_size
        
        self.stream = Array(60, self.mov_avg_size * 2)

        data = self.get_x_elems(x_elems=self.mov_avg_size)
        self.stream.add(data)
        print("[MovingAvg] mov_avg_size: ", self.mov_avg_size)

    def run(self):
        i = 0
        while True:
            # get next segment if needed
            #print(self.name, " capacity of stream: ", self.stream.capacity, " len: ", len(self.stream))
            if (i + self.mov_avg_size >= len(self.stream)):
                data = self.get()
                if data is False:
                    self.end()
                    return

                self.stream.add(data)
            processed = self.moving_average(i) 
            self.put(processed)
            size_in_bytes = processed.nbytes
            del processed
            i += 1
            #print(self.name, " index ", i, " bytes: ", size_in_bytes )
    
    def moving_average(self, start_index):
        subset = self.stream.data[:,start_index:start_index + self.mov_avg_size]
        avg = np.average(subset, axis=1)
        return avg
