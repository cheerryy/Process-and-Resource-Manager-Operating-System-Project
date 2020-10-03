class PCB:
    def __init__(self,pid,priority):#__init__是特殊方法
        #声明_pid,_priority等是pcb的变量
        self._pid=pid  #0=init,1=user,2=system 用于确定放在ready list 的第几位
        self._priority=priority
        self._status='ready'
        self._parent=None
        self._children=[]
        self._resources=[]


    def get_info(self):
        return {
            "pid":self._pid,
            "priority":self._priority,
            "status":self._status,
            "parent":self._parent.get_pid() if self._parent is not None else None,
            "children":[x.get_pid() for x in self._children],
            "resources":self._resources
        }

    def set_parent(self,parent):
        self._parent=parent

    def set_children(self,chilren):
        self._children.append(chilren)#把新孩子放到队尾

    def get_pid(self):
        return self._pid

    def get_parent(self):
        return self._parent

    def delete_children(self,pid):
        children=[x for x in self._children if x.get_pid()==pid]
        children_to_delete=children[0]
        self._children.pop(self._children.index(children_to_delete))

    def get_all_resources(self):
        return self._resources

    def get_status(self):
        return self._status

    def get_children(self):
        return self._children

    def set_status(self,status):
        self._status=status

    def get_priority(self):
        return self._priority

    def get_resource(self,rid):#返回rid对应的rcb
        for x in self._resources:
            if x['rid']==rid:
                return x

        return []#没找到对应rid的资源则返回空

    def set_resources(self,resourcer):
        resource_exist=[x for x in self._resources if x['rid']==resourcer['rid']]
        if len(resource_exist)==0:
            self._resources.append(resourcer)
        else:
            for x in resource_exist:
                if resourcer['status']==0:
                    self._resources.pop([y['rid'] for y in self._resources].index(x['rid']))
                else:
                    x['status']=resourcer['status']
