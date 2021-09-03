class Prompter:
    def __init__(self, node, g=0, h=0):
        self.node = node
        self.g = g
        self.h = h

    def set_prompter_cost(self, tupla):
        self.node = tupla[0]
        self.g = tupla[1]

    def set_prompter_heuristic(self, tupla):
        self.node = tupla[0]
        self.h = tupla[1]

    def set_prompter_cost_heuristic(self, tupla):
        self.node = tupla[0][0]
        self.g = tupla[0][1]
