from connectives import LogicalElement

class LogElNode:
    def __init__(self):
        self.data = LogicalElement()
        self.left = None
        self.right = None


    def is_empty(self):
        return self.data.is_empty()

    def set_data(self, data):
        self.data = data

def print_tree(node: LogElNode, prefix="", is_left=True):
    """
    Recursively prints the binary tree structure with visual lines.
    """
    if not node:
        return

    # Print the right child first to correctly represent the tree visually
    if node.right:
        print_tree(node.right, prefix + ("│   " if is_left else "    "), False)

    # Print the current node
    print(f'{prefix}{"└── " if is_left else "┌──"}{node.data}')

    # Print the left child
    if node.left:
        print_tree(node.left, prefix + ("    " if is_left else "│   "), True)