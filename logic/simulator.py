import string

def format_bits(bits):
    bstr = ''.join([str(x) for x in bits])
    return bstr.replace('0','_').replace('1','-')

def format_record(full_record,gatefilter=None):
    gates = list(full_record.keys())
    gates.sort()
    for gate in gates:
        if gatefilter and gate in gatefilter:
            print "##",gate,"##"
            for pin in full_record[gate]:
                print pin.ljust(5), format_bits(full_record[gate][pin])


class Simulator(object):
    def __init__(self):
        self.nodes = list()
        self.frame = 0

    def add_node(self, node):
        self.nodes.append(node)

    def run(self,frames=1):
        while frames > 0:
            frames = frames - 1
            self.frame = self.frame + 1
            for node in self.nodes:
                node.timeslice(self.frame)


class TSMixin(object):
    def __init__(self, samplerate=1):
        self.recorded_output = dict()
        self.samplerate = samplerate
        self.samplesleft = self.samplerate

    def add_node(self, node):
        Simulator.add_node(self, node)
        self.recorded_output[node.name] = dict()
        for i in node.output_ports:
            self.recorded_output[node.name][i] = list()

    def reset(self):
        for i in self.recorded_output.keys():
            for j in self.recorded_output[i].keys():
                self.recorded_output[i][j] = list()

    def run(self, frames=1, count=1):
        while (count):
            Simulator.run(self, frames)
            self.samplesleft -= 1
            if (self.samplesleft <= 0):
                for node in self.nodes:
                    for port in node.output_ports:
                        self.recorded_output[node.name][port].append(node.out_port_states[port])
                self.samplesleft = self.samplerate
            count = count - 1

class TestSimulator(Simulator):
    def __init__(self):
        Simulator.__init__(self)
        self.recorded_output = dict()

    def add_node(self, node):
        Simulator.add_node(self, node)
        self.recorded_output[node.name] = dict()
        for i in node.output_ports:
            self.recorded_output[node.name][i] = list()


    def run(self, frames=1, count=1):
        while (count):
            Simulator.run(self, frames)
            for node in self.nodes:
                for port in node.output_ports:
                    self.recorded_output[node.name][port].append(node.out_port_states[port])
            count = count - 1

