from enum import Enum
import shutil
import os
import ctypes
import itertools
import os
import string
import platform

def check_disk_space(path):
    
    """ chech the path space total,used and free spaces
    arguments : path (directory)
    return : dectionary includes the statistices   
    
    """
    # statistices variable
    stat = 0 
        
    try:    
        # extracte the statistices of the directory  
        stat = shutil.disk_usage(path)  
    except:
        print("Path Error --- check_disk_space()")
        print("the returned statistices is relevent to the user dirctory ")       
    try:
        # extracte the statistices of the user directory
        path = os.path.expanduser('~')
        stat = shutil.disk_usage(path)       
    except:
        print("Error ")  
    return {"total":stat[0],"used":stat[1],"free":stat[2]}



class uploading_data():
    DATA = list()
    
upload_data = uploading_data.DATA    


def get_available_drives():
    if 'Windows' not in platform.system():
        return []
    drive_bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
    return list(itertools.compress(string.ascii_uppercase,
               map(lambda x:ord(x) - ord('0'), bin(drive_bitmask)[:1:-1])))

# Enum type to express the Connection status
class Connection_Status(Enum):
    CONNECTED = True
    NOT_CONNECTED = False

# Enum type to express the Connection status
class Connection_Status_IP(Enum):
    CONNECTED = True
    NOT_CONNECTED = False
    
# Enum type to express the program status
class program_States(Enum):
    IDLE = 0
    CHECK_CONNECTION = 1
    UPLOAD = 2
    VALIDATION = 3
    DELETE = 4

Internet_Connection_Status = None
Internet_Connection_Status_IP = None

Program_State = program_States.IDLE
Files = []


  

class Uploading_Folder_Status(Enum):
    FOLDER_UPLOADING_DONE = True
    FOLDER_UPLOADING_NOT_DONE = False
class Uploading_File_Status(Enum):
    FILE_UPLOADING_DONE = True
    FILE_UPLOADING_NOT_DONE = False
    
Uploading_Folder_state = Uploading_Folder_Status.FOLDER_UPLOADING_DONE
Uploading_file_state = Uploading_File_Status.FILE_UPLOADING_DONE