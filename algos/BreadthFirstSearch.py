import collections


class Graph:
    def __init__(self, v):
        self.v = v  # 顶点
        self.adjacency = [[] for _ in range(v)]  # 邻接表

    def add_edge(self, s, t):  # 无向图一条边存两次
        self.adjacency[s].append(t)
        self.adjacency[t].append(s)

    def bfs(self, s, t):
        # s表示起始顶点，t表示终止顶点，获得一条s至t的最短路径
        if s == t:
            return
        # visited记录已经被访问的顶点
        visited = [None] * self.v
        visited[s] = True
        # queue用来存储已经被访问、但其相连的顶点还没有被访问的顶点
        queue = collections.deque()
        queue.append(s)
        # prev用来记录搜索路径
        prev = [-1] * self.v
        while queue:
            w = queue.popleft()
            for neighbour in self.adjacency[w]:
                if not visited[neighbour]:
                    prev[neighbour] = w
