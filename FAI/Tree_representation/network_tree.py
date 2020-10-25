import sys
import os
PATH, TAIL = os.path.split(os.path.abspath(os.getcwd()))
sys.path.insert(1, PATH + '/Basic Search Algorithms')
from network import Network


class Node(object):
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def print_nodefamily(self):
        prefix = " " * 3 * self.get_level()
        prefix += "|--" if self.parent else "--"
        print(prefix, str(self.data))
        if self.children:
            for child in self.children:
                child.print_nodefamily()

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level


class NetworkTree(object):
    def __init__(self):
        self.root = None

    def build_tree(self, current_node):
        if current_node.data == 0:
            self.root = current_node
        children_val = [val for val in network.return_connections(current_node.data) if val > current_node.data]
        for child_val in children_val:
            child = Node(child_val)
            current_node.add_child(child)
            self.build_tree(child)

    def print_tree(self):
        self.root.print_nodefamily()


if __name__ == "__main__":
    amountOfNodes = 10
    branchingFactor = 2
    goal = amountOfNodes-1
    network = Network(amountOfNodes, branchingFactor, seed=0, secure_path_to_goal=True)
    print(network.cost_matrix)

    root = Node(0)
    networkTree = NetworkTree()
    networkTree.build_tree(root)

    networkTree.print_tree()
