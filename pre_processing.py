from CREPE.communication.stream_service import StreamService, StreamSegmentIterator

class AvgPreProcess(StreamService):
    def __init__(self, name, port):
        StreamService.__init__(self,name, port)
        
    def start(self, pull_conn):
        self.pull_conn = pull_conn
        self.seg_iter = StreamSegmentIterator(_range = 100)
        self.start_loop(self.loop,[])

    def shutdown(self):
        print("[AvgPreProcess] terminating ", self.name)
        self.terminate_service()

    def loop(self): 
        len_of_stream = 0
        while True:
            seg = self.seg_iter.next_or_wait(self.pull_conn, timeout=50)
            print("[AvgPreProcess] self: ", self, " seg: ", seg)
            if seg is False:
                break
            pre_processed = self.pre_process_segments(seg)
            self.append_stream_segment_data(pre_processed)
            len_of_stream += 1
        print("[AvgPreProcess] Length of new stream is: ", len_of_stream)   
    
    def pre_process_rows(data):
        avg = sum(data) / len(data)
        return avg

    def pre_process_segments(data):
        avg = [sum(x) / len(x) for x in data]
        return avg

