class PriorityQueue:
    def __init__(self):
        self.queue = []

    def append(self, data, priority):
        if self.empty():
            self.queue.append((data, priority))
        else:
            i = 0
            success = False
            for d in self.queue:
                if priority[0] < d[1][0]:
                    self.queue.insert(i, (data, priority))
                    success = True
                    break
                i += 1
            if not success:
                self.queue.append((data, priority))

    def empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    def remove(self):
        return self.queue.pop(0)

    def clear(self):
        self.queue.clear()

    def contains(self, item):
        for data in self.queue:
            if data[0] == item:
                return True
        return False

    def replace(self, item, priority):
        tmp = []
        for data in self.queue:
            if data[0] == item:
                pass
            else:
                tmp.append(data)
        self.queue = tmp
        self.append(item, priority)

    def get_priority(self, item):
        for data in self.queue:
            if data[0] == item:
                return data[1][0]
        return 0
