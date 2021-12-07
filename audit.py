#!/usr/bin/env python

import csv
import os
import os.path
from stat import *
from ast import literal_eval

new_dict = {}
old_dict = {}


def compare_old_and_new():  # function that compares old and new data in specified directory
    for key in new_dict.keys():
        if key not in old_dict.keys():  # checks if new directory/symbolic link/ file was added
            if str(new_dict[key][1])[2] == '4':
                print(f"New directory created at {key} named {new_dict[key][0]}")
            elif str(new_dict[key][1])[3] == '2':
                print(f"New symbolic link created at {key} named {new_dict[key][0]}")
            else:
                print(f"New file created at {key} named {new_dict[key][0]}")
    for key in old_dict.keys():
        if key not in new_dict.keys():  # checks if any directories/symbolic links/ files were deleted
            if str(old_dict[key][1])[2] == '4':
                print(f"The directory {old_dict[key][0]} was deleted at {key}")
            elif str(old_dict[key][1])[3] == '2':
                print(f"The symbolic link {old_dict[key][0]} was deleted at {key}")
            else:
                print(f"The file {old_dict[key][0]} was deleted at {key}")
    for key in new_dict.keys():
        if key in old_dict.keys():  # handles the case for files that existed last login
            if new_dict[key][2] != old_dict[key][2]: # handles the case when a file has changed in size
                if new_dict[key][2] > old_dict[key][2]:  # reports when a file has increased in size
                    if str(old_dict[key][1])[2] == '4':
                        print(
                            f"The directory {new_dict[key][0]} increased in size from {old_dict[key][2]} bytes to {new_dict[key][2]} bytes at {key}")
                    elif str(old_dict[key][1])[3] == '0':
                        print(
                            f"The file {new_dict[key][0]} increased in size from {old_dict[key][2]} bytes to {new_dict[key][2]} bytes at {key}")
                else:  # reports when a file has decreased in size
                    if str(old_dict[key][1])[2] == '4':
                        print(
                            f"The directory {new_dict[key][0]} decreased in size from {old_dict[key][2]} bytes to {new_dict[key][2]} bytes at {key}")
                    elif str(old_dict[key][1])[3] == '0':
                        print(
                            f"The file {new_dict[key][0]} decreased in size from {old_dict[key][2]} bytes to {new_dict[key][2]} bytes at {key}")
            if new_dict[key][1][-1] != old_dict[key][1][-1]:  # reports when a file's permissions have changed
                print(f"{new_dict[key][0]}'s permissions have changed from {old_dict[key][1]} to {new_dict[key][1]} at {key}")
                if int(new_dict[key][1][-1]) == 1:  # reports any changes in the permissions for others 
                    print("\tothers can execute")
                elif int(new_dict[key][1][-1]) == 2:
                    print("\tothers can write")
                elif int(new_dict[key][1][-1]) == 3:
                    print("\tothers can execute and write")
                elif int(new_dict[key][1][-1]) == 4:
                    print("\tothers can read")
                elif int(new_dict[key][1][-1]) == 5:
                    print("\tothers can execute and read")
                elif int(new_dict[key][1][-1]) == 6:
                    print("\tothers can write and read")
                elif int(new_dict[key][1][-1]) == 7:
                    print("\tothers can read, write and execute")
                else:
                    print("\tothers have no permissions")
            if new_dict[key][1][-2] != old_dict[key][1][-2]:  # reports any changes in the permissions for the group
                print(f"{new_dict[key][0]}'s permissions have changed from {old_dict[key][1]} to {new_dict[key][1]}")
                if int(new_dict[key][1][-2]) == 1:
                    print("\tgroup can execute")
                elif int(new_dict[key][1][-2]) == 2:
                    print("\tgroup can write")
                elif int(new_dict[key][1][-2]) == 3:
                    print("\tgroup can execute and write")
                elif int(new_dict[key][1][-2]) == 4:
                    print("\tgroup can read")
                elif int(new_dict[key][1][-2]) == 5:
                    print("\tgroup can execute and read")
                elif int(new_dict[key][1][-2]) == 6:
                    print("\tgroup can write and read")
                elif int(new_dict[key][1][-2]) == 7:
                    print("\tgroup can read, write and execute")
                else:
                    print("\tgroup have no permissions")
            if new_dict[key][1][-3] != old_dict[key][1][-3]:  # reports any changes in the permissions for the owner
                print(f"{new_dict[key][0]}'s permissions have changed from {old_dict[key][1]} to {new_dict[key][1]}")
                if int(new_dict[key][1][-3]) == 1:
                    print("\towner can execute")
                elif int(new_dict[key][1][-3]) == 2:
                    print("\towner can write")
                elif int(new_dict[key][1][-3]) == 3:
                    print("\towner can execute and write")
                elif int(new_dict[key][1][-3]) == 4:
                    print("\towner can read")
                elif int(new_dict[key][1][-3]) == 5:
                    print("\towner can execute and read")
                elif int(new_dict[key][1][-3]) == 6:
                    print("\towner can write and read")
                elif int(new_dict[key][1][-3]) == 7:
                    print("\towner can read, write and execute")
                else:
                    print("\towner have no permissions")


def read_from_file(filepath):  # reads from the previously created "database" and puts the information into a dictionary
    try:
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                k, v = row
                old_dict[k] = literal_eval(v)
    except IOError:
        print("I/O error")


def write_to_file(filepath):  # writes the current information about the file system into a csv file which will act as the "database"
    try:
        with open(filepath, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for data, value in new_dict.items():
                writer.writerow([data, value])
    except IOError:
        print("I/O error")


def recursive(path):  # function that recurses through all directories and subdirectories
    obj = os.scandir(path)  # creates a stream from everything in the path

    for entry in obj:  # loops through everything in the current path
        if entry.is_symlink():  # adds symoblic links to dictionary
            new_dict[f"{path}/{entry.name}"] = [entry.name, oct(os.lstat(entry)[ST_MODE]), os.lstat(entry)[ST_SIZE]]
        if entry.is_dir(follow_symlinks=False):  # adds directories to dictionary, ignoring symoblic links
            new_dict[f"{path}/{entry.name}"] = [entry.name, oct(os.stat(entry)[ST_MODE]), os.stat(entry)[ST_SIZE]]
            recursive(path + '/' + entry.name)  # calls the recursive function again from the directory we have found
        elif entry.is_file(follow_symlinks=False):  # adds files to dictionary, ignoring symoblic links
            new_dict[f"{path}/{entry.name}"] = [entry.name, oct(os.stat(entry)[ST_MODE]), os.stat(entry)[ST_SIZE]]


def main(path):
    recursive(path)  # gets information about current filesystem
    filePath = os.path.join(path, "audit.csv")
    if not os.path.exists(filePath):  # checks if we have already auditted the desired directory
        write_to_file(filePath)  # creates new database in the path to compare for next time
        print("This program will begin an audit from your specified path upon login")
    else:
        read_from_file(filePath)  # if already auditted, read from the database
        compare_old_and_new()  # compares the past filesystem information to the current and reports changes
        write_to_file(filePath)  # writes the current system information to the database
        print("Audit completed")


if __name__ == "__main__":
    # CHANGE PATH TO THE DESIRED DIRECTORY TO SCAN
    path = '/home/ironsj/'

    main(path)
