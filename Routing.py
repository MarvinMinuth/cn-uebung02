import sys

from Netgraph import Netgraph
import random
import copy


def create_random(number_of_nodes, max_cost=25):
    if number_of_nodes < 1:
        print("Number of nodes must be greater than 0!")
        return
    random_graph = Netgraph()
    for i in range(number_of_nodes):
        random_graph.add_node()
    for i in range(number_of_nodes - 1):
        random_graph.add_random_edge(random.randint(1, max_cost))
    while not random_graph.is_complete():
        random_graph.add_random_edge(random.randint(1, max_cost))
    return random_graph


class RoutingTable:
    def __init__(self, netgraph):
        self.last = {}
        self.netgraph = netgraph
        self.length = netgraph.node_count
        # create initial tables
        self.node_tables = {}
        self.count = 0
        self.change = True

        for node in netgraph.nodes:
            self.node_tables[node] = []
            for n in range(self.length):
                self.node_tables[node].append([])
                for m in range(self.length):
                    if netgraph.nodes[m] == node or netgraph.nodes[n] == node \
                            or netgraph.nodes[m] not in node.get_neighbors():
                        self.node_tables[node][n].append('x')
                    else:
                        self.node_tables[node][n].append(' ')

            for edge in node.edges:
                neighbor = node.get_neighbor_at_edge(edge)
                index = netgraph.nodes.index(neighbor)
                if self.node_tables[node][index][index] == ' ' or self.node_tables[node][index][index] > edge.cost:
                    self.node_tables[node][index][index] = edge.cost

        self.print_and_update()

    def print_and_update(self):
        # update and print tables
        while self.change:
            self.change = False
            self.print()
            self.update()

    def update(self):
        # copy
        for node in self.node_tables.keys():
            self.last[node] = copy.deepcopy(self.node_tables[node])

        # update
        for node, table in self.node_tables.items():
            for x in range(self.length):
                if table[x][x] != 'x':
                    for y in range(self.length):
                        via = self.netgraph.nodes[x]
                        cost_to_via = table[x][x]
                        cost_via = sys.maxsize
                        if table[y][x] != 'x' and x != y:
                            for c in range(self.length):
                                if self.last[via][y][c] != ' ' and self.last[via][y][c] != 'x' and self.last[via][y][c] < cost_via:
                                    cost_via = self.last[via][y][c]
                            if cost_via == sys.maxsize:
                                table[y][x] = ' '
                            elif table[y][x] != cost_to_via + cost_via:
                                self.change = True
                                table[y][x] = cost_to_via + cost_via

    def print(self):
        print(f'T: {self.count}')
        self.count += 1
        for row in range(self.length + 1):
            output = ' '
            for tab in range(self.length):
                for cell in range(self.length + 1):
                    if row == 0 and cell == 0:
                        entry = f'von {self.netgraph.nodes[tab].name}'
                        if len(str(entry)) > 5:
                            output = output + f'{entry} |'
                        else:
                            output = output + f'{entry} \t|'
                    elif row == 0:
                        entry = f'via {self.netgraph.nodes[cell - 1].name}'
                        if len(str(entry)) > 5:
                            output = output + f'{entry} |'
                        else:
                            output = output + f'{entry} \t|'
                    elif cell == 0:
                        output = output + f'zu {self.netgraph.nodes[row - 1].name} \t|'
                    else:
                        entry = self.node_tables[self.netgraph.nodes[tab]][row - 1][cell - 1]
                        if len(str(entry)) < 2:
                            output = output + f'{entry} \t \t|'
                        else:
                            output = output + f'{entry} \t|'
                if tab < self.length - 1:
                    output = output + '\t|'
            print(output)
        print('')


print('RANDOM GRAPH:')
rnd_routing = RoutingTable(create_random(4))

# exercise 3:
print('\nGIVEN GRAPH:')
g = Netgraph()
g.add_node('A')
g.add_node('B')
g.add_node('C')
g.add_node('D')

g.add_edge(1, g.nodes[0], g.nodes[1])
g.add_edge(2, g.nodes[0], g.nodes[2])
g.add_edge(8, g.nodes[1], g.nodes[2])
g.add_edge(6, g.nodes[1], g.nodes[3])

gvn_routing = RoutingTable(g)

print('change cost of edge {B, D} to 200:')
gvn_routing.node_tables[g.nodes[1]][3][3] = 200
gvn_routing.node_tables[g.nodes[3]][1][1] = 200
gvn_routing.change = True
gvn_routing.print_and_update()
