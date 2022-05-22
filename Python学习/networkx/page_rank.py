from matplotlib import pyplot as plt
import networkx as nx
# 七，计算每个顶点的PageRank值
# 每个顶点的PageRank（简称PR）值，是访问顶点的概率，可以通过networkx.pagerank()
# 函数来计算，该函数根据顶点的入边和边的权重来计算顶点的PR值，
# 也就是说，PR值跟顶点的入边有关，跟入边的weight（权重）属性有关：
# pagerank(
#       g_1,
#       alpha=0.85,
#       personalization=None,
#       max_iter=100,
#       tol=1e-06,
#       nstart=None,
#       weight='weight',
#       dangling=None)
# 常用参数注释：
    # g：无向图会被转换为有向图，一条无向边转换为两条有向边；
    # alpha：阻尼参数，默认值是0.85，取值范围为0到1, 代表从图中某一特定点指向其他任意点的概率；
    # weight：默认值是weight，表示使用edge的weight属性作为权重，如果没有指定，那么把edge的权重设置为1；
# 1，举个例子
# 例如，创建一个有向图，由三个顶点（A、B和C），两条边（A指向B，A指向C），边的权重都是0.5
if __name__ == "__main__":
  g = nx.DiGraph()
  g.add_weighted_edges_from([('A', 'B', 0.5), ('A', 'C', 0.5)])
  print(nx.pagerank(g))
  g['A']['C']['weight'] = 1
  print(nx.pagerank(g))
# 2，查看各个顶点的PR值
# 根据图来创建PageRank，并查看各个顶点的PageRank值
  pr = nx.pagerank(g)
  # page_rank_value=pr['A']
  for node, pageRankValue in pr.items():
    print("%s,%.4f" % (node, pageRankValue))
