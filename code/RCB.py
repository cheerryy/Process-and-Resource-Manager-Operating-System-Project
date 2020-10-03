class RCB:
    def __init__(self,rid,status):
        self._rid=rid
        self._max=status
        self._status=status
        self._waiting_list=[]
        self._allocated_list=[]

    def set_allocated_list(self,process):
        #根据pid查process在不在分配队里，
        allocated_existed=[x for x in self._allocated_list if process['pid']==x['pid']]
        #若不在，则将该process放到分配队队尾
        if len(allocated_existed)==0:
            self._allocated_list.append(process)
        # 若在，对于每个进程，如果分配给他的是0，就不要在分配队里了
        # 否则，把该process占有的记录到队里面
        # x用于循环进程，status表示分配出去了多少
        else:
            for x in allocated_existed:
                if process['status']==0:
                    self._allocated_list.pop([y['pid'] for y in self._allocated_list].index(x['pid']))
                else:
                    x['status']=process['status']


    def set_waiting_list(self,process):#某个进程在等待Ri资源？
        waiting_existed=[x for x in self._waiting_list if process['pid']==x['pid']]

        if len(waiting_existed)==0:#原来没在等，则加入等待序列
            self._waiting_list.append(process)
        else:#若已经在等
            for x in waiting_existed:
                if process['status']==0:#该进程对于资源Ri需求量为0，则把别的pop上来，把他移开
                    self._waiting_list.pop([y['pid'] for y in self._waiting_list].index(x['pid']))
                else:#否则，按需要的量等待
                    x['status']=process['status']

    def get_status(self):
        return self._status

    def set_status(self,num):
        self._status=num

    def get_allocated_status(self,pid):#给某个进程分配了多少
        allocated=[x for x in self._allocated_list if x['pid']==pid]
        if len(allocated)!=0:
            return allocated[0]['status']
        else:
            return 0

    def get_rid(self):
        return self._rid

    def get_waiting_list(self):
        return self._waiting_list

    def get_max(self):
        return self._max

    def get_allocated_list(self):
        return self._allocated_list
