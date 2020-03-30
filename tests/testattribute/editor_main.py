import sys


from PyQt5.QtWidgets import *

from tests.testattribute.editor_window import Window


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = Window()
    wnd.editor.addBoxes()
    wnd.show()

    sys.exit(app.exec_())
