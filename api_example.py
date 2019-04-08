from CREPE import CREPE, CrepeModus
from readout_layer import ReadoutLayer
from CREPE.utils.get_queue import get_queue
from CREPE.communication.hw_api.hw_api import HWAPIWrapper
import time
import os,sys,inspect 
from ir_preprocessor import IRPreprocessor
# Find the path to the test_data folder.
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_to_test_data_folder = __currentdir + "/test_data/"

# Feel free to change this method, currently it is for testing purposes
def main():
    # Get the absolute path for the test file
    path_to_data = path_to_test_data_folder + "4.h5"

    # Make functions ready to be inserted into the pipeline
    queue_services = list()

    hw_api_kwargs = {}
    queue_services.append([HWAPIWrapper, hw_api_kwargs])

    ir_pro_kwargs = {}
    queue_services.append([IRPreprocessor, ir_pro_kwargs])

    #Create a crepe object and start it
    crep = CREPE(modus=CrepeModus.LIVE, file_path=path_to_data, queue_services=queue_services)
    
    readout_queue = get_queue(crep, "HWAPI")
    while True:
        data = readout_queue.get()
        #print("Got: ", data)


    crep.shutdown()



if __name__ == "__main__":
    main()
