"In computing, serialization (or serialisation) is the" \
"process of translating data structures or object state " \
"into a format that can be stored - our case will be json"
class Serializable():
    def __init__(self):
        self.id = id(self)

    def serialize(self):
        raise NotImplemented()

    def deserialize(self, data, hashmap={}):
        raise NotImplemented()

"The Scene History"
from editor_edge import GraphicsEdge

class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.history_stack = []
        self.history_current_step = -1
        self.history_limit = 32

    def undo(self):
        if self.history_current_step > 0:
            self.history_current_step -= 1
            self.restoreHistory()

    def redo(self):
        if self.history_current_step + 1 < len(self.history_stack):
            self.history_current_step += 1
            self.restoreHistory()


    def restoreHistory(self):
        "Restoring history current_step:"
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])


    def storeHistory(self, desc):
        "Storing history current_step"
        # if the pointer (history_current_step) is not at the end of history_stack
        if self.history_current_step+1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.history_current_step+1]

        # history is outside of the limits
        if self.history_current_step+1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -= 1

        hs = self.createHistoryStamp(desc)

        self.history_stack.append(hs)
        self.history_current_step += 1


    def createHistoryStamp(self, desc):
        sel_obj = {
            'boxes': [],
            'edges': [],
        }
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'box'):
                sel_obj['boxes'].append(item.box.id)
            elif isinstance(item, GraphicsEdge):
                sel_obj['edges'].append(item.edge.id)

        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': sel_obj,
        }

        return history_stamp


    def restoreHistoryStamp(self, history_stamp):
        self.scene.deserialize(history_stamp['snapshot'])
        # restore selection
        for edge_id in history_stamp['selection']['edges']:
            for edge in self.scene.edges:
                if edge.id == edge_id:
                    edge.grEdge.setSelected(True)
                    break

        for box_id in history_stamp['selection']['boxes']:
            for box in self.scene.boxes:
                if box.id == box_id:
                    box.grBox.setSelected(True)
                    break

