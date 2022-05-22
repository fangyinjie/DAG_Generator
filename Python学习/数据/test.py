import pandas as pd
#导入二维数组操作模块pandas
# data = pd.read_csv('iris.csv') #导入数据\
# print(data.head()) #打印数据前五行，结构如下：
# SepalLength  SepalWidth  PetalLength  PetalWidth Name0
# 5.1         3.5          1.4         0.2     Iris-setosa1
# 4.9         3.0          1.4         0.2    Iris-setosa2
# 4.7         3.2          1.3         0.2     Iris-setosa3
# 4.6         3.1          1.5         0.2      Iris-setosa4
# 5.0         3.6          1.4         0.2     Iris-setosa


import matplotlib.pyplot as plt
import matplotlib

our_NoCore= [3.2, 3.6, 2.8, 2.9, 2.9, 3.6, 3.3, 4.6, 3.4, 3.1]
our_Nopar = [5.4, 5.2, 5.6, 5.0, 5.7, 5.4, 5.5, 5.4, 5.2, 5.3]
our_NoCri = [2.2, 2.4, 2.3, 2.3, 2.7, 2.1, 2.4, 2.4, 2.6, 2.4]
SepalLength  = {"123":our_NoCore}
fig1, ax1 = plt.subplots()
ax1.boxplot(our_NoCore)
ax1.boxplot(    our_NoCore,
                patch_artist=True,
                boxprops=dict(facecolor="darkred", color="darkred")     # 颜色
            )

plt.show()

import seaborn as sns

tips = sns.load_dataset("tips")
print(tips.head())

ax = sns.boxplot(x="day", y="total_bill", hue="smoker",data=tips)
plt.show()
