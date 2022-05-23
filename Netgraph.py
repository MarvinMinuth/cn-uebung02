import sys
import random
from math import log2, floor, ceil, sqrt


# Aufgabe 1:
class Netgraph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.node_count = 0
        self.edge_count = 0

    class Node:
        def __init__(self, netgraph, name=None):
            self.netgraph = netgraph
            if name is None:
                self.name = f"V{netgraph.node_count}"
            else:
                self.name = name
            self.edges = []
            netgraph.node_count += 1

        def __gt__(self, other):
            return len(self.edges) > len(other.edges)

        def get_neighbor_at_edge(self, edge):
            if self == edge.nodes[0]:
                return edge.nodes[1]
            else:
                return edge.nodes[0]

        def get_neighbors(self):
            neighbors = []
            for edge in self.edges:
                neighbors.append(self.get_neighbor_at_edge(edge))
            return neighbors

        def delete(self):
            for edge in self.edges:
                edge.delete()
            self.netgraph.nodes.remove(self)
            self.netgraph.node_count -= 1

        def __str__(self):
            return self.name

    class Edge:
        def __init__(self, netgraph, cost, node_one, node_two):
            self.netgraph = netgraph
            self.nodes = [node_one, node_two]
            self.cost = cost
            node_one.edges.append(self)
            node_two.edges.append(self)
            netgraph.edge_count += 1

        def delete(self):
            for node in self.nodes:
                node.edges.remove(self)
            self.netgraph.edges.remove(self)
            self.netgraph.edge_count -= 1

    def add_node(self, name=None):
        node = self.Node(self, name)
        self.nodes.append(node)

    def add_edge(self, cost, node_one, node_two):
        edge = self.Edge(self, cost, node_one, node_two)
        self.edges.append(edge)

    def delete_node(self, node):
        node.delete()

    def delete_edge(self, edge):
        edge.delete()

    def print(self):
        return_string = "\t\t"
        for i in range(self.edge_count):
            if i >= 10:
                return_string = return_string + f"|E{i}\t"
            else:
                return_string = return_string + f"|E{i}\t\t"
        return_string = return_string + "\n"
        for node in self.nodes:
            if len(node.name) > 3:
                return_string = return_string + node.name + "\t"
            else:
                return_string = return_string + node.name + "\t\t"
            for edge in self.edges:
                if edge in node.edges:
                    if edge.cost >= 100:
                        return_string = return_string + "|" + str(edge.cost) + "\t"
                    else:
                        return_string = return_string + "|" + str(edge.cost) + "\t\t"
                else:
                    return_string = return_string + "|" + str(0) + "\t\t"
            return_string = return_string + "\n"
        print(return_string)

    def clone(self):
        clone_graph = Netgraph()
        for node in self.nodes:
            clone_graph.add_node(node.name)
        for edge in self.edges:
            index_node_one = self.nodes.index(edge.nodes[0])
            index_node_two = self.nodes.index(edge.nodes[1])
            clone_graph.add_edge(edge.cost, clone_graph.nodes[index_node_one], clone_graph.nodes[index_node_two])
        return clone_graph

    # Hilfsfunktion zu A2 (h): zufällige Kante erzeugen
    def add_random_edge(self, cost):
        if cost <= 0:
            print("Cost needs to be greater than 0!")
            return
        if self.node_count < 2:
            print("There are not enough nodes in the graph!")
            return
        random_one = random.randint(0, self.node_count - 1)
        random_two = random.randint(0, self.node_count - 1)
        while random_one == random_two:
            random_two = random.randint(0, self.node_count - 1)
        self.add_edge(cost, self.nodes[random_one], self.nodes[random_two])

    # Hilfsfunktion zu A2 (h): Vollständigkeit überprüfen (BFS)
    def is_complete(self):
        not_visited = []
        for node in self.nodes:
            not_visited.append(node)
        queue = [not_visited[0]]
        not_visited.pop(0)
        while queue:
            for neighbor in queue[0].get_neighbors():
                if neighbor in not_visited:
                    queue.append(neighbor)
                    not_visited.remove(neighbor)
            queue.pop(0)
        return not not_visited

    def get_neighbors(self, node):
        return node.get_neighbors()

    # Aufgabe 3 (a)
    def get_grade(self):
        grade = 0
        for node in self.nodes:
            node_grade = len(node.edges)
            if node_grade > grade:
                grade = node_grade
        return grade

    # Aufgabe 3 (b): Konnektivität mit Hilfe von Stoer-Wagner
    def get_connectivity(self):
        if self.is_complete():
            return self.clone().minimum_cut()  # Graph kopieren, damit Original bestehen bleibt
        else:
            print("Graph is not complete!")
            return

    def merge_nodes(self, node_one, node_two):
        for edge in node_one.edges:
            if edge not in node_two.edges:
                if edge.nodes[0] == node_one:
                    self.add_edge(edge.cost, node_two, edge.nodes[1])
                else:
                    self.add_edge(edge.cost, node_two, edge.nodes[0])
        node_one.delete()

    # Überprüfe "Dichte" des Knotens in A
    def w(self, A, node):
        assert node not in A
        count = 0
        for neighbor in self.get_neighbors(node):
            if neighbor in A:
                count += 1
        return count

    def min_cut_phase(self, node):
        A = {node}
        V = set(self.nodes)
        order = [node]
        while A != V:
            w_candidates = [(self.w(A, v), v) for v in V - A]  #: Kandidaten für am dichtesten verbundenen Knoten bestimmen
            _, x = max(w_candidates)  # "Knotengröße" bestimmt durch Anzahl der Kanten
            A.add(x)
            order.append(x)
        t, s = order[-1], order[-2]
        min_cut = len(t.edges)
        self.merge_nodes(t, s)
        return min_cut

    def minimum_cut(self):
        min_cut = len(self.nodes[0].edges)
        while self.node_count > 1:
            min_cut_candidate = self.min_cut_phase(self.nodes[0])
            if min_cut_candidate < min_cut:
                min_cut = min_cut_candidate
        return min_cut

    # Aufgabe 3 (c): Durchmesser mit Hilfe von Dijkstra
    # Anzahl der Mehrfachkanten bestimmt Höhe der Kosten
    def dijkstra(self, node):
        queue = [node]
        done = []
        cost = {}
        for v in self.nodes:
            cost[v] = sys.maxsize
        cost[node] = 0

        while queue:
            next_node = queue[0]
            for neighbor in next_node.get_neighbors():
                if neighbor not in done:
                    queue.append(neighbor)
                    if cost[next_node] + next_node.get_neighbors().count(neighbor) < cost[neighbor]:
                        cost[neighbor] = cost[next_node] + next_node.get_neighbors().count(neighbor)  # Mehrfachkanten einbeziehen
            queue.pop(0)
            done.append(next_node)
        return cost

    def max_path_from_node(self, node):
        return max(i for i in self.dijkstra(node).values())

    def diameter(self):
        max_paths = []
        for node in self.nodes:
            max_paths.append(self.max_path_from_node(node))
        return max(max_paths)


