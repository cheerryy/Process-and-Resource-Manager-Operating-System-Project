import re
import sys
from Resourcer import Resourcer
from Processor import Processor

def system_init():
    processor_tmp=Processor()
    resourcer_tmp=Resourcer()

    #for x in processor_tmp.get_running_list():
     #   print(x + " ", end='')
    return processor_tmp,resourcer_tmp

def read_test_shell(filename):
    try:
        file=open(filename)
        text_lines=file.readlines()
        for line in text_lines:
            analysis(line)
        file.close()
    except IOError as e:
        print(e.strerror)
        return 0
    else:
        file.close()
        return 0

def analysis(inputs):
    #格式处理，删除两边空格，删除输入中多个空格
    inputs=inputs.strip()
    inputs=re.sub('[ ]+',' ',inputs)
    #print(inputs)
    #解析输入，用空格分割，保存为ip数组
    ip=inputs.split(" ")
    #若ip长度为3
    if len(ip)==3:
    #create process
        if ip[0]=='cr':#cr pid priority
            pid=ip[1]
            priority=int(ip[2])

            if priority!=1 and priority!=2:
                print("priority can only be 1 or 2")
                return 0

            processor.create_process(pid=pid,priority=priority)
    #request resource
        elif ip[0]=='req':#req rid num
            rid=ip[1]
            num=float(ip[2])
            if num.is_integer() and abs(num)==num:#num is positive integer
                processor.request_resource(resourcer=resourcer,rid=rid, request_status=num)
            else:
                print("request number should be a positive integer")
                return 0

    #release resource
        elif ip[0]=='rel':
            rid=ip[1]

            # 特殊错误情况
            try:
                num=float(ip[2])
            except ValueError as e:
                print(e)
                return 0
            else:
                if num.is_integer() and abs(num)==num:
                    processor.release_resource(resourcer=resourcer, rid=rid, release_status=num)
                else:
                    print("release num should be a positive number")

        else:
            print(ip[0]+"is an invalid command")
            return 0
    #长度为2
    elif len(ip)==2:
    #show a process
        if ip[0]=='lp':
            pid=ip[1]
            processor.get_process_info(pid=pid)
            return 0
    #delete process
        elif ip[0]=='de':
            pid=ip[1]
            if pid=='init':
                print("cannot delete init process")
                return 0
            processor.delete_process(pid=pid,time=0,resourcer=resourcer)
        elif ip[0]=='run':
            filename=ip[1]
            read_test_shell(filename)

        else:
            print(ip[0]+"is an invalid command")
    #长度为1
    else:
    #time out
        if inputs=='to':
            processor.time_out()
    #list all process
        elif inputs=='lp':
            running=processor.get_running_list()
            ready=processor.get_ready_list()
            blocked=processor.get_blocked_list()

            print("running list:"+str(running))
            print("ready list:" + str(ready))
            print("blocked list:" + str(blocked))

            return 0
        elif inputs=='ready':
            zero=processor.get_ready_list_zero()
            one=processor.get_ready_list_one()
            two=processor.get_ready_list_two()
            running=processor.get_running_list()
            one=running+one
            print("priority=2:"+str(two))
            print("priority=1:" + str(one))
            print("priority=0:" + str(zero))
    #list all resources
        elif inputs=='lr':
            resource_list=resourcer.get_resource_list()
            [print(x) for x in resource_list]
            return 0
        elif inputs=='lb':
            block_list=resourcer.get_blocked()
            [print(x) for x in block_list]
            return 0
        elif inputs=='init':
            processor.create_process('init', 0)  # 创建init进程
    #exit
        elif inputs=='exit':
            return -1
    #help document
        elif inputs=='help':
            print("run test file: run filename")
            print("create a process: cr pid priority")
            print("request a resource: req rid num")
            print("release a resource: rel rid num")
            print("list a process: lp pid")
            print("delete a process: del pid")
            print("time out: to")
            print("list all process status: lp")
            print("list ready list by priority: ready")
            print("list all resource status: lr")
            print("list blocked list: lb")
            print("exit: exit")
            return 0
        else:
            print(inputs+"is an invalid command")

    #for x in processor.get_running_list():
    #   print("process "+x+" is running",end='\n')

if __name__=='__main__':
    processor, resourcer =system_init()

    if len(sys.argv)==2:
        filename=sys.argv[1]
        read_test_shell(filename)
    if len(sys.argv)==1:#读用户输入
        while(True):
            X=input(" ")
            code=analysis(X)
            if code==-1:
                break


