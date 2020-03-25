"In computing, serialization (or serialisation) is the" \
"process of translating data structures or object state " \
"into a format that can be stored - our case will be json"
class Serializable():
    def __init__(self):
        self.id = id(self)

    def serialize(self):
        raise NotImplemented()

    def deserialize(self, data, hashmap={}):
        raise NotImplemented()

"For the Clipboard"
from collections import OrderedDict
from edge import GraphicsEdge, Edge
from box import Box

class SceneClipboard():
    def __init__(self, scene):
        self.scene = scene

    def serializeSelected(self, delete=False):
        "COPY TO CLIPBOARD"

        sel_boxes, sel_edges, sel_sockets = [], [], {}

        # sort edges and boxes
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'box'):
                sel_boxes.append(item.box.serialize())
                for socket in (item.box.inputs + item.box.outputs):
                    sel_sockets[socket.id] = socket
            elif isinstance(item, GraphicsEdge):
                sel_edges.append(item.edge)
        # debug
            #print("  BOXES\n      ", sel_boxes)
            #print("  EDGES\n      ", sel_edges)
            #print("  SOCKETS\n     ", sel_sockets)

        # remove all edges which are not connected to a box in our list
        edges_to_remove = []
        for edge in sel_edges:
            if edge.start_socket.id in sel_sockets and edge.end_socket.id in sel_sockets:
                pass
            else:
                "edge is not connected with both sides"
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            sel_edges.remove(edge)

        # make final list of edges
        edges_final = []
        for edge in sel_edges:
            edges_final.append(edge.serialize())

        "our final edge list"
        data = OrderedDict([
            ('boxes', sel_boxes),
            ('edges', edges_final),
        ])

        # if CUT (aka delete) remove selected items
        if delete:
            self.scene.grScene.views()[0].deleteSelected()
            # store our history
            self.scene.history.storeHistory("Cut out elements from scene")

        return data


    def deserializeFromClipboard(self, data):
        hashmap = {}

        # calculate mouse pointer - scene position
        view = self.scene.grScene.views()[0]
        mouse_scene_pos = view.last_scene_mouse_position

        # calculate selected objects bbox and center
        minx, maxx, miny, maxy = 0, 0, 0, 0
        for box_data in data['boxes']:
            x, y = box_data['pos_x'], box_data['pos_y']
            if x < minx: minx = x
            if x > maxx: maxx = x
            if y < miny: miny = y
            if y > maxy: maxy = y
        bbox_center_x = (minx + maxx) / 2
        bbox_center_y = (miny + maxy) / 2

        # calculate the offset of the newly creating boxes
        offset_x = mouse_scene_pos.x() - bbox_center_x
        offset_y = mouse_scene_pos.y() - bbox_center_y

        # create each box
        for box_data in data['boxes']:
            new_box = Box(self.scene)
            new_box.deserialize(box_data, hashmap, restore_id=False)

            # readjust the new box's position
            pos = new_box.pos
            new_box.setPos(pos.x() + offset_x, pos.y() + offset_y)

        # create each edge
        if 'edges' in data:
            for edge_data in data['edges']:
                new_edge = Edge(self.scene)
                new_edge.deserialize(edge_data, hashmap, restore_id=False)

        # store history
        self.scene.history.storeHistory("Pasted elements in scene")


"The Scene History"
class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.clear()
        self.history_limit = 32

    def clear(self):
        self.history_stack = []
        self.history_current_step = -1

    def undo(self):
        if self.history_current_step > 0:
            self.history_current_step -= 1
            self.restoreHistory()

    def redo(self):
        if self.history_current_step + 1 < len(self.history_stack):
            self.history_current_step += 1
            self.restoreHistory()


    def restoreHistory(self):
        "Restoring history current_step:"
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])


    def storeHistory(self, desc):
        "Storing history current_step"
        # if the pointer (history_current_step) is not at the end of history_stack
        if self.history_current_step+1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.history_current_step+1]

        # history is outside of the limits
        if self.history_current_step+1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -= 1

        hs = self.createHistoryStamp(desc)

        self.history_stack.append(hs)
        self.history_current_step += 1


    def createHistoryStamp(self, desc):
        sel_obj = {
            'boxes': [],
            'edges': [],
        }
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'box'):
                sel_obj['boxes'].append(item.box.id)
            elif isinstance(item, GraphicsEdge):
                sel_obj['edges'].append(item.edge.id)

        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': sel_obj,
        }

        return history_stamp


    def restoreHistoryStamp(self, history_stamp):
        self.scene.deserialize(history_stamp['snapshot'])
        # restore selection
        for edge_id in history_stamp['selection']['edges']:
            for edge in self.scene.edges:
                if edge.id == edge_id:
                    edge.grEdge.setSelected(True)
                    break

        for box_id in history_stamp['selection']['boxes']:
            for box in self.scene.boxes:
                if box.id == box_id:
                    box.grBox.setSelected(True)
                    break

import traceback
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def dumpException(e):
    print("EXCEPTION:", e)
    traceback.print_tb(e.__traceback__)

def loadStylesheet(filename):
    print('STYLE loading:', filename)
    file = QFile(filename)
    file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = file.readAll()
    QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

def loadStylesheets(*args):
    res = ''
    for arg in args:
        file = QFile(arg)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        res += "\n" + str(stylesheet, encoding='utf-8')
    QApplication.instance().setStyleSheet(res)



