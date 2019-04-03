from CREPE import CREPE, CrepeModus
from CREPE.utils.get_queue import get_queue 
from CREPE.communication.queue_service import is_poison_pill, QueueService

import time
import os,sys,inspect 

# Find the path to the test_data folder.
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_to_test_data_folder = __currentdir + "/test_data/"

# A simple way to get data
def main():
    # Get the absolute path for the test file
    file_path = path_to_test_data_folder + "4.h5"

    #Create a crepe object and start it
    crep = CREPE(modus=CrepeModus.FILE, file_path=file_path)    
    
    #get_data_from_meame_direct_from_queue(crep)
    get_data_from_meame_with_helper(crep)
    #get_data_from_meame_with_easier_helper(crep)

def get_data_from_meame_direct_from_queue(crep):
    # Get the hdf5 queue
    queue = crep.get_first_queue()
        
    # Our simple experiment is just to count how many data points we have in a channel :)
    len_of_stream = 0
     
    # Now we want to iterate 
    while True:
        try: 
            # get the next element in the queue
            data = queue.get(timeout=1) #1 seconds timeout
            if is_poison_pill(data):
                break
        except: # .get raises error on timeout
            break
        # Add the length of this data
        len_of_stream += len(data[0])

    print("The length of a row is ", len_of_stream)
    
    # Shutdown crepe
    crep.shutdown()

def get_data_from_meame_with_helper(crep):
    helper = QueueService(name="HELPER", queue_in=crep.get_first_queue())
    i = 0
    while True:
        data = helper.get()
        if data is False:
            crep.shutdown()
            break
        i += len(data[0])
    print("Got ", i, " elements in each row")

def get_data_from_meame_with_easier_helper(crep):
    def data_func(data):
        #do something with data, for example print it
        print(data)
    crep.wait(data_func)

if __name__ == "__main__":
    main()
