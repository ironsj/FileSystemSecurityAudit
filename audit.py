#!/usr/bin/env python

import csv
import os
import os.path
from stat import *
from ast import literal_eval

dict = {}
old_dict = {}


def compare_old_and_new():
    for key in dict.keys():
        if key not in old_dict.keys():
            if str(dict[key][1])[2] == '4':
                print(f"New directory created at {key} named {dict[key][0]}")
            elif str(dict[key][1])[3] == '2':
                print(f"New symbolic link created at {key} named {dict[key][0]}")
            else:
                print(f"New file created at {key} named {dict[key][0]}")
    for key in old_dict.keys():
        if key not in dict.keys():
            if str(old_dict[key][1])[2] == '4':
                print(f"The directory {old_dict[key][0]} was deleted at {key}")
            elif str(old_dict[key][1])[3] == '2':
                print(f"The symbolic link {old_dict[key][0]} was deleted at {key}")
            else:
                print(f"The file {old_dict[key][0]} was deleted at {key}")
    for key in dict.keys():
        if key in old_dict.keys():
            if dict[key][2] != old_dict[key][2]:
                if dict[key][2] > old_dict[key][2]:
                    if str(old_dict[key][1])[2] == '4':
                        print(f"The directory {dict[key][0]} increased in size from {old_dict[key][2]} bytes to {dict[key][2]} bytes at {key}")
                    else:
                        print(f"The file {dict[key][0]} increased in size from {old_dict[key][2]} bytes to {dict[key][2]} bytes at {key}")
                else:
                    if str(old_dict[key][1])[2] == '4':
                        print(f"The directory {dict[key][0]} decreased in size from {old_dict[key][2]} bytes to {dict[key][2]} bytes at {key}")
                    else:
                        print(f"The file {dict[key][0]} decreased in size from {old_dict[key][2]} bytes to {dict[key][2]} bytes at {key}")
            if dict[key][1][-1] != old_dict[key][1][-1]:
                print(f"{dict[key][0]}'s permissions have changed from {old_dict[key][1]} to {dict[key][1]} at {key}")
                if int(dict[key][1][-1]) == 1:
                    print("\tothers can execute")
                elif int(dict[key][1][-1]) == 2:
                    print("\tothers can write")
                elif int(dict[key][1][-1]) == 3:
                    print("\tothers can execute and write")
                elif int(dict[key][1][-1]) == 4:
                    print("\tothers can read")
                elif int(dict[key][1][-1]) == 5:
                    print("\tothers can execute and read")
                elif int(dict[key][1][-1]) == 6:
                    print("\tothers can write and read")
                elif int(dict[key][1][-1]) == 7:
                    print("\tothers can read, write and execute")
                else:
                    print("\tothers have no permissions")
            if dict[key][1][-2] != old_dict[key][1][-2]:
                print(f"{dict[key][0]}'s permissions have changed from {old_dict[key][1]} to {dict[key][1]}")
                if int(dict[key][1][-2]) == 1:
                    print("\tgroup can execute")
                elif int(dict[key][1][-2]) == 2:
                    print("\tgroup can write")
                elif int(dict[key][1][-2]) == 3:
                    print("\tgroup can execute and write")
                elif int(dict[key][1][-2]) == 4:
                    print("\tgroup can read")
                elif int(dict[key][1][-2]) == 5:
                    print("\tgroup can execute and read")
                elif int(dict[key][1][-2]) == 6:
                    print("\tgroup can write and read")
                elif int(dict[key][1][-2]) == 7:
                    print("\tgroup can read, write and execute")
                else:
                    print("\tgroup have no permissions")
            if dict[key][1][-3] != old_dict[key][1][-3]:
                print(f"{dict[key][0]}'s permissions have changed from {old_dict[key][1]} to {dict[key][1]}")
                if int(dict[key][1][-3]) == 1:
                    print("\towner can execute")
                elif int(dict[key][1][-3]) == 2:
                    print("\towner can write")
                elif int(dict[key][1][-3]) == 3:
                    print("\towner can execute and write")
                elif int(dict[key][1][-3]) == 4:
                    print("\towner can read")
                elif int(dict[key][1][-3]) == 5:
                    print("\towner can execute and read")
                elif int(dict[key][1][-3]) == 6:
                    print("\towner can write and read")
                elif int(dict[key][1][-3]) == 7:
                    print("\towner can read, write and execute")
                else:
                    print("\towner have no permissions")


def read_from_file(filepath):
    try:
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                k, v = row
                old_dict[k] = literal_eval(v)
    except IOError:
        print("I/O error")


def write_to_file(filepath):
    try:
        with open(filepath, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for data, value in dict.items():
                writer.writerow([data, value])
    except IOError:
        print("I/O error")


def recursive(path):
    obj = os.scandir(path)

    for entry in obj:
        if entry.is_symlink():
            dict[f"{path}/{entry.name}"] = [entry.name, oct(os.lstat(entry)[ST_MODE]), os.lstat(entry)[ST_SIZE]]
        if entry.is_dir(follow_symlinks = False):
            # print(f"{entry.name} {oct(os.stat(entry)[ST_MODE])} {os.stat(entry)[ST_SIZE]}")
            dict[f"{path}/{entry.name}"] = [entry.name, oct(os.stat(entry)[ST_MODE]), os.stat(entry)[ST_SIZE]]
            recursive(path + '/' + entry.name)
        elif entry.is_file(follow_symlinks = False):
            dict[f"{path}/{entry.name}"] = [entry.name, oct(os.stat(entry)[ST_MODE]), os.stat(entry)[ST_SIZE]]
            # print(f"{entry.name} {oct(os.stat(entry)[ST_MODE])} {os.stat(entry)[ST_SIZE]}")


def main(path):
    recursive(path)
    filePath = os.path.join(path, "audit.csv")
    if not os.path.exists(filePath):
        write_to_file(filePath)
        print("This program will begin an audit from your specified path upon login")
    else:
        read_from_file(filePath)
        compare_old_and_new()
        write_to_file(filePath)
        print("Audit completed")
    # print(dict)
    # print(old_dict)


if __name__ == "__main__":
    path = '/home/ironsj/SchoolFolders/CIS452/FSSA'

    main(path)
