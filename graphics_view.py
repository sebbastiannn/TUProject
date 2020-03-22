from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from socket import GraphicsSocket
from edge import *                   #Edge, EDGE_TYPE_BEZIER

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10

DEBUG = True

class GraphicsView(QGraphicsView):
    # get the position (x,y) for each box etc / for deserialization
    scenePosChanged = pyqtSignal(int, int)

    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()

        self.setScene(self.grScene)

        self.mode = MODE_NOOP
        self.rubberBandDraggingRectangle = False

        "For zoom"
        self.zoomInFactor = 1.25
        self.zoomClamp = True               # if True there will be max and min Zoom
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    def initUI(self):
        "make everthing looks smoother and more pixel"
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        "Update the Scene in case of movement and reset the lines behind the object that was moved"
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        "hide the scrollbars"
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        "For scrolling"
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    "what happen when we press mouse button"
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    "what happen when we release mouse button"
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    "MIDDLE MOUSE BUTTON EVENT"
    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    "LEFT MOUSE BUTTON EVENT"
    def leftMouseButtonPress(self, event):
        # get item which we clicked on
        item = self.getItemAtClick(event)

        # we store the position of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # logic
        if type(item) is GraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        # without clicking on socket will crush the system
        if item is None:
            self.rubberBandDraggingRectangle = True

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        # get item which we release mouse button on
        item = self.getItemAtClick(event)

        # logic
        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        if self.rubberBandDraggingRectangle:
            self.grScene.scene.history.storeHistory("Selection changed")
            self.rubberBandDraggingRectangle = False

        super().mouseReleaseEvent(event)

    "RIGHT MOUSE BUTTON EVENT"
    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)
        item = self.getItemAtClick(event)
        if isinstance(item, GraphicsEdge): print('RMB:', item.edge, ' connecting sockets:',
                                                        item.edge.start_socket, '<-->', item.edge.end_socket)
        if type(item) is GraphicsSocket: print('RMB DEBUG:', item.socket, 'has edges:', item.socket.edges)
        if item is None:
            print('SCENE:')
            print('  Boxes:')
            for box in self.grScene.scene.boxes: print('    ', box)
            print('  Edges:')
            for edge in self.grScene.scene.edges: print('    ', edge)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.drag_edge.grEdge.setDestination(pos.x(), pos.y())
            self.drag_edge.grEdge.update()

        self.last_scene_mouse_position = self.mapToScene(event.pos())

        self.scenePosChanged.emit(
            int(self.last_scene_mouse_position.x()), int(self.last_scene_mouse_position.y())
        )

        super().mouseMoveEvent(event)

    "Press event for delete"
    def keyPressEvent(self, event):
        # Use this code below if you wanna have shortcuts in this widget.
        # You want to use this, when you don't have a window which handles these shortcuts for you

        #if event.key() == Qt.Key_Delete:
            #self.deleteSelected()
        # S for Save
        #elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
            #self.grScene.scene.saveToFile("graph.json.txt")
        # L for Load
        #elif event.key() == Qt.Key_L and event.modifiers() & Qt.ControlModifier:
            #self.grScene.scene.loadFromFile("graph.json.txt")

        #elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and not event.modifiers() & Qt.ShiftModifier:
            #self.grScene.scene.history.undo()

        #elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
            #self.grScene.scene.history.redo()

        #elif event.key() == Qt.Key_H:
            #print("HISTORY:     len(%d)" % len(self.grScene.scene.history.history_stack),
                  #" -- current_step", self.grScene.scene.history.history_current_step)
            #ix = 0
            #for item in self.grScene.scene.history.history_stack:
                #print("#", ix, "--", item['desc'])
                #ix += 1
        #else:
            super().keyPressEvent(event)

    "deleting selected item"
    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, GraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'box'):
                item.box.remove()
        # store deleted stuff
        self.grScene.scene.history.storeHistory("Delete selected")

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        self.drag_start_socket = item.socket
        self.drag_edge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP
        # View::edgeDragEnd ~ End dragging edge
        self.drag_edge.remove()
        self.drag_edge = None

        if type(item) is GraphicsSocket:
            if item.socket != self.drag_start_socket:
                if item.socket != self.drag_start_socket:
                    # if we released dragging on a socket (other then the beginning socket)

                    # we wanna keep all the edges comming from target socket
                    if not item.socket.is_multi_edges:
                        item.socket.removeAllEdges()

                    # we wanna keep all the edges comming from start socket
                    if not self.drag_start_socket.is_multi_edges:
                        self.drag_start_socket.removeAllEdges()

                    new_edge = Edge(self.grScene.scene, self.drag_start_socket, item.socket, edge_type=EDGE_TYPE_BEZIER)
                    #"View::edgeDragEnd ~  created new edge:", new_edge, "connecting",new_edge.start_socket, "<-->", new_edge.end_socket)
                    # history
                    self.grScene.scene.history.storeHistory("Created new edge by dragging")
                    return True

        # View::edgeDragEnd ~ everything done
        return False


    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y()) > edge_drag_threshold_sq

    "overwrite the normal wheel Event so we can add max an min zoom"
    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

