DEBUG = False

class Event(object):
    def __init__(self, origin, originspec, time):
        self.origin = origin
        self.time = time
        self.processed = False
        self.originspec = originspec

    def set_processed(self):
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
        self.in_events = dict()

        self.input_ports = list()
        self.output_ports = list()

        self.connected_outputs = dict()
        self.in_port_states = dict()
        self.out_port_states = dict()

    def add_input(self, input, state=0):
        self.input_ports.append(input)
        self.in_port_states[input] = state

    def add_output(self, output, state=0):
        self.output_ports.append(output)
        self.out_port_states[output] = state


    def event_available(self, port, time):
        if self.in_events.has_key(port) and time != self.in_events[port].time:
            return self.in_events[port]
        else:
            return None

    def timeslice(self, time):
        self.lastslice = time

    def timeslice_updatestates(self, time):
        evsAvail = self.in_events.keys()
        for port in evsAvail:
            if self.in_events[port].processed:
                self.in_port_states[port] = self.in_events[port].state
                del self.in_events[port]

    def connect_output(self, output, destination, destination_port):
        if output in self.output_ports:
            if not self.connected_outputs.has_key(output):
                self.connected_outputs[output] = list()
            self.connected_outputs[output].append((destination, destination_port))

        else:
            raise NoPort()

    def send_state_change(self, output, state, time):
        if output in self.output_ports:
            self.out_port_states[output] = state
            if self.connected_outputs.has_key(output):
                newevent = StateChangeEvent(self, output, time, state)
                for dest,destport in self.connected_outputs[output]:
                    dest.recv_state_change(destport, newevent)

        else:
            raise NoPort()

    def recv_state_change(self, port, event):
        if DEBUG:
            print 'RECV: %s:%s %s' % (self.name, port, event)
        if port in self.input_ports:
            self.in_events[port] = event
        else:
            raise NoPort()

class ClockedMixin(object):
    nr = 0
    def __init__(self):
        self.add_input('CLK')

    def timeslice(self, time):
        ev = self.event_available('CLK',time)
        if ev:
            if (ev.state == 1) and (self.in_port_states['CLK'] == 0):
                self.clk_rise(time)
            elif (ev.state == 0) and (self.in_port_states['CLK'] == 1):
                self.clk_fall(time)
            ev.set_processed()

    def clk_rise(self):
        pass

    def clk_fall(self):
        pass


