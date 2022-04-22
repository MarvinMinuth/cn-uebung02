# Marvin Minuth, 1077466
# Aufgabe 1:
# Netzwerkgraph als Inzidenzmatrix mit Kosten als Einträge
# Knoten und Kanten beginnen jeweils bei Index 1, nicht 0!
# Weiterhin können Knoten benannt werden und sind eindeutig durch ihren Index im Graphen bestimmt

from math import log2, ceil
import random


class Graph:
    def __init__(self):
        self.graph = [["+ "]]
        self.node_count = 0
        self.edge_count = 0

    def add_node(self, name=None):
        self.node_count = self.node_count+1
        if name is None:
            name = f"V{self.node_count}"
        self.graph.append([name])

    # Kante hinzufügen, benötigt Kosten und zu verbindende Knoten
    # Selbstschleifen nicht zugelassen
    def add_edge(self, cost, node_one, node_two):
        if cost <= 0:
            print("Cost needs to be greater than 0!")
            return
        number_of_nodes = len(self.graph)-1
        if number_of_nodes < 2:
            print("There are not enough nodes in the graph!")
            return
        if node_one > number_of_nodes or node_two > number_of_nodes:
            print(f"Given index out of range (1 - {number_of_nodes})")
            return
        self.edge_count = self.edge_count+1
        name = f"E{self.edge_count}"
        self.graph[0].append(name)
        for i in range(1, number_of_nodes+1):
            if i == node_one or i == node_two:
                self.graph[i].append(cost)
            else:
                self.graph[i].append(str(0))

    def change_cost_by_index(self, edge_index, new_cost):
        number_of_edges = len(self.graph[0])-1
        if number_of_edges < 1:
            print("There are no edges in the graph!")
            return
        if new_cost < 1:
            print("Cost needs to be greater than 0!")
            return
        if edge_index < 1 or edge_index > number_of_edges:
            print(f"Cannot change cost of edge at index {edge_index}. Index is not in range (1 - {number_of_edges})")
            return
        name = self.graph[0][edge_index]
        old_cost = 0
        for row in range(1, len(self.graph)):
            if int(self.graph[row][edge_index]) != 0:
                old_cost = self.graph[row][edge_index]
                self.graph[row][edge_index] = new_cost
        print(f"Cost for {name} changed from {old_cost} to {new_cost}")

    def delete_edge_by_index(self, edge_index):
        number_of_edges = len(self.graph[0])-1
        if number_of_edges < 1:
            print("There are no edges in the graph!")
            return
        if edge_index < 1 or edge_index > number_of_edges:
            print(f"Cannot delete edge at index {edge_index}. Index is not in range (1 - {number_of_edges})")
            return
        name = self.graph[0][edge_index]
        for row in self.graph:
            row.pop(edge_index)
        print(f"Edge {name} deleted!")

    def delete_node_by_index(self, node_index):
        number_of_nodes = len(self.graph)-1
        if number_of_nodes < 1:
            print("There are no nodes in the graph!")
            return
        if node_index < 1 or node_index > number_of_nodes:
            print(f"Cannot delete node at index {node_index}. Index is not in range (1 - {number_of_nodes})")
            return
        name = self.graph[node_index][0]
        index = 1
        while index < len(self.graph[node_index]):
            if int(self.graph[node_index][index]) != 0:
                self.delete_edge_by_index(index)
                index = index-1
            index = index+1
        self.graph.pop(node_index)
        print(f"Node {name} deleted!")

    def __str__(self):
        return_string = ""
        for row in self.graph:
            for edge in row:
                if len(str(edge)) >= 3 and str(edge).startswith("E"):
                    return_string = return_string + str(edge) + "\t|"
                else:
                    return_string = return_string + str(edge) + "\t\t|"
            return_string = return_string + "\n"
        return return_string

    def print(self):
        print(self)

    def clone(self):
        clone = Graph()
        for i in range(1, self.node_count+1):
            clone.add_node()
        for i in range(1, self.edge_count+1):
            edge = []
            cost = 0
            for j in range(1, self.node_count+1):
                if int(self.graph[j][i]) != 0:
                    cost = (self.graph[j][i])
                    edge.append(j)
            clone.add_edge(cost, edge[0], edge[1])
        return clone

    def add_random_edge(self, cost):
        if cost <= 0:
            print("Cost needs to be greater than 0!")
            return
        number_of_nodes = len(self.graph)-1
        if number_of_nodes < 2:
            print("There are not enough nodes in the graph!")
            return
        random_one = random.randint(1, self.node_count)
        random_two = random.randint(1, self.node_count)
        while random_one == random_two:
            random_two = random.randint(1, self.node_count)
        self.add_edge(cost, random_one, random_two)

    # Aufgabe 3
    def get_grade(self):
        graph_grade = 0
        for node in range(1, len(self.graph)):
            node_grade = 0
            for edge in range(1, len(self.graph[node])):
                if int(self.graph[node][edge]) != 0:
                    node_grade += 1
            if graph_grade < node_grade:
                graph_grade = node_grade
        return graph_grade


