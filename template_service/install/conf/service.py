#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Description:
#   This application is used to discovery the pyhsical disk by using the MegaCLI tool.
#
#


import commands
import os
import sys
import json
from optparse import OptionParser

def discovery_service(server_array):
    array = []
    for d in server_array:
        disk = {}
        disk['{#SERVER_NAME}'] = d
        array.append(disk)
    return json.dumps({'data': array}, indent=4, separators=(',',':'))

def server_status(server_name):
    if server_name == 'xserver':
        check=os.popen('ps -ef |grep -java           |grep xserver |grep -v grep |wc -l').readlines()
    elif server_name == 'xserver_guard':
        check=os.popen('ps -ef |grep xserver_guard.py|grep -v grep | wc -l').readlines()
    elif server_name == 'reifs':
        check=os.popen('ps -ef |grep reifs           |grep -v grep | wc -l').readlines()
    else:
        check="  "  
    if check[0] < "1":
        return 0
    else:
        return 1

def init_option():
    usage = """
    """
    parser = OptionParser(usage=usage, version="0.1")
    return parser


parser = init_option()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    server_array = ['xserver', 'reifs',
                    'xserver_guard']
    
    if sys.argv[1] == 'discovery':
        print discovery_service(server_array)
    elif sys.argv[1]== 'status':
        print server_status(sys.argv[2])
