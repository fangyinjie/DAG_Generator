import numpy as np

Ti = np.array([[0, 1, 0, 0, 1, 1, 0],
              [0, 0, 1, 0, 1, 0, 0],
              [0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 1, 0, 1, 1],
              [0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0]])

print(Ti.shape())                       # 输出（7,7）

I = np.identity(7)                      # 生成7 * 7 单位矩阵（浮点型）
T = np.array(Ti).astype(bool)            # int型数据矩阵转化成bool类型的数据矩阵
I = np.array(I).astype(bool)
In = ~I                                 # 矩阵取反
M = (T | I)                             # T I矩阵取或运算
Mold = np.identity(7)                   # 生成7 * 7 单位矩阵
Mnew = M                                # np.zeros((7,7))
while(~(Mold == Mnew).all()):
    Mold = Mnew
    Mnew = np.dot(Mold, M)

# xk = T[:,0]
# xkpp = np.array([1, xk.shape[1]])   # ndim = 0是按照输入的维度来算
while(~(Mold == Mnew).all()):
    Mold = Mnew
    Mnew = np.dot(Mold, M)

x0 = T.T[:,0]
# x0 = T.T
print(x0)
D = Mnew & In
print(D)
Di = np.array(D).astype(int)
print(Di)
RES = T & (~(np.dot(T, D)))
print(RES)
# print(Di**2)
# print(Di**3)
# print(Di**4)
# print(Di**5)


