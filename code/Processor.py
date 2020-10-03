from PCB import PCB

class Processor:
    def __init__(self):
        #创建内部的三个list
        self._ready_list=[]
        self._running_list=[]
        self._blocked_list=[]

    def create_process(self,pid,priority):
        #用pid判断进程是否已经存在(pid 在所有进程的pid集合)

        if len(self._running_list)!=0 and pid in [x.get_pid() for x in self.get_process_list()]:
            print("process"+pid+"has existed")
            return
        #进程原来不存在,创建新的pcb并把它附加在ready list 末尾
        new_pcb=PCB(pid,priority)
        self._ready_list.append(new_pcb)

        #双向设置parent
        if len(self._running_list)!=0:
            new_pcb.set_parent(self._running_list[0])
            self._running_list[0].set_children(new_pcb)

        self.schedule()

    def delete_process(self,pid,time,resourcer):#资源管理器
        #根据pid找到对应的进程process
        processes=[x for x in self.get_process_list() if x.get_pid()==pid]
        if len(processes)==0:
            print("process is not exist")
        else:
            process=processes[0]

        #父进程删除该子进程
        parent=process.get_parent()
        parent.delete_children(pid=pid)
        #删除孩子
        process_children=process.get_children()
        [self.delete_process(pid=x.get_pid(),time=time+1,resourcer=resourcer) for x in process_children]


        #释放资源
        resources=process.get_all_resources()
        if len(resources)!=0:
            for i in range(len(resources)):
                self.release_resource(resourcer=resourcer,rid=resources[0]['rid'],release_status=resources[0]['status'],process=process)

        #移出等待资源队列，对每个资源都status=0移除等待
        for x in resourcer._resource_list:
            x.set_waiting_list(process={
                "pid":process.get_pid(),
                "priority":process.get_priority(),
                "status":0
            })

        #移除进程序列
        process_status=process.get_status()
        if process_status=='running':
            self._running_list.pop([x.get_pid() for x in self._running_list].index(pid))
        elif process_status=='blocked':
            self._blocked_list.pop([x.get_pid() for x in self._blocked_list].index(pid))
        elif process_status=='ready':
            self._ready_list.pop([x.get_pid() for x in self._ready_list].index(pid))

        #调度
        if time==0:#time==0 说明是当前这个进程，调度一次，如果是子进程在删除的时候执行到这里，不执行调度
            self.schedule()


    def schedule(self):
        #在ready list中找出要运行的进程tasks——优先级最高，到达最早
        system=[x for x in self._ready_list if x.get_priority()==2]
        user=[x for x in self._ready_list if x.get_priority()==1]
        if len(system)!=0:
            tasks=system
        elif len(user)!=0:
            tasks=user
        else:
            tasks=[x for x in self._ready_list if x.get_priority()==0]

        #若running list为空，直接把他放第一个开始运行
        if len(self._running_list)==0:
            self._running_list.append(tasks[0])
            tasks[0].set_status("running")
            self._ready_list.pop(self._ready_list.index(tasks[0]))
            print("process "+self._running_list[0].get_pid()+" is running")

        #若运行队列非空
        else:
            #tasks优先级更大就抢占
            if tasks[0].get_priority()>self._running_list[0].get_priority():
                print("process "+tasks[0].get_pid()+" is running. "+"process " +self._running_list[0].get_pid()+" is ready")

                #把原来在运行的放到ready list
                self._running_list[0].set_status("ready")
                self._ready_list.append(self._running_list[0])
                self._running_list.pop()
                #把tasks放到running list
                tasks[0].set_status("running")
                self._ready_list.pop(self._ready_list.index(tasks[0]))
                self._running_list.append(tasks[0])
            #否则不动
            else:
                print("process " + self._running_list[0].get_pid() + " is running", end="\n")
                return


    def request_resource(self,resourcer,rid,request_status,process=None):#资源管理器，rid，要多少，谁要
        #先处理特殊的process为none的情况，确定好process
        if process is None:
            process=self._running_list[0]

        #调用request函数，得到返回值code，根据code操作
        code=resourcer.request(process=process,rid=rid,request_status=request_status)
        print("process " + str(process.get_pid()) + " request " + str(request_status) + " " + str(rid), end="\n")

        #若code==0，请求成功
        if code==0:
            #判断
            process_resource=process.get_resource(rid)

            # 若本来没有，调用set进行设置
            if len(process_resource)==0:
                process.set_resources(resourcer={
                    "rid":rid,
                    "status":request_status
                })
            #若该process本来就有这个资源，叠加
            else:
                process_resource['status']+=request_status

        #若code==1，请求的太多，放入blocked list
        elif code==1:
            process.set_status("blocked")
            self._blocked_list.append(process)
            self._running_list.pop(self._running_list.index(process))
            print("process "+process.get_pid()+" is blocked")
        self.schedule()


    def release_resource(self,resourcer,rid,release_status,process=None):#资源管理器，rid，放多少，哪个进程
        #process没赋值，则默认为running的第一个
        if process is None:
            process=self._running_list[0]

        #如果process本来就没有rid的资源
        if len(process.get_resource(rid))==0:
            print("release resource that was not allocated")

        #正常情况。
        #先获得原来分配了多少
        status_allocated=int(process.get_resource(rid=rid)['status'])
        release_status=int(release_status)
        #若已分配的>要求释放的（释放部分），则调用set，修改数值
        if status_allocated>=release_status:
            code=resourcer.release(process=process,rid=rid,release_status=release_status)
            #code=0,在资源方面释放成功
            if code==0:
                process.set_resources(resourcer={
                    "rid":rid,
                    "status":status_allocated-release_status
                })
                print("release "+rid)
                #把在等待rid的资源的进程释放出来
                block_process=[x for x in self._blocked_list]#x is a pcb's list，阻塞的进程们
                flag=False
                #对于每个阻塞的进程x
                for x in block_process:
                    rcb=resourcer.get_rcb(rid=rid)
                    waiting_list=rcb.get_waiting_list()#从阻塞队里面找出等待该rid资源的进程们
                    for y in waiting_list:
                        if y['pid']==x.get_pid():
                        # 如果比我先来的都被阻塞了，我就退出
                            if flag is True: return
                        #否则
                            if rcb.get_status()>=y['status']:#剩余的资源大于正在阻塞的进程所需要的
                                #x从blocked list去ready list
                                x.set_status('ready')
                                x.set_resources(resourcer={
                                    "rid":rid,
                                    "status":y['status']
                                })
                                self._ready_list.append(x)
                                self._blocked_list.pop(self._blocked_list.index(x))
                                #y从资源等待list释放
                                rcb.get_waiting_list().pop(rcb.get_waiting_list().index(y))

                                #索取资源
                                resourcer.request(process=x,rid=rid,request_status=y['status'])
                                #进行调度
                                self.schedule()
                                print("wake up process "+y['pid'],end="\n")
                            else:#被阻塞，阻塞判断位改变
                                flag=True
            #code=-1
            else:
                print("release error")
        #否则报错
        else:
            print("release too much")

    def get_process_list(self):
        return self._running_list+self._ready_list+self._blocked_list

    def time_out(self):
        length=len(self._ready_list)
        print("process " +self._running_list[0].get_pid()+" is ready")

        #running的第一个放到ready尾部
        first_running_process=self._running_list[0]
        first_running_process.set_status('ready')
        self._ready_list.append(first_running_process)
        self._running_list.pop()

        #再次调度
        self.schedule()


    def get_running_list(self):
        return [x.get_pid() for x in self._running_list]

    def get_process_info(self,pid):
        process_list=self.get_process_list()
        info=[x.get_info() for x in process_list if x.get_pid()==pid]
        if len(info)==0:
            print("process"+pid+"is not existed")
            return
        print(info[0])

    def get_ready_list(self):
        return [x.get_pid() for x in self._ready_list]

    def get_blocked_list(self):
        return [x.get_pid() for x in self._blocked_list]

    def get_ready_list_zero(self):
        return [x.get_pid() for x in self._ready_list if x.get_priority()==0]

    def get_ready_list_one(self):
        return [x.get_pid() for x in self._ready_list if x.get_priority()==1]

    def get_ready_list_two(self):
        return [x.get_pid() for x in self._ready_list if x.get_priority()==2]