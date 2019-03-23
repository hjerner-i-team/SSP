from CREPE import CREPE
from CREPE.utils import get_connection
from CREPE.communication.stream_service import StreamRowIterator, StreamSegmentIterator
from CREPE.communication.hdf5_reader import HDF5Reader 
from CREPE.settings import RPCPORTS, RPYC_CONFIG

import os,sys,inspect 
# Find the path to the test_data folder.
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_to_test_data_folder = __currentdir + "/test_data/"


# Feel free to change this method, currently it is for testing purposes
def main():
    # Get the absolute path for the test file
    path_to_data = path_to_test_data_folder + "4.h5"
    h5 = HDF5Reader(path_to_data)
    
    h5.generate_H5_stream()

    h5.start_service("STREAM")
    
    print("this")


    #Create a crepe object and start it
    #crep = CREPE("__TESTING")
         
    # Get the connection for the stream whichs contains the data
    conn = get_connection("STREAM")
    
    # Get a row iterator
    row_iter = StreamSegmentIterator(_range = 100)
    
    # Our simple experiment is just to count how many data points we have in a channel :)
    len_of_stream = 0
    
    print("Starting to iterate")
    # Now we want to iterate 
    while True:
        # Get the next set of data. 
        row = row_iter.next_or_wait(conn, timeout=1)

        # If there is no more data then the .next_or_wait will timeout and return false
        if row is False:
            break

        # Add the length of this data
        len_of_stream += len(row[0])

    print("The length from the stream was: ", len_of_stream)
    
    h5.terminate_service()
    # Shutdown crepe
    #crep.shutdown()

if __name__ == "__main__":
    main()
