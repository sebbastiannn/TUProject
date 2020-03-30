from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from tests.testtoolbar.editor_main_widget import MainWidget
from tests.testtoolbar.editor_scene import Scene
from tests.testtoolbar.editor_box import Box


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.scene = Scene()

        self.createToolBars()

        # create node editor widget
        self.editor = MainWidget(self)
        self.setCentralWidget(self.editor)

        # set window properties
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Editor")
        self.show()

    def createToolBars(self):
        # initialize toolbar
        toolbar = QToolBar("my main toolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)
        "buttons"
        button_action = QAction(QIcon("addBox.png"), "New box", self)
        button_action.setStatusTip("Add a new Box")
        button_action.triggered.connect(self.addNewBox)
        toolbar.addAction(button_action)

    def addNewBox(self):
        print("addnewbox called")
        box = Box(self.scene, "Box")
        box.setPos(0, 0)



