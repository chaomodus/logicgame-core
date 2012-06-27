from base import Node
import os

class BasicGate(Node):
    nr = 0
    def __init__(self, name='GATE%d'):
        Node.__init__(self, name)
        self.add_input('A')
        self.add_input('B')
        self.add_output('OUT')
        self.lastout = 0

    def timeslice(self, time):
        Node.timeslice(self, time)

        A = self.in_port_states['A']
        B = self.in_port_states['B']

        aevent = self.event_available('A',time)
        bevent = self.event_available('B',time)
        if aevent:
            aevent.set_processed()
            A = aevent.state
        if self.in_events.has_key('B'):
            bevent.set_processed()
            B = bevent.state

        result = self.operator(A, B)
        if result != self.lastout:
            self.lastout = result
            self.send_state_change('OUT', result, time)

        self.timeslice_updatestates(time)


class NOT(Node):
    nr = 0
    def __init__(self, name='NOT%d'):
        Node.__init__(self, name)
        self.add_input('IN')
        self.add_output('OUT')

    def timeslice(self, time):
        Node.timeslice(self,time)

        ev = self.event_available('IN',time)
        if ev:
            newstate = int(not ev.state)
            ev.set_processed()
        else:
            newstate = int(not self.in_port_states['IN'])

        if self.out_port_states['OUT'] != newstate:
            self.send_state_change('OUT',newstate, time)

        self.timeslice_updatestates(time)



class AND(BasicGate):
    nr = 0
    def __init__(self, name='AND%d'):
        BasicGate.__init__(self, name)

    def operator(self, A, B):
        return int(A and B)

class OR(BasicGate):
    nr = 0
    def __init__(self, name='OR%d'):
        BasicGate.__init__(self, name)

    def operator(self, A, B):
        return int(A or B)


class XOR(BasicGate):
    nr = 0
    def __init__(self, name='XOR%d'):
        BasicGate.__init__(self, name)

    def operator(self, A, B):
        return int(A ^ B)

class NAND(BasicGate):
    nr = 0
    def __init__(self, name='NAND%d'):
        BasicGate.__init__(self, name)

    def operator(self, A, B):
        return int(not (A and B))

class NOR(BasicGate):
    nr = 0
    def __init__(self, name='NOR%d'):
        BasicGate.__init__(self, name)

    def operator(self, A, B):
        return int(not (A or B))


class XNOR(BasicGate):
    nr = 0
    def __init__(self, name='XNOR%d'):
        BasicGate.__init__(self, name)

    def operator(self, A, B):
        return int(not (A ^ B))


