class Node(object):
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None


class BST(object):
    '''
    Each node has at most 2 children (left and right child). Binary search trees differ from binary trees in that
    the entries are ordered, e.g. If we print out the in-order of the BST, we get a sorted list in an increasing order.
    '''
    def __init__(self):
        self.root = None

    def _insert(self, value, node):
        if value < node.value:
            if not node.left:
                node.left = Node(value)
            else:
                self._insert(value, node.left)
        elif value > node.value:
            if not node.right:
                node.right = Node(value)
            else:
                self._insert(value, node.right)
        else:
            print("The value is already in the tree!")

    def insert(self, value):
        # inserting the root
        if not self.root:
            self.root = Node(value)
        else:
            self._insert(value, self.root)

    def _find(self, value, node):
        if value == node.value:
            return True
        elif value < node.value and node.left:
            if node.left:
                return self._find(value, node.left)
            else:
                return False
        else:
            if node.right:
                return self._find(value, node.right)
            else:
                return False

    def find(self, value):
        if not self.root:
            return None
        else:
            is_found = self._find(value, self.root)
            return is_found

'''
                    8
                  /   \
                 3     10
                / \
               1   6
'''

if __name__ == "__main__":
    tree = BST()
    list = [8, 3, 10, 1, 6]
    # construct the tree illustrated above
    for value in list:
        tree.insert(value)

    # check values in the BST tree
    print("Value 8 is present in the tree: ", tree.find(8))
    print("Value 6 is present in the tree: ", tree.find(6))
    print("Value 11 is present in the tree: ", tree.find(11))
