from multiprocessing import Process, Queue
import numpy as np
import time

class Stream():
    def __init__(self, rows, max_size):
        self.rows = rows
        self.data = np.zeros((rows, max_size))
        self.capacity = max_size
        self.size = 0

    def grow(self):
        print("growing", self.size, self.capacity)
        if self.size == self.capacity:
            self.capacity *= 4
            print("new capacity: ", self.capacity) 
            new_data = np.zeros((self.rows, self.capacity))
            print("new array: ", new_data)
            new_data[:,:self.size] = self.data
            print("after copying")
            self.data = new_data

    def add(self, seg):
        self.grow()   
        for i, row in enumerate(seg):
            for j, elem in enumerate(row):
                self.data[i][self.size + j] = elem
        
        self.size += len(seg[0])
    
    def __len__(self):
        return self.size

class LoopQueue():
    def __init__(self, name, q_out, q_in, rows=None):
        self.name = name
        
        print("LoopQueue object with name: ", name)
        
        self.q_out = q_out
        self.q_in = q_in
        
        if rows is not None:
            print(self.name, " created stream of size ", rows, 1000)
            self.stream = Stream(rows, 1000)
        else:
            print(self.name, " did not create a stream")

    
    # TODO add check for equal seg dim
    def append_segment(self, seg):
        self.stream.add(seg)

    def put(self, seg):
        self.q_out.put(seg)

    def get(self):
        return self.q_in.get()

    def get_and_build(self, num_elems):
        tmp = 0
        while True:
            data = self.get()
            self.append_segment(data)
            tmp += len(data[0])
            if tmp >= num_elems:
                break
    
    def get_and_append(self):
        data = self.get()
        self.append_segment(data)

    def get_and_append_if_need(self, start_index, min_len):
        remaining = len(self.stream) - start_index
        #print(self.name, " get_and_append_if_need remaing: ", remaining)
        if remaining <= min_len:
            self.get_and_append()

class GenerateData(LoopQueue):
    def __init__(self, q_out):
        LoopQueue.__init__(self, name="GENDATA", q_out=q_out, q_in=None)

    def loop(self):
        while True:
            rand_data = np.random.rand(60, 100)
            rand_data = rand_data * 200
            self.put(rand_data)
            time.sleep(0.01)

class ProcessData(LoopQueue):
    def __init__(self, q_out, q_in):
        LoopQueue.__init__(self, name="PROCESSDATA" , q_out=q_out, q_in=q_in, rows=60)
        # we need at least 1000 elems before we can start to preprocess
        self.mov_avg_size = 1000
        self.get_and_build(self.mov_avg_size)

    def loop(self):
        i = 0
        while True:
            # get next segment if needed
            #print(self.name, " capacity of stream: ", self.stream.capacity, " len: ", len(self.stream))
            self.get_and_append_if_need(start_index=i, min_len=self.mov_avg_size)
            processed = self.moving_average(i) 
            self.put(processed)
            size_in_bytes = processed.nbytes
            del processed
            i += 1
            print(self.name, " index ", i, " bytes: ", size_in_bytes )
    
    def moving_average(self, start_index):
        return np.average(self.stream.data[:,start_index:start_index + self.mov_avg_size], axis=0)

def generate_data(q_out):
    gen_data = GenerateData(q_out)
    gen_data.loop()
    print("after gen loop")

def process_data(q_out, q_in):
    process_data = ProcessData(q_out, q_in)
    process_data.loop()
    print("after pro loop")

def main():
    gen_data_queue = Queue()
    gen_data_process = Process(target=generate_data, args=(gen_data_queue,))
    gen_data_process.start()

    pro_data_queue = Queue()
    pro_data_process = Process(target=process_data, args=(pro_data_queue, gen_data_queue))
    pro_data_process.start()

    while True:
        pass
        #data = pro_data_queue.get()
        #print("Average: ", data)
if __name__ == "__main__":
    main()
