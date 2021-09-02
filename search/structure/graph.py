from search.structure.node import Node


class Graph:
    def __init__(self, path):
        self.list = []
        with open(path, 'r') as f:
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
