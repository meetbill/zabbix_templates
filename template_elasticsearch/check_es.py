#coding:utf8

import sys
import json
import time
import subprocess


class Result(object):
    def __init__(self, command=None, retcode=None, output=None):
        self.command = command or ''
        self.retcode = retcode
        self.output = output
        self.success = False
        if retcode == 0:
            self.success = True

def _run_timeout(command,timeout=10):
    timeout=int(timeout)
    process = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    t_beginning = time.time()
    seconds_passed = 0
    while True:
        if process.poll() is not None:
            break
        seconds_passed = time.time() - t_beginning
        if timeout and seconds_passed > timeout:
            process.terminate()
            return Result(command=command, retcode=124,output="timeout")
        time.sleep(0.1)
    output, _ = process.communicate()
    return Result(command=command, retcode=process.returncode,output=output)

def status():
    r = _run_timeout('curl -sXGET http://127.0.0.1:9200/_cluster/health/?pretty', timeout=2)
    if r.success:
        elastic_outputInfo = r.output
        elastic_outputInfo = json.loads(elastic_outputInfo)
        if elastic_outputInfo["status"] == "green":
            return 0
        if elastic_outputInfo["status"] == "yellow":
            return 1
        else:
            return 2    
    else:
        return 2
                
        
if __name__ == "__main__":
    import inspect
    if len(sys.argv) < 2:
        print "Usage:"
        for k,v in globals().items():
            if inspect.isfunction(v) and k[0] != "_":
                print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[1:-1].replace(",", "")
        sys.exit(-1)
    else:
        print status()
              
        

