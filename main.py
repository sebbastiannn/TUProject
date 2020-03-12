import sys
from PyQt5.QtWidgets import *

from editor_main_window import EditorMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = EditorMainWindow()

    sys.exit(app.exec_())
