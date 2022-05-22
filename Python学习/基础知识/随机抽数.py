# from random import seed, randint, random
import random
# 方法一：
#[random.randint(0,100) for _ in range(2)]
# 输出： [34, 44]

#方法二：
#list中随机去取K个数
k =3
list=[[1,2],[3,4],[5,6],[7,8],[9,10]]
# list=[1,2,3,4,5,6,7,8,9,10]
print(random.sample(list, k))
