import string

def formatBits(bits):
    bstr = ''.join([str(x) for x in bits])
    return bstr.replace('0','_').replace('1','-')

def formatRecord(fullRecord,gatefilter=None):
    gates = list(fullRecord.keys())
    gates.sort()
    for gate in gates:
        if gatefilter and gate in gatefilter:
            print "##",gate,"##"
            for pin in fullRecord[gate]:
                print pin.ljust(5), formatBits(fullRecord[gate][pin])
    

class Simulator(object):
    def __init__(self):
        self.nodes = list()
        self.frame = 0
    
    def addNode(self, node):
        self.nodes.append(node)
        
    def run(self,frames=1):
        while frames > 0:
            frames = frames - 1
            self.frame = self.frame + 1
            for node in self.nodes:
                node.timeslice(self.frame)


class TestSimulator(Simulator):
    def __init__(self):
        Simulator.__init__(self)
        self.recordedOutput = dict()

    def addNode(self, node):
        Simulator.addNode(self, node)
        self.recordedOutput[node.name] = dict()
        for i in node.outputPorts:
            self.recordedOutput[node.name][i] = list()
        

    def run(self, frames=1, count=1):
        while (count):
            Simulator.run(self, frames)
            for node in self.nodes:
                for port in node.outputPorts:
                    self.recordedOutput[node.name][port].append(node.outPortStates[port])
            count = count - 1

