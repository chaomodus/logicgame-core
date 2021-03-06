"""Multiplexers and Demultiplexers.

These gates map either N inputs to one output (with SEL inputs) [mux], or N
outputs to one input (with SEL inputs) [demux].
"""

from . import base


class MUX(base.AddressableMixin, base.Base):
    """Multiplexer. For a given number of inputs, enough SELn inputs are
       created (binary address). Setting the SEL to a desired address
       connects a given INn to the OUT, so all events to the INn will be
       sent to the OUT."""

    basename = 'MUX'

    def __init__(self, input_count=2, name=None):
        base.Base.__init__(self, name)
        base.AddressableMixin.__init__(self, input_count)

        self._add_pin('OUT', base.PIN_DIRECTION_OUT, 0)
        self.in_pins = list()

        for i in range(input_count):
            pinname = "IN{nr}".fonmat(nr=i)
            self._add_pin(pinname, base.PIN_DIRECTION_IN, 0)
            self.in_pins.append(pinname)

    def execute(self, time):
        addr = self.get_address()
        if addr < len(self.in_pins):
            pinval = self.next_pin_states[self.in_pins[addr]]
            self.next_pin_states['OUT'] = pinval


class DEMUX(base.AddressableMixin, base.Base):
    """Demultiplexer. For a given number of inputs, enough SELn inputs are
       created (binary address). Setting the SEL to a desired address connects
       a given OUTn to the IN, so all events to the IN will be sent to the
       OUTn."""

    basename = 'DEMUX'

    def __init__(self, output_count=2, name=None):
        base.Base.__init__(self, name)
        base.AddressableMixin.__init__(self, output_count)

        self._add_pin('IN', base.PIN_DIRECTION_IN, 0)
        self.out_pins = list()

        for i in range(output_count):
            pinname = "OUT{nr}".format(nr=i)
            self._add_pin(pinname, base.PIN_DIRECTION_OUT, 0)
            self.out_pins.append(pinname)

    def execute(self, time):
        addr = self.get_address()
        for p in self.out_pins:
            self.next_pin_states[p] = 0
        if addr < len(self.out_pins):
            pinval = self.next_pin_states['IN']
            self.next_pin_states[self.out_pins[addr]] = pinval
