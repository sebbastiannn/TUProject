from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

"Content from Scene"
class Scene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        self.boxes = []

        self.scene_width = 1000
        self.scene_height = 1000

        self.initUI()

    def initUI(self):
        self.grScene = QGraphicsScene(self)
        self.grScene.setSceneRect(-self.scene_width // 2, -self.scene_height // 2, self.scene_width, self.scene_height)

    def addBox(self, box):
        self.boxes.append(box)
