# title: 12
# aim: Program to implement A* Search Algorithm.

import heapq


class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, u, v, cost):
        if u not in self.edges:
            self.edges[u] = {}
        if v not in self.edges:
            self.edges[v] = {}
        self.edges[u][v] = cost
        self.edges[v][u] = cost


class AStarSearch:
    def __init__(self, graph):
        self.graph = graph

    def heuristic(self, a, b):
        return 1

    def search(self, start, goal):
        queue = []
        heapq.heappush(queue, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while queue:
            current = heapq.heappop(queue)[1]
            if current == goal:
                break
            for neighbor, cost in self.graph.edges[current].items():
                new_cost = cost_so_far[current] + cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(goal, neighbor)
                    heapq.heappush(queue, (priority, neighbor))
                    came_from[neighbor] = current
        return came_from


graph = Graph()
graph.add_edge("A", "B", 1)
graph.add_edge("A", "C", 4)
graph.add_edge("B", "C", 2)
graph.add_edge("B", "D", 5)
graph.add_edge("C", "D", 1)

astar = AStarSearch(graph)
came_from = astar.search("A", "D")
print(came_from)
