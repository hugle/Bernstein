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

    def test_compute_minimum_cover(self):
        fds = FDList()
        fds.add_fd(FD(frozenset(['A']), frozenset(['D'])))
        fds.add_fd(FD(frozenset(['B', 'C']), frozenset(['A', 'D'])))
        fds.add_fd(FD(frozenset(['C']), frozenset(['B'])))
        fds.add_fd(FD(frozenset(['E']), frozenset(['A'])))
        fds.add_fd(FD(frozenset(['E']), frozenset(['D'])))

        min_cover = find_minimal_cover(fds)

        expected_fds = FDList()
        expected_fds.add_fd(FD(frozenset(['A']), frozenset(['D'])))
        expected_fds.add_fd(FD(frozenset(['C']), frozenset(['B'])))
        expected_fds.add_fd(FD(frozenset(['E']), frozenset(['A'])))
        expected_fds.add_fd(FD(frozenset(['C']), frozenset(['A'])))

        self.assertEqual(expected_fds.__str__(), min_cover.__str__())
