import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(".")
from network import Network
#%%

class Node(object):
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def print_nodefamily(self):
        prefix = " " * 4 * self.get_level()
        prefix += "└──>" if self.parent else "──>"
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
        children_val = [val for val in network.return_connections(current_node.data)
                        if not self.is_loop(val, current_node)]
        for child_val in children_val:
            child = Node(child_val)
            current_node.add_child(child)
            self.build_tree(child)

    def print_tree(self):
        self.root.print_nodefamily()

    @staticmethod
    def is_loop(child_val, parent_node):
        loop = False
        while not loop and parent_node is not None:
            if parent_node.data == child_val:
                loop = True
            else:
                parent_node = parent_node.parent
        return loop

#%%
# test the visualisation of the arbitrary network tree
if __name__ == "__main__":
    # define the attributes of the tree
    amountOfNodes = 7
    branchingFactor = 1
    goal = amountOfNodes-1
    network = Network(amountOfNodes, branchingFactor, seed=1, secure_path_to_goal=True)
    print(network.cost_matrix)

    # build the tree from a root
    root = Node(0)
    networkTree = NetworkTree()
    networkTree.build_tree(root)

    networkTree.print_tree()
