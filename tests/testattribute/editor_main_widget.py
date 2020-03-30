from PyQt5.QtWidgets import *

from tests.testattribute.editor_scene import Scene
from tests.testattribute.editor_box import Box
from tests.testattribute.editor_graphics_view import GraphicsView


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # crate graphics scene
        self.scene = Scene()

        # create graphics view
        self.view = GraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

    def addBoxes(self):
        box1 = Box(self.scene, "Box 1")
        box2 = Box(self.scene, "Box 2")
        box1.setPos(-350, -250)
        box2.setPos(-75, 0)


