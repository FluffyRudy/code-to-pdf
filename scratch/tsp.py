# title: 5
# aim: Program to implement Travelling Salesman Problem using Python.

import itertools


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, cost):
        if u not in self.graph:
            self.graph[u] = {}
        if v not in self.graph:
            self.graph[v] = {}
        self.graph[u][v] = cost
        self.graph[v][u] = cost

    def tsp(self):
        if not self.graph:
            return [], 0

        vertices = list(self.graph.keys())
        min_path = float("inf")
        min_route = []

        for perm in itertools.permutations(vertices[1:]):
            current_path = [vertices[0]] + list(perm) + [vertices[0]]
            current_cost = sum(
                self.graph[current_path[i]].get(current_path[i + 1], float("inf"))
                for i in range(len(current_path) - 1)
            )
            if current_cost < min_path:
                min_path = current_cost
                min_route = current_path

        return min_route, min_path


g = Graph()
g.add_edge("A", "B", 10)
g.add_edge("A", "C", 15)
g.add_edge("B", "C", 35)
g.add_edge("B", "D", 25)
g.add_edge("C", "D", 30)
print(g.tsp())
