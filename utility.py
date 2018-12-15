
from Queue import PriorityQueue

pq = PriorityQueue()


class Node(object):
    def __init__(self, level=None, path=None, bound=None):
        self.level = level
        self.path = path
        self.bound = bound

    def __cmp__(self, other):
        return cmp(self.bound, other.bound)

    def __str__(self):
        return str(tuple([self.level, self.path, self.bound]))

