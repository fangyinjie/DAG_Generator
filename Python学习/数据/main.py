import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def list_generator(mean, dis, number):  # 封装一下这个函数，用来后面生成数据
    return np.random.normal(mean, dis * dis, number)  # normal分布，输入的参数是均值、标准差以及生成的数量


if __name__ == "__main__":
    filename = 'data.txt'  # txt文件和当前脚本在同一目录下，所以不用写具体路径
    pos = []
    Efield = []
    pp = []
    with open(filename, 'r') as file_to_read:
        lines = file_to_read.readline()
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
                pass
            lines = lines.rstrip("\n")
            pp.append(lines.split(",", -1))
            # p_tmp, E_tmp = [i for i in lines.split()]  # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            # pos.append(p_tmp)  # 添加新读取的数据
            # Efield.append(E_tmp)
            # pass
    our_NoCore = []
    our_Nopar = []
    our_NoCri = []
    other_NoCore = []
    other_Nopar = []
    other_NoCri = []

    else_other = []
    for i in pp:
        buff = []
        # buff.append(int(i[1]))
        # buff.append(int(i[3]))
        # buff.append(int(i[4]))
        # buff.append(int(i[5]))
        # buff.append(int(i[6]))
        buff = float(i[6])
        i[2] = i[2].rstrip(" ")
        i[0] = i[0].rstrip(" ")
        if (i[2] == 'NoCore'):
            if (i[0] == 'our'):
                our_NoCore.append(buff)
            elif (i[0] == 'other'):
                other_NoCore.append(buff)
            else:
                else_other.append(buff)
        elif (i[2] == 'NoPar'):
            if (i[0] == 'our'):
                our_Nopar.append(buff)
            elif (i[0] == 'other'):
                other_Nopar.append(buff)
            else:
                else_other.append(buff)
        elif (i[2] == 'NoCri'):
            if (i[0] == 'our'):
                our_NoCri.append(buff)
            elif (i[0] == 'other'):
                other_NoCri.append(buff)
            else:
                else_other.append(buff)
        else:
            else_other.append(buff)


    # our_NoCore = []
    # our_Nopar = []
    # our_NoCri = []
    # other_NoCore = []
    # other_Nopar = []
    # other_NoCri = []

    our = []
    other = []
    for i in range(len(our_NoCore)):
        our_NoCore[i]=(our_NoCore[i])/(max(our_NoCore) - min(our_NoCore))
    for i in range(len(our_Nopar)):
        our_Nopar[i]=(our_Nopar[i])/(max(our_Nopar) - min(our_Nopar))
    for i in range(len(our_NoCri)):
        our_NoCri[i]=(our_NoCri[i])/(max(our_NoCri) - min(our_NoCri))
    for i in range(len(other_NoCore)):
        other_NoCore[i]=(other_NoCore[i])/(max(other_NoCore) - min(other_NoCore))
    for i in range(len(other_Nopar)):
        other_Nopar[i] = (other_Nopar[i]) / (max(other_Nopar) - min(other_Nopar))
    for i in range(len(other_NoCri)):
        other_NoCri[i] = (other_NoCri[i]) / (max(other_NoCri) - min(other_NoCri))

    for i in range(len(our_NoCore)):
        our_buff=[]
        our_buff.append(our_NoCore[i])
        our_buff.append(our_Nopar[i])
        our_buff.append(our_NoCri[i])
        our.append(our_buff)
    for i in range(len(other_NoCore)):
        other_buff = []
        other_buff.append(other_NoCore[i])
        other_buff.append(other_Nopar[i])
        other_buff.append(other_NoCri[i])
        other.append(other_buff)

    our = np.array(our)
    other = np.array(other)
    # plt.figure(figsize=(6, 6), dpi=60)  # 设置画板

    # fig, axes = plt.subplots(1, 2)
    fig, axes = plt.subplots()
    # plt.title("Multi Box-plot Test")

    colors = ["darkred", "darkgreen", "darkblue"]
    # .boxplot(our_NoCore_1, labels=["our_NoCore_1"])
    # axes.boxplot(
    #             our,
    #             positions=[2, 4, 6],
    #             # labels=['A','B','C'],
    #             sym='o',            # 异常点的形状，参照marker的形状
    #             vert=True,          # 图是否竖着画
    #             whis=1.5,           # 上下须与上下四分位的距离，默认为1.5倍的四分位差
    #             color= "darkred",
    #             showfliers=False)   # 是否显示异常值
    pass
    pass
    plt.boxplot([our,our],
                    # positions=["NoCore", "Nopar", "NoCri"],
                    positions=[2,4,6,12,14,16],
                    widths=1.5,
                    patch_artist=True,
                    showmeans=False,
                    showfliers=False,
                    medianprops={"color": "white", "linewidth": 0.5},
                    boxprops={"facecolor": "C0", "edgecolor": "white","linewidth": 0.5},
                    whiskerprops={"color": "C0", "linewidth": 1.5},
                    capprops={"color": "C0", "linewidth": 1.5})
    #
    # axes[0].boxplot(other,
    #                 positions=[2, 4, 6],
    #                 widths=1.5,
    #                 patch_artist=True,
    #                 showmeans=False, showfliers=False,
    #                 medianprops={"color": "white", "linewidth": 0.5},
    #                 boxprops={"facecolor": "C0", "edgecolor": "white","linewidth": 0.5},
    #                 whiskerprops={"color": "C0", "linewidth": 1.5},
    #                 capprops={"color": "C0", "linewidth": 1.5})

    # plt.savefig("b.png")



    # bp_dict = data.boxplot(by="Name",
    #                        grid=False,
    #                        fontsize = 10,
    #                        rot = 30,
    #                        patch_artist = True,
    #                        return_type = 'both')

    #
    # for row_key, (ax, row) in bp_dict.iteritems():  # 给每个box添加颜色
    #     ax.set_xlabel('')
    #     for i, box in enumerate(row['boxes']):
    #         box.set_facecolor(colors[i])
    #         plt.show()
    #
    # plt.savefig('boxplot.pdf')
    plt.show()

