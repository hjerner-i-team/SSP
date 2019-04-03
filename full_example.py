from CREPE import CREPE, CrepeModus
from CREPE.communication.queue_service import QueueService
from moving_average import MovingAvg
from readout_layer import ReadoutLayer
from CREPE.utils.get_queue import get_queue
import time
import os,sys,inspect 
# Find the path to the test_data folder.
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_to_test_data_folder = __currentdir + "/test_data/"

# Feel free to change this method, currently it is for testing purposes
def main():
    # Get the absolute path for the test file
    path_to_data = path_to_test_data_folder + "4.h5"

    # Make functions ready to be inserted into the pipeline
    queue_services = list()

    mov_avg_kwargs = {"mov_avg_size":500}    
    queue_services.append([MovingAvg, mov_avg_kwargs])

    readout_layer_kwargs = {}
    queue_services.append([ReadoutLayer, readout_layer_kwargs])

    #Create a crepe object and start it
    crep = CREPE(modus=CrepeModus.LIVE, file_path=path_to_data, queue_services=queue_services)
   
    end = QueueService(name="END", queue_in=crep.get_last_queue())
    while True:
        data = end.get()
        if data is False:
            crep.shutdown()
            return




if __name__ == "__main__":
    main()