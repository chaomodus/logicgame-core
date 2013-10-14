

PIN_DIRECTION_IN = 0
PIN_DIECTION_OUT = 1

class DeplicatePinError(Exception):
    pass

class Event(object):
    def __init__(self, time, value, origin, origin_pin):
        self.value = value
        self.processed = False
        self.origin = origin
        self.origin_pin = origin_pin

class Pin(object):
    def __init__(self, pin_holder, pin_name):
        self.pin_holder = pin_holder
        self.pin_name = pin_name

    def __eq__(self, other):
        return (self.pin_holder == other.pin_holder) and
               (self.pin_name == other.pin_name)

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
        self.output_event_queue = list()

        self.pin_states = dict()
        self.next_pin_states = dict()
        self.pin_info = dict()
        self.output_connections = dict()

        self.time = init_time

    def _next_name(self):
        nr = self.__class__._number
        self.__class__._number += 1
        return self.basename + str(nr)


    def _add_pin(self, pin_name, pin_direction, init_state):
        if self.pin_info.has_key(pin_name)
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

    def recv_event(self, event):
        self.input_event_queue.append(event)

    def process_inputs(self, time):
        # iterate waiting events and update next input pin states based on this
        pass

    def execute(self, time, changed_pins):
        # to be implemented by the gates in question (examine next input states and update output states based on differences).
        pass

    def process_outputs(self, time):
        # check all of the output pin states against the previous states and produce update events on differences
        pass

    def __repr__(self):
        return '<%s %s>' % (str(self.__class__.__name__), self.name)

class Bus(Base):
    basename='Bus'

class MUX(Base):
    basename='MUX'
    pass

class LUT(Base):
    basename='LUT'
    pass
