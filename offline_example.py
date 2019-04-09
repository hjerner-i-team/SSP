from CREPE import CREPE, CrepeModus, get_queue, QueueService, NeuroProcessor

import time
import os,sys,inspect 
import numpy as np
# Find the path to the test_data folder.
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_to_test_data_folder = __currentdir + "/test_data/"

#Output of meame_listener will be 60*100 numpy arrays by default
class FrequencyExtractor(QueueService):
    def __init__(self, N = 10000, bitrate = 10000, cutoff = 500, in_seg_len = 100, queue_in = None, queue_out = None):
        QueueService.__init__(self, name="FREQ_EXTRACT" , queue_out=queue_out, queue_in=queue_in)
        self.N = N
        self.bitrate = bitrate
        self.cutoff = cutoff

    def run(self):
        while(True):
            x = self.get_n_col(self.N, 60, 100)
            if(x is False):
                self.end()
                return

            F = np.fft.rfft(x, axis = 1)
            T = self.N/self.bitrate
            top_freq = np.argmax(np.abs(F[:,:self.cutoff]), axis = 1)/T
            self.put(top_freq)
        
#class MeameDecoder(QueueService):
#    outputchannels = [0,3,6

def main():
    mode = CrepeModus.LIVE

    # Make functions ready to be inserted into the pipeline
    queue_services = list()
    
    frequency_ex_kwargs = {"N":10000, "bitrate":10000}
    queue_services.append([FrequencyExtractor, frequency_ex_kwargs])
    crep = CREPE(modus=mode, queue_services = queue_services)

    end = QueueService(name="END", queue_in=crep.get_last_queue())
    while True:
        data = end.get()
        print("Got: ", data)
        if data is False:
            print("shutting down crepe")
            crep.shutdown()
            return

if __name__ == "__main__":
    main()
