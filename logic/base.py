"""Base classes with much of the core event-passing functionality, connectivity
and utilities for implementing gates."""

PIN_DIRECTION_IN = 0
PIN_DIRECTION_OUT = 1

import string
import math
import weakref

invert = {0: 1, 1: 0}


def staticvariable(variable, defaultvalue):
    def decorate(func):
        setattr(func, variable, defaultvalue)
        return func
    return decorate


class DuplicatePinError(Exception):
    pass


class Event(object):
    """A very simple event state object."""
    def __init__(self, time, value, origin, origin_pin, destination_pin):
        self.time = time
        self.value = int(value)
        self.origin = origin
        self.origin_pin = origin_pin
        self.destination_pin = destination_pin


class Pin(object):
    """Represents a pin, holder of connectivity state."""
    def __init__(self, pin_holder, pin_name):
        self.pin_holder = weakref.ref(pin_holder)
        self.pin_name = pin_name

    def __eq__(self, other):
        return (self.pin_holder() == other.pin_holder()) and (self.pin_name == other.pin_name)

    def __ne__(self, other):
        return not self.__eq__(other)

    def partner_alive(self):
        return not (self.pin_holder() is None)

    def send_event(self, event):
        if self.partner_alive():
            return self.pin_holder().recv_event(event)
        return None


class Enumerator(object):
    basename = 'ENUM'
    _number = 0

    def __init__(self, name=None):
        if name:
            self.name = name
        else:
            self.name = self._next_name()

    def _next_name(self, basename=None):
        nr = self.__class__._number
        self.__class__._number += 1
        if not basename:
            basename = self.basename
        return basename + str(nr)

    def __repr__(self):
        return "<{class} {name}>".format(self.__class__.__name__, self.name)


class Base(Enumerator):
    """Base class for all gates. Implements connectivity and event passing.

       Order of method calls in simulation:

       * recieve all input events, update next_state (process_inputs)
       * call process method (execute)
       * update next state with output states (done in execute)
       * compare states and emit output events (process_outputs)

       Most functionality of descended gates is implemented in execute, which
       looks at the contents of next_pin_states and updates those contents as
       needed.
"""
    basename = 'BASE'

    def __init__(self, name=None, init_time=0):
        Enumerator.__init__(self, name)

        self.input_event_queue = list()

        # format: {pin name: 1/0, ...}
        self.pin_states = dict()
        self.next_pin_states = dict()

        # format {pin name: {'direction':DIRECTION, 'init_state': default value}, ...}
        self.pin_info = dict()

        # format {pin_name: (Pin(), ...), ...}
        self.output_connections = dict()

        # format {pin_name: {(partner obj, partner pin name): 1/0, ...)}, ...}
        self.input_wire_states = dict()

        self.time = init_time

    def _add_pin(self, pin_name, pin_direction, init_state=0):
        """Internal use. Descendents of this class should call this to add
           pins."""
        if pin_name in self.pin_info:
            raise DuplicatePinError()
        self.pin_states[pin_name] = init_state
        self.next_pin_states[pin_name] = init_state
        self.pin_info[pin_name] = {'direction': pin_direction,
                                   'init_state': init_state}
        if pin_direction:
            self.output_connections[pin_name] = list()

    def connect_pin(self, pin_name, partner_object, partner_pin):
        """Connect an output pin pin_name to a partner object's input pin
           partner_pin."""
        newpin = Pin(partner_object, partner_pin)
        for p in self.output_connections[pin_name]:
            if newpin == p:
                return None
        self.output_connections[pin_name].append(newpin)
        partner_object.on_connected(partner_pin, self, pin_name)
        newpin.send_event(Event(self.time,
                                self.pin_states[pin_name],
                                self, pin_name, partner_pin))

    def disconnect_pin(self, pin_name, partner_object, partner_pin):
        """Remove a connection to partner_oject from pin_name."""
        if pin_name in self.output_connections:
            for pin_obj in self.output_connections[pin_name]:
                if (pin_obj.pin_holder() is partner_object) and (pin_obj.pin_name == partner_pin):
                    self.output_connections.remove(pin_obj)
                    return partner_object.on_disconnected(partner_pin, self, pin_name)

    def disconnect_all(self, partner_object):
        """Repeatedly calls disconnect_pin for each pin connected to
           partner_object."""
        for pin in self.output_connections:
            cleanup = []
            for pin_obj in self.output_connections[pin]:
                if pin_obj.pin_holder() is partner_object:
                    cleanup.append(pin_obj)
            for item in cleanup:
                self.output_connections[pin].remove(item)
                if item.pin_holder() is not None:
                    item.pin_holder().on_disconnected(item.pin_name, self, pin)

    def on_connected(self, pin_name, partner_object, partner_pin):
        """Called when the output pin from a separate gate connects to this
           object."""
        pass

    def on_disconnected(self, pin_name, partner_object, partner_pin):
        """Called when the output pin from a separate gate disconnects from
           this object.

           By default cleans up input wires.
        """
        if pin_name in self.input_wire_states:
            if (partner_object, partner_pin) in self.input_wire_states[pin_name]:
                del self.input_wire_states[pin_name][(partner_object, partner_pin)]

    def pin_changed_p(self, pin_name):
        """Returns True if the given local pin has changed since last cycle."""
        return self.next_pin_states[pin_name] != self.pin_states[pin_name]

    def recv_event(self, event):
        """Append an event into the input event queue. Protocol dictates that
           if it's successful it must return True."""
        self.input_event_queue.append(event)
        return True

    def process_inputs(self, time):
        """Updates wire state cache based on input events and then next_pin_states
           based on wire states."""
        # update next_state based on input events.
        for ev in self.input_event_queue:
            if ev.time <= time:
                self.input_wire_states.setdefault(ev.destination_pin, {})
                self.input_wire_states[ev.destination_pin][(ev.origin, ev.origin_pin)] = ev.value
        for pin in self.next_pin_states:
            if pin in self.input_wire_states:
                tot = 0
                tot = sum(self.input_wire_states[pin].values())
                if tot >= 1:
                    self.next_pin_states[pin] = 1
                else:
                    self.next_pin_states[pin] = 0

        self.input_event_queue = list()

    def execute(self, time):
        """To be implemented by downstream gates. Basically, examine input pins
           in next_pin_states and update output pins in next_pin_states."""
        raise NotImplementedError()

    def process_outputs(self, time):
        """Checks the states of output pins in next_pin_states and sends events
           on any changed pins.

           Also performs a cleanup step on any dead output pins.
        """
        cleanup = list()
        for pin, value in self.next_pin_states.iteritems():
            if self.pin_states[pin] != value:
                if pin in self.output_connections:
                    for conn in self.output_connections[pin]:
                        newev = Event(time, value, self, pin, conn.pin_name)
                        if not conn.send_event(newev):
                            # our partner is gone
                            cleanup.append((pin, conn))
                    self.pin_states[pin] = value
        # cleanup dead partners
        for outpin, conn in cleanup:
            self.output_connections[outpin].remove(conn)


