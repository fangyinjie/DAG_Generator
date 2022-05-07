class Core:
    Periodically = list(enumerate(['BUSY', 'IDLE'], start=0))

    def __init__(self, Core_ID):
        # 一. 核的基本参数
        self.Core_ID            = Core_ID   # 核的ID号码，名称，例如'Cortex-M3'；
        self.Core_State_Is_IDLE = True 	    # 为True表示核忙碌，为False表示核空闲；
        self.Core_Running_Task  = []	    # 核上的运行任务记录；每个元素为:
        # (DAG_ID, Task_ID, Start_Time, Finish_Time, WCET)
        self.Last_comleted_Time = 0	        # 返回记录core的最近一次的完成时间，初始值为0；

    def Get_Core_Running_List(self):
        # 返回Core_Running_Task列表；
        return self.Core_Running_Task

    def Insert_Task(self, DAG_ID, Task_ID, Star_Time, WCET):
        # 向Core_Running中加入元素
        self.Core_Running_Task.append(
            (DAG_ID,     Task_ID,   Star_Time,  WCET,   Star_Time + WCET)
        )
        self.Last_comleted_Time = Star_Time + WCET  # 更新core的完成时间
        self.Insert_Core_Busy()                     # 更新core状态为BUSY
        return True

    def Insert_Core_Busy(self):
        self.Core_State_Is_IDLE = False

    def Insert_Core_False(self):
        self.Core_State_Is_IDLE = True

    def Show_Core(self):
        print(" Core_ID:", self.Core_ID)
        print(" Core_State_Is_IDLE:", self.Core_State_Is_IDLE)
        print(" Last_comleted_Time:", self.Last_comleted_Time)
        print(" Running List:", len(self.Core_Running_Task))
        for x in range(0, len(self.Core_Running_Task)):
            print("     ", self.Core_Running_Task[x])


if __name__ == "__main__":

    # 节点号； 节点名； 节点优权重； 节点优先级
    core = Core(Core_ID="1_1")
    core.Insert_Task(DAG_ID=1, Task_ID=1, Star_Time=100, WCET=34556)
    core.Insert_Task(DAG_ID=1, Task_ID=2, Star_Time=100, WCET=34556)
    core.Insert_Task(DAG_ID=1, Task_ID=3, Star_Time=100, WCET=34556)
    core.Show_Core()

