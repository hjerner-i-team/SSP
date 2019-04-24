from CREPE import CREPE, CrepeModus, get_queue, QueueService, HWAPIWrapper 
from CREPE.communication.meame_speaker.config_decimal import *
from CREPE.communication.meame_speaker.speaker import *
from ir_preprocessor import IRPreprocessor
from plotter import * 

import time
import os,sys,inspect 
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Queue

# Find the path to the test_data folder.
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_to_test_data_folder = __currentdir + "/test_data/"

#Output of meame_listener will be 60*100 numpy arrays by default
class FrequencyExtractor(QueueService):
    def __init__(self, N = 10000, bitrate = 10000, cutoff = 100, in_seg_len = 100, **kwargs):
        QueueService.__init__(self, name="FREQ_EXTRACT" , **kwargs)
        self.N = N
        self.bitrate = bitrate
        self.cutoff = cutoff

    def run(self):
        i=0
        while(True):
            #x = self.get_n_col(self.N, 60, 100)
            y = self.get()
            if(y is False):
                self.end()
                return


            F = np.fft.rfft(y, axis = 1)
            T = self.N/self.bitrate
            w = np.fft.rfftfreq(self.N,T/self.N)

            plotter.plot(np.arange(self.N), y[0,:], 'AVG','moving average channel 0')
            plotter.plot(w[:self.cutoff], np.abs(F[0,:self.cutoff]), 'FFT','FFT channel 0')

            top_freq = np.argmax(np.abs(F[:,:self.cutoff]), axis = 1)/T
            print(top_freq)
            self.put(top_freq)
        
class MeameDecoder(QueueService):
    def __init__(self, outputchannels, **kwargs):
        QueueService.__init__(self, name="MEAME_DECODER", **kwargs)
        self.outputchannels = outputchannels
        self.action = np.array(["None", "Rock", "Scissor", "Paper"])
        self.action_values = np.array([10,15,20,25])
    
    def run(self):
        while(True):
            freq = 0
            channel_freqs = self.get()
            if channel_freqs is False:
                self.end()
                return

            for i in self.outputchannels:
                freq+= channel_freqs[i]
                
            freq = freq/len(self.outputchannels)
            idx = (np.abs(self.action_values-freq)).argmin() 
            print(self.action[idx])
            self.put(self.action[idx])

class MovingAvg(QueueService):
    def __init__(self, N = 10000, n = 100, **kwargs):
        QueueService.__init__(self, name="MOVING_AVG", **kwargs)
        self.N = N
        self.n = n

    def run(self):
        while(True):
            y = self.get_n_col(self.N, 60, 100)
            if(y is False):
                self.end()
                return


            plotter.plot(np.arange(self.N), y[0,:], 'RAW','meame output channel 0')
            ret = np.cumsum(np.concatenate((y,np.zeros((60,self.n-1))),axis=1), dtype=float, axis = 1)
            ret[:,self.n:] = ret[:,self.n:] - ret[:,:-self.n]
            self.put(ret[:,self.n - 1:] / self.n)


def main():
    global plotter
    plotter = VisdomLinePlotter(env_name='CREPE')
    queue_plot = Queue()


    mode = CrepeModus.LIVE
    #do_remote_example()

    # Make functions ready to be inserted into the pipeline
    queue_services = list()
    
    #moving average
    moving__avg_kwargs = {"N":10000, "n":100}
    queue_services.append([MovingAvg, moving__avg_kwargs])

    #Frequency extractor
    frequency_ex_kwargs = {"N":10000, "bitrate":10000}
    queue_services.append([FrequencyExtractor, frequency_ex_kwargs])
     
    #Meame-decoder
    outputchannels = [0,2,3,5,7,8,50,51,54,56,57,59]
    meame_decoder_kwargs = { "outputchannels":outputchannels }
    queue_services.append([MeameDecoder, meame_decoder_kwargs])

    #HW-api
    hw_api_kwargs = {}
    queue_services.append([HWAPIWrapper, hw_api_kwargs])

    #IR-preprocessor
    ir_pro_kwargs = {queue_plot:queue_plot}
    queue_services.append([IRPreprocessor, ir_pro_kwargs])
    
    # Maeame speaker args CREPE
    meame_speaker_periods = { "None": 5000, "Rock": 2500, "Scissors": 1650, "Paper": 1250, }

    #Start CREPE
    crep = CREPE(modus=mode, meame_speaker_periods=meame_speaker_periods, queue_services = queue_services)

    #Retrieve the output of data flow for debugging purposes
#    end = QueueService(name="END", queue_in=crep.get_last_queue())
    while True:
        data = queue_plot.get()
        plotter.plot_map(data, "IMG", "input image")
#        data = end.get()
#        print("Got: ", data)
#        if data is False:
#            print("shutting down crepe")
#            crep.shutdown()
#            return

if __name__ == "__main__":
    main()
