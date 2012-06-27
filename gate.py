from base import Node
import os

class BasicGate(Node):
    nr = 0
    def __init__(self, name='GATE%d'):
        Node.__init__(self, name)
        self.addInput('A')
        self.addInput('B')
        self.addOutput('OUT')
        self.lastout = 0

    def timeslice(self, time):
        Node.timeslice(self, time)

        A = self.inPortStates['A']
        B = self.inPortStates['B']

        aevent = self.eventAvailable('A',time)
        bevent = self.eventAvailable('B',time)
        if aevent:
            aevent.setProcessed()
            A = aevent.state
        if self.inEvents.has_key('B'):
            bevent.setProcessed()
            B = bevent.state

        result = self.operator(A, B)
        if result != self.lastout:
            self.lastout = result
            self.sendStateChange('OUT', result, time)

        self.timeslice_updatestates(time)


class NOT(Node):
    nr = 0
    def __init__(self, name='NOT%d'):
        Node.__init__(self, name)
        self.addInput('IN')
        self.addOutput('OUT')

    def timeslice(self, time):
        Node.timeslice(self,time)

        ev = self.eventAvailable('IN',time)
        if ev:
            newstate = int(not ev.state)
            ev.setProcessed()
        else:
            newstate = int(not self.inPortStates['IN'])

        if self.outPortStates['OUT'] != newstate:
            self.sendStateChange('OUT',newstate, time)

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


