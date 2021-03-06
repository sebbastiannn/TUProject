from tests.testtoolbar.editor_graphics_box import GraphicsBox



class Box():
    def __init__(self, scene, title="Undefined Box"):
        super().__init__()
        self._title = title
        self.scene = scene


        self.grBox = GraphicsBox(self)
        self.title = title
        # eigenschaften hinzufügen hier
        self.capacity = 42
        self.scene.addBox(self)
        self.scene.grScene.addItem(self.grBox)

    # The grBox know the Box Position
    @property
    def pos(self):
        return self.grBox.pos()
    # set the position of the Box
    def setPos(self, x, y):
        self.grBox.setPos(x, y)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.grBox.title = self._title