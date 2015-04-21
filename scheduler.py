from threading import Thread
import time

class scheduler(Thread):
    def __init__(self, interval, closure, arg=None):
        super(scheduler, self).__init__()
        self.interval = interval
        self.closure = closure
        self.arg = arg

    def run(self):
        while(True):
            if self.arg is None:
                self.closure()
            else:
                self.closure(self.arg)
            time.sleep(self.interval)

