from CREPE import CREPE, CrepeModus, QueueService, get_queue

from moving_average import MovingAvg
from readout_layer import ReadoutLayer
import time
import os,sys,inspect 

# Find the path to the test_data folder.
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_to_test_data_folder = __currentdir + "/test_data/"

# Feel free to change this method, currently it is for testing purposes
def main():
    # Get the absolute path for the test file
    path_to_data = path_to_test_data_folder + "3.h5"

    # Make functions ready to be inserted into the pipeline
    queue_services = list()

    mov_avg_kwargs = {"mov_avg_size":500}    
    queue_services.append([MovingAvg, mov_avg_kwargs])

    readout_layer_kwargs = {}
    queue_services.append([ReadoutLayer, readout_layer_kwargs])
    
    # Maeame speaker args CREPE
    meame_speaker_periods = { "None": 5000, "Rock": 2500, "Scissors": 1650, "Paper": 1250, }
    
    #Create a crepe object and start it
    crep = CREPE(modus=CrepeModus.TEST, meame_speaker_periods=meame_speaker_periods, file_path=path_to_data, queue_services=queue_services)
    
    crep.wait()
    # if you want to do something with the data from the last queue, then send in a function:
    # crep.wait(lambda data: print(data))
    """ Alternative to crep.wait() in case you want to do something with the last queue/data
    end = QueueService(name="END", queue_in=crep.get_last_queue())
    while True:
        data = end.get()
        if data is False:
            crep.shutdown()
            return
    """



if __name__ == "__main__":
    main()
