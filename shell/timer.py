# from http://www.huyng.com/posts/python-performance-analysis/
import time

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.secs = 0
        self.start = 0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        print '\n:: (command executed in %f ms)' % self.msecs

    def start_timer(self):
        self.start = time.time()

    def tick(self):
        self.secs = time.time() - self.start

