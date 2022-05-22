import matplotlib.pyplot as plt
"""
def gatt(CHS,Processing_time,Setup_time,Transpotation_time,M_num,O_Max_len,J_num):
    # D=Decode_Matrix(CHS, Processing_time, Setup_time, Transpotation_time, M_num, O_Max_len, J_num)
    # # print(CHromo)
    # End_time=D[1]
    # Start_time=D[0]
    # S_start=D[2]
    # S_end=D[3]
    # T_start=D[4]
    # T_end=D[5]
    # T0 = J_num * O_Max_len
    # N = M_num
    # Start = []
    # End = []
    # M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink','Thistle','Magenta','SlateBlue','RoyalBlue','Cyan','Aqua','floralwhite','ghostwhite','goldenrod','mediumslateblue','navajowhite',
    #          'navy','sandybrown','moccasin']
    # S_color='white'
    # T_color='grey'
    # s=('/', '+', 'x', '\\', '||', 'o', '///','//' '.','//','#','||')
    for i in range(N):
        for j in range(T0):
            if End_time[i][j] != 0 and End_time[i][j] - Start_time[i][j] != 0:
                plt.barh(i*3, width=End_time[i][j] - Start_time[i][j],height=0.8, left=Start_time[i][j],
                              color=M[int(j/O_Max_len)],edgecolor='black')
                plt.text(x=Start_time[i][j] + 0.1, y=i*3, s=(int(j/O_Max_len)+1, j%O_Max_len+1),fontsize=8)
            if S_end[i][j] != 0 and S_end[i][j] - S_start[i][j] != 0:
                plt.barh(i * 3+1, width=S_end[i][j] - S_start[i][j], height=0.8, left=S_start[i][j],
                         color=S_color, edgecolor='black')
                plt.text(x=S_start[i][j] + 0.1, y=i * 3+1, s=(int(j / O_Max_len) + 1, j % O_Max_len + 1),
                         fontsize=8)
            if T_end[i][j] != 0 and T_end[i][j] - T_start[i][j] != 0:
                plt.barh(i * 3+2, width=T_end[i][j] - T_start[i][j], height=0.8, left=T_start[i][j],
                         color=T_color, edgecolor='black')
                plt.text(x=T_start[i][j] + 0.1, y=i * 3+2, s=(int(j / O_Max_len) + 1, j % O_Max_len + 1),
                         fontsize=8)
                Start.append(Start_time[i][j])
                End.append(End_time[i][j])
"""

plt.barh(y=12,              # y轴中线坐标
         width=10,          # 宽度
         height=1,        # 高度
         left=3,            # x左边坐标
         color='grey',
         edgecolor='black')
plt.text(x=3,
         y=12,
         s='sdd',
         fontsize=8)
plt.show()
