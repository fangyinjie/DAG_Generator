import numpy as np
import math

degree      = [5,2,2,2,2,2,4,3]
degreein    = [0,1,1,1,1,1,3,3]
degreeout   = [5,1,1,1,1,1,1,0]

shape       = [1,5,1,1]

mean = np.mean(degreeout)
variance = np.var(degreeout)                        # 方差
standard_deviation2 = np.std(degreeout, ddof = 0)   # 标准差


print("平均值:", str(mean))
print("方差:", str(variance))
print("标准差:", str(standard_deviation2))

# print("稠密度:", 8*math.log2(8))
print("稠密度:", 11/(8*(8-1)))
# result = 0.253493383743
