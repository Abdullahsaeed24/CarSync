import pandas as pd
import datetime
import time
import os
    
Log = { "Date[dd-mm-yy]":[],
        "Time[hh:mm:ss](UTC)":[],
        "IntConnStatus":[],
        "Event":[],
        "Name":[],
        "Path":[]
        }

def main(ConStat, Event, Name='', Path=''):

    
    def AddDate():
        # print('AddDate')
        D = datetime.date.today()
        Log["Date[dd-mm-yy]"].append(D)
    
    
    def AddTime():
        # print('AddTime')
        gmt = time.gmtime(time.time())
        T = str(gmt.tm_hour)+':'+str(gmt.tm_min)+':'+str(gmt.tm_sec)
        Log["Time[hh:mm:ss](UTC)"].append(T)
    
    
    def Add_ConnStatus(S):
        # print('Add_ConnStatus')
        Log["IntConnStatus"].append(S)
    
    
    def Add_Event(E):
        # print('Add_Event')
        Log["Event"].append(E)
        
    def Add_Name(N):
        Log["Name"].append(N)
    
    def Add_Path(P):
        Log["Path"].append(P)
    
    
    def Create_LogFile(Data):
        # print('Create_LogFile')
        # print('Data',Data)
        DataFrame = pd.DataFrame(Data)
        # print('Saving DataFrame to CSV file...')
        # print('Dataframe:',DataFrame)
        file_path = os.path.realpath(os.path.dirname(__file__))
        DataFrame.to_csv(file_path+r"\UploadFolder\LogFile.csv")
         
         
    def writeToCSV(ConStat='Connection status',Event='Default Event',Name='',Path=''):
        AddDate()
        AddTime()
        Add_ConnStatus(ConStat)
        Add_Event(Event)
        Add_Name(Name)
        Add_Path(Path)
        Create_LogFile(Log)
        
    writeToCSV(ConStat, Event, Name, Path)