# Aufgabe 2:
# TODO: Hypercube, Torus, Fat-Tree

# Hilfsfunktion zur Überprüfung von Pfadvollständigkeit
def find_paths(graph):
    number_of_nodes = int(graph.node_count)
    not_visited = [i for i in range(2, number_of_nodes+1)]
    queue = [1]
    # path = "1"
    while queue:
        node = queue[0]
        queue.pop(0)
        for i in range(1, graph.edge_count+1):
            if int(graph.graph[node][i]) != 0:
                for j in range(1, number_of_nodes+1):
                    if int(graph.graph[j][i]) != 0:
                        if j in not_visited:
                            not_visited.pop(not_visited.index(j))
                            queue.append(j)
                            # path = f"{path} - {j}"
    return len(not_visited) == 0
            

def create_ring(number_of_nodes):
    if number_of_nodes < 2:
        print("At least three nodes needed to create a ring!")
        return
    ring_graph = Graph()
    for i in range(number_of_nodes):
        ring_graph.add_node()
    for i in range(number_of_nodes-1):
        ring_graph.add_edge(1, i+1, i+2)
    ring_graph.add_edge(1, number_of_nodes, 1)
    return ring_graph


def create_star(number_of_nodes):
    if number_of_nodes < 2:
        print("At least two nodes needed to create a star!")
        return
    star_graph = Graph()
    for i in range(number_of_nodes):
        star_graph.add_node()
    for i in range(2, number_of_nodes+1):
        star_graph.add_edge(1, 1, i)
    return star_graph


def create_vollverbunden(number_of_nodes):
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    vollverbunden_graph = Graph()
    for i in range(number_of_nodes):
        vollverbunden_graph.add_node()
    for i in range(1, number_of_nodes+1):
        for j in range(i+1, number_of_nodes+1):
            vollverbunden_graph.add_edge(1, i, j)
    return vollverbunden_graph


# Funktioniert so noch nicht!
def create_hypercube(number_of_nodes):
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    hypercube_graph = Graph()
    dimensions = ceil(log2(number_of_nodes))
    for i in range(number_of_nodes):
        hypercube_graph.add_node()
    for i in range(1, dimensions+1):
        for j in range(1, int((2**i)/2)+1):
            node_two = (2**i)+1-j
            if node_two <= number_of_nodes:
                hypercube_graph.add_edge(1, j, node_two)
    return hypercube_graph


def create_k_tree(number_of_nodes, number_of_children):
    if number_of_children != 2 and number_of_children != 4 and number_of_children != 8:
        print("Number of children must be 2, 4 or 8!")
        return
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    tree_graph = Graph()
    for i in range(number_of_nodes):
        tree_graph.add_node()
    parent = 1
    child = 2
    while child <= number_of_nodes:
        tree_graph.add_edge(1, parent, child)
        child += 1
        if child == (parent*number_of_children)+2:
            parent += 1
    return tree_graph


def create_random(number_of_nodes):
    if number_of_nodes < 2:
        print("At least two nodes needed to create a star!")
        return
    random_graph = Graph()
    for i in range(number_of_nodes):
        random_graph.add_node()
    for i in range(number_of_nodes-1):
        random_graph.add_random_edge(1)
    while not find_paths(random_graph):
        random_graph.add_random_edge(1)
    return random_graph


# debug_graph = Netzwerkgraph()
# for i in range(3):
#     debug_graph.add_node()
# for i in range(10):
#     debug_graph.add_edge(1, 2, 3)
#
# debug_graph.print()
#
# print(find_paths(debug_graph))


# ring = create_ring(10)
# star = create_star(10)
# vollverbunden = create_vollverbunden(10)
# # hypercube = create_hypercube(16)
# tree_two = create_k_tree(10, 2)
# tree_four = create_k_tree(10, 4)
# tree_eight = create_k_tree(10, 8)
random_graph = create_random(10)

random_graph.print()

# Aufgabe 4:
# print("Grade bei 10 Teilnehmer*innen:")
# print(f"Ring: {ring.get_grade()}")
# print(f"Stern: {star.get_grade()}")
# print(f"2-Tree: {tree_two.get_grade()}")
# print(f"4-Tree: {tree_four.get_grade()}")
# print(f"8-Tree: {tree_eight.get_grade()}")
# print(f"Vollverbunden: {vollverbunden.get_grade()}")
