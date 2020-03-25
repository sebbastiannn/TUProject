
from tests.testtoolbar.editor_graphics_scene import GraphicsScene

"Content from Scene"
class Scene():
    def __init__(self):
        super().__init__()

        self.boxes = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        self.grScene = GraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addBox(self, box):
        self.boxes.append(box)
