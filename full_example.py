
from CREPE import CREPE, CrepeModus
from CREPE.communication.stream_service import StreamRowIterator, StreamSegmentIterator
from pre_processing import AvgPreProcess
from readout import readout_layer

import os,sys,inspect 
# Find the path to the test_data folder.
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_to_test_data_folder = __currentdir + "/test_data/"

# Feel free to change this method, currently it is for testing purposes
def main():
    # Get the absolute path for the test file
    path_to_data = path_to_test_data_folder + "4.h5"

    #Create a crepe object and start it
    crep = CREPE(path_to_file=path_to_data)
   
    # name of service
    name = "PREPROCESS"

    # generate new RPCPORT
    port = crep.gen_new_RPCPORT(name)
    
    # get the stream connection
    stream_conn = crep.get_connection("STREAM")
    print("[full example] pre: ", stream_conn)
    print("[full example] pre: ", stream_conn.root)

    # create pre process object
    pre = AvgPreProcess(name, port)
    
    print("[full example] pre: ", pre)

    pre.start(stream_conn)
    
    while True:
        pass
    
    # shutdown self made processes
    pre.shutdown()
    
    # Shutdown crepe
    crep.shutdown()

if __name__ == "__main__":
    main()
