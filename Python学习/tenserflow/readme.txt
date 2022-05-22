tf.contrib.layers.12_regularizer()
                    11、12、sum、apply
                    regularizer     ——正则运算；     p1(权重)        p2(所求矩阵)


tf.MatMul:      tf的矩阵相乘算法
tf.multiply:    矩阵间点乘算法

sparse_softmax_cross_entropy_with_logits            (实际__.预测结果)
tf_nn_softmax_cross_entropy_with_logits             (求交叉熵)

tf.train.AdamOptimizer

np.dot([] [])                                       两个矩阵点乘
tf.Variable
tf.clop_by_value(A, min, max)                       在一个张量A的每个元素压缩在（min max）之间，小于min则返回min大于max则返回max
tf.reduce_mean(input_tensor, reduction_indices = None, keep_dins=False, name=None)
取张量均值，2参数      0   每行的均值row取均值
                    1   每列的均值
tf.split(split_dim, num_split, value, name='split')
切割张量成更小的张量
s_d     分割开始方向
n_s     切成几段

X_train,    X_test,     y_train,    y_test = cross_validation.train_test_split
(train_data, train_target, test_size = 0.4, random_state = 0)
# train_test_split 是交叉验证中常用的函数，功能是从样本中随机的按比例选取train_data和test_data


endswith()方法用于判断字符串是否以指定后缀结尾，如指定了返回True
    否则返回False。可选参数“start”与“end”为检索字符的开始与结束的位置。
endswith(suffix, start#开始位置#, end#结束位置#)


