"""
The objective of this script will be to create an experiment folder with duplicate raw files renamed
to actual experiments.


Created on Mon June 4th 11:42AM 2018

@author: Dolu Obatusin

"""

# import required modules / libraries
import os
# import numpy as np
# import json
import re
from datetime import datetime
import shutil
import json
import sys
import getopt
import errno


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

# Function to get timestamps from log file


def ins_enable_timestamps(log_file):
    global datetime_object1
    pattern = re.compile("Enable Sensing")
    for i, line in enumerate(open(log_file)):
        for match in re.finditer(pattern, line):
            t_sensing = line[15:]
            datetime_object1 = datetime.strptime(t_sensing.strip(), '%m/%d/%Y %I:%M:%S %p')
    #             print("Enable Sensing:",datetime_object2)

    pattern = re.compile("INS TimeStamp")
    for i, line in enumerate(open(log_file)):
        for match in re.finditer(pattern, line):
            t_ins = line[14:]
            datetime_object2 = datetime.strptime(t_ins.strip(), '%m/%d/%Y %I:%M:%S %p')
    #             print("INS TimeStamp:",datetime_object1)
    #         print('Found on line %s' % (i+1))

    # Convert Enable Sensing to datetime

    return [datetime_object1, datetime_object2]

# Function to create log dictionary


def create_logdict(inputfile):
    log_files = []
    logfile_dict = {}
    for path, directories, files in os.walk(inputfile, topdown=True):
        if files:
            for f in files:
                if f.endswith('LOG.txt'):
                    log_files.append(f)
                    logfile_dict[path] = log_files
            log_files = []
    return logfile_dict

# Create a data dictionary of path and log files - only include paths that have log files

def createpathfiles(inputfile):
    global new_folder
    logfile_dict = create_logdict(inputfile)

    pathfiles_dict = {}
    path_files = []
    errorfiles = []
    # Operate according to each path
    for key in logfile_dict:
    #     print(key)

    # create a folder in path based on log file
        for k in logfile_dict[key]:
    #         print(k)
            log_file = key + '/'+ k
            if k.endswith('LOG.txt'):
    #             pass
                new_folder = log_file.strip('_LOG.txt')
                if not(os.path.exists(new_folder)):
                    os.makedirs(new_folder)
    # Get INS & Sensing start time from log file
    #         print(log_file)
            datetime_object1, datetime_object2 = ins_enable_timestamps(log_file)
    #         print(datetime_object1)
    #         print(datetime_object2)
    # Loop through path to get all files
    #     print( ' ')
            for path, directories, files in os.walk(key, topdown=True):
                if files:
#                     print(files)
                    for f in files:
                        if f.endswith('.xml') or f.endswith('.txt'):
#                             print(f)
                            try:
                                datetime_object3 = datetime.strptime(f[6:27], '_%Y_%m_%d_%H_%M_%S_')
#                                 print(f,'--',datetime_object3)
                                if datetime_object1 <= datetime_object3 <= datetime_object2:
                                    path_files.append( key + '/'+ f)
                                    pathfiles_dict[new_folder] = path_files
                            except ValueError:
                                errorfiles.append(f)
                        else:
                            continue

        # compare each file's timestamp to INS & Sensing starttime and add to dictionary of {new folder: files}

                    path_files = []
    return pathfiles_dict, errorfiles


# Finally move files into their respective session folders


def movefiles(pathfiles_dict):
    for key in pathfiles_dict:
        print(key)
        print('-'*40)
        for i in pathfiles_dict[key]:
            #         print(i)
            if os.path.exists(i):
                shutil.move(i, key)
            else:
                continue

# # Get the file name for the new file to write


def mapfolder(inputfile,pathfiles_dict):
    patient_id = os.path.basename(inputfile)
    dst = inputfile + '/' + patient_id + '_' + 'pathfiles.txt'
    # Save map to text file
    # If the file name exists, write a JSON string into the file.
    if dst:
        # Writing JSON data
        with open(dst, 'w') as f:
            json.dump(pathfiles_dict, f) # use `json.loads` to do the reverse


"""Collect command-line options in a dictionary"""

# Function to check if path ends in DBSXXX


def checkid(inputfile):
    patiendID = os.path.basename(inputfile)
    # print(patiendID)
    pattern = re.compile("DBS\d")
    for match in re.finditer(pattern, inputfile):
        patientIDMatch = inputfile[match.span()[0]:]
        # print(patientIDMatch)
        if patientIDMatch == patiendID:
            print("Please wait...")
            logfile_dict = create_logdict(inputfile)
            pathfiles_dict, errorfiles = createpathfiles(inputfile)
            movefiles(pathfiles_dict)
            mapfolder(inputfile,pathfiles_dict)
        else:
            print('File path must point to patient folder (i.e. DBSXXX)')


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('rawtoexperiment.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('rawtoexperiment.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file is "', inputfile)
    print('Output file is "', outputfile)

    if not(os.path.exists(inputfile)):
        print('Path not found')
    else:
        checkid(inputfile)
        "Complete"


if __name__ == "__main__":
    main(sys.argv[1:])