class Passthrough(Base):
    """A very simple gate which allows internal connections between pins to
       pass state between inputs and outputs."""
    basename = 'PT'

    def __init__(self, name=None):
        Base.__init__(self, name)
        self.connections = dict()

    def add_pin(self, pin_name, pin_direction, pin_connection=None):
        self._add_pin(pin_name, pin_direction)
        if pin_direction == PIN_DIRECTION_IN and pin_connection:
            if pin_name not in self.connections:
                self.connections[pin_name] = list()
            self.connections[pin_name].append(pin_connection)

    def execute(self, time):
        for p, conns in self.connections.items():
            for c in conns:
                if c in self.pin_states:
                    self.next_pin_states[c] = self.next_pin_states[p]


class Buffer(Passthrough):
    basename = 'BUF'

    def __init__(self, name=None):
        Passthrough.__init__(self, name)
        self.add_pin('OUT', PIN_DIRECTION_OUT, None)
        self.add_pin('IN', PIN_DIRECTION_IN, 'OUT')


def addr_range(bits):
    """Generate a bitmap for each enumerated address for a given number of
       bits."""
    for addr in xrange(2**bits):
        yield tuple([int(x) for x in
                     tuple(string.rjust(bin(addr)[2:], bits, '0'))])


class AddressableMixin(object):
    """A mixin which adds SELn inputs to a gate for selecting an enumerated
       address."""
    def __init__(self, max_selector, selector_prefix='SEL'):
        self._a_m_sel_pins = list()
        self._a_m_curr_address = None
        self._a_m_prefix = selector_prefix
        selector_bits = int(math.ceil(math.log(max_selector, 2.0)))

        for i in range(selector_bits):
            pin_name = "{prefix}{nr}".format(prefix=selector_prefix, nr=i)
            self._add_pin(pin_name,
                          PIN_DIRECTION_OUT,
                          0)
            self._a_m_sel_pins.append(pin_name)

    def get_address(self):
        return int("".join([str(self.next_pin_states[p])
                            for p in self._a_m_sel_pins]), 2)


class NOT(Base):
    """A very simple gate which inverts the value of events sent to its IN
       port and sends them to its OUT port."""
    basename = 'NOT'

    def __init__(self, name=None):
        Base.__init__(self, name=name)
        self._add_pin('IN', PIN_DIRECTION_IN)
        self._add_pin('OUT', PIN_DIRECTION_OUT)

        self.execute(0)
        self.process_outputs(0)

    def execute(self, time):
        self.next_pin_states['OUT'] = invert[self.next_pin_states['IN']]
