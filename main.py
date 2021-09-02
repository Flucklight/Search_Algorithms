import sys
from search.structure.graph import Graph
from search.strategy import Strategy as search
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 600)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            event.ignore()


class LoadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 600)
        self.setWindowTitle('Cargar Archivo')
        self.listbox_view = ListBoxWidget(self)
        self.btn = QPushButton('Cargar', self)
        self.btn.setGeometry(850, 400, 200, 50)
        self.btn.clicked.connect(lambda: self.init_main(self.get_selected_item()))

    def get_selected_item(self):
        item = QListWidgetItem(self.listbox_view.currentItem())
        return item.text()

    def init_main(self, path):
        if path != '':
            self.main = MainWindow(path)
            self.main.show()
            self.close()
        else:
            dialog = QDialog()
            label = QLabel(dialog)
            dialog.resize(300, 50)
            dialog.setWindowTitle('Error')
            label.setText('La ruta no fue seleccionada')
            label.move(90, 10)
            dialog.exec_()


class MainWindow(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.resize(1200, 600)
        self.setWindowTitle('Algoritmos de Busqueda')
        self.graph = Graph(path)
        self.move = []
        self.drag = False

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        for node in self.graph.list:
            qp.setPen(QColor(Qt.red))
            qp.drawEllipse(int(node.x), int(node.y), 50, 50)
            qp.setPen(QColor(Qt.black))
            qp.drawText(int(node.x) + 15, int(node.y) + 60, node.name)
            for route in node.route:
                qp.drawLine(int(node.x) + 25, int(node.y) + 25, int(route.x) + 25, int(route.y) + 25)
        qp.end()

    def mousePressEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            for node in self.graph.list:
                if int(node.x) <= event.pos().x() <= int(node.x) + 50 \
                        and int(node.y) <= event.pos().y() <= int(node.y) + 50:
                    self.move = node
                    self.drag = True
                    break

    def mouseMoveEvent(self, event):
        if self.drag:
            self.move.x = event.pos().x()
            self.move.y = event.pos().y()
            self.update()

    def mouseReleaseEvent(self, *args, **kwargs):
        if self.drag:
            self.drag = False
            self.move = []


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = LoadWindow()
    window.show()
    sys.exit(app.exec_())
