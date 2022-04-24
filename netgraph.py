class Netgraph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_node(self, node=None):
        if node is None:
            self.nodes.add(Node())
        else:
            self.nodes.add(node)

    def add_new_edge(self, cost, node_one, node_two):
        edge = Edge(cost, node_one, node_two)
        self.edges.add(edge)

    def add_edge(self, edge):
        self.


class Node:
    def __init__(self, name=None):
        if name is None:
            self.name = "Node"
        else:
            self.name = name
        self.edges = set()


class Edge:
    def __init__(self, cost, node_one, node_two):
        self.nodes = {node_one, node_two}
        self.cost = cost
        node_one.edges.add(self)
        node_two.edges.add(self)
