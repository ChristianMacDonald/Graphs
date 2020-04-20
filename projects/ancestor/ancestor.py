from collections import deque

class Graph:
    def __init__(self):
        self.nodes = {}
    
    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = set()
    
    def add_edge(self, child, parent):
        parents = self.nodes[child]
        if parent not in parents:
            parents.add(parent)
    
    def get_parents(self, child):
        return self.nodes[child]

def dft(graph, starting_node):
    stack = deque()
    stack.append((starting_node, 0))
    visited = set()
    visited_pairs = set()

    while len(stack) > 0:
        current_pair = stack.pop()
        visited_pairs.add(current_pair)
        current_node, current_distance = current_pair

        if current_node not in visited:
            visited.add(current_node)
            parents = graph.get_parents(current_node)

            for parent in parents:
                stack.append((parent, current_distance + 1))
    
    longest_distance = 0
    furthest_ancestor = -1

    for node, distance in visited_pairs:
        if distance > longest_distance:
            longest_distance = distance
            furthest_ancestor = node
        elif distance == longest_distance:
            if node < furthest_ancestor:
                furthest_ancestor = node
    
    return furthest_ancestor

def earliest_ancestor(ancestors, starting_node):
    graph = Graph()
    
    for parent, child in ancestors:
        graph.add_node(child)
        graph.add_node(parent)
        graph.add_edge(child, parent)
    
    return dft(graph, starting_node)