# Marvin Minuth, 1077466
# Aufgabe 1:
# Netzwerkgraph als Inzidenzmatrix mit Kosten als Einträge
# Knoten und Kanten beginnen jeweils bei Index 1, nicht 0!
class Netzwerkgraph:
    def __init__(self):
        self.graph = [["+ "]]
        self.node_count = 0
        self.edge_count = 0

    def add_node(self):
        self.node_count = self.node_count+1
        name = f"V{self.node_count}"
        self.graph.append([name])

    # Kante hinzufügen, benötigt Kosten und zu verbindende Knoten
    # Selbstschleifen und Multiverbindungen in Aufgabenstellung nicht erwähnt, deshalb zugelassen
    def add_edge(self, cost, node_one, node_two):
        if cost <= 0:
            print("Cost needs to be greater than 0!")
            return
        number_of_nodes = len(self.graph)-1
        if number_of_nodes < 1:
            print("There are no nodes in the graph!")
            return
        if node_one > number_of_nodes or node_two > number_of_nodes:
            print(f"Given index out of range (1 - {number_of_nodes})")
            return
        self.edge_count = self.edge_count+1
        name = f"E{self.edge_count}"
        self.graph[0].append(name)
        for i in range(1, number_of_nodes):
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
                return_string = return_string + str(edge) + "\t|"
            return_string = return_string + "\n"
        return return_string

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
# TODO: Hypercube, Matrix, Zufall
# Für Zufall: Hilfsfunktion zur Überprüfung von Pfadvollständigkeit

def create_ring(number_of_nodes):
    if number_of_nodes < 2:
        print("At least three nodes needed to create a ring!")
        return
    ring_graph = Netzwerkgraph()
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
    star_graph = Netzwerkgraph()
    for i in range(number_of_nodes):
        star_graph.add_node()
    for i in range(2, number_of_nodes+1):
        star_graph.add_edge(1, 1, i)
    return star_graph


def create_tree(number_of_nodes, number_of_children):
    if number_of_children != 2 and number_of_children != 4 and number_of_children != 8:
        print("Number of children must be 2, 4 or 8!")
        return
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    tree_graph = Netzwerkgraph()
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


def create_vollvermascht(number_of_nodes):
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    vollvermascht_graph = Netzwerkgraph()
    for i in range(number_of_nodes):
        vollvermascht_graph.add_node()
    for i in range(1, number_of_nodes+1):
        for j in range(i+1, number_of_nodes+1):
            vollvermascht_graph.add_edge(1, i, j)
    return vollvermascht_graph


ring = create_ring(10)
star = create_star(10)
vollvermascht = create_vollvermascht(10)
tree_two = create_tree(10, 2)
tree_four = create_tree(10, 4)
tree_eight = create_tree(10, 8)

# Aufgabe 4:
print("Grade bei 10 Teilnehmer*innen:")
print(f"Ring: {ring.get_grade()}")
print(f"Stern: {star.get_grade()}")
print(f"2-Tree: {tree_two.get_grade()}")
print(f"4-Tree: {tree_four.get_grade()}")
print(f"8-Tree: {tree_eight.get_grade()}")
print(f"Vollvermascht: {vollvermascht.get_grade()}")
