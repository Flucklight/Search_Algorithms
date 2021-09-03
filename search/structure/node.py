class Node:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.route = []
        self.fee = {}
        self.path = 0
        self.x = x
        self.y = y
        self.start = False
        self.finish = False
        self.visited = False
        self.prompter = False
        self.track = False

    def set_path(self, path):
        self.path = path
