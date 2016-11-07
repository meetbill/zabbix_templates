#!/usr/bin/python
#encoding=UTF8
'''
@author: 遇见王斌
2016-11-06

功能:检测 mysql 是否可写

测试方法
#python mysql_func.py  -i is_can_write
'''

import commands
import sys
import os
from optparse import OptionParser
import re

from my_lib.QLog import Log
from my_lib import QCmd
import ConfigParser

class Mysql(object):
    def __init__(self,debug=True):
        config = ConfigParser.ConfigParser()
        config.read(".mysql.ini")
        self._iphost = config.get("mysql", "ip")
        self._username = config.get("mysql","user")
        self._password = config.get("mysql","password")
        self._port = config.get("mysql","port")
        self.logpath = config.get("log","logpath")
        self._mysql_path = config.get("bin","mysql_path")
        self._logger = Log(self.logpath,is_console=debug, mbs=10, count=5)
        
    def get_logger(self):
        return self._logger

    def get_mysql_cmd_output(self, cmdstr, hostname=None,username=None,password=None,port=None):
        try:
            hostname= hostname if hostname else self._iphost
            username = username if username else self._username
            passwd = password if password else self._password
            port = port if port else self._port

            mysql_bin_path = "mysql"
            if os.path.isfile(self._mysql_path):
                mysql_bin_path = self._mysql_path
            sql_cmstr = '%s -h%s -P%s -u%s -p%s -e "%s"' % (mysql_bin_path,hostname,port,username, passwd, cmdstr)
            
            (stdo,stde,retcode) = QCmd.docmd(sql_cmstr, timeout=1, raw=True)
            #(ret, result) = commands.getstatusoutput(sql_cmstr)
            
            logstr = "sql_cmdstr:%s\nret:%s\nstdo:%s\nstde:%s" % (sql_cmstr, retcode, stdo, stde)
            if retcode == 0:
                self._logger.info(logstr)
                return stdo
            else:
                self._logger.error(logstr)
                result = None
    
            return result
        except Exception as expt:
            import traceback
            tb = traceback.format_exc()
            self._logger.error(tb)
    
    def get_item_from_sql_output(self,result, item):
        try:
            if not result:
                return '0'

            output_list = re.split("[\n]+", str(result).strip())
            item = str(item).lower().strip()
            for line in output_list:
                line = str(line).strip().replace(" ", "").lower().strip("|")
                line_ary = re.split("\|", line)
                if item == line_ary[0]:
                    return line_ary[1]
            return '0'
        except Exception as expt:
            import traceback
            tb = traceback.format_exc()
            self._logger.error(tb)
                
    def is_mysql_can_write(self, hostname=None, port=None):
        cmdstr = "insert into test.t_zabbix(insert_timestamp)values(current_timestamp());"
        result = self.get_mysql_cmd_output(cmdstr,hostname=hostname,port=port)
        if result == None: ## 超时写入，判定为不可写入
            return 0
        return 1


def main():

    usage = "usage: %prog [options]\n Check MySQL Function"
    parser = OptionParser(usage)
    parser.add_option("-d", "--debug",  
                      action="store_true", dest="debug", default=False,  
                      help="if output all process")
    parser.add_option("-i", 
                      "--item", 
                      action="store", 
                      dest="item", 
                      type="string", 
                      default='Uptime', 
                      help="which item to fetch")
    
    (options, args) = parser.parse_args()
    if 1 >= len(sys.argv):
        parser.print_help()
        return

    mysql = Mysql(debug=options.debug)
    try:
        
        item = options.item
        if item == "is_can_write":
            print mysql.is_mysql_can_write()
        #print mysql.get_item_val(options.item)

    except Exception as expt:
        import traceback
        tb = traceback.format_exc()
        mysql.get_logger().error(tb)


if __name__ == '__main__':
    root_path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(root_path)
    main()
