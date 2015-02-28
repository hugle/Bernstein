import unittest

from Algorithm.Utility import *


class TestFuncDependency(unittest.TestCase):

    def setUp(self):
        pass

    def test_compute_closure(self):
        fds = FDList()
        fd1 = FD(frozenset(['A']), frozenset(['C']))
        fd2 = FD(frozenset(['A']), frozenset(['B']))
        fd3 = FD(frozenset(['B', 'C']), frozenset(['D']))
        fd4 = FD(frozenset(['C', 'D']), frozenset(['E']))
        fds.add_fd(fd1)
        fds.add_fd(fd2)
        fds.add_fd(fd3)
        fds.add_fd(fd4)

        A = frozenset(['A'])

        X = compute_closure(A, fds)

        self.assertTrue(frozenset(['A', 'B', 'C', 'D', 'E']) >= X)

    def test_compute_closure(self):
        fds = FDList()
        fd1 = FD(frozenset(['A']), frozenset(['C']))
        fd2 = FD(frozenset(['A']), frozenset(['B']))
        fd3 = FD(frozenset(['B', 'C']), frozenset(['A']))
        fd4 = FD(frozenset(['D']), frozenset(['E']))
        fds.add_fd(fd1)
        fds.add_fd(fd2)
        fds.add_fd(fd3)
        fds.add_fd(fd4)

        A = frozenset(['A'])

        X = compute_closure(A, fds)

        self.assertTrue(frozenset(['A', 'B', 'C']) >= X)

    def test_compute_closure_failure(self):
        fds = FDList()
        fd1 = FD(frozenset(['C']), frozenset(['B']))
        fd2 = FD(frozenset(['B', 'C']), frozenset(['D']))
        fd3 = FD(frozenset(['D']), frozenset(['E']))
        fd4 = FD(frozenset(['A']), frozenset(['C']))
        fds.add_fd(fd1)
        fds.add_fd(fd2)
        fds.add_fd(fd3)
        fds.add_fd(fd4)

        A = frozenset(['A'])

        X = compute_closure(A, fds)

        self.assertFalse(frozenset(['A', 'B', 'C']) >= X)
        self.assertTrue(frozenset(['A', 'B', 'C', 'D', 'E']) >= X)


