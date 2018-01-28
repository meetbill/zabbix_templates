#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2018-01-24 22:06:02

# File Name: server.py
# Description:

"""

import os
import sys
import json

server_array = ['xserver', 'reifs','xserver_guard']
def discovery():
    array = []
    for d in server_array:
        disk = {}
        disk['{#SERVER_NAME}'] = d
        array.append(disk)
    print json.dumps({'data': array}, indent=4, separators=(',',':'))

def discovery_file(config_file):
    server_array = []
    if os.path.exists(config_file):
        with open(config_file,"r") as f:
            for line in f.readlines():
                server_array.append(line.strip())
    array = []
    for d in server_array:
        disk = {}
        disk['{#SERVER_NAME}'] = d
        array.append(disk)
    print json.dumps({'data': array}, indent=4, separators=(',',':'))

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

if __name__ == '__main__':
    import inspect
    if len(sys.argv) < 2:
        print "Usage:"
        for k, v in sorted(globals().items(), key=lambda item: item[0]):
            if inspect.isfunction(v) and k[0] != "_":
                args, __, __, defaults = inspect.getargspec(v)
                if defaults:
                    print sys.argv[0], k, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                        str(["%s=%s" % (a, b) for a, b in zip(
                            args[-len(defaults):], defaults)])[1:-1].replace(",", "")
                else:
                    print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[1:-1].replace(",", "")
        sys.exit(-1)
    else:    
        func = eval(sys.argv[1])
        args = sys.argv[2:]
        try: 
            r = func(*args)
        except Exception, e:
            print "Usage:"
            print "\t", "python %s" % sys.argv[1], str(func.func_code.co_varnames[:func.func_code.co_argcount])[1:-1].replace(",", "")
            if func.func_doc:
                print "\n".join(["\t\t" + line.strip() for line in func.func_doc.strip().split("\n")])
            print e
            r = -1
            import traceback
            traceback.print_exc()
        if isinstance(r, int):
            sys.exit(r)    
