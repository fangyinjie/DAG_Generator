import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
rcParams['axes.unicode_minus'] = False
rcParams['font.sans-serif'] = ['Simhei']
y1 = (1,2,3,4,5,6,7,8,10)
y2 = (1,2,3,10,5,6,7,8,15)
data = pd.DataFrame({"Seq2seq": y1, "LSTM": y2})
df = pd.DataFrame(data)
df.plot.box()
plt.xlabel("",fontsize=16)
plt.ylabel("",fontsize=16)
plt.grid(linestyle="--", alpha=0.8)
print(df.describe())#显示中位数、上下四分位数、标准偏差等内容
plt.show()
