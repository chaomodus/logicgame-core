import base
from collections import defaultdict

class Container(Base):
    basename='CONTAINER'

    def __init__(self, name=None, inputs=(), outputs=()):
        Base.__init__(self, name)
        for inp in inputs:
            self._add_pin(inp, base.PIN_DIRECTION_IN)

        for outp in outputs:
            self._add_pin(outp, base.PIN_DIRECTION_OUT)
        
        self.input_maps = defaultdict(list)
        self.output_maps = defaultdict(list)

        self.components = dict()
        
    def add_component(self, comp, input_maps={}, output_maps={}):
        self.components[comp.__hash__] = comp
        for k in input_maps.keys():
            self.input_maps[k].append((comp,input_maps[k]))
        for k in output_maps.keys():
            self.output_maps[k].append((comp,output_maps[k]))
            
    def execute(self, time):
        for comp in sel.components:
            

class Simulator(Container):
    basename='SIMULATOR'

    def __init__(sel, name=None):
        Container.__init__(self, name)

    def simulate(self, ticks=1):
        # run the simulation loop /ticks/ times.
        pass


