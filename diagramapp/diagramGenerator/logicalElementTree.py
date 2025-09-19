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
