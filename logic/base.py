PIN_DIRECTION_IN = 0
PIN_DIRECTION_OUT = 1

import string
import math

invert = {0:1,1:0}

class DeplicatePinError(Exception):
    pass

class Event(object):
    def __init__(self, time, value, origin, origin_pin, destination_pin):
        self.time = time
        self.value = int(value)
        self.origin = origin
        self.origin_pin = origin_pin
        self.destination_pin = destination_pin

class Pin(object):
    def __init__(self, pin_holder, pin_name):
        self.pin_holder = pin_holder
        self.pin_name = pin_name

    def __eq__(self, other):
        return (self.pin_holder == other.pin_holder) and (self.pin_name == other.pin_name)

    def __ne__(self, other):
        return not self.__eq__(other)

    def send_event(self, event):
        return pin_holder.recv_event(self.pin_name, event)



# recieve all input events, update next_state
# call process method
# update next state with output states
# compare states and emit output events
class Base(object):
    basename='Base'
    _number=0

    def __init__(self, name=None, init_time = 0):
        if name:
            self.name = name
        else:
            self.name = self._next_name()

        self.input_event_queue = list()

        self.pin_states = dict()
        self.next_pin_states = dict()
        self.pin_info = dict()
        self.output_connections = dict()

        self.time = init_time

    def _next_name(self, basename=None):
        nr = self.__class__._number
        self.__class__._number += 1
        if not basename:
            basename=self.basename
        return basename + str(nr)


    def _add_pin(self, pin_name, pin_direction, init_state=0):
        if self.pin_info.has_key(pin_name):
            raise DuplicatePinError()
        self.pin_states[pin_name] = init_state
        self.next_pin_states[pin_name] = init_state
        self.pin_info[pin_name] = {'direction':pin_direction, 'init_state':init_state}
        if pin_direction:
            self.output_connections[pin_name] = list()

    def connect_pin(self, pin_name, partner_object, partner_pin):
        newpin = Pin(partner_object, partner_pin)
        for p in self.output_connections[pin_name]:
            if newpin == p:
                return None
        self.output_connections.append(newpin)
        newpin.send_event(Event(self.time, self.pin_states[pin_name], self, pin_name))

    def pin_changed_p(self, pin_name):
        return self.next_pin_states[pin_name] != self.pin_states[pin_name]

    def recv_event(self, event):
        self.input_event_queue.append(event)

    def process_inputs(self, time):
        # update next_state based on input events.
        for ev in self.input_event_queue:
            if ev.time <= time:
                if self.next_pin_states.has_key(ev.destination_pin):
                    self.next_pin_states[ev.destination_pin] = ev.value

    def execute(self, time):
        # to be implemented by the gates in question (examine next input states and update output states based on differences).
        raise NotImplementedError()

    def process_outputs(self, time):
        # check all of the output pin states against the previous states and produce update events on differences
        for pin,value in self.next_pin_states.iteritems():
            if self.pin_states[pin] != value:
                if self.output_connections.has_key(pin):
                    for conn in self.output_connections[pin]:
                        newev = Event(time, value, self, pin, conn.pin_name)
                        conn.send_event(newev)
                    self.pin_states[pin] = value

    def __repr__(self):
        return '<%s %s>' % (str(self.__class__.__name__), self.name)

def addr_range(bits):
    for addr in xrange(2**bits):
        yield tuple([int(x) for x in tuple(string.rjust(bin(addr)[2:], bits, '0'))])

class AddressableMixin(object):
    def __init__(self, max_selector, selector_prefix='SEL'):
        self._a_m_sel_pins = list()
        self._a_m_curr_address = None
        self._a_m_prefix = selector_prefix
        selector_bits = int(math.ceil(math.log(max_selector, 2.0)))

        for i in range(selector_bits):
            self._add_pin('%s%d' % (selector_prefix,i), PIN_DIRECTION_OUT, 0)
            self._a_m_sel_pins.append('%s%d' % (selector_prefix,i))

    def get_address(self):
        return int("".join([str(self.next_pin_states[p]) for p in self._a_m_sel_pins]), 2)

class NOT(Base):
    basename='NOT'

    def __init__(self, name=None):
        Base.__init__(self, name=name)
        self._add_pin('IN', PIN_DIRECTION_IN)
        self._add_pin('OUT',PIN_DIRECTION_OUT)

        self.execute(0)
        self.process_outputs(0)

    def execute(self, time):
        self.next_pin_states['OUT'] = invert[self.next_pin_states['IN']]
