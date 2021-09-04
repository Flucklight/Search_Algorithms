from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from gui.main_window import MainWindow


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 600)
        self.links = ['./graph.gp']
        self.addItems(self.links)

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
            self.links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    self.links.append(str(url.toLocalFile()))
                else:
                    self.links.append(str(url.toString()))
            self.addItems(self.links)
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
            main = MainWindow(path)
            main.show()
            self.close()
        else:
            dialog = QDialog()
            label = QLabel(dialog)
            dialog.resize(300, 50)
            dialog.setWindowTitle('Error')
            label.setText('La ruta no fue seleccionada')
            label.move(90, 10)
            dialog.exec_()
