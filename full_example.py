from CREPE import CREPE, CrepeModus
import time
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
   

if __name__ == "__main__":
    main()
