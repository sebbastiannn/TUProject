import os
import sys
import inspect

from PyQt5.QtWidgets import *
from class_collection import loadStylesheet


from window import Window
import qss.darkskin_resources

if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = Window()
    wnd.editor.addBoxes()
    module_path = os.path.dirname(inspect.getfile(wnd.__class__))

    loadStylesheet(os.path.join(module_path, 'qss/editor-darkskin.qss'))

    wnd.show()

    sys.exit(app.exec_())