# Aufgabe 2:

def create_ring(number_of_nodes, cost=1):
    if number_of_nodes < 3:
        print("Number of nodes should be at least 3.")
        return
    ring_graph = Netgraph()
    ring_graph.add_node()
    for i in range(1, number_of_nodes):
        ring_graph.add_node()
        ring_graph.add_edge(cost, ring_graph.nodes[i - 1], ring_graph.nodes[i])
    ring_graph.add_edge(cost, ring_graph.nodes[0], ring_graph.nodes[-1])
    return ring_graph


def create_star(number_of_nodes, cost=1):
    if number_of_nodes < 1:
        print("Number of nodes should be at least 1.")
        return
    star_graph = Netgraph()
    star_graph.add_node()
    for i in range(1, number_of_nodes):
        star_graph.add_node()
        star_graph.add_edge(cost, star_graph.nodes[0], star_graph.nodes[i])
    return star_graph


def create_vollverbunden(number_of_nodes, cost=1):
    if number_of_nodes < 1:
        print("Number of nodes should be at least 1.")
        return
    vollverbunden_graph = Netgraph()
    for i in range(number_of_nodes):
        vollverbunden_graph.add_node()
    for i in range(number_of_nodes):
        for j in range(i + 1, number_of_nodes):
            vollverbunden_graph.add_edge(cost, vollverbunden_graph.nodes[i], vollverbunden_graph.nodes[j])
    return vollverbunden_graph


def create_hypercube(number_of_nodes, cost=1):
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    hypercube_graph = Netgraph()
    dimensions = ceil(log2(number_of_nodes))
    hypercube_graph.add_node()
    for dim in range(1, dimensions):
        copy = hypercube_graph.clone()
        for i in range(len(hypercube_graph.nodes)):
            hypercube_graph.add_edge(cost, hypercube_graph.nodes[i], copy.nodes[i])
            hypercube_graph.nodes.append(copy.nodes[i])
            hypercube_graph.node_count += 1
        for edge in copy.edges:
            hypercube_graph.edges.append(edge)
            hypercube_graph.edge_count += 1
    for i in range(len(hypercube_graph.nodes)):  # Namen anpassen
        hypercube_graph.nodes[i].name = f"V{i}"
    rest = number_of_nodes - (2**(dimensions-1))
    # restliche Knoten werden mit je einem bestehenden Knoten einfach verbunden, nicht weiter untereinander
    while rest != 0:
        hypercube_graph.add_node()
        hypercube_graph.add_edge(1, hypercube_graph.nodes[rest-1], hypercube_graph.nodes[-1])
        rest -= 1
    return hypercube_graph


