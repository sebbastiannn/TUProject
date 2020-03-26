from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui

from tests.testtoolbar.editor_graphics_box import GraphicsBox
from tests.testtoolbar.editor_box_attributes import BoxAttributes

class GraphicsView(QGraphicsView, QWidget):
    left_clicked = QtCore.pyqtSignal(int)
    right_clicked = QtCore.pyqtSignal(int)
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.left_click_count = 0
        self.right_click_count = 0


        self.initUI()

        self.setScene(self.grScene)

    def initUI(self):
        "make everthing looks smoother and more pixel"
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        "Update the Scene in case of movement and reset the lines behind the object that was moved"
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        "hide the scrollbars"
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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

    def timeout(self):
        if self.left_click_count >= self.right_click_count:
            self.left_clicked.emit(self.left_click_count)
        else:
            self.right_clicked.emit(self.right_click_count)
        self.left_click_count = self.right_click_count = 0

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
        super().mousePressEvent(event)

    def middleMouseButtonRelease(self, event):
        super().mousePressEvent(event)

    "LEFT MOUSE BUTTON EVENT"
    def leftMouseButtonPress(self, event):
        item = self.getItemAtClick(event)

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        item = self.getItemAtClick(event)
        if type(item) is GraphicsBox:
            self.left_click_count += 1
            if not self.timer.isActive():
                self.timer.start()
            if self.left_click_count <= 1:
                print("click")
            else:
                print("double click")
                self.box_Attribut = BoxAttributes()



        super().mouseReleaseEvent(event)


    "RIGHT MOUSE BUTTON EVENT"
    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

class ClickHandler():
    def __init__(self, time):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(time)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.click_count = 0

    def timeout(self):
        if self.click_count == 1:
            print('Single click')
        elif self.click_count > 1:
            print('Double click')
        self.click_count = 0

    def __call__(self):
        self.click_count += 1
        if not self.timer.isActive():
            self.timer.start()
