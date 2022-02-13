#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################################
# Randomized DAG Generator
# Fang YJ
# Real-Time Systems Group
# Hunan University HNU
################################################################################

from random import randint  # , random
import random as rand
import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# Class: DAG (Directed Acyclic Graph Task)
class DAG:
    def __init__(self):
        # parameters (or use default)
        self.name       = 'Tau_{null}'  # DAG的名称
        self.G          = nx.DiGraph()  # DAG:-networkX结构
        self.task_num   = 0             # DAG中节点（job）的数量
        # generator mine
        self.parallelism    = 3         # 并行度
        self.Critical_path  = 5         # 关键路径长度

    def get_graph(self):  # 返回G
        return self.G

    def save(self, basefolder="data/"):
        # create base folder (if not exists)
        if not os.path.exists(basefolder):
            os.makedirs(basefolder)
        nx.write_gpickle(self.G, basefolder + self.name + '.gpickle')  # save graph (gpickle)
        nx.write_gml(self.G, basefolder + self.name + '.gml')  # save graph (gml)

    def load(self, basefolder="./data/"):
        pass

    def gen(self, algorithm):  # 生成 DAG
        if algorithm == "mine":
            self.gen_mine()
        else:
            return 1
        return 0

    #####################################
    #   获取DAG的并行度和关键路径长度
    #   DAG generator 算法4#
    #####################################
    def dag_param_critical_update(self):
        # 关键路径
        node_list = nx.dag_longest_path(self.G)
        # 获取拓扑分层
        rank_list = [sorted(generation) for generation in nx.topological_generations(self.G)]
        app = []
        for rank_x in rank_list:
            app.append(len(rank_x))
        self.Critical_path = len(node_list)  # 关键路径长度
        self.parallelism = max(app)
        print('关键路径：{0}'.format(node_list))
        print('拓扑分层：{0}'.format(rank_list))

    #####################################
    #   根据DAG的节点num打印节点的属性；
    #   def node_property
    #   param：
    #       node_number;
    #####################################
    def node_property(self, node_number):
        # for node_x in self.G.nodes(data=True):
        node_x = self.G.node[node_number]
        assert (node_number == node_x[0])
        print("node_id", node_x[0], node_number)
        print("node_Node_ID", node_x[1].get('Node_ID'))
        print("node_rank", node_x[1].get('rank'))
        print("node_critic", node_x[1].get('critic'))
        # self.G.node[0]['critic'] == True

    def print_data(self):
        # print(self.G.graph)
        # print(self.G.nodes(data=True))  # 输出所有可能的DAG结果数量；
        print(self.G.nodes.data(data=True))
        print(self.G.edges.data(data=True))

    #####################################
    #   Transitive reduction函数
    #   param:
    #       matrix: Adjacency Matrix
    #   return:
    #       A matrix that has been reduced in transitive
    #####################################
    def transitive_reduction_matrix(self):
        matrix = np.array(nx.adjacency_matrix(self.G).todense())
        row, columns = matrix.shape
        assert (row == self.task_num)
        assert (columns == self.task_num)
        print("matrix shape is ({0},{1})".format(row, columns))
        i_test = np.eye(self.task_num).astype(bool)
        i_matrix = matrix.astype(bool)
        D = np.power((i_matrix | i_test), self.task_num)  # (M | I)^n
        D = D.astype(bool) & (~i_test)
        TR = matrix & (~(np.dot(i_matrix, D)))  # Tr = T ∩ （-（T . D））
        return nx.DiGraph(TR)

    #########################################
    #   DAG graph_node_position_determine
    #   参数：
    #       G：一个DAG；
    #   注：更新self.pos,方便作图
    #       pos = nx.spring_layout(G.get_graph())               #- spring_layout：    用Fruchterman - Reingold算法排列节点
    #       pos = nx.random_layout(G.get_graph())               #- random_layout：    节点随机分布
    #       pos = nx.circular_layout(G.get_graph())             #- circular_layout：  节点在一个圆环上均匀分布
    #       pos = nx.shell_layout(G.get_graph())                #- shell_layout：     节点在同心圆上分布
    #       pos = nx.spectral_layout(G.get_graph(), scale=15)   #- spectral_layout：  根据图的拉普拉斯特征向量排列节
    #########################################
    def graph_node_position_determine(self):
        node_map        = []
        position_map    = []
        color_map       = []
        node_list       = nx.dag_longest_path(G.get_graph())    # 关键路径
        # assert self.Critical_path == len(node_list), (self.Critical_path, len(node_list))
        p_list = np.zeros(self.Critical_path, dtype=int)
        for node_xx in self.G.nodes(data=True):
            node_rank = node_xx[1].get('rank')
            if node_xx[0] in node_list:          # 判断是否在关键路径里
                node_xx[1]['critic'] = True
                k = 0
                color = 'green'
            else:
                p_list[node_rank] += 1
                k = p_list[node_rank]
                color = '#1f78b4'
            node_map.append(node_xx[0])
            position_map.append([100 * node_rank / self.Critical_path, 100 * k / self.parallelism])
            color_map.append(color)
        n_pos = dict(zip(node_map, np.array(position_map)))         # 构建pos列表
        nx.draw_networkx_nodes(self.G,  n_pos,
                               nodelist=node_map, node_color=color_map,
                               node_size=500, node_shape='o')  # 绘制节点
        nx.draw_networkx_edges(self.G,  n_pos)   # 绘制边
        nx.draw_networkx_labels(self.G, n_pos)   # 标签

    #####################################
    #   DAG generator 算法3#
    #   图的Node属性：
    #       Node_num：       节点号码(自然ID)；
    #       rank(level)：    节点所在层；
    #       critic：         节点是否是关键节点
    #   图的Node属性：
    #       Null
    #####################################
    def gen_mine(self):
        assert (self.parallelism >= 1)
        assert (self.Critical_path >= 3)
        # 步骤一：initial a new graph G               # e.g. G = nx.DiGraph(Index=self.task_num)
        #   添加节点；确定rank的节点
        self_critical_path  = self.Critical_path    # 关键路径长度
        self_parallelism    = self.parallelism      # 图的并行度
        self_Node_num       = 0                     # DAG的节点数量
        self.G.add_node(0, Node_ID='souce_node', rank=0, critic=False, WCET=1)  # 起始节点（1）；rank=0
        for x in range(1, self_critical_path - 1):
            m = randint(1, self_parallelism)  # 随机每层的节点数量（不能大于并行度）
            for y in range(1, m + 1):
                self_Node_num += 1
                self.G.add_node(self_Node_num, Node_ID='job{}'.format(self_Node_num), rank=x, critic=False, WCET=1)
        self.G.add_node(self_Node_num + 1, Node_ID='sink_node', rank=self_critical_path - 1, critic=False, WCET=1)
        self.task_num = self_Node_num + 2   # +2算上source和sink
        self.G.add_edge(0, 1)
        for x in range(1, self_critical_path - 1):  # 从第2层开始到倒数第二层
            ancestors_list      = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') < x)]
            descendants_list    = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') > x)]
            self_list           = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') == x)]
            successors_list     = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') == (x+1))]
            for y in self_list:
                k1 = randint(1, len(ancestors_list))
                k2 = randint(1, len(descendants_list))
                ancestors_group = rand.sample(ancestors_list, k1)
                descendants_group = rand.sample(descendants_list, k2)
                for z in ancestors_group:
                    self.G.add_edge(z[0], y[0])
                for z in descendants_group:
                    self.G.add_edge(y[0], z[0])
            self.G.add_edge(self_list[0][0], successors_list[0][0])
        self.name = 'Tau_{:d}'.format(self.task_num)
        # self.G = nx.DiGraph(self.Matrix)                  # 邻接矩阵生成一个有向图netWorkX；属性全无；
        # ## transitive reduction 传递约简； ## #
        self.transitive_reduction_matrix()                  # 更新graph
        # print(np.array(nx.adjacency_matrix(self.G).todense()))
        self_G = nx.DiGraph(self.transitive_reduction_matrix())     # 1.自己写的方法，
        lp = list(self_G.edges())                                   # 1.networkx包
        # lp = list(nx.transitive_reduction(self.G).edges())        # 2.networkx包
        self.G.clear_edges()
        self.G.add_edges_from(lp)
        # print(np.array(nx.adjacency_matrix(self.G).todense()))


