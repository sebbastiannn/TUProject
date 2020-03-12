import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

"The QGraphicsView class provides a widget for displaying the contents of a QGraphicsScene."
"QGraphicsView visualizes the contents of a QGraphicsScene in a scrollable viewport. " \
"QGraphicsView is part of the Graphics View Framework. " \
"The QGraphicsScene class provides a surface for managing a large number of 2D graphical items."
"The class serves as a container for QGraphicsItems."
"It is used together with QGraphicsView for visualizing graphical items, such as lines, rectangles, text, " \
"or even custom items, on a 2D surface. QGraphicsScene is part of the Graphics View Framework"

from editor_graphics_scene import GraphicsScene

"Content from Scene"
class Scene():
    def __init__(self):
        self.boxes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        self.grScene = GraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addBox(self, box):
        self.boxes.append(box)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeBox(self, box):
        self.boxes.remove(box)

    def removeEdge(self, edge):
        self.edges.remove(edge)


