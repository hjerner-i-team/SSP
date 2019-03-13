import CREPE
from CREPE.main import crepe_start
from CREPE.utils import get_connection
from CREPE.communication.stream_service import StreamRowIterator, StreamSegmentIterator

import os,sys,inspect 
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# The path to the test_data folder.
path_to_test_data = __currentdir + "/test_data/4.h5"

def main():
    print(path_to_test_data)
    crepe_start(path_to_test_data)
    conn = get_connection("STREAM")
    row_iter = StreamSegmentIterator(_range = 100)
    t = []
    i = 0
    import time
    while True:
        i += 1
        row = row_iter.next(conn)
        if row is not False:
            #print(row)
            t.append(row)
        else:
            time.sleep(0.1)
            if i > 100:
                break
    print(len(t))

if __name__ == "__main__":
    main()
