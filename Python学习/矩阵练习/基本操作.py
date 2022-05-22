import numpy as np

# 2-D array: 2 x 3
two_dim_matrix_one = np.array([[1, 2, 3],
                               [4, 5, 6]])
# 2-D array: 3 x 2
two_dim_matrix_two = np.array([[1, 2],
                               [3, 4],
                               [5, 6]])

two_multi_res = np.dot(two_dim_matrix_one, two_dim_matrix_two)      # 点乘运算

print('two_multi_res: %s' % (two_multi_res))

# 1-D array
one_dim_vec_one = np.array([1, 2, 3])
one_dim_vec_two = np.array([4, 5, 6])
one_result_res = np.dot(one_dim_vec_one, one_dim_vec_two)           # 点乘运算
print('one_result_res: %s' % (one_result_res))

# 1.异或运算:
#   bool1^bool2
# 2.或运算:
#   bool1 | bool2
#   bool1 or bool2
# 3.与运算:
#   bool1 & bool2
#   bool1 and bool2
# 4.非运算：
#   not bool1
#
#   np.logical_not(cond1)
#       out:array([False,  True, False, False,  True], dtype = bool)
#   ~cond1
#       out:array([False,  True, False, False,  True], dtype = bool)
# 5.亦或运算：
#   cond1 = np.array([True, False, True, True, False])
#   cond2 = np.array([False, True, True, True, False])
#       方法（1）：
#   cond1 ^ cond2
#   out:array([ True,  True, False, False, False], dtype=bool)
#       方法（2）：
#   np.bitwise_xor(cond1, cond2)
#   out:array([ True,  True, False, False, False], dtype=bool)
# 与：&；
# 或：|；
# 布尔当作0、1处理
# int计算，Bool型计算过程可以看做是0或1
# -True
# out:-1
# result = 1 * (cond1 ^ cond2) + 2 * (cond1 & cond2) + 3 * ~(cond1 | cond2)
# out:array([1, 1, 2, 2, 3])

# 创建一维数组
# a = np.array([0,1,4])
# 创建多维数组
# b = np.array([[1,2,3,4], [5,6,7,8]])
# 创建整数类型的数组
# c = np.array(range(6), dtype = int)
# 创建两个维度，数据类型是整数的数组
# d = np.array(range(6), dtype = int, ndmin=2)          # 数据类型是整数，数据维度是2
# 输入的是几个维度，就自动生成几个维度的数组
# f=np.array([range(6),range(6)],ndmin=0,dtype=float)   # ndim=0是按照输入的维度来算
# 创建一个值均为0的2*2多维ndarray对象
# np.zeros((2,2))
# test1 = np.zeros((2, 2), dtype = bool)
# test2 = np.zeros((2, 2), dtype = bool)
# test1[0][1] = True  # 行 列
# test2[1][1] = True  # 行 列
# test = test1 + test2

# 创建一个值均为1的1*2维ndarray对象
# np.ones([1,2])
# 创建一个值均为7的3*3维ndarray对象
# np.full((3,3),7)
# 创建一个4*4维对角矩阵
# np.eye(4)
# np.eye(4,k=1) #向后面移动一位

# 数据类型转换：
# 浮点型
# np.float64(42)
# 整型
# b = np.int8(60)
# 注意：转换的值不要超出数据类型的范围
# np.int8(400)          #-112
# 布尔类型,注意：除了0为false,其他的数字都为true
# np.bool(0)            # false
# np.bool(1)            # true
# np.float64(True)      # 1.0
# np.int(False)         # 0
# np.int(True)          # 1

# 类似range,创建浮点型的数组
# np.arange(7, dtype = 'f')
# 创建复数型的数组
# np.arange(7, dtype = 'D')
