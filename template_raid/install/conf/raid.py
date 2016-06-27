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


MEGACLI_EXEC = '/opt/MegaRAID/MegaCli/MegaCli64'
LIST_DISK_OPT = '-PDList -aALL -NoLog'

SLOT_NUMBER = 'Slot Number'
DEVICE_ID = 'Device Id'
WWN = 'WWN'
MEC = 'Media Error Count'
OEC = 'Other Error Count'
PFC = 'Predictive Failure Count'
PD_TYPE = 'PD Type'
RAW_SIZE = 'Raw Size'
FIRMWARE_STATE = 'Firmware state'
INQUIRY_DATA = 'Inquiry Data'


class Disk(object):
#{{{ __init__
    def __init__(self, dev_id, slot_number, mec, oec, pfc, pd_type,
                 raw_size, firmware_state, inquiry_data):
        self.dev_id = dev_id
        self.slot_number = slot_number
        # Media Error Count
        self.mec = mec
        # Other Error Count
        self.oec = oec
        # Predictive Failure Count
        self.pfc = pfc
        # PD Type
        self.pd_type = pd_type
        # Size
        self.raw_size = raw_size
        # Firmware State ("Failed", "Online, Spun Up", "Online, Spun Down", "Unconfigured(bad)", "Unconfigured(good), Spun down", "Hotspare, Spun down", "Hotspare, Spun up" or "not Online")
        self.firmware_state = firmware_state
        # Inquiry data
        self.inquiry_data = inquiry_data
#}}}
#{{{ jsonfiy
    def jsonfiy(self):
        pass
#}}}
#{{{__str__
    def __str__(self):
        return '%s %s %s %s %s %s %s %s  %s' % (
            self.dev_id, self.slot_number, self.mec, self.oec,
            self.pfc, self.pd_type, self.raw_size, self.firmware_state,
            self.inquiry_data
        )
#}}}

def check_megacli(cli_path):
    if not os.path.exists(cli_path) or not os.access(cli_path, os.X_OK):
        print 'MegaCLI is needed in %s with executable priviledge.' % (cli_path)
        sys.exit(1)


def line_generator(string):
    line = []
    for c in string:
        if c != '\n':
            line.append(c)
        else:
            yield ''.join(line)
            line = []


def get_value(line):
    return line.split(':')[1].strip()


def make_disk_array(mega_output):
    disk_array = []
    for line in line_generator(mega_output):
        if line.startswith(SLOT_NUMBER):
            slot_number = get_value(line)
        elif line.startswith(DEVICE_ID):
            dev_id = get_value(line)
        elif line.startswith(MEC):
            mec = get_value(line)
        elif line.startswith(OEC):
            oec = get_value(line)
        elif line.startswith(PFC):
            pfc = get_value(line)
        elif line.startswith(PD_TYPE):
            pd_type = get_value(line)
        elif line.startswith(RAW_SIZE):
            raw_size = get_value(line)
        elif line.startswith(FIRMWARE_STATE):
            fw_state = get_value(line)
        elif line.startswith(INQUIRY_DATA):
            inquiry_data = get_value(line)

            disk = Disk(dev_id, slot_number, mec, oec, pfc, pd_type,
                        raw_size, fw_state, inquiry_data)
            disk_array.append(disk)
    return disk_array


def discovery_physical_disk(disk_array):
    array = []
    for d in disk_array:
        disk = {}
        disk['{#DISK_ID}'] = d.dev_id
        array.append(disk)
    return json.dumps({'data': array}, indent=4, separators=(',',':'))


def count_media_error(disk_array, disk_id):
    for disk in disk_array:
        if int(disk.dev_id) == int(disk_id):
            return disk.mec
    return '-1'

def count_other_error(disk_array, disk_id):
    for disk in disk_array:
        if int(disk.dev_id) == int(disk_id):
            return disk.oec
    return '-1'

def count_predictive_error(disk_array, disk_id):
    for disk in disk_array:
        if int(disk.dev_id) == int(disk_id):
            return disk.pfc
    return '-1'


def get_disk_array():
    check_megacli(MEGACLI_EXEC)
    (status, output) = commands.getstatusoutput('%s %s' % (MEGACLI_EXEC, LIST_DISK_OPT))
    if status != 0:
        print 'Exec MegaCLI failed, please check the log.'
        sys.exit(1)
    #print output
    disk_array = make_disk_array(output)
    #print disk_array
    return disk_array


def init_option():
    usage = """
    """
    parser = OptionParser(usage=usage, version="0.1")
    return parser


parser = init_option()


if __name__ == '__main__':
    (options, args) = parser.parse_args()

    if len(args) < 1:
        print parser.print_help()
        sys.exit(1)

    disk_array = get_disk_array()
    #print disk_array
    command = args.pop(0)
    if command == 'pd_discovery':
        print discovery_physical_disk(disk_array)
    elif command == 'mec':
        print count_media_error(disk_array, args.pop())
    elif command == 'oec':
        print count_other_error(disk_array, args.pop())
    elif command == 'pfc':
        print count_predictive_error(disk_array, args.pop())
