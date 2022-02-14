import time


class Time:
    def __init__(self, name=None):
        self.name = name
        self.time_start = time.time()

    def elapsed(self):
        return time.time() - self.time_start
