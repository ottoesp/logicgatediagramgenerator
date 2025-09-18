class LogicalElement:
    def __init__(self, name = ""):
        self.name = name
    def is_empty(self):
        return self.name == ""
    def __str__(self):
        return f'[{self.name}]'


class Connective(LogicalElement):
    def __init__(self, name = "", binding_strength = 10):
        LogicalElement.__init__(self, name)
        self.binding_strength = binding_strength



class Variable(LogicalElement):
    pass



connectives = [
    Connective("and", 0),
    Connective("or", 0),
    Connective("not", 1)
]
