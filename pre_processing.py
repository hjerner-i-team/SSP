from CREPE.communication.stream_service import StreamService, StreamSegmentIterator
import numpy as np

class AvgPreProcess(StreamService):
    def __init__(self, name, port, pull_conn):
        StreamService.__init__(self,name, port)
        self.seg_iter = StreamSegmentIterator(_range = 100)
        self.pull_conn = pull_conn
    
    def shutdown(self):
        print("[AvgPreProcess] terminating ", self.name)
        self.terminate_service()

    def loop(self): 
        len_of_stream = 0
        while True:
            seg = self.seg_iter.next_or_wait(self.pull_conn, timeout=50)
            #print("[AvgPreProcess] self: ", self, " len seg: ", len(seg[0]))
            if seg is False:
                break
            #print("[AvgPreProcess] after break statemnt" )
            #pre_processed = self.pre_process_segments(seg)
            #print("[AvgPreProcess] after preprocess func call" )
            #print("isinstance list: ", isinstance(seg, list))
            #print("isinstance np: ", isinstance(seg, np.ndarray))
            #self.append_stream_segment_data(seg)
            #print("[AvgPreProcess] after append_stream_segment_data" )
            len_of_stream += 1
            print("[AvgPreProcess] Length of new stream is: ", len_of_stream)   
        print("[AvgPreProcess] Length of new stream is: ", len_of_stream)   
    
    def pre_process_rows(self, data):
        avg = sum(data) / len(data)
        return avg

    def pre_process_segments(self, data):
        #print("[AvgPreProcess] in pre_process func" )
        #print("[AvgPreProcess] ", len(data), len(data[0]) )
        #avg = [sum(x) / len(x) for x in data]
        avg = []
        """
        avg = []
        for x in data:
            tmp_avg = 0
            for y in x:
                tmp_avg += y
            tmp_avg = tmp_avg / len(x)
            print("[AvgPreProcess] tmp_avg:", tmp_avg )
            avg.append(tmp_avg)
        print("[AvgPreProcess] avg[0]", avg[0] )
        """
        return avg

    def init_and_run(name, port, stream_conn):
        pp = AvgPreProcess(name,port,stream_conn)
        pp.start_loop(pp.loop)


