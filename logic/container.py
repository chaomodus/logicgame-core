from . import base
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
class Package(base.Enumerator, Container):
    basename = 'PKG'

    def __init__(self, name=None):
        Container.__init__(self)
        base.Enumerator.__init__(self, name)

        self.INPUTS = base.Passthrough(name=self.name+'.INPUT')
        self.OUTPUTS = base.Passthrough(name=self.name+'.OUTPUT')

    def execute(self, tm):
        self.INPUTS.execute(tm)
        self.INPUTS.process_outputs(tm)

        Container.execute(self,tm)

        self.OUTPUTS.process_inputs(tm)
        self.OUTPUTS.execute(tm)

    def recv_event(self, event):
        self.INPUTS.recv_event(event)

    def connect_pin(self, pin_name, partner_object, partner_pin):
        self.OUTPUTS.connect_pin(pin_name, partner_object, partner_pin)

    def process_inputs(self, tm):
        self.INPUTS.process_inputs(tm)

    def process_outputs(self, tm):
        self.OUTPUTS.process_outputs(tm)

    def add_pin(self, pin_name, pin_direction):
        if pin_direction == base.PIN_DIRECTION_IN:
            self.INPUTS.add_pin(pin_name+'.OUT', base.PIN_DIRECTION_OUT)
            self.INPUTS.add_pin(pin_name, base.PIN_DIRECTION_IN, pin_name+'.OUT')
        else:
            self.OUTPUTS.add_pin(pin_name+'.IN', base.PIN_DIRECTION_IN, pin_name)
            self.OUTPUTS.add_pin(pin_name, base.PIN_DIRECTION_OUT)

    def connect_pin_internal_input(self, pin_name, partner_object, partner_pin):
        if self.INPUTS.pin_info.has_key(pin_name):
            self.INPUTS.connect_pin(pin_name+'.OUT', partner_object, partner_pin)

    def connect_pin_internal_output(self, pin_name, partner_object, partner_pin):
        if self.OUTPUTS.pin_info.has_key(pin_name):
            partner_object.connect_pin(partner_pin, self.OUTPUTS, pin_name+'.IN')

    def connect_pin_internal_passthrough(self, in_pin, out_pin):
        self.INPUTS.connect_pin(in_pin+'.OUT', self.OUTPUTS, out_pin+'.IN')

    @property
    def pin_states(self):
        outp = self.INPUTS.pin_states.copy()
        outp.update(self.OUTPUTS.pin_states)
        return outp


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
            frame[g.name] = g.pin_states.copy()

        # collect gate states
        self.data.append((tm,frame))
