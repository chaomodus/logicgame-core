import gate
import simulator
import clock

a = gate.AND()
b = gate.OR()

c = clock.Clock(period=5)
c1 = clock.Clock(period=5,state=1)

n = gate.NOT()
n1 = gate.NOT()
n2 = gate.NOT()
n3 = gate.NOT()
n4 = gate.NOT()
n5 = gate.NOT()
n6 = gate.NOT()
n.connectOutput('OUT',n1,'IN')
n1.connectOutput('OUT',n2,'IN')
n2.connectOutput('OUT',n3,'IN')
n3.connectOutput('OUT',n4,'IN')
n4.connectOutput('OUT',n5,'IN')
n5.connectOutput('OUT',n6,'IN')
c.connectOutput('CLK',n,'IN')

n4.connectOutput('OUT',a,'A')
c.connectOutput('CLK',a,'B')
n4.connectOutput('OUT',b,'A')
c.connectOutput('CLK',b,'B')

mysim = simulator.TestSimulator()
mysim.addNode(a)
mysim.addNode(b)
mysim.addNode(c)
mysim.addNode(c1)
mysim.addNode(n)
mysim.addNode(n1)
mysim.addNode(n2)
mysim.addNode(n3)
mysim.addNode(n4)
mysim.addNode(n5)
mysim.addNode(n6)
mysim.run(1,150)
print simulator.formatRecord(mysim.recordedOutput,gatefilter=(c.name,c1.name,a.name,b.name))
