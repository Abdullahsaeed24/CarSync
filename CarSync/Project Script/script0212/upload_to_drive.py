# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 09:03:20 2022

@author: tnejedly
"""

#!/usr/bin/python3

"""Example cooment to make pylint stop giving me errors."""

import datetime
import hashlib
import mimetypes
import time
import sys,os
import httplib2
import shared_data as sd
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
# from oauth2client.tools import run

from oauth2client.file import Storage
from apiclient.http import MediaFileUpload
# Import our folder uploading script
# import initial_upload
import requests
import json
import platform
import socket
from urllib.request import urlopen

import dataframe_script
#import socket

PC_NAME = platform.node()
def Uploading(FULL_PATH):
    """Input of this function is a full path of the folder that will be uploaded.
       The path is written in the text file, which is the only input to the script
    """

    # dataframe_script.main("test1","test2")

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/drive-python-quickstart.json
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
              'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive']
    # client secret destination is in the folder with the script
    CLIENT_SECRET_FILE = os.path.realpath(os.path.dirname(__file__)) + r"\client_secret.json"
    # google application name
    APPLICATION_NAME = 'CarsDataSyncApp'
    
    # DIR_NAME is a name of the root folder that will be uploaded (last folder in the full path)
#    DIR_NAME = "UploadToDriveTestFolder"
    try:    
        DIR_NAME = FULL_PATH.split('\\')[-1]
    except:
        print("Path must be correct (string).")


    def Check_Internet_Connection_IP():
        try:
            #explanation in Internet_Connection.py script
            IPaddress=socket.gethostbyname(socket.gethostname())
            if IPaddress=="127.0.0.1":     
                sd.Internet_Connection_Status_IP = sd.Connection_Status_IP.NOT_CONNECTED
                sd.Program_State = sd.program_States.CHECK_CONNECTION
                return False
            else:
                sd.Internet_Connection_Status_IP = sd.Connection_Status_IP.CONNECTED
                sd.Program_State = sd.program_States.UPLOAD
                return True
        except Exception as e:
            print("Error while checking internet connection by IP address:",e)
            connection = Check_both_URL_IP()
            message = "Error while checking internet connection by IP address: "+str(e)
            dataframe_script.main(connection, message)
            
    def Check_Internet_Connection():
        #explanation in Internet_Connection.py script
        try:
            global Internet_Connection_Status
            while True:
                    global Internet_Connection_Status
                    try:
                        response = urlopen('https://www.google.com/', timeout = 5)
                        Internet_Connection_Status = sd.Connection_Status.CONNECTED
                        return True
                    except:
                        Internet_Connection_Status = sd.Connection_Status.NOT_CONNECTED
                        return False
        except Exception as e:
            print("Error while checking internet connection by responsing to url address:",e)
            connection = Check_both_URL_IP()
            message = "Error while checking internet connection bz responsing to url address: "+str(e)
            dataframe_script.main(connection,message)
    
    def Check_both_URL_IP():
        try:
            file_path = os.path.realpath(os.path.dirname(__file__))
            e = datetime.datetime.utcnow()
            Connection_IP = Check_Internet_Connection_IP()
            Connection_URL = Check_Internet_Connection()
            if Connection_IP and Connection_URL:
                with open(file_path+"\ConnectionStatus.txt", "a+") as f:
                    f.write(str(e)+"(UTC)"+" Connected\n")
                print(str(e)+"(UTC)"+" Internet Connected")
                return True
            else:
                with open(file_path+"\ConnectionStatus.txt", "a+") as f:
                    f.write(str(e)+"(UTC)"+" Internet NOT Connected\n")
                print(str(e)+"(UTC)"+" Internet NOT Connected")
                return False
        except Exception as e:
            print("Error while checking internet connection:",e)
            connection = Check_both_URL_IP()
            message = "Error while checking internet connection: "+str(e)
            dataframe_script.main(connection,message)

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
            print("Error while writing to changelog.txt:",e)
            connection = Check_both_URL_IP()
            message = "Error while writing to changelog.txt: "+str(e)
            dataframe_script.main(connection,message)         
            
    def folder_upload(service):
        '''Uploads folder and all it's content (if it doesnt exists)
        in root folder.
        Args:
            items: List of folders in root path on Google Drive.
            service: Google Drive service instance.
        Returns:
            Dictionary, where keys are folder's names
            and values are id's of these folders.
        '''
        
        #check if uploading is done and the script is ready for next uploading. 
        try:
            if  sd.Uploading_Folder_state == sd.Uploading_Folder_Status.FOLDER_UPLOADING_DONE:
                # when uploading is done, another can begin
                sd.Uploading_Folder_state = sd.Uploading_Folder_Status.FOLDER_UPLOADING_NOT_DONE
            
            parents_id = {}
            #OS.walk() generate the file names in a directory tree by walking the tree either top-down or bottom-up. 
            #For each directory in the tree rooted at directory top (including top itself), 
            #it yields a 3-tuple (dirpath, dirnames, filenames).
            for root, _, files in os.walk(FULL_PATH, topdown=True):
                last_dir = root.split('\\')[-1] # pick name of last directory
                pre_last_dir = root.split('\\')[-2] # pick name of pre-last dir. (parent of the last)
                if pre_last_dir not in parents_id.keys(): 
                    pre_last_dir = []
                else:
                    pre_last_dir = parents_id[pre_last_dir]
                    
                #folder_metadata are used for creating folder (it needs name, parent and type)
                folder_metadata = {'name': last_dir,
                                   'parents': [pre_last_dir],
                                   'mimeType': 'application/vnd.google-apps.folder'}
                print("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" CREATING NEW FOLDER: "+str(folder_metadata['name']))
                TextFileWrite("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" CREATING NEW FOLDER: "+str(folder_metadata['name']))
                connection = Check_both_URL_IP()
                message = "CREATING NEW FOLDER"
                name = str(folder_metadata['name'])
                dataframe_script.main(connection,message,name)
                #creating new folder
                create_folder = service.files().create(body=folder_metadata,
                                                       fields='id').execute()
                folder_id = create_folder.get('id', []) #findin out an id of new folder
                parents_id[last_dir] = folder_id 
            sd.Uploading_Folder_state = sd.Uploading_Folder_Status.FOLDER_UPLOADING_DONE #uploading done, another can begin
            return parents_id
        except Exception as e:
            print("Error while creating new folder in drive (folder_upload() function)")
            print(e)
            connection = Check_both_URL_IP()
            message = "Error while creating new folder in drive (folder_upload() function)"
            dataframe_script.main(connection,message)
        
    
    
    def check_upload(service):
        """This function reads google drive folders and return their id
        """     
        try:
            if Check_both_URL_IP():
                results = service.files().list(
                    pageSize=100,
                    q="'root' in parents and trashed != True and \
                    mimeType='application/vnd.google-apps.folder'").execute()
                items = results.get('files', [])
                # return items
    #        print("check_upload items:",items)
            # Check if folder exists, and then create it or get this folder's id.    
                if DIR_NAME in [item['name'] for item in items]:
                    folder_id = [item['id'] for item in items
                                 if item['name'] == DIR_NAME][0]
                else:
                    parents_id = folder_upload(service)
                    folder_id = parents_id[DIR_NAME]
            
                return folder_id#, FULL_PATH
        except Exception as e:
            print("Error while checking folders on google drive:",e)
            connection = Check_both_URL_IP()
            message = "Error while checking folders on google drive: "+str(e)
            dataframe_script.main(connection,message)
            
    def get_credentials():
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Returns:
            Credentials, the obtained credential.
        """
        try:
            home_dir = os.path.expanduser('~')
            credential_dir = os.path.join(home_dir, '.credentials')
            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir,
                                           'drive-python-sync.json')
            
            store = Storage(credential_path)
            credentials = store.get()
            if not credentials or credentials.invalid:
                flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
                flow.user_agent = APPLICATION_NAME
                credentials = tools.run_flow(flow, store, flags=None)
            return credentials
        except Exception as e:
            print("Error while getting credentials:",e)
            connection = Check_both_URL_IP()
            message = "Error while getting credentials: "+str(e)
            dataframe_script.main(connection,message)
        
    def get_tree(folder_name, tree_list, root, parents_id, service):
        """Gets folder tree relative paths.
        Recursively gets through subfolders, remembers their names ad ID's.
        Args:
            folder_name: Name of folder, initially
            name of parent folder string.
            folder_id: ID of folder, initially ID of parent folder.
            tree_list: List of relative folder paths, initially
            empy list.
            root: Current relative folder path, initially empty string.
            parents_id: Dictionary with pairs of {key:value} like
            {folder's name: folder's Drive ID}, initially empty dict.
            service: Google Drive service instance.
        Returns:
            List of folder tree relative folder paths.
        """
        try:
            folder_id = parents_id[folder_name]
            if Check_both_URL_IP():
                results = service.files().list(
                    pageSize=1000,
                    q=("%r in parents and \
                    mimeType = 'application/vnd.google-apps.folder'and \
                    trashed != True" % folder_id)).execute()
            
                items = results.get('files', [])
                # return items
    #        print("get_tree items:",items)
                root += folder_name + os.path.sep
        
                for item in items:
                    parents_id[item['name']] = item['id']
                    tree_list.append(root + item['name'])
                    folder_id = [i['id'] for i in items
                                 if i['name'] == item['name']][0]
                    folder_name = item['name']
                    get_tree(folder_name, tree_list,
                             root, parents_id, service)
        except Exception as e:
            print("Error while getting folder structure on google drive:",e)
            connection = Check_both_URL_IP()
            message = "Error while getting folder structure on google drive"+str(e)
            dataframe_script.main(connection,message)
    
    def by_lines(input_str):
        """Helps Sort items by the number of slashes in it.
        Returns:
            Number of slashes in string.
        """
        return input_str.count(os.path.sep)
            
    
    def main_upload():
        print("--------start of main_upload()--------")
        """Syncronizes computer folder with Google Drive folder.
        Checks files if they exist, uploads new files and subfolders,
        deletes old files from Google Drive and refreshes existing stuff.
        """
        
        # dataframe_script.main('test1','test2')
        
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)

        #this line deletes trash
        service.files().emptyTrash().execute()
        
        # Get id of Google Drive folder and it's path (from other script)
        # folder_id, full_path = initial_upload.check_upload(service)
        sd.Uploading_file_state = sd.Uploading_File_Status.FILE_UPLOADING_DONE
        
        folder_id = check_upload(service)
        folder_name = FULL_PATH.split(os.path.sep)[-1]
        tree_list = []
        root = ''
        parents_id = {}
    
        parents_id[folder_name] = folder_id
        get_tree(folder_name, tree_list, root, parents_id, service)
        os_tree_list = []
        root_len = len(FULL_PATH.split(os.path.sep)[0:-2])

            # Get list of folders three paths on computer
        for root, dirs, files in os.walk(FULL_PATH, topdown=True):
            for name in dirs:
                var_path = (os.path.sep).join(
                    root.split(os.path.sep)[root_len + 1:])
                os_tree_list.append(os.path.join(var_path, name))
        
        # new folders on drive, which you dont have(i suppose hehe)
        upload_folders = list(set(os_tree_list).difference(set(tree_list)))
        # foldes that match
        exact_folders = list(set(os_tree_list).intersection(set(tree_list)))
        # Add starting directory
        exact_folders.append(folder_name)
        print("exact_folders start:",exact_folders)
        # Sort uploadable folders
        # so now in can be upload from top to down of tree
        upload_folders = sorted(upload_folders, key=by_lines)
        print("upload_folders start:")
        for i in upload_folders:
            print(i)
        
