#!/usr/bin/python
#coding=utf8
"""
# Author: Bill
# Created Time : 2016-07-27 23:18:24

# File Name: mdb_sstat.py
# Description:

"""
import sys
import os
from optparse import OptionParser
import re
import time
import platform
import json
import types
#######Log
import logging
from logging.handlers import RotatingFileHandler
class ColoredFormatter(logging.Formatter):
    '''A colorful formatter.'''
 
    def __init__(self, fmt = None, datefmt = None):
        logging.Formatter.__init__(self, fmt, datefmt)
        # Color escape string
        COLOR_RED='\033[1;31m'
        COLOR_GREEN='\033[1;32m'
        COLOR_YELLOW='\033[1;33m'
        COLOR_BLUE='\033[1;34m'
        COLOR_PURPLE='\033[1;35m'
        COLOR_CYAN='\033[1;36m'
        COLOR_GRAY='\033[1;37m'
        COLOR_WHITE='\033[1;38m'
        COLOR_RESET='\033[1;0m'
         
        # Define log color
        self.LOG_COLORS = {
            'DEBUG': '%s',
            'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
            'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
            'ERROR': COLOR_RED + '%s' + COLOR_RESET,
            'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
            'EXCEPTION': COLOR_RED + '%s' + COLOR_RESET,
        }

    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)
 
        return self.LOG_COLORS.get(level_name, '%s') % msg
class Log(object):
    
    '''
    log
    '''
    def __init__(self, filename, level="debug", logid="qiueer", mbs=20, count=10, is_console=True):
        '''
        mbs: how many MB
        count: the count of remain
        '''
        try:
            self._level = level
            #print "init,level:",level,"\t","get_map_level:",self._level
            self._filename = filename
            self._logid = logid

            self._logger = logging.getLogger(self._logid)
            
            
            if not len(self._logger.handlers):
                self._logger.setLevel(self.get_map_level(self._level))  
                
                fmt = '[%(asctime)s] %(levelname)s\n%(message)s'
                datefmt = '%Y-%m-%d %H:%M:%S'
                formatter = logging.Formatter(fmt, datefmt)
                
                maxBytes = int(mbs) * 1024 * 1024
                file_handler = RotatingFileHandler(self._filename, mode='a',maxBytes=maxBytes,backupCount=count)
                self._logger.setLevel(self.get_map_level(self._level))  
                file_handler.setFormatter(formatter)  
                self._logger.addHandler(file_handler)
    
                if is_console == True:
                    stream_handler = logging.StreamHandler(sys.stderr)
                    console_formatter = ColoredFormatter(fmt, datefmt)
                    stream_handler.setFormatter(console_formatter)
                    self._logger.addHandler(stream_handler)

        except Exception as expt:
            print expt
            
    def tolog(self, msg, level=None):
        try:
            level = level if level else self._level
            level = str(level).lower()
            level = self.get_map_level(level)
            if level == logging.DEBUG:
                self._logger.debug(msg)
            if level == logging.INFO:
                self._logger.info(msg)
            if level == logging.WARN:
                self._logger.warn(msg)
            if level == logging.ERROR:
                self._logger.error(msg)
            if level == logging.CRITICAL:
                self._logger.critical(msg)
        except Exception as expt:
            print expt
            
    def debug(self,msg):
        self.tolog(msg, level="debug")
        
    def info(self,msg):
        self.tolog(msg, level="info")
        
    def warn(self,msg):
        self.tolog(msg, level="warn")
        
    def error(self,msg):
        self.tolog(msg, level="error")
        
    def critical(self,msg):
        self.tolog(msg, level="critical")
            
    def get_map_level(self,level="debug"):
        level = str(level).lower()
        #print "get_map_level:",level
        if level == "debug":
            return logging.DEBUG
        if level == "info":
            return logging.INFO
        if level == "warn":
            return logging.WARN
        if level == "error":
            return logging.ERROR
        if level == "critical":
            return logging.CRITICAL

def docmd(command,timeout=300, raw=False):
        '''
        功能：
                执行命令
        参数：command，命令以及其参数/选项
                timeout，命令超时时间，单位秒
                debug，是否debug，True输出debug信息，False不输出
                raw，命令输出是否为元素的输出，True是，False会将结果的每一行去除空格、换行符、制表符等，默认False
        返回：
                含有3个元素的元组，前两个元素类型是list，第三个元素类型是int，第一个list存储stdout的输出，第二个list存储stderr的输出，第三int存储命令执行的返回码，其中-1表示命令执行超时
        示例：
                cmd.docmd("ls -alt")
        '''
        import subprocess, datetime, os, time, signal
        start = datetime.datetime.now()

        ps = None
        retcode = 0
        if platform.system() == "Linux":
                ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        else:
                ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        while ps.poll() is None:
                time.sleep(0.2)
                now = datetime.datetime.now()
                if (now - start).seconds > timeout:
                        os.kill(ps.pid, signal.SIGINT)
                        retcode = -1
                        return (None,None,retcode)
        stdo = ps.stdout.readlines()
        stde = ps.stderr.readlines()
        
        if not ps.returncode:
                retcode = ps.returncode
        if raw == True:  #去除行末换行符
                stdo = [line.strip("\n") for line in stdo]
                stde = [line.strip("\n") for line in stde]
        if raw == False: #去除行末换行符，制表符、空格等
                stdo = [str.strip(line) for line in stdo]
                stde = [str.strip(line) for line in stde]
        return (stdo,stde,retcode)
