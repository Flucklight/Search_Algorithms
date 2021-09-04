from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from search.structure.graph import Graph
from search.structure.node import Node
from search.strategy import Strategy as Search


def middle_point(p1, p2):
    return int((p1 + p2) / 2)


class MainWindow(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.resize(1500, 600)
        self.setWindowTitle('Algoritmos de Busqueda')
        menu = QMenu(self)
        menu.addAction('Altura', lambda: self.search('dfs'))
        menu.addSeparator()
        menu.addAction('Anchura', lambda: self.search('bfs'))
        menu.addSeparator()
        menu.addAction('Iterativa', lambda: self.search('ids'))
        menu.addSeparator()
        menu.addAction('Uniforme', lambda: self.search('ucs'))
        menu.addSeparator()
        menu.addAction('Voraz', lambda: self.search('greedy'))
        menu.addSeparator()
        menu.addAction('A*', lambda: self.search('A*'))
        self.btn = QPushButton('Buscar', self)
        self.btn.setMenu(menu)
        self.btn.setGeometry(1250, 250, 200, 50)
        self.graph = Graph(path)
        self.start_node = self.graph.list[0]
        self.start_node.start = True
        self.finish_node = self.graph.list[-1]
        self.finish_node.finish = True
        self.move = []
        self.drag = False
        self.enable = True

    def select(self, event):
        for node in self.graph.list:
            if int(node.x) <= event.pos().x() <= int(node.x) + 50 \
                    and int(node.y) <= event.pos().y() <= int(node.y) + 50:
                return node
        return Node('')

    def action(self, action, event):
        select = self.select(event)
        if action == 'start' and select.name != '':
            self.graph.restart()
            self.start_node.start = False
            self.start_node = select
            self.start_node.start = True
            self.update()
        if action == 'finish' and select.name != '':
            self.graph.restart()
            self.finish_node.finish = False
            self.finish_node = select
            self.finish_node.finish = True
            self.update()

    def search(self, strategy):
        if strategy == 'dfs':
            self.enable = False
            Search.depth_first_search(self.start_node, self.finish_node, self.graph, self)
            self.enable = True
        elif strategy == 'bfs':
            self.enable = False
            Search.breadth_first_search(self.start_node, self.finish_node, self.graph, self)
            self.enable = True
        elif strategy == 'ids':
            self.enable = False
            Search.iterative_depth_search(self.start_node, self.finish_node, self.graph, self)
            self.enable = True
        elif strategy == 'ucs':
            self.enable = False
            Search.uniform_cost_search(self.start_node, self.finish_node, self.graph, self)
            self.enable = True
        elif strategy == 'greedy':
            self.enable = False
            Search.greedy_search(self.start_node, self.finish_node, self.graph, self)
            self.enable = True
        elif strategy == 'A*':
            self.enable = False
            Search.a_star(self.start_node, self.finish_node, self.graph, self)
            self.enable = True

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        for node in self.graph.list:
            if node.track:
                qp.setPen(QColor(Qt.yellow))
            elif node.finish:
                qp.setPen(QColor(Qt.red))
            elif node.start:
                qp.setPen(QColor(Qt.darkGreen))
            elif node.prompter:
                qp.setPen(QColor(Qt.darkMagenta))
            elif node.prompter:
                qp.setPen(QColor(Qt.darkCyan))
            else:
                qp.setPen(QColor(Qt.darkBlue))
            qp.drawEllipse(int(node.x), int(node.y), 50, 50)
            qp.setPen(QColor(Qt.black))
            qp.drawText(int(node.x) + 15, int(node.y) + 60, node.name)
            for route in node.route:
                qp.drawLine(int(node.x) + 25, int(node.y) + 25, int(route.x) + 25, int(route.y) + 25)
                qp.drawText(middle_point(int(node.x), int(route.x)) + 25,
                            middle_point(int(node.y), int(route.y)) + 25,
                            str(node.fee[route.name]))
        qp.end()

    def contextMenuEvent(self, event):
        if self.enable:
            menu = QMenu(self)
            menu.addAction('Inicio', lambda: self.action('start', event))
            menu.addSeparator()
            menu.addAction('Fin', lambda: self.action('finish', event))
            menu.exec(event.globalPos())

    def mousePressEvent(self, event):
        select = self.select(event)
        if event.buttons() and Qt.LeftButton and select.name != '' and self.enable:
            self.move = select
            self.drag = True

    def mouseMoveEvent(self, event):
        if self.drag:
            if 0 <= event.pos().x() <= 1150 and 0 <= event.pos().y() <= 540:
                self.move.x = event.pos().x()
                self.move.y = event.pos().y()
                self.update()

    def mouseReleaseEvent(self, event):
        if self.drag:
            self.drag = False
            self.move = []

    def closeEvent(self, event):
        self.graph.save_structure()
