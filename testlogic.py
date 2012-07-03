import logic
import logic.gate
import logic.simulator
import logic.clock

a = logic.gate.AND()
b = logic.gate.OR()

c = logic.clock.Clock(period=5)
c1 = logic.clock.Clock(period=5,state=1)

n = logic.gate.NOT()
n1 = logic.gate.NOT()
n2 = logic.gate.NOT()
n3 = logic.gate.NOT()
n4 = logic.gate.NOT()
n5 = logic.gate.NOT()
n6 = logic.gate.NOT()
n.connect_output('OUT',n1,'IN')
n1.connect_output('OUT',n2,'IN')
n2.connect_output('OUT',n3,'IN')
n3.connect_output('OUT',n4,'IN')
n4.connect_output('OUT',n5,'IN')
n5.connect_output('OUT',n6,'IN')
c.connect_output('CLK',n,'IN')

n4.connect_output('OUT',a,'A')
c.connect_output('CLK',a,'B')
n4.connect_output('OUT',b,'A')
c.connect_output('CLK',b,'B')

mysim = logic.simulator.TestSimulator()
mysim.add_node(a)
mysim.add_node(b)
mysim.add_node(c)
mysim.add_node(c1)
mysim.add_node(n)
mysim.add_node(n1)
mysim.add_node(n2)
mysim.add_node(n3)
mysim.add_node(n4)
mysim.add_node(n5)
mysim.add_node(n6)
mysim.run(1,150)
print logic.simulator.format_record(mysim.recorded_output,gatefilter=(c.name,c1.name,a.name,b.name))
