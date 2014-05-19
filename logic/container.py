import base
from collections import defaultdict

# super generic container takes care of sequencing the execution of its contents as one cycle.
# does not fully implement the base protocol
class Container(object):
    def __init__(self):
        self.contents = list()

    def add_gate(self, gate):
        self.contents.append(gate)

    def execute(self, tm):
        [g.process_inputs(tm) for g in self.contents]
        [g.execute(tm) for g in self.contents]
        [g.process_outputs(tm) for g in self.contents]

# less generic container, implements the full base protocol and has inputs and outputs
class Package(Container, base.Base):
    pass

# a less generic container, does not implement full base prototocol, but collects data from its contents at each execution
class Simulator(Container):
    def __init__(self):
        Container.__init__(self)
        self.data = list()

    def simulate(self, basetime=0, ticks=1):
        t = basetime
        while t < (basetime + ticks):
            self.execute(t)
            t += 1

    def execute(self, tm):
        Container.execute(self, tm)

        frame=dict()
        for g in self.contents:
            if g.__dict__.has_key('pin_states'):
                frame[g.name] = dict(g.pin_states)

        # collect gate states
        self.data.append((tm,frame))