def get_logstr(list_dict, max_key_len=16, join_str="\n"):
    log_str = ""
    for conf in list_dict:
        for (key,val) in dict(conf).iteritems():
            log_str = log_str + str(key).ljust(max_key_len) + ": " + str(val) + join_str
    log_str = log_str.strip() # 去掉尾部 \n
    return log_str
def get_user_passwd_by_port(conffile, port):
    if os.path.exists(conffile) == False:
        return (None,None)
    with open(conffile,'r') as fd:
        alllines = fd.readlines()
        for line in alllines:
            line = str(line).strip()
            if not line or line.startswith("#"):continue
            ln_ary = re.split('[ ,;]+', line)
            if len(ln_ary) < 3:continue
            if str(port) == ln_ary[0]:
                return (ln_ary[1],ln_ary[2])
    return (None, None)
class MGdb(object):
    def __init__(self, iphost="127.0.0.1", port=27017, username=None, password=None, force=False, debug=True):
        self._iphost = iphost
        self._port = port
        self._username = username
        self._password = password
        self._force = force
        
        self._logpath = "/tmp/zabbix_mongodb.log"
        self._cache_file = "/tmp/zabbix_mongodb_cache_%s.txt" %(port)
        if not port:
            self._cache_file = "/tmp/zabbix_mongodb_cache.txt"
    
        self._logger = Log(self._logpath,level="error",is_console=debug, mbs=5, count=5)
        
    def get_logger(self):
        return self._logger

    def get_port_list(self,port_list=""):
        # sudo权限，必须授予
        # [root@localhost ~]# tail -n 2 /etc/sudoers
        # Defaults:zabbix   !requiretty 
        # zabbix ALL=(root) NOPASSWD:/bin/netstat
        data = list()
        if port_list:
            for port in port_list:
                data.append({"{#MONGODB_PORT}": port})
        else:
            binname = "mongod"
            cmdstr = "netstat  -nlpt | grep '%s' | awk '{print $4}'|awk -F: '{print $2}'|uniq" % (binname)
            disk_space_info = []
            (stdo_list, stde_list, retcode) = docmd(cmdstr, timeout=3, raw = False)
            
            log_da = [{"cmdstr": cmdstr},{"ret": retcode},{"stdo": "".join(stdo_list)}, {"stde": "".join(stde_list)}]
            logstr = get_logstr(log_da, max_key_len=10)
            
            if retcode !=0:
                self._logger.error(logstr)
                return {}
            else:
                self._logger.info(logstr)
                
            for port in stdo_list:
                port = int(str(port).strip())
                data.append({"{#MONGODB_PORT}": port})
        import json
        return json.dumps({'data': data}, sort_keys=True, indent=7, separators=(",",":"))
    
    def _get_result(self, iphost=None, port=None, username=None, password=None):
        try:
            hostname= iphost if iphost else self._iphost
            port = port if port else self._port
            username = username if username else self._username
            password = password if password else self._password
            resobj = None
            
            if self._force == False:
                if os.path.exists(self._cache_file):
                    with open(self._cache_file, "r") as fd:
                        alllines = fd.readlines()
                        fd.close()
                        if alllines and len(alllines)>1:
                            old_unixtime = int(str(alllines[0]).strip())
                            now_unixtime = int(time.time())
                            if (now_unixtime - old_unixtime) <= 60: ## 1min内
                                resobj = str(alllines[1]).strip()
                                resobj = json.loads(resobj)

                if resobj:
                    log_da = [{"msg": "Get From Cache File"}, {"content": str(resobj)}]
                    logstr = get_logstr(log_da, max_key_len=10)
                    self._logger.info(logstr)
                    return resobj
            
            pbinpaths = [
                         "/usr/local/mongodb/bin/mongo",
                         "/opt/mongodb/bin/mongo",
                         "/home/mongodb/mongodb/bin/mongo",
            ]
            cmdstr = None
            for bp in pbinpaths:
                if os.path.exists(bp):
                    if username and password:
                        cmdstr = "echo 'db.serverStatus()' | %s admin --host '%s'  --port %s -u %s -p %s --quiet" % (bp, hostname, port, username, password)
                    else:
                        cmdstr = "echo 'db.serverStatus()' | %s admin --host '%s'  --port %s --quiet" % (bp, hostname, port)
                    break
            if not cmdstr:
                print "the mongo not find"
                return None

            (stdo_list, stde_list, retcode) = docmd(cmdstr, timeout=3, raw = False)
            
            log_da = [{"cmdstr": cmdstr},{"ret": retcode},{"stdo": None if not stdo_list else "".join(stdo_list)}, {"stde": None if not stde_list else"".join(stde_list)}]
            logstr = get_logstr(log_da, max_key_len=10)
        
            if retcode !=0:
                    self._logger.error(logstr)
                    return None
            else:
                self._logger.info(logstr)
            
            stdo_str = "".join(stdo_list)
            stdo_str = stdo_str.replace("NumberLong(", "").replace(")","").replace("ISODate(","").replace("ObjectId(","")
            #print stdo_str
            resobj = json.loads(stdo_str)
            now_unixtime = int(time.time())
            with open(self._cache_file, "w") as fd:
                fd.write(str(now_unixtime)+"\n")
                fd.write(stdo_str)
                fd.close()

            return resobj
        except Exception as expt:
            import traceback
            tb = traceback.format_exc()
            self._logger.error(tb)

    def get_item_val(self, *items):
        resobj = self._get_result()
        src_res = resobj
        for item in items:
            if resobj and type(resobj) == types.DictType and resobj.has_key(item):
                resobj = resobj[item]
        if resobj == None or resobj == src_res:
            resobj = 0
        return resobj
    
    def get_result(self):
        return self._get_result()
    
    def get_item_tval(self,  items, val_type="int"):
        val = self.get_item_val(*items)
        if val == None:return None  #0也满足此条件
        if val_type == "int":
            return int(val)
        if val_type == "float":
            fval = "%.2f" % (val)
            return float(fval)
        if val_type == "str":
            return str(val)
        
        return int(val)
    
    def print_all_key_val(self):
        resobj = self._get_result()
        print json.dumps(resobj, indent=4)
