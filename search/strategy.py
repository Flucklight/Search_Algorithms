import math
from search.item.priority_queue import PriorityQueue
from search.item.prompter import Prompter
from search.structure.node import Node


def track_back(prompter, start, graph, window):
    graph.restart()
    while prompter.name != start.name:
        prompter.track = True
        prompter = prompter.path
        window.update()
    prompter.track = True
    window.update()


def point_to_point_distance(point_a, point_b):
    return math.sqrt(math.pow((point_b.x - point_a.x), 2) + math.pow((point_b.y - point_a.y), 2))


class Strategy:
    @staticmethod
    def depth_first_search(start, finish, graph, window):
        prompter = Prompter(start)
        prompter.node.prompter = True
        window.update()
        graph.restart()
        while prompter.node.name != finish.name:
            change = False
            prompter.node.visited = True
            for track in prompter.node.route:
                if not track.visited:
                    track.path = prompter.node
                    prompter.node.prompter = False
                    prompter.node = track
                    prompter.node.prompter = True
                    change = True
                    break
            if not change:
                prompter.node.prompter = False
                prompter.node = prompter.node.path
                prompter.node.prompter = True
            window.update()
        track_back(prompter.node, start, graph, window)

    @staticmethod
    def breadth_first_search(start, finish, graph, window):
        frontier = [start]
        graph.restart()
        prompter = Prompter(Node(''))
        while prompter.node.name != finish.name:
            prompter.node.prompter = False
            prompter.node = frontier.pop(0)
            prompter.node.visited = True
            prompter.node.prompter = True
            if len(prompter.node.route) != 0:
                for track in prompter.node.route:
                    if not track.visited:
                        track.path = prompter.node
                        frontier.append(track)
            window.update()
        track_back(prompter.node, start, graph, window)

    @staticmethod
    def iterative_depth_search(start, finish, graph, window):
        graph.restart()
        height = 1
        prompter = Prompter(start)
        prompter.node.prompter = True
        index = 0
        while prompter.node.name != finish.name:
            change = False
            prompter.node.visited = True
            if index < height:
                for track in prompter.node.route:
                    if not track.visited:
                        track.path = prompter.node
                        prompter.node.prompter = False
                        prompter.node = track
                        prompter.node.prompter = True
                        index += 1
                        change = True
                        break
            if not change and index != 0:
                index -= 1
                prompter.node = prompter.node.path
            elif index == 0:
                height += 1
                graph.restart()
            window.update()
        track_back(prompter.node, start, graph, window)

    @staticmethod
    def uniform_cost_search(start, finish, graph, window):
        frontier = PriorityQueue()
        graph.restart()
        frontier.append(start, 0)
        prompter = Prompter(Node(''))
        while prompter.node.name != finish.name:
            prompter.node.prompter = False
            prompter.set_prompter_cost(frontier.remove())
            prompter.node.prompter = True
            prompter.node.visited = True
            for track in prompter.node.route:
                if not track.visited:
                    total_cost = prompter.g + prompter.node.fee[track.name]
                    if frontier.contains(track):
                        if total_cost < frontier.get_priority(track):
                            track.path = prompter.node
                            frontier.replace(track, total_cost)
                    else:
                        track.path = prompter.node
                        frontier.append(track, total_cost)
            window.update()
        prompter = prompter.node
        track_back(prompter, start, graph, window)

    @staticmethod
    def greedy_search(start, finish, graph, window):
        frontier = PriorityQueue()
        frontier.append(start, 0)
        graph.restart()
        prompter = Prompter(Node(''))
        while prompter.node.name != finish.name:
            prompter.node.prompter = True
            prompter.set_prompter_heuristic(frontier.remove())
            prompter.node.prompter = True
            prompter.node.visited = True
            for track in prompter.node.route:
                if not track.visited:
                    heuristic = point_to_point_distance(track, finish)
                    track.path = prompter.node
                    frontier.append(track, heuristic)
            window.update()
        prompter = prompter.node
        track_back(prompter, start, graph, window)

    @staticmethod
    def a_star(start, finish, graph, window):
        frontier = PriorityQueue()
        frontier.append((start, 0), 0)
        graph.restart()
        prompter = Prompter(Node(''))
        while prompter.node.name != finish.name:
            prompter.node.prompter = False
            prompter.set_prompter_cost_heuristic(frontier.remove())
            prompter.node.prompter = True
            prompter.node.visited = True
            for track in prompter.node.route:
                if not track.visited:
                    total_cost = prompter.g + prompter.node.fee[track.name]
                    heuristic = point_to_point_distance(track, finish)
                    f = total_cost + heuristic
                    if frontier.contains(track):
                        if f < frontier.get_priority(track):
                            track.path = prompter.node
                            frontier.replace((track, total_cost), f)
                    else:
                        track.path = prompter.node
                        frontier.append((track, total_cost), f)
            window.update()
        prompter = prompter.node
        track_back(prompter, start, graph, window)
