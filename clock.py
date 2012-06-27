from base import Node

class Clock(Node):
    nr = 0
    def __init__(self, name='CLK%d', period=1,state=0):
        Node.__init__(self, name)

        self.add_output('CLK')
        self.initperiod = period
        self.period = period
        self.initstate = state
        self.state = None

    def timeslice(self, time):
        timepass = time - self.lastslice
        lastslice = self.lastslice
        Node.timeslice(self, time)

        if self.state is None:
            self.state = self.initstate
            self.send_state_change('CLK', self.state, time)
        else:
            period = self.period
            while (timepass):
                period = period - 1
                timepass = timepass - 1
                if period == 0:
                    self.state = int(not self.state)
                    self.send_state_change('CLK', self.state, lastslice + (time - timepass))
                    period = self.initperiod

            self.period = period