if __name__ == "__main__":
    # Parallelism = input("请输入DAG的并行度：")
    # print("你输入的内容是: ", Parallelism)
    # Critical_path = input("请输入DAG的关键路径长度：")
    # print("你输入的内容是: ", Critical_path)
    plt.figure()                            # (figsize=(100.0, 100.0))
    G = DAG()                               # 初始化DAG
    G.parallelism   = 4 # int(Parallelism)      # 输入并行度
    G.Critical_path = 6 # int(Critical_path)    # 输入关键路径长度
    G.gen("mine")

    G.graph_node_position_determine()

    G.dag_param_critical_update()

    anti = nx.antichains(G.get_graph(), topo_order=None)    # 从DAG中生成antichains；
    print('G是aperiodic图：{}'.format(nx.is_aperiodic(G.get_graph())))      # 如果`G`是aperiodic(周期的)则返回true；
    # print(nx.root_to_leaf_paths(G.get_graph()))           # 在DAG中产生一个root - to - leaf paths
    # 一个source node；（node_num:0）;
    # 一个sink   node；（node_num:(task_num+1)）;
    # 1 critical path 关键路径及节点         # 完成；
    print('Critical path=:{0}'.format(nx.dag_longest_path(G.G)))       # 关键路径
    # 2 最短路径：
    shortest_path = list(nx.all_shortest_paths(G.G, 0, G.task_num - 1))
    print('DAG的最短路径：{0}'.format(len(shortest_path)))
    for path in shortest_path:
        print(path)
    # d-denscendants 有掉件的独立性；
    # （1）test_markov_condition(graph):
    for node in G.G.nodes:
        parents = set(G.G.predecessors(node))
        non_descendants = G.G.nodes - nx.descendants(G.G, node) - {node} - parents
        # Y : G - node的后代节点 - node节点 - node的前驱节点；
        # X : node节点；
        # Z : node的前驱节点；
        assert nx.d_separated(G.G, {node}, non_descendants, parents)

    """Algorithms to characterize the number of triangles in a graph."""
    # print(nx.triangles(G.G))            # （报错）Compute the number of triangles.
    # print(nx.average_clustering(G.G))   # 0.0 Compute the average clustering coefficient for the graph G.
    # print(nx.clustering(G.G))           # 节点：0 Compute the clustering coefficient for nodes.
    # print(nx.square_clustering(G.G))    # （OK）Compute the squares clustering coefficient for nodes.
    # print(nx.generalized_degree(G.G))   # （报错）Compute the generalized degree for nodes.
    """Find the k-cores of a graph."""
    print("每个vertex的core数:", nx.core_number(G.G))  # Returns the core number for each vertex.
    # A k-core is a maximal subgraph that contains nodes of degree k or more.
    print("图G的k-core:", nx.k_core(G.G).edges(data=True))        # Returns the k-core of G.
    #   The k-shell is the subgraph induced by nodes with core number k.
    #   That is, nodes in the k-core that are not in the (k+1)-core.
    print("图G的k_shell:", nx.k_shell(G.G).edges(data=True))      # Returns the k-shell of G.
    #   The k-crust is the graph G with the edges of the k-core removed
    #   and isolated nodes found after the removal of edges are also removed.
    print("图G的k_crust:", nx.k_crust(G.G).edges(data=True))      # Returns the k-crust of G.
    #   The k-corona is the subgraph of nodes in the k-core which have
    #   exactly k neighbours in the k-core.
    #   def k_corona(G, k, core_number=None):
    print("图G的k_corona:", nx.k_corona(G.G, None).edges(data=True))    # Returns the k-corona of G.
    """Routines to find the boundary of a set of nodes."""
    print("edge_boundary:", list(nx.edge_boundary(G.G, [1])))
    print("node_boundary:", list(nx.node_boundary(G.G, [1])))
    """Dominance algorithms."""
    # Returns the immediate dominators of all nodes of a directed graph.
    print("immediate_dominators:", nx.immediate_dominators(G.G, 0))
    # Returns the dominance frontiers of all nodes of a directed graph.
    print("dominance_frontiers:", nx.dominance_frontiers(G.G, 0))
    """Flow Hierarchy."""
    # Returns the flow hierarchy of a directed network.
    # print("flow_hierarchy:", nx.flow_hierarchy(G.G))
    """Algorithms for finding the lowest common ancestor of trees and DAGs."""
    # print("tree_all_pairs_lowest_common_ancestor:", list(nx.tree_all_pairs_lowest_common_ancestor(G.G)))
    # print("lowest_common_ancestor:", list(nx.lowest_common_ancestor(G.G, 2, 3)))
    print("all_pairs_lowest_common_ancestor:", list(nx.all_pairs_lowest_common_ancestor(G.G)))
    """Algorithms to calculate reciprocity in a directed graph."""
    print("reciprocity:", nx.reciprocity(G.G))                  # Compute the reciprocity in a directed graph.
    print("overall_reciprocity:", nx.overall_reciprocity(G.G))  # Compute the reciprocity for the whole graph.
    """Functions for computing and verifying regular graphs."""
    # 定义（regular graph）：图中每个节点都有相同的度。regular有向图是指每个顶点的入度和出度相等的图。
    # is_regular：Determines whether the graph ``G`` is a regular graph.
    print("Graph is_regular:", nx.is_regular(G.G))
    # 定义（k-regular graph）：a graph where each vertex has degree k.不支持有向图
    # is_k_regular：Determines whether the graph ``G`` is a k-regular graph.
    """Hubs and authorities analysis of graph structure."""
    # h, a = nx.hits(G.G)   # Returns HITS hubs and authorities values for nodes.
    print("HITS hubs and authorities values for nodes:\n", nx.hits(G.G))
    # Returns the HITS authority matrix.
    print("authority_matrix:\n", nx.authority_matrix(G.G))
    # Returns the HITS hub matrix.
    print("hub_matrix:\n", nx.hub_matrix(G.G))
    """PageRank analysis of graph structure. """
    # Returns the PageRank of the nodes in the graph.
    print("pagerank:\n", nx.pagerank(G.G))
    # Returns the Google matrix of the graph.
    print("google_matrix:\n", nx.google_matrix(G.G))
    # Returns the PageRank of the nodes in the graph.
    # print("pagerank_numpy:\n", nx.pagerank_numpy(G.G))
    # Returns the PageRank of the nodes in the graph.
    # print("pagerank_scipy:\n", nx.pagerank_scipy(G.G))
    """# tracersal #"""
    """Basic algorithms for breadth-first searching(BFS) the nodes of a graph."""
    # Iterate over edges in a breadth-first-search starting at source.
    print("bfs_edges:\n", list(nx.bfs_edges(G.G, 0)))
    # Returns an oriented tree constructed from of a breadth-first-search starting at source.
    print("bfs_tree:\n", list(nx.bfs_tree(G.G, 0)))
    # Returns an iterator of predecessors in breadth-first-search from source.
    print("bfs_predecessors:\n", list(nx.bfs_predecessors(G.G, 0)))
    # Returns an iterator of successors in breadth-first-search from source.
    print("bfs_successors:\n", list(nx.bfs_successors(G.G, 0)))
    # Returns all nodes at a fixed `distance` from `source` in `G`.
    print("descendants_at_distance:\n", list(nx.descendants_at_distance(G.G, 0, G.Critical_path-2)))
    """Basic algorithms for depth-first searching(DFS) the nodes of a graph."""
    # Iterate over edges in a depth-first-search (DFS).
    print("dfs_edges:\n", list(nx.dfs_edges(G.G, source=0)))
    # Returns oriented tree constructed from a depth-first-search from source.
    print("dfs_tree:\n", list(nx.dfs_tree(G.G, source=0)))
    # Returns dictionary of predecessors in depth-first-search from source.
    print("dfs_predecessors:\n", list(nx.dfs_predecessors(G.G, source=0)))
    # Returns dictionary of successors in depth-first-search from source.
    print("dfs_successors:\n", list(nx.dfs_successors(G.G, source=0)))
    # Generate nodes in a depth-first-search post-ordering starting at source.
    print("dfs_postorder_nodes:\n", list(nx.dfs_postorder_nodes(G.G, source=0)))
    # Iterate over edges in a depth-first-search (DFS) labeled by type.
    print("dfs_labeled_edges:\n", list(nx.dfs_labeled_edges(G.G, source=0)))
    """Algorithms for a breadth - first traversal of edges in a graph."""
    # A directed, breadth-first-search of edges in `G`, beginning at `source`.
    print("edge_bfs:\n", list(nx.edge_bfs(G.G, source=0)))
    """Algorithms for a depth - first traversal of edges in a graph."""
    # A directed, depth-first-search of edges in `G`, beginning at `source`.
    print("edge_dfs:\n", list(nx.edge_dfs(G.G, source=0)))
    """Functions for identifying isolate (degree zero) nodes."""
    # Determines whether a node is an isolate.
    # def is_isolate(G, n):
    # Iterator over isolates in the graph.
    print("isolates:\n", list(nx.isolates(G.G)))
    # Returns the number of isolates in the graph.
    print("number_of_isolates:\n", nx.number_of_isolates(G.G))

    # 3.node_num节点的前驱、后继、祖先、后代    # 完成；
    for self_node in G.G.nodes(data=True):
        print('node_num=:{0}'.format(self_node))
        print('\t前驱节点（predecessors）：{0}'.format(list(G.G.predecessors(self_node[0]))))
        print('\t祖先节点（ancestors）：{0}'.format(nx.ancestors(G.get_graph(), self_node[0])))
        print('\t后继节点（successors）：{0}'.format(list(G.G.successors(self_node[0]))))
        print('\t后代节点（descendants）：{0}'.format(nx.descendants(G.get_graph(), self_node[0])))
        print('\t节点的邻居（neighbors）：{0}'.format(list(nx.neighbors(G.G, self_node[0]))))  # 就是后继节点 successors
        print('\t节点的度（degree）：{0}'.format(nx.degree(G.G, self_node[0])))  # node 0 with degree 1
        print('\t节点的入度（in_degree）：{0}'.format(G.G.in_degree(self_node[0])))
        print('\t节点的出度（out_degree）：{0}'.format(G.G.out_degree(self_node[0])))

    # 4.1 节点的拓扑排序
    # print('node_topological_sort:{}'.format(list(nx.topological_sort(G.get_graph()))))
    print('4.1 node_topological_sort:{}'.format(list(nx.topological_sort(G.G))))
    # 4.2 边的拓扑排序
    print('4.2 edge_topological_sort:{}'.format(list(nx.topological_sort(nx.line_graph(G.G)))))
    # 获取ID为node_n的后继节点；     获取ID为node_n的前驱节点；
    # Makespan                          # 待完成！
    plt.title('DAG generator' +
              '\n Is a DAG:{0}'.format(nx.is_directed_acyclic_graph(G.get_graph())) +  # 检测是否是有向无环图
              '\n number of nodes for DAG:{0}'.format(G.G.number_of_nodes()) +         # 返回G的节点数量
              '\n number of edges for DAG:{0}'.format(G.G.number_of_edges()) +          # 返回G的边数量
              '',
              fontsize=10, color="black", weight="light", ha='left', x=0)   # style="italic",
    plt.xlabel('crirical={}'.format(G.Critical_path))
    plt.ylabel('param={}'.format(G.parallelism))
    plt.show()
    # G.save(basefolder="data/")

    # 传递闭包***
    # 有向图的 transitive closure；
    # nx.transitive_closure(G, reflexive=False)
    # 如果有向无环形图的transitive closure；
    # nx.transitive_closure_dag(G.get_graph(), topo_order=None)
    # print('1', np.array(nx.adjacency_matrix(G.get_graph()).todense()))
    # print('2', np.array(nx.adjacency_matrix(G1).todense()))
