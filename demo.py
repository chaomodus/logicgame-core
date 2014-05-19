import logic.clock as clock
import logic.gate as gate
import logic.container as container
import sys

c0 = clock.Clock(16)
c1 = clock.Clock(2)
a = gate.AND(2)
c0.connect_pin('CLK',a,'IN0')
c1.connect_pin('CLK',a,'IN1')
s = container.Simulator()

s.add_gate(c0)
s.add_gate(c1)
s.add_gate(a)

s.simulate(0,75)

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
