##### 项目功能

利用python模拟一个进程与资源管理器的设计，包括进程创建、撤销、调度，资源申请和释放，定时器中断功能等等

详见pdf文件

##### 使用方法

- 本程序运行环境为pycharm，将源代码用pycharm打开，运行main.py文件。
- 输入”run input.txt“即可运行测试案例，或输入其他支持的命令（见“支持指令”部分）。

##### 程序清单

本程序源代码包括——

- main.py，主程序
- PCB.py，进程控制块模块
- RCB.py，资源控制块模块
- Processor.py，进程管理器模块
- Resourcor.py，资源管理器模块
- input.txt，测试样例

##### 支持指令

- 运行测试文件run test file: run filename
- 创建新进程create a process: cr pid priority
- 申请资源request a resource: req rid num
- 释放资源release a resource: rel rid num
- 打印进程PCB信息list a process: lp pid
- 删除进程delete a process: del pid
- 时钟中断time out: to
- 打印进程状态list all process status: lp
- 打印就绪队列list ready list by priority: ready
- 打印资源状态list all resource status: lr
- 打印阻塞队列list blocked list: lb
- 退出exit: exit

##### 运行结果

详见pdf文件
