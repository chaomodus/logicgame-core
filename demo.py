import logic.clock as clock
import logic.gate as gate
import logic.container as container
import logic.base as base
import sys

not_clock=container.Package(name='NOTCLK')
not_clock.add_pin('OUT',base.PIN_DIRECTION_OUT)
n1 = base.NOT()
n2 = base.NOT()
n3 = base.NOT()
n1.connect_pin('OUT',n2,'IN')
n2.connect_pin('OUT',n3,'IN')
n3.connect_pin('OUT',n1,'IN')
not_clock.add_gate(n1)
not_clock.add_gate(n2)
not_clock.add_gate(n3)
not_clock.connect_pin_internal_output('OUT',n2, 'OUT')

c0 = clock.Clock(16)
c1 = clock.Clock(2)
a = gate.AND(2)


c0.connect_pin('CLK',a,'IN0')
c1.connect_pin('CLK',a,'IN1')

s = container.Simulator()
s.add_gate(c0)
s.add_gate(c1)
s.add_gate(a)
s.add_gate(not_clock)

s.simulate(0,80)

for i in s.data:
    if i[1]['AND0']['OUT']:
        sys.stdout.write('-')
    else:
        sys.stdout.write('_')

sys.stdout.write('\n')

for i in s.data:
    if i[1]['CLK0']['CLK']:
        sys.stdout.write('-')
    else:
        sys.stdout.write('_')

sys.stdout.write('\n')

for i in s.data:
    if i[1]['CLK1']['CLK']:
        sys.stdout.write('-')
    else:
        sys.stdout.write('_')

sys.stdout.write('\n')

for i in s.data:
    if i[1]['NOTCLK']['OUT']:
        sys.stdout.write('-')
    else:
        sys.stdout.write('_')

sys.stdout.write('\n')
