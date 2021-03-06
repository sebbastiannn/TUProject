from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from scene import Scene
from box import Box
from edge import *
from graphics_view import GraphicsView


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.filename = None

        self.initUI()


    def initUI(self):

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # crate graphics scene
        self.scene = Scene()



        # create graphics view
        self.view = GraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

    def addBoxes(self):
        box1 = Box(self.scene, "Box 1", inputs=[0, 0, 0], outputs=[1])
        box2 = Box(self.scene, "Box 2", inputs=[3, 3, 3], outputs=[1])
        box3 = Box(self.scene, "Box 3", inputs=[2, 2, 2], outputs=[1])
        box1.setPos(-350, -250)
        box2.setPos(-75, 0)
        box3.setPos(200, -150)

        edge1 = Edge(self.scene, box1.outputs[0], box2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.scene, box2.outputs[0], box3.inputs[0], edge_type=EDGE_TYPE_BEZIER)
