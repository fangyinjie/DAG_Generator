import core


class Processor:
    def __init__(self, processor_list, proccessor_ID):
        # Core_type = len(processor_list)
        # Core_type_0_num = processor_list[0]
        # Core_type_1_num = processor_list[1]
        # ……
        # 例如：processor_list = [1,5,6]
        # 有三类core，第一类 1个，第二类 5个，第三类 6个
        self.Processor_ID = proccessor_ID  # 处理器名称,例如：'GD_32'
        self.Core_list = []
        self.System_Time = 0
        for x in range(0, len(processor_list)):
            for y in range(0, processor_list[x]):
                self.Core_list.append(core.Core("{0}_{1}".format(x, y))) # 初始化所有的core

    def Get_Idle_Core_ID(self):
        # 获取当前空闲的core的列表
        temp_list = [x for x in self.Core_list if x.Core_State_Is_IDLE]
        return temp_list

    def Add_Task_To_Core(self, Core_ID, DAG_ID, Task_ID, Star_Time, WCET):
        # 向Core_ID为Core_ID的核添加任务
        temp_list = [x for x in self.Core_list if x.Core_ID == Core_ID]
        if len(temp_list) > 0:
            temp_list[0].Insert_Task(DAG_ID=DAG_ID, Task_ID=Task_ID, Star_Time=Star_Time, WCET=WCET)
            return True
        else:
            return False

    def Update_Processor_State(self, System_Time):
        # 向Core_ID为Core_ID的核添加任务
        if System_Time < self.System_Time:
            print("System_Time fault \n")
            return False

        temp_list = [x for x in self.Core_list if x.Last_comleted_Time <= System_Time]
        if len(temp_list) > 0:
            for x in temp_list:
                x.Insert_Core_False()   # 将core设置为空闲；
            return True
        else:
            return False

    def Show_Processor(self):
        print("Processor_ID:")
        print(self.Processor_ID)
        print("Processor List:")
        for x in range(0, len(self.Core_list)):
                self.Core_list[x].Show_Core()


if __name__ == "__main__":
    processor = Processor([5,6], 'GD_32')
    idle_core_list = processor.Get_Idle_Core_ID()
    processor.Add_Task_To_Core(idle_core_list[0].Core_ID, DAG_ID=1, Task_ID=1, Star_Time=100, WCET=34556)
    processor.Add_Task_To_Core(idle_core_list[0].Core_ID, DAG_ID=1, Task_ID=1, Star_Time=100, WCET=34556)
    processor.Add_Task_To_Core(idle_core_list[0].Core_ID, DAG_ID=1, Task_ID=1, Star_Time=100, WCET=34556)
    processor.Add_Task_To_Core(idle_core_list[0].Core_ID, DAG_ID=1, Task_ID=1, Star_Time=100, WCET=34556)
    processor.Add_Task_To_Core(idle_core_list[1].Core_ID, DAG_ID=1, Task_ID=1, Star_Time=100, WCET=34556)
    processor.Add_Task_To_Core(idle_core_list[2].Core_ID, DAG_ID=1, Task_ID=1, Star_Time=100, WCET=34556)
    processor.Add_Task_To_Core(idle_core_list[3].Core_ID, DAG_ID=1, Task_ID=1, Star_Time=100, WCET=34556)
    processor.Update_Processor_State(34656)
    processor.Show_Processor()

