import numpy as np
from random import randint

# python 使用类创建结构体
class DAG_class(object):
    class Struct(object):
        def __init__(self, Parallelism, Critical_path_length):
            self.Parallelism = Parallelism                      # 并行度——DAG宽度；
            self.Critical_path_length = Critical_path_length    # 关键路径长度——无权DAG的最大长度；
            self.Node_num = 2                                   # DAG中的总节点个数；大于等于2
            self.Node = [0 for x in range(0, self.Node_num)]    # Graph{NodeName;{后继节点}}
            self.DAG_list_disp = []

    def make_struct(self, Parallelism, Critical_path_length):
        if (Parallelism < 1) or (Critical_path_length < 3):
            print("input error")
            return -1
        return self.Struct(Parallelism, Critical_path_length)

    def DAG_generator(self, dag_class_obj):
        sub_DAG_list_disp=[]
        sub_DAG_list_disp.append(1)
        for x in range(1, dag_class_obj.Critical_path_length-1):
            m = randint(1, dag_class_obj.Parallelism-1)
            sub_DAG_list_disp.append(m)
            dag_class_obj.Node_num += m
        sub_DAG_list_disp.append(1)
        dag_class_obj.DAG_list_disp.append(sub_DAG_list_disp)
        print(dag_class_obj.DAG_list_disp)  # 输出所有可能的DAG结果数量；
        return self.DAG_combine(dag_class_obj.DAG_list_disp, dag_class_obj.Node_num)

    def DG(self, Parallelism, Critical_path_length, now_Num, G, dag_class_obj):
        selfG = G.copy()
        now_length = (Critical_path_length - len(G)) - 1
        if (now_length * Parallelism < now_Num) or (now_Num < 1):
            return 0
        if now_length == 1:
            selfG.append(now_Num)
            selfG.append(1)
            dag_class_obj.DAG_list_disp.append(selfG)
            return 0
        else:
            for y in range(1, Parallelism + 1):
                selfG = G
                selfG.append(y)
                self.DG(Parallelism, Critical_path_length, now_Num - y, selfG, dag_class_obj)
                del G[-1]
            return 0

    def DAG_combine(self, DAG_list_disp, Node_num):
        DAG_Node_Group = []     # [第几种节点分布图][第几层][具体元素]
        DAG_dist_group = []
        # 生成DAG_Node_Group
        # for x 代表不同的节点层分布图
        for x in range(0, len(DAG_list_disp)):
            DAG_Node_Group_sub = self.DAG_combine_init_group(DAG_list_disp[x])
            DAG_dist_group.append(self.DAG_combine_init_dist(DAG_list_disp[x], DAG_Node_Group_sub, Node_num))
            DAG_Node_Group.append(DAG_Node_Group_sub)
        return (DAG_dist_group, DAG_Node_Group)

    def DAG_combine_init_group(self, DAG_list_disp_sub):
        inter_dag_node_group = [0 for x in range(0, len(DAG_list_disp_sub))]
        inter_dag_node_group_sub = []
        inter_node_test = 0
        for x in range(0, len(DAG_list_disp_sub)):
            for y in range(0, DAG_list_disp_sub[x]):
                #inter_dag_node_group_sub.append([(x + 1),  inter_node_test + y + 1])  # 所属层号_节点号
                inter_dag_node_group_sub.append(inter_node_test + y)  # 节点号
            inter_node_test += DAG_list_disp_sub[x]
            inter_dag_node_group[x] = inter_dag_node_group_sub
            inter_dag_node_group_sub = []
        return inter_dag_node_group

    def DAG_combine_init_dist(self,DAG_list_disp_sub, DAG_Node_Group_sub, Node_num):
        Metrix_group = [0 for x in range(0, len(DAG_list_disp_sub))]
        for x in range(1, len(DAG_list_disp_sub)-1):
            ance_list   = []
            sucess_list = []
            pre         = []
            for y in range(0, x-1):                         # 所有除了前驱层的祖先层
                ance_list.append(DAG_list_disp_sub[y])
            for y in range(x+1, len(DAG_list_disp_sub)):    # 所有后继层
                sucess_list.append(DAG_list_disp_sub[y])
            pre.append(DAG_list_disp_sub[x - 1])            # 前驱层
            if len(ance_list) == 0:
                ance_group = []
            else:
                ance_group = self.f1(ance_list, False)
            sucess_group = self.f1(sucess_list, True)
            pre_group = self.f1(pre, True)
            self_level = x
            level_length = len(DAG_list_disp_sub)
            #print(ance_group)            # #print(pre_group)            #print(sucess_group)            #print(self_level)            #print(level_length)
            if len(ance_group) == 0:
                inpot_group = pre_group
            else:
                inpot_group = self.ance_suce_pre_merge(ance_group, pre_group)
            outpot_group = sucess_group
            Metrix_group[x] = self.dag_level_line_metrixgen(level_length, self_level, inpot_group, outpot_group)

        level_metrix = self.f3(Metrix_group, DAG_Node_Group_sub, Node_num)         # 本分布图所有的层级连线矩阵组[]
        return level_metrix

    def f1(self, list, start):
        all_list = []
        if len(list) == 0:
            print("f1 error!\n")
            return -1
        if len(list) == 1:
            if start:
                for x in range(1,list[0]+1):
                    test_list=[]
                    test_list.append(x)
                    all_list.append(test_list)
            else:
                for x in range(0,list[0]+1):
                    test_list=[]
                    test_list.append(x)
                    all_list.append(test_list)
            return all_list
        for x in range(0, list[0]+1):
            self_list = list.copy()
            del self_list[0]
            if x==0 and start==True:
                sub_list = self.f1(self_list, True)
            else:
                sub_list = self.f1(self_list, False)
            for y in range(0,len(sub_list)):
                test_list=[]
                test_list.append(x)
                test_list += sub_list[y]
                all_list.append(test_list)
        return all_list

    def ance_suce_pre_merge(self,ance_group, pre_group):
        all_list = []
        for x in range(0, len(ance_group)):
            for y in range(0, len(pre_group)):
                all_list.append(ance_group[x] + pre_group[y])
        return all_list

    def dag_level_line_metrixgen(self,level_length, self_level, inpot_group, outpot_group):
        Metrix = []
        for x in range(0, len(inpot_group)):
            for y in range(0, len(outpot_group)):
                Metrix_sub = np.zeros((level_length, level_length), dtype=int)
                for z in range(0, len(inpot_group[x])):
                    Metrix_sub[z][self_level] = inpot_group[x][z]
                for z in range(0, len(outpot_group[y])):
                    Metrix_sub[self_level][self_level + 1 + z] = outpot_group[y][z]
                # print(Metrix_sub)
                Metrix.append(Metrix_sub)
        return Metrix

    def f2(self,Metrix_group):
        ret_Mtrix_group_merge = []
        if (len(Metrix_group) == 3):
            return Metrix_group[1]
        else:
            sub_Metrix_group = Metrix_group.copy()
            del sub_Metrix_group[1]
            ret_Mtrix_group_merge_sub = self.f2(sub_Metrix_group)
            for x in range(0, len(Metrix_group[1])):
                for y in range(0, len(ret_Mtrix_group_merge_sub)):
                    sub_m = Metrix_group[1][x] + ret_Mtrix_group_merge_sub[y]
                    ret_Mtrix_group_merge.append(sub_m)
        return ret_Mtrix_group_merge

    # 函数f3 ：返回 某一分布图的所有可能的联结矩阵
    #   参数： Metrix_group_sub        某一节点分布图对应顺序
    #         DAG_Node_Group_sub      所有层可能的联结情况
    #         Node_num                所有节点的个数
    def f3(self, Metrix_group, DAG_Node_Group_sub, Node_num):
        Metrix_sub = np.zeros((Node_num, Node_num), dtype = bool)
        Metrix_node_group =  np.zeros((Node_num, Node_num), dtype=bool)
        for x in range(1, len(DAG_Node_Group_sub)-1):
            # Metrix_node_group.append(self.f4(Metrix_group[x], DAG_Node_Group_sub, Metrix_sub,x))
            Metrix_node_group += self.f4(Metrix_group[x], DAG_Node_Group_sub, Metrix_sub, x)
        return Metrix_node_group

    # 函数f4 ：返回某层的联结矩阵组
    #   参数： Metrix_group_sub        整图的节点分布
    #         DAG_Node_Group_sub      所有层可能的联结情况
    #         Metrix_sub              节点联结矩阵
    #         self_level              所在层
    def f4(self, Metrix_group_sub_level, DAG_Node_Group_sub, Metrix_sub, self_level):
        sub_metrix = Metrix_sub.copy()
        nude_num = len(DAG_Node_Group_sub[self_level])  # 本层的节点个数
        for x in range(0, nude_num):  # x代表每一层各节点的分布可能
            sub_axis = DAG_Node_Group_sub[self_level][x]  # 本层中的各节点号码
            m = randint(0, len(Metrix_group_sub_level)-1)
            sub_level_metrix = Metrix_group_sub_level[m]
            for z in range(0, self_level):
                input_num = sub_level_metrix[z][self_level]
                if input_num != 0:
                    for a in range(0, input_num):
                        in_node = DAG_Node_Group_sub[z][a]
                        sub_metrix[in_node][sub_axis] = True
            for z in range(self_level + 1, len(DAG_Node_Group_sub)):
                output_num = sub_level_metrix[self_level][z]
                if output_num != 0:
                    for a in range(0, output_num):
                        out_node = DAG_Node_Group_sub[z][a]
                        sub_metrix[sub_axis][out_node] = True
        return sub_metrix

    """
    def f4(self, Metrix_group_sub_level, DAG_Node_Group_sub, Metrix_sub, self_level):
        nude_num = len(DAG_Node_Group_sub[self_level])  # 本层的节点个数
        zuhe = self.f6(Metrix_group_sub_level, nude_num)
        retu = []
        #print(zuhe)
        for x in range(0, len(zuhe)):        # x代表每一层各节点的分布可能
            sub_metrix = Metrix_sub.copy()
            for y in range(0, len(zuhe[x])):
                sub_axis = DAG_Node_Group_sub[self_level][y]  # 本层中的各节点号码

                sub_level_metrix = zuhe[x][y]
                for z in range(0, self_level):
                    input_num = sub_level_metrix[z][self_level]
                    if input_num != 0:
                        for a in range(0, input_num):
                            in_node = DAG_Node_Group_sub[z][a]
                            sub_metrix[in_node][sub_axis] = True
                for z in range(self_level + 1, len(DAG_Node_Group_sub)):
                    output_num = sub_level_metrix[self_level][z]
                    if output_num != 0:
                        for a in range(0, output_num):
                            out_node = DAG_Node_Group_sub[z][a]
                            sub_metrix[sub_axis][out_node] = True
            retu.append(sub_metrix)
        return retu
    """

    def f6(self, Metrix_group_sub_level, node_num):
        sub_m=[]
        if node_num == 1:
            for x in range(0, len(Metrix_group_sub_level)):
                sub_sub_m = []
                sub_sub_m.append(Metrix_group_sub_level[x])
                sub_m.append(sub_sub_m)
            return sub_m
        else:
            ret_m = self.f6(Metrix_group_sub_level, node_num - 1)
            for x in range(0, len(Metrix_group_sub_level)):
                sub_sub_m=[]
                sub_sub_m.append(Metrix_group_sub_level[x])
                for y in range(0, len(ret_m)):
                    sub_m.append(sub_sub_m + ret_m[y])
            return sub_m

    def f7(self, level_metrix):
        ret_sum = []
        if len(level_metrix) == 1:
            return level_metrix[0]
        else:
            sub_level_metrix = level_metrix.copy()
            del sub_level_metrix[0]
            for x in range(0, len(level_metrix[0])):
                out_mextrix = self.f7(sub_level_metrix)
                for y in range(0, len(out_mextrix)):
                    sub_add = level_metrix[0][x] + out_mextrix[y]
                    ret_sum.append(sub_add)
            return ret_sum

    def f8(self, level_metrix, DAG_list_disp_sub):
        ret_sum = []
        sub_level_metrix = np.zeros(level_metrix[0][0].shape, dtype=bool)
        for x in range(0, len(DAG_list_disp_sub) - 2):
            for y in range(0, DAG_list_disp_sub[x+1]):
                m = randint(0, len(level_metrix[x])-1)
                sub_level_metrix += level_metrix[x][m]
        ret_sum.append(sub_level_metrix)
        return ret_sum
