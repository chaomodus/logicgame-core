DEBUG = False

class Event(object):
    def __init__(self, origin, originspec, time):
        self.origin = origin
        self.time = time
        self.processed = False
        self.originspec = originspec

    def setProcessed(self):
        self.processed = True

class StateChangeEvent(Event):
    def __init__(self, origin, originspec, time, state):
        Event.__init__(self, origin, originspec, time)
        self.state = state

    def __str__(self):
        return "<StateChangeEvent: %s:%s @ %d -> %d>" % (self.origin.name, self.originspec, self.time, self.state)

class LogicBaseException(Exception):
    pass

class NoPort(LogicBaseException):
    pass

class Node(object):
    nr = 0
    def __init__(self, name='NODE%d'):
        try:
            self.name = name % (self.__class__.nr)
        except TypeError:
            self.name = name

        self.__class__.nr = self.__class__.nr + 1

        self.lastslice = 0
        self.inEvents = dict()

        self.inputPorts = list()
        self.outputPorts = list()

        self.connectedOutputs = dict()
        self.inPortStates = dict()
        self.outPortStates = dict()

    def addInput(self, input, state=0):
        self.inputPorts.append(input)
        self.inPortStates[input] = state

    def addOutput(self, output, state=0):
        self.outputPorts.append(output)
        self.outPortStates[output] = state


    def eventAvailable(self, port, time):
        if self.inEvents.has_key(port) and time != self.inEvents[port].time:
            return self.inEvents[port]
        else:
            return None

    def timeslice(self, time):
        self.lastslice = time

    def timeslice_updatestates(self, time):
        evsAvail = self.inEvents.keys()
        for port in evsAvail:
            if self.inEvents[port].processed:
                self.inPortStates[port] = self.inEvents[port].state
                del self.inEvents[port]

    def connectOutput(self, output, destination, destinationPort):
        if output in self.outputPorts:
            if not self.connectedOutputs.has_key(output):
                self.connectedOutputs[output] = list()
            self.connectedOutputs[output].append((destination, destinationPort))

        else:
            raise NoPort()

    def sendStateChange(self, output, state, time):
        if output in self.outputPorts:
            self.outPortStates[output] = state
            if self.connectedOutputs.has_key(output):
                newevent = StateChangeEvent(self, output, time, state)
                for dest,destport in self.connectedOutputs[output]:
                    dest.recvStateChange(destport, newevent)

        else:
            raise NoPort()

    def recvStateChange(self, port, event):
        if DEBUG:
            print 'RECV: %s:%s %s' % (self.name, port, event)
        if port in self.inputPorts:
            self.inEvents[port] = event
        else:
            raise NoPort()

class ClockedMixin(object):
    nr = 0
    def __init__(self):
        self.addInput('CLK')

    def timeslice(self, time):
        ev = self.eventAvailable('CLK',time)
        if ev:
            if (ev.state == 1) and (self.inPortStates['CLK'] == 0):
                self.clkRise(time)
            elif (ev.state == 0) and (self.inPortStates['CLK'] == 1):
                self.clkFall(time)
            ev.setProcessed()

    def clkRise(self):
        pass

    def clkFall(self):
        pass