def create_torus(number_of_nodes, cost=1):
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    torus_graph = Netgraph()
    length = floor(sqrt(number_of_nodes))
    for i in range(number_of_nodes):
        torus_graph.add_node()
    row = 0
    while row < ceil(number_of_nodes/length):
        for i in range(length-1):
            if (row*length)+i+1 < number_of_nodes:
                torus_graph.add_edge(cost, torus_graph.nodes[(row*length)+i], torus_graph.nodes[(row*length)+i+1])
            else:  # letzten und ersten Knoten der Reihe verbinden, falls Graph nicht quadratisch
                if not i == 0:  # Knoten werden nicht mit sich selbst verbunden
                    torus_graph.add_edge(cost, torus_graph.nodes[(row*length)+i], torus_graph.nodes[(row*length)])
                torus_graph.add_edge(cost, torus_graph.nodes[(row*length)+i], torus_graph.nodes[i])
                break
            if (row*length)+i+length < number_of_nodes:
                torus_graph.add_edge(cost, torus_graph.nodes[(row*length)+i], torus_graph.nodes[(row*length)+i+length])
            else:  # letzte Reihe mit erster verbinden
                torus_graph.add_edge(cost, torus_graph.nodes[(row*length)+i], torus_graph.nodes[i])
        if (row*length)+length-1 < number_of_nodes:
            torus_graph.add_edge(cost, torus_graph.nodes[(row*length)+length-1], torus_graph.nodes[(row*length)])
            if ((row+1)*length)+length-1 < number_of_nodes:
                torus_graph.add_edge(cost, torus_graph.nodes[(row*length)+length-1], torus_graph.nodes[((row+1)*length)+length-1])
            else:
                torus_graph.add_edge(cost, torus_graph.nodes[(row*length)+length-1], torus_graph.nodes[length-1])
        row += 1
    return torus_graph


def create_k_tree(k, number_of_nodes, cost=1):
    if k != 2 and k != 4 and k != 8:
        print("Number of children must be 2, 4 or 8!")
        return
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    tree_graph = Netgraph()
    for i in range(number_of_nodes):
        tree_graph.add_node()
    parent_index = 0
    child_index = 1
    while child_index < number_of_nodes:
        tree_graph.add_edge(cost, tree_graph.nodes[parent_index], tree_graph.nodes[child_index])
        child_index += 1
        if child_index == (parent_index * k) + (k + 1):
            parent_index += 1
    return tree_graph


def create_fat_tree(number_of_nodes, cost=1):
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    tree_graph = Netgraph()
    height = floor(log2(number_of_nodes+1))
    for i in range(number_of_nodes):
        tree_graph.add_node()
    parent_index = 0
    child_index = 1
    while child_index < number_of_nodes:
        for i in range(height):
            tree_graph.add_edge(cost, tree_graph.nodes[parent_index], tree_graph.nodes[child_index])
        child_index += 1
        if child_index == (parent_index * 2) + (2 + 1):
            parent_index += 1
            height = floor(log2(number_of_nodes+1)) - floor(log2(parent_index+1))
    return tree_graph


def create_random(number_of_nodes, cost=1):
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    random_graph = Netgraph()
    for i in range(number_of_nodes):
        random_graph.add_node()
    for i in range(number_of_nodes - 1):
        random_graph.add_random_edge(cost)
    while not random_graph.is_complete():
        random_graph.add_random_edge(cost)
    return random_graph


# Aufgabe 4:
# ring = create_ring(10)
# star = create_star(10)
# vollverbunden = create_vollverbunden(10)
# hypercube = create_hypercube(10)
# torus = create_torus(10)
# tree_two = create_k_tree(2, 10)
# tree_four = create_k_tree(4, 10)
# tree_eight = create_k_tree(8, 10)
# fat_tree = create_fat_tree(10)
#
# print("Grade bei 10 Knoten:")
# print(f"Ring: {ring.get_grade()}")
# print(f"Stern: {star.get_grade()}")
# print(f"Vollverbunden: {vollverbunden.get_grade()}")
# print(f"Hypercube: {hypercube.get_grade()}")
# print(f"Torus: {torus.get_grade()}")
# print(f"2-Tree: {tree_two.get_grade()}")
# print(f"4-Tree: {tree_four.get_grade()}")
# print(f"8-Tree: {tree_eight.get_grade()}")
# print(f"Fat-Tree: {fat_tree.get_grade()}")
#
# print("\nKonnektivität bei 10 Knoten:")
# print(f"Ring: {ring.get_connectivity()}")
# print(f"Stern: {star.get_connectivity()}")
# print(f"Vollverbunden: {vollverbunden.get_connectivity()}")
# print(f"Hypercube: {hypercube.get_connectivity()}")
# print(f"Torus: {torus.get_connectivity()}")
# print(f"2-Tree: {tree_two.get_connectivity()}")
# print(f"4-Tree: {tree_four.get_connectivity()}")
# print(f"8-Tree: {tree_eight.get_connectivity()}")
# print(f"Fat-Tree: {fat_tree.get_connectivity()}")
#
# print("\nDurchmesser bei 10 Knoten:")
# print(f"Ring: {ring.diameter()}")
# print(f"Stern: {star.diameter()}")
# print(f"Vollverbunden: {vollverbunden.diameter()}")
# print(f"Hypercube: {hypercube.diameter()}")
# print(f"Torus: {torus.diameter()}")
# print(f"2-Tree: {tree_two.diameter()}")
# print(f"4-Tree: {tree_four.diameter()}")
# print(f"8-Tree: {tree_eight.diameter()}")
# print(f"Fat-Tree: {fat_tree.diameter()}")
