from collections import OrderedDict
from class_collection import Serializable

from PyQt5.QtWidgets import *

" Wird dann später mit einem Icon gefüllt"
class ContentWidget(QWidget, Serializable):
    def __init__(self, box, parent=None):
        # important to add because there will be a bug
        # when deleting the box
        # but not this widget
        self.box = box
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Some Title")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QTextEdit("foo"))

    def serialize(self):
        return OrderedDict([

        ])

    def deserialize(self, data, hashmap={}):
        return False


