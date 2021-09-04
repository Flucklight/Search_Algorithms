import sys
from PyQt5.QtWidgets import *

from gui.load_window import LoadWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = LoadWindow()
    window.show()
    sys.exit(app.exec_())
