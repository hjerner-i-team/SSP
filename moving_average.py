from CREPE import QueueService, GrowingArray
import numpy as np

class MovingAvg(QueueService):
    def __init__(self, mov_avg_size=1000, **kwargs):
        QueueService.__init__(self, name="MOVINGAVG" , **kwargs)

        self.mov_avg_size = mov_avg_size
        
        self.stream = GrowingArray(60, self.mov_avg_size * 1000)

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