def main():
    usage = "usage: %prog [options]\n Fetch mongodb status"
    parser = OptionParser(usage)
    
    parser.add_option("-l", "--list",  
                      action="store_true", dest="is_list", default=False,  
                      help="if list all port")

    parser.add_option("-H", "--host", action="store", dest="host", type="string", default='localhost', help="Connect to mongod host.")

    parser.add_option("-p", 
                      "--port", 
                      action="store", 
                      dest="port", 
                      type="int", 
                      default=27017, 
                      help="the port for mongodb, for example: 27017")
    
    parser.add_option("-u", 
                      "--user", 
                      action="store", 
                      dest="username", 
                      type="string", 
                      default=None, 
                      help="username")
    
    parser.add_option("-P", 
                      "--password", 
                      action="store", 
                      dest="password", 
                      type="string", 
                      default=None, 
                      help="password")

    parser.add_option("-i", 
                      "--item", 
                      dest="item", 
                      action="store",
                      type="string", 
                      default=None, 
                      help="which item to fetch")
    
    parser.add_option("-f", "--force",  
                      action="store_true", dest="force", default=False,  
                      help="if get from cache")
    
    parser.add_option("-d", "--debug",  
                      action="store_true", dest="debug", default=False,  
                      help="if open debug mode")
    parser.add_option("-a", "--all",  
                      action="store_true",dest="all", default=False,  
                      help="output all info")
    (options, args) = parser.parse_args()
    if 1 >= len(sys.argv):
        parser.print_help()
        return
    hostname = options.host
    port = options.port
    
    conffile = "/usr/local/public-ops/conf/.mongodb.passwd"
    username = options.username
    password = options.password
    
    if password == None or username == None:
        (username, password) = get_user_passwd_by_port(conffile, port)
        #print "Get (username=%s,password=%s) From Config File By port:%s" % (username, password, port)

    monitor_obj = MGdb(iphost=hostname, port=port, username=username, password=password, debug=options.debug, force=options.force)
    #################start
    port_list=[27017]
    if options.is_list == True:
        print monitor_obj.get_port_list(port_list)
        return
    
    if options.all == True:
        mg = MGdb(debug=False)
        mg.print_all_key_val()
        sys.exit(0)

    try:
        item = options.item
        item_ary = re.split("\.", item)
        print monitor_obj.get_item_tval(item_ary)

    except Exception as expt:
        import traceback
        tb = traceback.format_exc()
        monitor_obj.get_logger().error(tb)


if __name__ == '__main__':
    main()
