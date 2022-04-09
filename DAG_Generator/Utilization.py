from random import randint, random, uniform
import numpy as np


#####################################
# 把u随机分成n份
#####################################
def uunifast(n, u):
    sumU = u
    vectU = []
    for i in range(1, n):
        nextSumU = sumU * uniform(0, 1) ** (1.0 / (n - i))
        vectU.append(sumU - nextSumU)
        sumU = nextSumU
    vectU.append(sumU)
    return vectU


# ulimit    利用率上限 = 1
# nsets     生成的集合数量；
def uunifast_discard(n, u, nsets, ulimit=1):
    sets = []
    while len(sets) < nsets:
        # Classic UUniFast algorithm:
        utilizations = []
        sumU = u
        for i in range(1, n):
            nextSumU = sumU * random() ** (1.0 / (n - i))
            utilizations.append(sumU - nextSumU)
            sumU = nextSumU
        utilizations.append(sumU)
        # If no task utilization exceeds ulimit:
        if all(ut <= ulimit for ut in utilizations):
            sets.append(utilizations)
        print('uunifast_sum:', sum(utilizations))
        print('uunifast_set:', sets)
    return sets


# distribute workloads, w, to n nodes
# 给节点分配workloads
# np.random.uniform(low=1, high=2, size=(5))  # : 产生均匀分布的数组，起始值为low，high为结束值，size为形状
# np.random.normal(loc=1, scale=3, size=(5))  # : 产生正态分布的数组， loc为均值，scale为标准差，size为形状
# np.random.poisson(lam=5.0, size=(5))        # : 产生泊松分布的数组， lam随机事件发生概率，size为形状
# eg: a = np.random.uniform(0, 10, (3, 4))
#     a = np.random.normal(10, 5, (3, 4))
# random.uniform(val1, val2)    -> 接受两个数字参数，返回两个数字区间的一个浮点数，不要求val1小于等于val2
# random.randrange(1, 100, 2)   -> 返回[1,100]之间的奇数
# random.random()               -> 无参数，返回一个[0.0, 1.0)之间的浮点数
# random.randint(low, hight)    -> 返回一个位于[low,hight]之间的整数
# np.random.permutation(10) = np.random.shuffle(np.arange(10))  # 随机排列,无序
# np.random.rand(10)            -> 返回10个 [0.0, 1.0)之间的随机浮点数
# np.random.randn(10)           -> 返回10随机数，具有标准正态分布。
# np.random.randint(10,size=10) -> 返回10个10以内的整数
# round()                       -> 四舍五入
def gen_execution_times(n, w, dummy=False):
    c_dict = {}
    c_set = np.random.rand(n)
    f = sum(c_set) / w
    # normalise to w & assign to the execution time list
    for i in range(n):
        c_dict[i + 1] = c_set[i] / f

    return c_dict


if __name__ == "__main__":
    print('\t 1233333:', uunifast(10, 15))
    # 1分成10份生成2两个集合，每份不能大于1,
    # ulimit    利用率上限 = 1
    print('\t 2233333:', uunifast_discard(10, 1, 2, ulimit=1))
    # distribute workloads, w, to n nodes
    print('\t 3200:', gen_execution_times(10, 4, dummy=False))
    print('\t 3210:', gen_execution_times(10, 4, dummy=False))
    # print('\t 3201:', gen_execution_times(10, 4, round_c=False, dummy=True))
    # print('\t 3211:', gen_execution_times(10, 4, round_c=True,  dummy=True))
