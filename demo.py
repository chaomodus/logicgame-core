import logic.clock as clock
import logic.gate as gate
import logic.container as container
import logic.base as base
import sys


class P_DFLIPFLOP(container.Package):
    basename='PDFF'

    def __init__(self, name=None):
        container.Package.__init__(self, name)
        self.add_pin('D',base.PIN_DIRECTION_IN)
        self.add_pin('CLK',base.PIN_DIRECTION_IN)
        self.add_pin('Q',base.PIN_DIRECTION_OUT)
        self.add_pin('/Q',base.PIN_DIRECTION_OUT)

        for i in range(4):
            self.add_gate(gate.NAND(2))

        self.add_gate(base.NOT())

        self.connect_pin_internal_output('Q',self.contents[0], 'OUT')
        self.connect_pin_internal_output('/Q',self.contents[1], 'OUT')

        self.contents[0].connect_pin('OUT',self.contents[1], 'IN0')
        self.contents[1].connect_pin('OUT',self.contents[0], 'IN1')

        self.contents[2].connect_pin('OUT',self.contents[0], 'IN0')
        self.contents[3].connect_pin('OUT',self.contents[1], 'IN1')

        self.contents[4].connect_pin('OUT',self.contents[3], 'IN0')

        self.connect_pin_internal_input('D', self.contents[2], 'IN0')
        self.connect_pin_internal_input('D', self.contents[4], 'IN')

        self.connect_pin_internal_input('CLK', self.contents[2], 'IN1')
        self.connect_pin_internal_input('CLK', self.contents[3], 'IN1')

class PGEN(container.Package):
    basename='PGEN'

    def __init__(self, name=None):
        container.Package.__init__(self, name)

        self.add_pin('IN',base.PIN_DIRECTION_IN)
        self.add_pin('OUT',base.PIN_DIRECTION_OUT)

        self.add_gate(base.NOT())
        self.add_gate(gate.AND(2))

        self.contents[0].connect_pin('OUT',self.contents[1], 'IN0')
        self.connect_pin_internal_input('IN',self.contents[0], 'IN')
        self.connect_pin_internal_input('IN',self.contents[1], 'IN1')
        self.connect_pin_internal_output('OUT',self.contents[1],'OUT')

def sample(gate, pin, data, stride):
    out = list()
    s = stride
    point = 0
    for d in data:
        point += int(d[1][gate][pin])
        if s <= 0:
            datum = point / float(stride)
            point = 0
            out.append(datum)
            s = stride
        s -= 1
    return out

def format_data(dat):
    out = ''
    for i in dat:
        if i > 0.5:
            out = out + '-'
        else:
            out = out + '_'
    return out

c0 = clock.Clock(1253)
c1 = clock.Clock(2000)
divider = P_DFLIPFLOP()
pgen = PGEN()

c0.connect_pin('CLK',divider,'CLK')
c1.connect_pin('CLK',divider, 'D')
c0.connect_pin('CLK',pgen,'IN')
#divider.connect_pin('/Q', divider, 'D')

s = container.Simulator()
s.add_gate(c0)
s.add_gate(c1)
s.add_gate(divider)
s.add_gate(pgen)

s.simulate(0,8000)

print format_data(sample('CLK0','CLK',s.data, 100))
print format_data(sample('CLK1','CLK',s.data, 100))
print format_data(sample('PDFF0','Q',s.data, 100))
print format_data(sample('PDFF0','/Q',s.data, 100))
