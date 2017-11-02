#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2017-11-03 00:54:10

# File Name: raid.py
# Description:

"""
import commands
import os
import sys
import json


MEGACLI_EXEC = '/opt/MegaRAID/MegaCli/MegaCli64'
LIST_DISK_OPT = '-PDList -aALL -NoLog'

SLOT_NUMBER = 'Slot Number'
DEVICE_ID = 'Device Id'
WWN = 'WWN'
MEC = 'Media Error Count'
OEC = 'Other Error Count'
PFC = 'Predictive Failure Count'
PD_TYPE = 'PD Type'
FIRMWARE_STATE = 'Firmware state'


def _check_megacli(cli_path):
    if not os.path.exists(cli_path) or not os.access(cli_path, os.X_OK):
        print 'MegaCLI is needed in %s with executable priviledge.' % (cli_path)
        sys.exit(1)
def _line_generator(string):
    line = []
    for c in string:
        if c != '\n':
            line.append(c)
        else:
            yield ''.join(line)
            line = []
def _get_value(line):
    return line.split(':')[1].strip()
def _make_disk_dict(mega_output):
    disk_dict_all = {}
    for line in _line_generator(mega_output):
        if line.startswith(SLOT_NUMBER):
            slot_number = _get_value(line)
        elif line.startswith(DEVICE_ID):
            dev_id = _get_value(line)
        elif line.startswith(MEC):
            mec = _get_value(line)
        elif line.startswith(OEC):
            oec = _get_value(line)
        elif line.startswith(PFC):
            pfc = _get_value(line)
        elif line.startswith(PD_TYPE):
            pd_type = _get_value(line)
        elif line.startswith(FIRMWARE_STATE):
            fw_state = _get_value(line)

            device_dict = {}
            device_dict["slot_number"] = slot_number
            device_dict["dev_id"] = dev_id
            device_dict["mec"] = mec
            device_dict["oec"] = oec
            device_dict["pfc"] = pfc
            device_dict["pd_type"] = pd_type
            device_dict["fw_state"] = fw_state

            disk_dict_all[dev_id]=device_dict
    return disk_dict_all
def _get_disk_dict():
    _check_megacli(MEGACLI_EXEC)
    (status, output) = commands.getstatusoutput('%s %s' % (MEGACLI_EXEC, LIST_DISK_OPT))
    if status != 0:
        print 'Exec MegaCLI failed, please check the log.'
        sys.exit(1)
    #print output
    disk_dict = _make_disk_dict(output)
    return disk_dict
def pd_discovery():
    """
    discovery_physical_disk
    """
    array = []
    for dev_id in disk_dict_all:
        disk = {}
        disk['{#DISK_ID}'] = disk_dict_all[dev_id]["dev_id"]
        disk['{#SLOT_NUMBER}'] = disk_dict_all[dev_id]["slot_number"]
        array.append(disk)
    return json.dumps({'data': array}, indent=4, separators=(',',':'))
def media_error_count(disk_id):
    try:
        return disk_dict_all[disk_id]["mec"]
    except:
        return '-1'
def other_error_count(disk_id):
    try:
        return disk_dict_all[disk_id]["oec"]
    except:
        return '-1'
def predictive_error_count(disk_id):
    try:
        return disk_dict_all[disk_id]["pfc"]
    except:
        return '-1'

if __name__ == '__main__':
    import sys, inspect
    if len(sys.argv) < 2:
        print "Usage(1.0.2):"
        for k, v in sorted(globals().items(), key=lambda item: item[0]):
            if inspect.isfunction(v) and k[0] != "_":
                args, __, __, defaults = inspect.getargspec(v)
                if defaults:
                    print sys.argv[0], k, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                          str(["%s=%s" % (a, b) for a, b in zip(args[-len(defaults):], defaults)])[1:-1].replace(",", "")
                else:
                    print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[1:-1].replace(",", "")
        sys.exit(-1)
    else:
        disk_dict_all = _get_disk_dict()
        func = eval(sys.argv[1])
        args = sys.argv[2:]
        try:
            r = func(*args)
            print r
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
