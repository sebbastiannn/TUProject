from editor_graphics_box import GraphicsBox
from editor_content_widget import ContentWidget
from editor_socket import *

class Box():
    def __init__(self, scene, title="Undefined Box", inputs=[], outputs=[]):
        self.scene = scene

        self.title = title

        self.content = ContentWidget(self)
        self.grBox = GraphicsBox(self)

        self.scene.addBox(self)
        self.scene.grScene.addItem(self.grBox)

        self.socket_spacing = 22

        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []

        counter = 0
        for item in inputs:
            socket = Socket(box=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(box=self, index=counter, position=RIGHT_TOP, socket_type=item)
            counter += 1
            self.outputs.append(socket)

    "The grBox know the Box Position"
    def pos(self):
        return self.grBox.pos()
    "set the position of the Box"
    def setBoxPos(self, x, y):
        self.grBox.setPos(x, y)


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
            if socket.hasEdge():
                socket.edge.updatePositions()

    def remove(self):
        # Removing Node + remove all edges from sockets
        for socket in (self.inputs+self.outputs):
            if socket.hasEdge():
                # when the socket is conected to edge deleted it
                socket.edge.remove()
        # remove grNode
        self.scene.grScene.removeItem(self.grBox)
        self.grBox = None
        # remove node from the scene
        self.scene.removeBox(self)
        # everything was done


