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

    def test_compute_minimum_cover2(self):
        fds = FDList()
        fds.add_fd(FD(frozenset(['A']), frozenset(['B'])))
        fds.add_fd(FD(frozenset(['A']), frozenset(['C'])))
        fds.add_fd(FD(frozenset(['B']), frozenset(['C'])))
        fds.add_fd(FD(frozenset(['B']), frozenset(['D'])))
        fds.add_fd(FD(frozenset(['D']), frozenset(['B'])))
        fds.add_fd(FD(frozenset(['A', 'B', 'E']), frozenset(['F'])))
        fds.add_fd(FD(frozenset(['A', 'E']), frozenset(['D'])))

        min_cover = find_minimal_cover(fds)

        expected_fds = FDList()
        expected_fds.add_fd(FD(frozenset(['A']), frozenset(['B'])))
        expected_fds.add_fd(FD(frozenset(['B']), frozenset(['C'])))
        expected_fds.add_fd(FD(frozenset(['B']), frozenset(['D'])))
        expected_fds.add_fd(FD(frozenset(['D']), frozenset(['B'])))
        expected_fds.add_fd(FD(frozenset(['A', 'E']), frozenset(['F'])))

        self.assertEqual(expected_fds.__str__(), min_cover.__str__())

    def test_compute_min_cover_3(self):
        fds = FDList()
        fds.add_fd(FD(frozenset(['A', 'D']), frozenset(['B'])))
        fds.add_fd(FD(frozenset(['B']), frozenset(['C'])))
        fds.add_fd(FD(frozenset(['C']), frozenset(['D'])))
        fds.add_fd(FD(frozenset(['A', 'B']), frozenset(['E'])))
        fds.add_fd(FD(frozenset(['A', 'C']), frozenset(['F'])))
        fds.add_fd(FD(frozenset(['A', 'D']), frozenset(['F'])))
        fds.add_fd(FD(frozenset(['A', 'C']), frozenset(['E'])))

        min_cover = find_minimal_cover(fds)

        print min_cover

    def test_get_attribute_set(self):
        fds = FDList()
        fds.add_fd(FD(frozenset(['A']), frozenset(['B'])))
        fds.add_fd(FD(frozenset(['A']), frozenset(['C'])))
        fds.add_fd(FD(frozenset(['B']), frozenset(['C'])))
        fds.add_fd(FD(frozenset(['B']), frozenset(['D'])))
        fds.add_fd(FD(frozenset(['D']), frozenset(['B'])))
        fds.add_fd(FD(frozenset(['A', 'B', 'E']), frozenset(['F'])))
        fds.add_fd(FD(frozenset(['A', 'E']), frozenset(['D'])))

        attributes = get_fds_attributes(fds)
        self.assertEqual(set(['A', 'B', 'C', 'D', 'E', 'F']), attributes)

    @unittest.expectedFailure
    def test_get_attribute_set_wrong_type(self):
        attributes = get_fds_attributes([])
        return attributes

    def test_get_all_attributes_in_relation(self):
        relation = {'key': [frozenset(['X2', 'X1']), frozenset(['C', 'D'])], 'attr': set(['B'])}
        self.assertEqual(set(['X2', 'X1', 'C', 'D', 'B']), get_all_attributes_in_relation(relation))

    def test_superfluous_attribute_detection_algorithm(self):
        relation1 = {'key': [frozenset(['X1']), frozenset(['C', 'D'])], 'attr': set(['B'])}
        relation2 = {'key': [frozenset(['C', 'D'])], 'attr': set(['B', 'X1'])}
        self.assertEqual(10, len(get_all_keys_in_relation(relation1)))
        self.assertEqual(4, len(get_all_keys_in_relation(relation2)))

