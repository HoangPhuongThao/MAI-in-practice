class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# each node of the binary tree has at most 2 children
class BinaryTree(object):
    def __init__(self, root):
        self.root = Node(root)

    def print_tree(self, order_type):
        if order_type == "preorder":
            return self.preorder_print(self.root, "")
        elif order_type == "inorder":
            return self.inorder_print(self.root, "")
        elif order_type == "postorder":
            return self.postorder_print(self.root, "")
        else:
            return "Invalid order type!"

    def preorder_print(self, node, list):
        # root - left - right
        if node:
            list += str(node.value) + "-"
            list = self.preorder_print(node.left, list)
            list = self.preorder_print(node.right, list)
        return list

    def inorder_print(self, node, list):
        # left - root - right
        if node:
            list = self.inorder_print(node.left, list)
            list += str(node.value) + "-"
            list = self.inorder_print(node.right, list)
        return list

    def postorder_print(self, node, list):
        # left - right - root
        if node:
            list = self.postorder_print(node.left, list)
            list = self.postorder_print(node.right, list)
            list += str(node.value) + "-"
        return list

'''
                    1
                  /   \
                2       3
             /    \    /  \
            4     5   6    7
            
pre-order output: 1-2-4-5-3-6-7
in-order output: 4-2-5-1-6-3-7
post-order output: 4-5-2-6-7-3-1
'''

if __name__=="__main__":
    # construct the binary tree illustrated above
    tree = BinaryTree(1)
    tree.root.left = Node(2)
    tree.root.right = Node(3)
    tree.root.left.left = Node(4)
    tree.root.left.right = Node(5)
    tree.root.right.left = Node(6)
    tree.root.right.right = Node(7)

    # print out all orders
    print("Pre-order output: ", tree.print_tree("preorder"))
    print("In-order output:", tree.print_tree("inorder"))
    print("Post-order output:", tree.print_tree("postorder"))
    print(tree.print_tree("sj"))
