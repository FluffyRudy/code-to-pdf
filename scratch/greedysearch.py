# title: 13
# aim: Program to implement Greedy Search Algorithm.


class GreedySearch:
    def __init__(self, graph):
        self.graph = graph

    def search(self, start, goal):
        visited = set()
        queue = [(start, 0)]
        while queue:
            queue.sort(key=lambda x: x[1])
            current, cost = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                return cost
            for neighbor, edge_cost in self.graph[current].items():
                if neighbor not in visited:
                    queue.append((neighbor, cost + edge_cost))
        return None


graph = {
    "A": {"B": 1, "C": 2},
    "B": {"A": 1, "D": 3},
    "C": {"A": 2, "D": 1},
    "D": {"B": 3, "C": 1},
}
greedy = GreedySearch(graph)
result = greedy.search("A", "D")
print(result)
