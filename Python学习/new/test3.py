import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import numpy as np

def Normalize(array):
    '''
    Normalize the array
    '''
    mx = np.nanmax(array)
    mn = np.nanmin(array)
    t = (array-mn)/(mx-mn)
    return t

# file = 'data.txt'
# data1 = pd.read_csv(file, sep=",")
data1 = pd.read_csv('data_real.csv')
plt.figure()
data1.makespan = Normalize(data1.makespan)

# sns.boxplot(y='makespan', x='Core', hue="names", data=data1, dodge=False, width=0.2)
# sns.boxplot(x="makespan", y="Core", data=data1)

# sns.boxplot(y='makespan', x='Core',hue="names",data=data1, linewidth=1.5, showfliers=False)
# sns.boxplot(y='makespan', x='Parallelism',hue="names",data=data1, linewidth=1.5, showfliers=False)
sns.boxplot(y='makespan', x='cri',hue="names",data=data1, linewidth=1.5, showfliers=False)
plt.title("cri_test") # 图形标题
plt.xlabel("x cri") # x轴名称
plt.ylabel("y makespan") # y 轴名称
# sns.boxplot(x="age", y="cost", data=data, hue="sex", width=0.5, linewidth=1.0, palette="Set3")
plt.show()
