import subprocess
import argparse
import re
import argparse
import sys
import os
from os import path

def checkPreReq(input_file):
    exit = False
    input_file_exists = path.exists(input_file)
    if not input_file_exists:
        print("Configuration File does not exists")
        exit = True
    # try:
    #     subprocess.call(['which', 'ipmitool'])
    # except:
    #     print(" **** ERROR **** ipmitool is not available")
    #     exit = True
    if exit == True:
        sys.exit()

#parse the input file
def parse_input_file(file):
    data = dict()
    error = []
    try:
        with open(file,'r') as f:
            for each_entry in f:
                list = each_entry.split(':')
                if len(list) != 2:
                    error.append(each_entry)
                else:
                   data[list[0]] = list[1]

    except FileNotFoundError:
        print("File not Found")
        sys.exit()
    except:
        print("An error has occured")
        sys.exit()
    if len(error) != 0:
        print("ERROR WITH INPUT FILE FORMAT")
        for each_error in error:
            print(each_error)
        sys.exit()
    else:
        return data

#get the arguments
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',
                        help = 'File containing list of ip addresses, each entry must be in format Item Number, Serial Number, IPMI Mac, Unique password in this order separated by commas',
                        type = str,
                        nargs = '?')
    arguments = parser.parse_args()
    input_file = arguments.input_file
    return input_file

def Run_Commands(file):
    input_file_dict = parse_input_file(file)
    Run_ipmitool("ipmitool -H {} -U {} -P {} raw 0x30 0x70 0xf6 0x00 0x00 0x00".format(input_file_dict['IP'],input_file_dict['User Name'],input_file_dict['Password']))
def Run_ipmitool(*args):
    for a in args:
        print("{}\n".format(a))

    # res = subprocess.call(*args)
    # if res != 0:
    #     print(f'{}, failed!'.format(*args))

def main():
    input_file = get_arguments()
    checkPreReq(input_file)
    Run_Commands(input_file)
    print("FINISHED")

if __name__ == '__main__':
    main()
