import math

from search.item.priority_queue import PriorityQueue
from search.structure.node import Node


def contains(lst, obj):
    for data in lst:
        if data.name == obj.name:
            return True
    return False


def track_back(prompter, start):
    path = []
    while prompter.name != start.name:
        path.insert(0, prompter)
        prompter = prompter.path
    path.insert(0, prompter)
    return path


def point_to_point_distance(point_a, point_b):
    return math.sqrt(math.pow((point_b.x - point_a.x), 2) + math.pow((point_b.y - point_a.y), 2))


class Strategy:
    @staticmethod
    def depth_first_search(start, finish):
        visited = []
        prompter = start
        while prompter.name != finish.name:
            change = False
            if not contains(visited, prompter):
                visited.append(prompter)
            for track in prompter.route:
                if not contains(visited, track):
                    track.path = prompter
                    prompter = track
                    change = True
                    break
            if not change:
                prompter = prompter.path
        return track_back(prompter, start)

    @staticmethod
    def breadth_first_search(start, finish):
        frontier = [start]
        visited = []
        prompter = Node('', 0, 0)
        while prompter.name != finish.name:
            prompter = frontier.pop(0)
            visited.append(prompter)
            if len(prompter.route) != 0:
                for track in prompter.route:
                    if not contains(visited, track):
                        track.path = prompter
                        frontier.append(track)
        return track_back(prompter, start)

    @staticmethod
    def iterative_depth_search(start, finish):
        visited = []
        height = 1
        prompter = start
        index = 0
        while prompter.name != finish.name:
            change = False
            if not contains(visited, prompter):
                visited.append(prompter)
            if index < height:
                for track in prompter.route:
                    if not contains(visited, track):
                        track.path = prompter
                        prompter = track
                        index += 1
                        change = True
                        break
            if not change and index != 0:
                index -= 1
                prompter = prompter.path
            elif index == 0:
                height += 1
                visited = []
        return track_back(prompter, start)

    @staticmethod
    def uniform_cost_search(start, finish):
        frontier = PriorityQueue()
        frontier.append(start, 0)
        visited = []
        prompter = (Node('', 0, 0), 0)
        while prompter[0].name != finish.name:
            prompter = frontier.remove()
            visited.append(prompter[0])
            for track in prompter[0].route:
                if not contains(visited, track):
                    total_cost = prompter[1] + prompter[0].fee[track.name]
                    if frontier.contains(track):
                        if total_cost < frontier.get_priority(track):
                            track.path = prompter[0]
                            frontier.replace(track, total_cost)
                    else:
                        track.path = prompter[0]
                        frontier.append(track, total_cost)
        prompter = prompter[0]
        return track_back(prompter, start)

    @staticmethod
    def greedy_search(start, finish):
        frontier = PriorityQueue()
        frontier.append(start, 0)
        visited = []
        prompter = (Node('', 0, 0), 0)
        while prompter[0].name != finish.name:
            prompter = frontier.remove()
            visited.append(prompter[0])
            for track in prompter[0].route:
                if not contains(visited, track):
                    heuristic = point_to_point_distance(track, finish)
                    track.path = prompter[0]
                    frontier.append(track, heuristic)
        prompter = prompter[0]
        return track_back(prompter, start)

    @staticmethod
    def a_star(start, finish):
        frontier = PriorityQueue()
        frontier.append(start, 0)
        visited = []
        prompter = (Node('', 0, 0), 0)
        while prompter[0].name != finish.name:
            prompter = frontier.remove()
            visited.append(prompter[0])
            for track in prompter[0].route:
                if not contains(visited, track):
                    total_cost = prompter[1] + prompter[0].fee[track.name]
                    heuristic = point_to_point_distance(track, finish)
                    f = total_cost + heuristic
                    if frontier.contains(track):
                        if f < frontier.get_priority(track):
                            track.path = prompter[0]
                            frontier.replace(track, f)
                    else:
                        track.path = prompter[0]
                        frontier.append(track, f)
        prompter = prompter[0]
        return track_back(prompter, start)
