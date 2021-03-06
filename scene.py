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
import os
import json
from collections import OrderedDict
from class_collection import dumpException
from class_collection import Serializable, SceneHistory, SceneClipboard
from graphics_scene import GraphicsScene
from box import Box
from edge import Edge


class InvalidFile(Exception): pass

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
        self.clipboard = SceneClipboard(self)
    "For changing stuff"


    def initUI(self):
        self.grScene = GraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addBox(self, box):
        self.boxes.append(box)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeBox(self, box):
        if box in self.boxes:
            self.boxes.remove(box)
        else:
            print("!W:", "Scene::removeBox", "wanna remove box", box, "from self.boxes but it's not in the list!")

    def removeEdge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            print("!W:", "Scene::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")

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

    def deserialize(self, data, hashmap={}, restore_id=True):
        self.clear()
        hashmap = {}

        if restore_id: self.id = data['id']

        # create nodes
        for box_data in data['boxes']:
            Box(self).deserialize(box_data, hashmap, restore_id)

        # create edges
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap, restore_id)

        return True



