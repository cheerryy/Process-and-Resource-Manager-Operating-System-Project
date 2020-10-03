from RCB import RCB

class Resourcer:
    def __init__(self):
        r1 = RCB("R1", 1)
        r2 = RCB("R2", 2)
        r3 = RCB("R3", 3)
        r4 = RCB("R4", 4)

        self._resource_list=list()

        self._resource_list.append(r1)
        self._resource_list.append(r2)
        self._resource_list.append(r3)
        self._resource_list.append(r4)

    def request(self,process,rid,request_status):#哪个进程，要什么，要多少
        #若rid对应的资源存在于resource list
        if len([x for x in self._resource_list if x.get_rid()==rid])!=0:
            resource_requested=[x for x in self._resource_list if x.get_rid()==rid][0]
        #若剩余的>=请求的，申请成功
            if resource_requested.get_status()>=request_status:
                #剩余资源-=需求量
                resource_requested.set_status(resource_requested.get_status()-request_status)
                #维护分配资源
                allocated_status=resource_requested.get_allocated_status(process.get_pid())
                resource_requested.set_allocated_list(process={
                    "pid":process.get_pid(),
                    "priority":process.get_priority(),
                    "status":request_status+allocated_status
                })
                return 0
            else:
                #若剩余的<请求的，阻塞进程
                resource_requested.set_waiting_list(process={
                    "pid":process.get_pid(),
                    "priority":process.get_priority(),
                    "status":request_status
                })
                return 1
        else:
            print("Resource is not existed!")
            return -1

    def release(self,process,rid,release_status):
        #rid对应的资源存在
        if len([x for x in self._resource_list if x.get_rid()==rid])!=0:
            release=[x for x in self._resource_list if x.get_rid()==rid][0]#release is a RCB class
            allocated_status=release.get_allocated_status(process.get_pid())
            #若要释放的大于本来给他分配的，失败
            if allocated_status<release_status:
                print("release too much")
                return -1
            else:
            #否则成功
                #维护已分配状态
                release.set_status(release_status+release.get_status())
                #维护资源状态
                release.set_allocated_list(process={
                    "pid": process.get_pid(),
                    "priority": process.get_priority(),
                    "status": allocated_status-release_status
                })
                return 0
        else:
            print("Resource is not existed!")
            return -1

    def get_rcb(self,rid):
        rcb=[x for x in self._resource_list if x.get_rid()==rid]
        if len(rcb)!=0:
            return rcb[0]
        else:
            return []

    def get_resource_list(self):
        return [{
            "rid:":x.get_rid(),
            #"max:":x.get_max(),
            "status:":x.get_status(),
            #"waiting list:":x.get_waiting_list(),
            #"allocated list:": x.get_allocated_list()
            }
            for x in self._resource_list
        ]

    def get_blocked(self):
        return [{
            "rid":x.get_rid(),
            "pid":x.get_waiting_list()
        }
        for x in self._resource_list]