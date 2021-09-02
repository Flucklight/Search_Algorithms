class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.route = []
        self.fee = {}
        self.path = 0
        self.x = x
        self.y = y

    def set_path(self, path):
        self.path = path
