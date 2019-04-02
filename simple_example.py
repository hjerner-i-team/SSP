from CREPE import CREPE, CrepeModus
from CREPE.utils.get_queue import get_queue 

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
    
    # Get the hdf5 queue
    queue = get_queue(crep, "HDF5READER")
        
    # Our simple experiment is just to count how many data points we have in a channel :)
    len_of_stream = 0
    
    # Now we want to iterate 
    while True:
        try: 
            # get the next element in the queue
            data = queue.get(timeout=1) #1 seconds timeout
        except: # .get raises error on timeout
            break
        # Add the length of this data
        len_of_stream += len(data[0])

    print("The length of a row is ", len_of_stream)
    
    # Shutdown crepe
    crep.shutdown()

if __name__ == "__main__":
    main()
