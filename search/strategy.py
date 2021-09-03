import math
import time as t
from search.item.priority_queue import PriorityQueue
from search.item.prompter import Prompter
from search.structure.node import Node


def track_back(prompter, start, graph, window, file):
    graph.restart()
    track = []
    while prompter.name != start.name:
        track.insert(0, prompter)
        prompter.track = True
        prompter = prompter.path
        render(1, window)
    prompter.track = True
    track.insert(0, prompter)
    file.write('Camino: ')
    for node in track:
        if node.name != track[-1].name:
            file.write(node.name + '->')
        else:
            file.write(node.name + '\n')
    render(1, window)


def render(time, window):
    window.update()


def point_to_point_distance(point_a, point_b):
    return math.sqrt(math.pow((point_b.x - point_a.x), 2) + math.pow((point_b.y - point_a.y), 2))


class Strategy:
    @staticmethod
    def depth_first_search(start, finish, graph, window):
        prompter = Prompter(start)
        prompter.node.prompter = True
        render(1, window)
        graph.restart()
        with open('./reports/dfs.rpt', 'w') as report:
            report.write('Nodo inicial: {}\nNodo final: {}\n'.format(start.name, finish.name))
            t_start = t.time()
            while prompter.node.name != finish.name:
                report.write('\nApuntador: {}\n'.format(prompter.node.name))
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
                render(1, window)
            t_end = t.time()
            track_back(prompter.node, start, graph, window, report)
            elapsed_time = t_end - t_start
            report.write('Tiempo: %0.10f segundos' % elapsed_time)
        report.close()

    @staticmethod
    def breadth_first_search(start, finish, graph, window):
        frontier = [start]
        graph.restart()
        prompter = Prompter(Node(''))
        with open('./reports/bfs.rpt', 'w') as report:
            report.write('Nodo inicial: {}\nNodo final: {}\n'.format(start.name, finish.name))
            t_start = t.time()
            while prompter.node.name != finish.name:
                if len(frontier) != 0:
                    report.write('Frontera:\n')
                    for node in frontier:
                        if node.name != frontier[-1].name:
                            report.write('   Nodo = {}\n'.format(node.name))
                prompter.node.prompter = False
                prompter.node = frontier.pop(0)
                prompter.node.visited = True
                prompter.node.prompter = True
                report.write('\nApuntador: {}\n'.format(prompter.node.name))
                if len(prompter.node.route) != 0:
                    for track in prompter.node.route:
                        if not track.visited:
                            track.path = prompter.node
                            frontier.append(track)
                render(1, window)
            t_end = t.time()
            track_back(prompter.node, start, graph, window, report)
            elapsed_time = t_end - t_start
            report.write('Tiempo: %0.10f segundos' % elapsed_time)
        report.close()

    @staticmethod
    def iterative_depth_search(start, finish, graph, window):
        graph.restart()
        height = 1
        prompter = Prompter(start)
        prompter.node.prompter = True
        index = 0
        with open('./reports/ids.rpt', 'w') as report:
            report.write('Nodo inicial: {}\nNodo final: {}\n'.format(start.name, finish.name))
            t_start = t.time()
            while prompter.node.name != finish.name:
                report.write('\nApuntador: {}\n'.format(prompter.node.name))
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
                render(1, window)
            t_end = t.time()
            track_back(prompter.node, start, graph, window, report)
            elapsed_time = t_end - t_start
            report.write('Tiempo: %0.10f segundos' % elapsed_time)
        report.close()

    @staticmethod
    def uniform_cost_search(start, finish, graph, window):
        frontier = PriorityQueue()
        graph.restart()
        frontier.append(start, 0)
        prompter = Prompter(Node(''))
        with open('./reports/ucs.rpt', 'w') as report:
            report.write('Nodo inicial: {}\nNodo final: {}\n'.format(start.name, finish.name))
            t_start = t.time()
            while prompter.node.name != finish.name:
                if not frontier.empty():
                    report.write('Frontera:\n')
                    for data in frontier.queue:
                        report.write('   Nodo = {}, g = {}\n'.format(data[0].name, data[1]))
                prompter.node.prompter = False
                prompter.set_prompter_cost(frontier.remove())
                prompter.node.prompter = True
                prompter.node.visited = True
                report.write('\nApuntador: {}\n'.format(prompter.node.name))
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
                render(1, window)
            t_end = t.time()
            prompter = prompter.node
            track_back(prompter, start, graph, window, report)
            elapsed_time = t_end - t_start
            report.write('Tiempo: %0.10f segundos' % elapsed_time)
        report.close()

    @staticmethod
    def greedy_search(start, finish, graph, window):
        frontier = PriorityQueue()
        frontier.append(start, 0)
        graph.restart()
        prompter = Prompter(Node(''))
        with open('./reports/greedy.rpt', 'w') as report:
            report.write('Nodo inicial: {}\nNodo final: {}\n'.format(start.name, finish.name))
            t_start = t.time()
            while prompter.node.name != finish.name:
                if not frontier.empty():
                    report.write('Frontera:\n')
                    for data in frontier.queue:
                        report.write('   Nodo = {}, h = {}, '.format(data[0].name, data[1]))
                prompter.node.prompter = True
                prompter.set_prompter_heuristic(frontier.remove())
                prompter.node.prompter = True
                prompter.node.visited = True
                report.write('\nApuntador: {}\n'.format(prompter.node.name))
                for track in prompter.node.route:
                    if not track.visited:
                        heuristic = point_to_point_distance(track, finish)
                        track.path = prompter.node
                        frontier.append(track, heuristic)
                render(1, window)
            t_end = t.time()
            prompter = prompter.node
            track_back(prompter, start, graph, window, report)
            elapsed_time = t_end - t_start
            report.write('Tiempo: %0.10f segundos' % elapsed_time)
        report.close()

    @staticmethod
    def a_star(start, finish, graph, window):
        frontier = PriorityQueue()
        frontier.append((start, 0, 0), 0)
        graph.restart()
        prompter = Prompter(Node(''))
        with open('./reports/a_star.rpt', 'w') as report:
            report.write('Nodo inicial: {}\nNodo final: {}\n'.format(start.name, finish.name))
            t_start = t.time()
            while prompter.node.name != finish.name:
                if not frontier.empty():
                    report.write('Frontera:\n')
                    for data in frontier.queue:
                        report.write('   Nodo = {}, g = {}, h = {}, f = {}\n'.
                                     format(data[0][0].name, data[0][1], data[0][2], data[1]))
                prompter.node.prompter = False
                prompter.set_prompter_cost_heuristic(frontier.remove())
                prompter.node.prompter = True
                prompter.node.visited = True
                report.write('\nApuntador: {}\n'.format(prompter.node.name))
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
                            frontier.append((track, total_cost, heuristic), f)
                render(1, window)
            t_end = t.time()
            prompter = prompter.node
            track_back(prompter, start, graph, window, report)
            elapsed_time = t_end - t_start
            report.write('Tiempo: %0.10f segundos' % elapsed_time)
        report.close()
