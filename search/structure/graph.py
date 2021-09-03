from search.structure.node import Node


class Graph:
    def __init__(self, path):
        self.list = []
        self.path = path
        with open(self.path, 'r') as f:
            for name in f.readline()[:-1].split(','):
                data_format = name.split(':')
                self.list.append(Node(data_format[0], float(data_format[1]), float(data_format[2])))
            i = 0
            for line in f:
                j = 0
                for data in line[:-1].split(','):
                    if data != '*':
                        self.list[i].route.append(self.list[j])
                        self.list[i].fee[self.list[j].name] = float(data)
                    j += 1
                i += 1
        f.close()

    def restart(self):
        for node in self.list:
            node.visited = False
            node.track = False
            node.prompter = False

    def save_structure(self):
        with open('./graph.gp', 'w') as f:
            data = ''
            for node in self.list:
                data += (str(node.name) + ':'
                         + str(node.x) + ':'
                         + str(node.y) + ',')
            data = data[:-1] + '\n'
            f.write(data)
            for node in self.list:
                i = 0
                data = ''
                for j in range(len(self.list)):
                    if self.list[j].name == node.route[i].name:
                        data += str(node.fee[node.route[i].name]) + ','
                        if i < len(node.route) - 1:
                            i += 1
                    else:
                        data += '*,'
                data = data[:-1] + '\n'
                f.write(data)
        f.close()
