# Schedule Library imported
import schedule
import time
from time import sleep, perf_counter
import threading
import Internet_Connection as intcon
import shared_data as sd
import upload_to_drive as u
#import win32gui, win32con
import datetime
import os 
import json
#the_program_to_hide = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)
#file = open("ConnectionStatus.txt",'w')
#file.close()

def main():
#    def ConnectionStatus():
#        f=open("ConnectionStatus.txt", "a+")
#        e = datetime.datetime.now()
#        f.write(str(e)+"\n")
    
    # def ReadPaths(pathFile):
    #     with open(pathFile) as f:
    #         lines = f.readlines()
    #     return lines

    def TextFileWrite(message):
        """Writing messages to the changelog.txt
          Comparing files and folders, Uploading files, Refreshing files, Creating folders
        """
        try:
            # take path of the script. There will be generated, and written to the changelog.
            file_path = os.path.realpath(os.path.dirname(__file__))
            #open changelog
            with open(file_path+"\changelog.txt", "a+") as f:
                #write the message to the log
                f.write(str(message)+"\n")
        except Exception as e:
            print(e)
    
    def run_threaded(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()
    
    
    def run_threadedUpload(job_func):
        for FULL_PATH in FULL_PATHS:
    #        global FULL_PATH
            job_thread = threading.Thread(target=job_func,args = (str(FULL_PATH).strip(),))
#            if job_thread.is_alive():
#                job_thread.join()
            job_thread.start()
#            print('--------end of run_threadedUpload func--------')

    # parallelism scheduleing
#    u.Uploading(FULL_PATHS)
    schedule.every(30).seconds.do(run_threadedUpload,u.Uploading)
    schedule.every(5).seconds.do(run_threaded,intcon.Check_both_URL_IP)
#    schedule.every(10).seconds.do(run_threaded,ConnectionStatus)
    while True:
        time.sleep(1)
        FULL_PATHS = list()
        notInPath = list()
        file_path = os.path.realpath(os.path.dirname(__file__))
        paths = r"\config_file.json"
        jsonPath = file_path+paths
        try:
            with open(jsonPath) as confile:
                RUTjson = json.load(confile)
                try:
                    x = RUTjson['PATH']
                    if RUTjson['PATH'] == "":
                        print("NEED FOR ACTION: Fill path in config_file.json. Path must have double backslashes '\\'.")
                        TextFileWrite("NEED FOR ACTION: Fill path in config_file.json. Path must have double backslashes '\\'.")
                    else:
                        FULL_PATHSjson = RUTjson['PATH']
                        if type(FULL_PATHSjson) == type(list()):
                            for one_path in FULL_PATHSjson:
                                if os.path.exists(one_path):
                                    FULL_PATHS.append(one_path)
                                else:
                                    notInPath.append(one_path)
                                    print("Folder path does not exist. "+"("+str(one_path)+").")
                                    TextFileWrite("Folder path does not exist. "+"("+str(one_path)+").")
                                    
                            schedule.run_pending()
                        else:
                            print("NEED FOR ACTION: PATH in config_file.json must be a list. Add '[]'.")
                            TextFileWrite("NEED FOR ACTION: PATH in config_file.json must be a list. Add '[]'.")
                            time.sleep(5)
                except:
                    print('NEED FOR ACTION: There is no PATH option in config_file.json. There should be \'"PATH": ["C:\\path\\..."]\'.')      
                    TextFileWrite('NEED FOR ACTION: There is no PATH option in config_file.json. There should be \'"PATH": ["C:\\path\\..."]\'.')
                    time.sleep(5)
        except:
            print("NEED FOR ACTION: There is no file named 'config_file.json' or the syntax is bad. OR there are not double backslashes '\\\\' in PATH OR there are commas ',' missing.")
            TextFileWrite("NEED FOR ACTION: There is no file named 'config_file.json' or the syntax is bad. OR there are not double backslashes '\\\\' in PATH OR there are commas ',' missing.")
            time.sleep(5)
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        
