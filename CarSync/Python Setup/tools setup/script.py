"""
=========================================================================================================
* script.py
* Created: 29/11/2022 1:49 PM
* Author: Abdallah ISMAIL
=========================================================================================================
this is simple python script that aim to do 2 missions with handling thier Exceptions
The script missions are as following
1. Find the python Directory @ the current machine
2. Read the "requirement.txt" file that excist @ the same Directory and has the Required libraries
3. merge every requirement item and write them as command @ the setup.bat
"""

"""it worth noting that these tools are by default installed with the python visrion (3.10.4 or 3.10.5 are Recommended visrions)."""

import os
import sys

# to store the Directories
pythdir=[]

PATH = None
# to strore requirements
reqlist = []

# global Error variable to store the statues of the project and stop immediatly if Error happend
IsError = None


# access the batchfile.txt read the setup file Directory
try:

    #Batch_Directory = open('batchfile.txt','r')
    Batch_Directory = os.getcwd()+"\setup.bat"
    Batch_Directory = Batch_Directory.read()
    print(Batch_Directory)
    IsError = False

# if there is any error happend raise Exception
except Exception as E:
    IsError = True
    print("Error happend... {}.".format(E))



# find the python path
try:

    for u in sys.path:
        pythdir.append(u)

        print(u)
    print(len(pythdir))
    IsError = False

except Exception as E:

    IsError = True
    print("Error happend... {}.".format(E))



# if there is no error happend write commands @ setup.bat
if (not IsError ) :

    firstline ="@ECHO OFF\n"
    lastline = "pause"



    try:
        requirementsfile =open('requirements.txt','r')

        for line in requirementsfile:
            print(line.strip())
            reqlist.append(line.strip())

    except Exception as E:
        print(E)

    try:
        myBat = open(Batch_Directory,'w')
        myBat.writelines(firstline)
    except Exception as E:
        print(E)

    for i in range(len(pythdir)):

        if pythdir[i][-2:-1] == "\\":
            PATH = pythdir[i] + "pip install "
        else:
            PATH = pythdir[i]+"\\"+ "pip install "

        for line in reqlist:
            print(PATH+line.strip())
            myBat.writelines(PATH+line.strip())
            myBat.write("\n")

        print("***"*50)

    for i in range(len(pythdir)):

        if pythdir[i][-2:-1] == "\\":
            PATH = pythdir[i] + "scripts\pip install "
        else:
            PATH = pythdir[i]+"\\"+ "scripts\pip install "

        for line in reqlist:
            print(PATH+line.strip())
            myBat.writelines(PATH+line.strip())
            myBat.write("\n")

        print("###"*50)

    myBat.write(lastline)
    # close the opend files
    myBat.close()
    requirementsfile.close()
print("Going to run .bat file.")
os.system("setup.bat")
print("Finished running .bat file.")
