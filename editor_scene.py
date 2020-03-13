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
import json
from collections import OrderedDict
from editor_class_collection import Serializable, SceneHistory
from editor_graphics_scene import GraphicsScene
from editor_box import Box
from editor_edge import Edge


"Content from Scene"
class Scene(Serializable):
    def __init__(self):
        super().__init__()

        self.boxes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()
        self.history = SceneHistory(self)

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

    def clear(self):
        while len(self.boxes) > 0:
            self.boxes[0].remove()

    def saveToFile(self, filename):
        with open(filename, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
        print("saving to", filename, "was successfull.")

    def loadFromFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            self.deserialize(data)

    def serialize(self):
        boxes, edges = [], []
        for box in self.boxes: boxes.append(box.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('boxes', boxes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}):
        print("deserializating data", data)
        self.clear()
        hashmap = {}

        # create nodes
        for box_data in data['boxes']:
            Box(self).deserialize(box_data, hashmap)

        # create edges
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap)

        return True



