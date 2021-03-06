from collections import OrderedDict
from class_collection import Serializable
from graphics_box import GraphicsBox
from content_widget import ContentWidget
from socket import *

class Box(Serializable):
    def __init__(self, scene, title="Undefined Box", inputs=[], outputs=[]):
        super().__init__()
        self._title = title
        self.scene = scene

        self.content = ContentWidget(self)
        self.grBox = GraphicsBox(self)
        self.title = title

        self.scene.addBox(self)
        self.scene.grScene.addItem(self.grBox)

        self.socket_spacing = 22

        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []

        counter = 0
        for item in inputs:
            socket = Socket(box=self, index=counter, position=LEFT_BOTTOM, socket_type=item, multi_edges=False)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(box=self, index=counter, position=RIGHT_TOP, socket_type=item, multi_edges=True)
            counter += 1
            self.outputs.append(socket)

    "The grBox know the Box Position"

    @property
    def pos(self):
        return self.grBox.pos()
    "set the position of the Box"
    def setPos(self, x, y):
        self.grBox.setPos(x, y)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.grBox.title = self._title

    def getSocketPosition(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.grBox.width
        y = 0 if (position in (LEFT_TOP_Y, RIGHT_TOP_Y)) else self.grBox.height

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grBox.height - self.grBox.edge_size - self.grBox._padding - index * self.socket_spacing
        elif position in (LEFT_TOP, RIGHT_TOP):
            # start from top
            y = self.grBox.title_height + self.grBox._padding + self.grBox.edge_size + index * self.socket_spacing
        elif position in (RIGHT_TOP_Y, RIGHT_BOTTOM_Y):
            # start
            x = self.grBox.edge_size + self.grBox._padding + index * self.socket_spacing
        else:
            # if position in (LEFT_TOP_Y, LEFT_BOTTOM_Y)
            x = self.grBox._padding + self.grBox.edge_size + index * self.socket_spacing

        return [x, y]

    "update the connected edges with the sockets"
    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            # if socket.hasEdge():
            for edge in socket.edges:
                edge.updatePositions()


    def remove(self):
        # Removing Node + remove all edges from sockets
        for socket in (self.inputs + self.outputs):
            # if socket.hasEdge():
            for edge in socket.edges:
                # removing from socket:", socket, "edge:", edge)
                edge.remove()
        # remove grNode
        self.scene.grScene.removeItem(self.grBox)
        self.grBox = None
        # remove node from the scene
        self.scene.removeBox(self)

    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.grBox.scenePos().x()),
            ('pos_y', self.grBox.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', self.content.serialize()),
        ])

    def deserialize(self, data, hashmap={}, restore_id=True):
        if restore_id: self.id = data['id']
        hashmap[data['id']] = self

        self.setPos(data['pos_x'], data['pos_y'])
        self.title = data['title']

        data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
        data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)

        self.inputs = []
        for socket_data in data['inputs']:
            new_socket = Socket(box=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.inputs.append(new_socket)

        self.outputs = []
        for socket_data in data['outputs']:
            new_socket = Socket(box=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap, restore_id)
            self.outputs.append(new_socket)

        return True




