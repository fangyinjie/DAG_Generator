from matplotlib import pyplot as plt
dataArray=[5,6,2,4,8,9,10,2,4,5,3,5,15]
dataArray2=[1,2,7,9,5,7,6,8,2,3,4,10,2,4,0]
fig,axes=plt.subplots( 2, 2)
axes[1,1].boxplot((dataArray,dataArray2),labels=["A","B"])
axes[0,1].boxplot((dataArray,dataArray2),labels=["A","B"])
plt.title("Multi Box-plot Test")
plt.savefig("b.png")
plt.show()