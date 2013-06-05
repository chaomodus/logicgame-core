from simulator import Simulator
import datetime

# milliseconds = (c.days * 24 * 60 * 60 + c.seconds) * 1000 + c.microseconds / 1000.0

class RTSimulator(Simulator):
    def __init__(self, fps=30):
        Simulator.__init__(self)
        self.lasttime = 0
        self.fps = fps
        self.perframe = (1.0 / fps) * 1000
        self.lasttime = datetime.datetime.now()

    def slice(self):
        now = datetime.datetime.now()
        framediff = now - self.lasttime
        ms = (framediff.days * 24 * 60 * 60 + framediff.seconds) * 1000 + framediff.microseconds / 1000.0

        if (ms >= self.perframe):
            self.lasttime = now
            self.run(1)


