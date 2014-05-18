import base

class MUX(base.AddressableMixin, base.Base):
    basename='MUX'

    def __init__(self, input_count=2, name=None):
        base.Base.__init__(self, name)
        base.AddressableMixin.__init__(self,input_count)

        self._add_pin('OUT', base.PIN_DIRECTION_OUT, 0)
        self.in_pins = list()

        for i in range(input_count):
            self._add_pin('IN%d' % i, base.PIN_DIRECTION_IN, 0)
            self.in_pins.append('IN%d' % i)

    def execute(self, time):
        addr = self.get_address()
        if addr < len(self.in_pins):
            self.next_pin_states['OUT'] = self.next_pin_states[self.in_pins[addr]]



class DEMUX(base.AddressableMixin, base.Base):
    basename='DEMUX'

    def __init__(self, output_count=2, name=None):
        base.Base.__init__(self, name)
        base.AddressableMixin.__init__(self, output_count)

        self._add_pin('IN', base.PIN_DIRECTION_IN, 0)
        self.out_pins = list()

        for i in range(output_count):
            self._add_pin('OUT%d' % i, base.PIN_DIRECTION_OUT, 0)
            self.out_pins.append('OUT%d' % i)


    def execute(self, time):
        addr = self.get_address()
        for p in self.out_pins:
            self.next_pin_states[p] = 0
        if addr < len(self.out_pins):
            self.next_pin_states[self.out_pins[addr]] = self.next_pin_states['IN']