###############################################################################
#                      creating new folder to the cloud                       #  
###############################################################################         
        # Here we upload new (abcent on Drive) folders
        for folder_dir in upload_folders:
            try:
                print("folder that will be uploaded:", folder_dir)
                # time.sleep(5)
                var = os.path.join(os.path.join("C:\\", *FULL_PATH.split(os.path.sep)[0:-1])) + os.path.sep
                variable = var + folder_dir
                last_dir = folder_dir.split(os.path.sep)[-1]
                pre_last_dir = folder_dir.split(os.path.sep)[-2]
                folder_metadata = {'name': last_dir,
                                   'parents': [parents_id[pre_last_dir]],
                                   'mimeType': 'application/vnd.google-apps.folder'}
                print("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" UPLOADING NEW FOLDER:", folder_metadata['name']+" in "+str(pre_last_dir))
                TextFileWrite("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" UPLOADING NEW FOLDER: "+str(folder_metadata['name'])+" in "+str(variable))
    
                connection = Check_both_URL_IP()
                message = "UPLOADING NEW FOLDER"
                name = str(folder_metadata['name'])
                path = str(variable)
                dataframe_script.main(connection,message,name,path)
                
                parent_id = folder_metadata['parents'][0]
                if Check_both_URL_IP():
                    results = service.files().list(
                        pageSize=100,
                        q="parents in '"+parent_id+"' and trashed != True and \
                        mimeType='application/vnd.google-apps.folder'").execute()
                    items = results.get('files', [])
      
                foldersOnDrive = list()
                for item in items:
                    foldersOnDrive.append(item['name'])
                print("Folders on drive before uploading new one:", foldersOnDrive)
    
                if folder_metadata['name'] not in foldersOnDrive:
                    print("folder "+str(folder_metadata['name'])+" is not on cloud and will be uploaded.")
                    create_folder = service.files().create(
                        body=folder_metadata, fields='id').execute()
                    folder_id = create_folder.get('id', [])
                    parents_id[last_dir] = folder_id            
                
                    if Check_both_URL_IP():
                        results = service.files().list(
                            pageSize=100,
                            q="parents in '"+parent_id+"' and trashed != True and \
                            mimeType='application/vnd.google-apps.folder'").execute()
                        items = results.get('files', [])
                
                    foldersUploadedOnDrive = list()
                    for item in items:
                        foldersUploadedOnDrive.append(item['name'])
                    print("Folders on drive after uploading:", foldersUploadedOnDrive)
                    # time.sleep(3)
                    if folder_metadata['name'] in foldersUploadedOnDrive:
                        print("Folder was uploaded SUCCESSFULLY.")
                        connection = Check_both_URL_IP()
                        message = "Folder was uploaded SUCCESSFULLY."
                        name = str(folder_metadata['name'])
                        path = str(variable)
                        dataframe_script.main(connection,message,name,path)
            except Exception as e:
                print("Error while uploading new folder:",e)
                connection = Check_both_URL_IP()
                message = "Error while uploading new folder"+str(e)
                dataframe_script.main(connection,message)
###############################################################################
#                   comparing existing files in the folder                    #  
############################################################################### 
        # Check files in existed folders and replace them
        # with newer versions if needed
        for folder_dir in exact_folders:
            try:
                var = (os.path.sep).join(FULL_PATH.split(
                    os.path.sep)[0:-1]) + os.path.sep
        
                variable = var + folder_dir
                last_dir = folder_dir.split(os.path.sep)[-1]
                print("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" COMPARING: "+str(variable))
                TextFileWrite("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" COMPARING: "+str(variable))
                
                connection = Check_both_URL_IP()
                message = "COMPARING"
                path = str(variable)
                dataframe_script.main(connection,message,path)
                
                try:
                    os_files = [f for f in os.listdir(variable)
                                if os.path.isfile(os.path.join(variable, f))]
                    # for os_file in os_files:
                        # print("OS_FILE:", os_file)
                except:
                    print("!!!!! PATH DOESNT EXIST !!!!!")
                    connection = Check_both_URL_IP()
                    message = "!!! PATH of folder for upload is missing !!!"
                    dataframe_script.main(connection,message)
                    sys.exit()
                if Check_both_URL_IP():
                    results = service.files().list(
                        pageSize=1000, q=('%r in parents and \
                        mimeType!="application/vnd.google-apps.folder" and \
                        trashed != True' % parents_id[last_dir]),
                        fields="files(id, name, mimeType, \
                        modifiedTime, md5Checksum)").execute()
                    items = results.get('files', [])
                
                refresh_files = [f for f in items if f['name'] in os_files]                
                upload_files = [f for f in os_files
                                if f not in [j['name'] for j in items]]
            except Exception as e:
                print("Error while comparing file:",e)
                connection = Check_both_URL_IP()
                message = "Error while comparing file: "+str(e)
                dataframe_script.main(connection,message)
###############################################################################
#                   refreshing existing files in the folder                   #  
###############################################################################  
            # Check files that exist both on Drive and on PC
            for drive_file in refresh_files:
                # print("FOR refreshing")
                file_dir = os.path.join(variable, drive_file['name'])
                try:
                    os_file_md5 = hashlib.md5(open(file_dir, 'rb').read()).hexdigest()
                    if 'md5Checksum' in drive_file.keys():
                        # print(1, file['md5Checksum'])
                        drive_md5 = drive_file['md5Checksum']
                        # print(2, os_file_md5)
                    else:
                        # print('No hash')
                        drive_md5 = None
                        # print(drive_md5 != os_file_md5)
        
                    if (drive_md5 != os_file_md5):# or (file_time > drive_time):
                        print(">>> drive_md5: "+str(drive_md5)+" | os_file_md5: "+str(os_file_md5))
                        # In the IF statement is an option to update file regarding to its time.
                        # But the time will be different everytime, so it will update every time.
                        # That means its slow and not optimal. It is in the older version of the code
                        print("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" REFRESHING: "+str(drive_file['name'])+" in "+str(variable))
                        if drive_file['name'] != 'changelog.txt':
                            TextFileWrite("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" REFRESHING: "+str(drive_file['name'])+" in "+str(variable))
                            connection = Check_both_URL_IP()
                            message = "REFRESHING"
                            name = str(drive_file['name'])
                            path = str(variable)
                            dataframe_script.main(connection,message,name,path)    
        
                        file_id = [f['id'] for f in items
                                   if f['name'] == drive_file['name']][0]
                        file_mime = [f['mimeType'] for f in items
                                     if f['name'] == drive_file['name']][0]
        
                        # File's new content.
                        # file_mime = mimetypes.MimeTypes().guess_type(file_dir)[0]
                        file_metadata = {'name': drive_file['name'],
                                         'parents': [parents_id[last_dir]]}
    
                        media_body = MediaFileUpload(file_dir, mimetype=file_mime)
                        if Check_both_URL_IP():
                            print("Start refreshing file.")
                            service.files().update(fileId=file_id,
                                                   media_body=media_body,
                                                   fields='id').execute()
                            print("End of refreshing.")
                except Exception as e:
                    print("Error while refreshing file:",e)
                    connection = Check_both_URL_IP()
                    message = "Error while refreshing file: "+str(e)
                    dataframe_script.main(connection,message)
###############################################################################
#                   uploading missing files to the folder                     #  
###############################################################################    
            def FilesOnDrive(parents):
                if Check_both_URL_IP():
                    results = service.files().list(
                        pageSize=1000, q=('%r in parents and \
                        mimeType!="application/vnd.google-apps.folder" and \
                        trashed != True' % parents),
                        fields="files(id, name, mimeType, \
                        modifiedTime, md5Checksum)").execute()
                    items = results.get('files', []) 
                return items
               
            for os_file in upload_files:
                # print("FOR upload")
                # time.sleep(3)
                print("Uploading state before check:",sd.Uploading_file_state)
                # time.sleep(3)
                if sd.Uploading_file_state == sd.Uploading_File_Status.FILE_UPLOADING_DONE:
                    sd.Uploading_file_state = sd.Uploading_File_Status.FILE_UPLOADING_NOT_DONE
                    print("Uploading state after check:", sd.Uploading_file_state)
                    time.sleep(3)
                    print('os_file that we want upload:',os_file)
                    time.sleep(3)
                    try:                        
                        file_name, file_extension = os.path.splitext(os_file)
                        if str(file_extension) == '.csv' or os_file == 'changelog.txt' or os_file == 'ConnectionStatus.txt':
                            file_dir = os.path.join(variable, os_file)
                            filemime = mimetypes.MimeTypes().guess_type(file_dir)[0]
                            file_metadata = {'name': os_file,
                                             'parents': [parents_id[last_dir]]}
                            print("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" UPLOADING NEW FILE: "+str(file_metadata['name'])+" in "+str(variable))
                            TextFileWrite("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" UPLOADING NEW FILE: "+str(file_metadata['name'])+" in "+str(variable))
                            connection = Check_both_URL_IP()
                            message = "UPLOADING NEW FILE"
                            name = str(file_metadata['name'])
                            path = str(variable)
                            dataframe_script.main(connection,message,name,path)
                            media_body = MediaFileUpload(file_dir, mimetype=filemime)
                            items = FilesOnDrive(parents_id[last_dir])
                            
                            #checking if google drive folder is empty, if so, upload first file there
                            if len(items) == None or len(items) == 0:
                                print("There is nothing on the google drive folder (Items len() is None or 0).")
                                if Check_both_URL_IP():
                                    print("Start of uploading file")
                                    service.files().create(body=file_metadata,
                                                            media_body=media_body,
                                                            fields='id').execute()
                                    print("End of uploading file")
                                    #double check if file was uploaded
                                    #read names of files on the drive
                                    print("Checking drive after upload")
                                    itemsAfterUpload = FilesOnDrive(parents_id[last_dir])
                                    itemsOnCloudAfterUpload = list()
                                    for item in itemsAfterUpload:
                                        itemsOnCloudAfterUpload.append(item['name'])
                                    print("Items on drive after upload:",itemsOnCloudAfterUpload)
                                    #check if the file we were uploading is on google drive
                                    if os_file in itemsOnCloudAfterUpload:
                                        print("***"+str(os_file)+" UPLOADED SUCCESSFULLY.***")
                                        TextFileWrite("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" SUCCESSFUL UPLOAD: "+str(file_metadata['name'])+" in "+str(variable))
                                        connection = Check_both_URL_IP()
                                        message = "SUCCESSFUL UPLOAD"
                                        name = str(file_metadata['name'])
                                        path =str(variable)
                                        dataframe_script.main(connection,message,name,path)
                                        sd.Uploading_file_state = sd.Uploading_File_Status.FILE_UPLOADING_DONE
                                        print("Uploading done, status is now:", sd.Uploading_file_state)
                            # else:
                                # print("!@#$!@#$!@#$!@#$@!#$@#$@#$@#!$!@#$!@#$@#!$@!#@!#$")
                            #     #file is already on the google drive
                            #     sd.Uploading_file_state = sd.Uploading_File_Status.FILE_UPLOADING_DONE
                            #     print(str(os_file)+" is already uploaded on the drive.")
                            #     time.sleep(3)
    
                            #if there is something on the cloud already, take names of the files
                            itemsOnCloud = list()
                            if len(items) != None or len(items) != 0:
                                items = FilesOnDrive(parents_id[last_dir])
                                for item in items:
                                    itemsOnCloud.append(item['name'])
                                print("items already uploaded on the drive:", itemsOnCloud)
                                time.sleep(3)
                                #check if the file is among the files that are on the drive. If not, it will be uploaded.
                                if os_file not in itemsOnCloud:
                                    print(str(os_file)+" is not uploaded yet but will be uploaded now.")
                                    time.sleep(3)
                                    if Check_both_URL_IP():
                                        print("Start of uploading file")
                                        service.files().create(body=file_metadata,
                                                                media_body=media_body,
                                                                fields='id').execute()
                                        print("End of uploading file")
                                    #double check if file was uploaded
                                    #read names of files on the drive
                                    print("Checking drive after upload")
                                    itemsAfterUpload = FilesOnDrive(parents_id[last_dir])
                                    itemsOnCloudAfterUpload = list()
                                    for item in itemsAfterUpload:
                                        itemsOnCloudAfterUpload.append(item['name'])
                                    print("Items on drive after upload:",itemsOnCloudAfterUpload)
                                    #check if the file we were uploading is on google drive
                                    if os_file in itemsOnCloudAfterUpload:
                                        print("***"+str(os_file)+" UPLOADED SUCCESSFULLY.***")
                                        TextFileWrite("---> "+str(datetime.datetime.utcnow())+"(UTC)"+" SUCCESSFUL UPLOAD: "+str(file_metadata['name'])+" in "+str(variable))
                                        connection = Check_both_URL_IP()
                                        message = "SUCCESSFUL UPLOAD"
                                        name = str(file_metadata['name'])
                                        path = str(variable)
                                        dataframe_script.main(connection,message)
                                        sd.Uploading_file_state = sd.Uploading_File_Status.FILE_UPLOADING_DONE
                                        print("Uploading done, status is now:", sd.Uploading_file_state)
                                else:
                                    #file is already on the google drive
                                    sd.Uploading_file_state = sd.Uploading_File_Status.FILE_UPLOADING_DONE
                                    print(str(os_file)+" is already uploaded on the drive.")
                                    time.sleep(3)
                    except Exception as e:
                        connection = Check_both_URL_IP()
                        message = "Error while uploading file: "+str(e)
                        dataframe_script.main(connection,message)
                        print("Error while uploading file:",e)
                    
    # try:
    main_upload()
    # except Exception as e:
        # print("error2",e)

while(1):
    FULL_PATH = r"C:\Users\tnejedly\Desktop\Script29_11\UploadFolder"
    Uploading(FULL_PATH)
    time.sleep(5)