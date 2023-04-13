from os.path import abspath,exists,dirname
import os
def prepare_file_folder(filename):
    
    filte = dirname(abspath(filename))
    if exists(filte):
        os.mkdir(filte)
    return filte
    
    


if __name__ == "__main__":
    print( prepare_file_folder('./11/33/test.py'))
