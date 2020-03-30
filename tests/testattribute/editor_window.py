from PyQt5.QtWidgets import *

from tests.testattribute.editor_main_widget import MainWidget
from tests.testattribute.editor_scene import Scene

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.scene = Scene()
        # create node editor widget
        self.editor = MainWidget(self)
        self.setCentralWidget(self.editor)

        # set window properties
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Editor")
        self.show()

