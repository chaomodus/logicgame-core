from . import base
import math

sign = lambda x: math.copysign(1.0, x)
squarewave = lambda time, period: ((1+sign(((time - period / 2) % period) - period / 2)) / 2)

class Clock(base.Base):
    basename='CLK'
    def __init__(self, period=1, phase=0, name=None):
        base.Base.__init__(self, name)
        self._add_pin('CLK',base.PIN_DIRECTION_OUT, init_state=phase)
        self._add_pin('RST',base.PIN_DIRECTION_IN)

        self.init_phase = phase
        self.basetime = 0
        self.period = period

    def execute(self, time):
        if self.next_pin_states['RST'] == 1:
            self.next_pin_states['CLK'] = self.init_phase
            self.basetime = time
        else:
            sq = squarewave(time - self.basetime, self.period)
            if self.init_phase:
                self.next_pin_states['CLK'] = base.invert[sq]
            else:
                self.next_pin_states['CLK'] = sq
