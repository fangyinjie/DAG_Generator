# 线性空间
# 线性子空间
# 线性空间的基
# 两个基之间的过度矩阵
# 元素的坐标
# 线性变换的矩阵
# 基的度量矩阵
# 标准正交基
from scipy.linalg import *
import numpy as np

a=np.array([[1,2,3],[2,1,3],[3,2,1]])
a=a.T
print(a)
b=orth(a)
print(orth(a))
two_multi_res = np.dot(a, b)
print(two_multi_res)

