import schedule
import time
from urllib.request import urlopen
import socket
from enum import Enum
import shared_data as sd
import datetime
import os
import json

def Check_Internet_Connection_IP():

    """ Check the internet connection over IP address
    if the device is not Connected to the interenet the localhost IP is "127.0.0.1"
    otherwise will be another IP
    The connection status written in shared variables between the modules

     INPUT : NO passed parameters
     OUTPUT: NO return

    """
    IPaddress=socket.gethostbyname(socket.gethostname())
    if IPaddress=="127.0.0.1":
#        print("No internet, your localhost is "+ IPaddress)      
        sd.Internet_Connection_Status_IP = sd.Connection_Status_IP.NOT_CONNECTED
        sd.Program_State = sd.program_States.CHECK_CONNECTION
        return False
    else:
#        print("Connected, with the IP address: "+ IPaddress )
        sd.Internet_Connection_Status_IP = sd.Connection_Status_IP.CONNECTED
        sd.Program_State = sd.program_States.UPLOAD
        return True

def Check_Internet_Connection():

    """ Check the internet connection by open any URL
    if the device is not Connected to the interenet the program will generate an exception indicate that
    the device is not Connected to the internet

    The connection status written in shared variables between the modules

     INPUT : NO passed parameters
     OUTPUT: NO return

    """
    global Internet_Connection_Status

    while True:
            global Internet_Connection_Status
            try:
#                response = urlopen('https://drive.google.com/drive/u/2/folders/1OzJ7RVw5bPTAJB4uq1KbdF74E51jI4ME', timeout = 5)
                response = urlopen('https://www.google.com/', timeout = 5)
#                print("Response from URL: "+str(response))
                Internet_Connection_Status = sd.Connection_Status.CONNECTED
                return True
            except:
#                print("No internet connection ...............")
                Internet_Connection_Status = sd.Connection_Status.NOT_CONNECTED
                return False


def Check_both_URL_IP():
    file_path = os.path.realpath(os.path.dirname(__file__))
    e = datetime.datetime.utcnow()
    Connection_IP = Check_Internet_Connection_IP()
    Connection_URL = Check_Internet_Connection()
    if Connection_IP and Connection_URL:
        with open(file_path+"\ConnectionStatus.txt", "a+") as f:
            f.write(str(e)+"(UTC)"+" Connected\n")
        print(str(e)+"(UTC)"+" Internet Connected")
    else:
        with open(file_path+"\ConnectionStatus.txt", "a+") as f:
            f.write(str(e)+"(UTC)"+" Internet NOT Connected\n")
        print(str(e)+"(UTC)"+" Internet NOT Connected")
        try:
            with open(file_path+'\config_file.json') as confile:
                RUTssid = json.load(confile)
                try:
                    x = RUTssid['SSID']
                    if RUTssid['SSID'] == "" or type(RUTssid['SSID']) != type(str()):
                        print("NEED FOR ACTION: Fill SSID in config_file.json. SSID must be a string '\"\"'")
                    else:            
                        ssid_correct = RUTssid['SSID']
                        os.system(f'''cmd /c "netsh wlan connect name={ssid_correct}"''')
                except:
                    print('NEED FOR ACTION: There is no SSID option in config_file.json. There should be \'"SSID": "RUT955_xxxx"\'.')
        except:
            print("NEED FOR ACTION: There is no file named 'config_file.json' or the syntax is bad. OR there are not double backslashes '\\\\' in PATH OR there are commas ',' missing.")


def Get_Internet_Connection_Status() ->"bool":
    return sd.Internet_Connection_Status


data = [182,2,3,56,6,9]

if __name__ == "__main__":
#    Check_Internet_Connection_IP()
#    Check_Internet_Connection()
    Check_both_URL_IP()
#    print(repr(Get_Internet_Connection_Status()))

    pass
