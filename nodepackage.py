from base import Node

class NodePackage(Node):
    nr = 0
    def __init__(self, name='PKG%d'):
        Node.__init__(self,name)
        self.contents = list()

    def timeslice(self, time):
        Node.timeslice(self, time)

        for node in self.contents:
            node.timeslice(time)

    def add_virtual_input(self, input, state=0):
        pass

    def add_virtual_output(self, input, state=0):
        pass

    def add_node(self, node):

