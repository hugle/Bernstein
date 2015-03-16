import unittest
from Algorithm.Bernstein import *


class TestBernstein(unittest.TestCase):

    def setUp(self):
        pass

    def test_compute_partition(self):
        expected_fds = FDList()
        expected_fds.add_fd(FD(frozenset(['A']), frozenset(['B'])))
        expected_fds.add_fd(FD(frozenset(['B']), frozenset(['C'])))
        expected_fds.add_fd(FD(frozenset(['B']), frozenset(['D'])))
        expected_fds.add_fd(FD(frozenset(['D']), frozenset(['B'])))
        expected_fds.add_fd(FD(frozenset(['A', 'E']), frozenset(['F'])))

        result = Bernstein.partition(expected_fds)

        self.assertEqual(4, len(result))

    def test_merge_key1(self):
        fds1 = FDList()
        fds1.add_fd(FD(frozenset(['A']), frozenset(['B'])))
        fds2 = FDList()
        fds2.add_fd(FD(frozenset(['B']), frozenset(['C'])))
        fds2.add_fd(FD(frozenset(['B']), frozenset(['D'])))
        fds3 = FDList()
        fds3.add_fd(FD(frozenset(['D']), frozenset(['B'])))
        fds4 = FDList()
        fds4.add_fd(FD(frozenset(['A', 'E']), frozenset(['F'])))

        fds_list = [fds1, fds2, fds3, fds4]

        H = FDList()
        H.add_fd(FD(frozenset(['A']), frozenset(['B'])))
        H.add_fd(FD(frozenset(['B']), frozenset(['C'])))
        H.add_fd(FD(frozenset(['B']), frozenset(['D'])))
        H.add_fd(FD(frozenset(['D']), frozenset(['B'])))
        H.add_fd(FD(frozenset(['A', 'E']), frozenset(['F'])))

        result = Bernstein.merge_keys(fds_list, H)

        expected_second_result = FDList()
        expected_second_result.add_fd(FD(frozenset(['B']), frozenset(['C'])))

        result_tuple = result[1]

        self.assertEqual(fds1.__str__(), result[0].__str__())
        self.assertEqual(expected_second_result.__str__(), result_tuple[0].__str__())
        self.assertEqual(fds4.__str__(), result[2].__str__())

    def test_merge_key2(self):
        algo = Bernstein()
        fds = FDList()
        fds.add_fd(FD(frozenset(['X1', 'X2']), frozenset(['A', 'D'])))
        fds.add_fd(FD(frozenset(['C', 'D']), frozenset(['X1', 'X2'])))
        fds.add_fd(FD(frozenset(['A', 'X1']), frozenset(['B'])))
        fds.add_fd(FD(frozenset(['B', 'X2']), frozenset(['C'])))
        fds.add_fd(FD(frozenset(['C']), frozenset(['A'])))

        algo.compute(fds)

        merged_list = algo.get_merged_fd_lists()

        expexted1 = FDList()
        expexted1.add_fd(FD(frozenset(['X1', 'X2']), frozenset(['A'])))
        expexted2 = FDList()
        expexted2.add_fd(FD(frozenset(['A', 'X1']), frozenset(['B'])))
        expexted3 = FDList()
        expexted3.add_fd(FD(frozenset(['B', 'X2']), frozenset(['C'])))
        expexted4 = FDList()
        expexted4.add_fd(FD(frozenset(['C']), frozenset(['A'])))

        result_tuple = merged_list[0]

        self.assertEqual(4, len(merged_list))
        self.assertEqual(expexted1.__str__(), result_tuple[0].__str__())
        self.assertEqual(expexted2.__str__(), merged_list[1].__str__())
        self.assertEqual(expexted3.__str__(), merged_list[2].__str__())
        self.assertEqual(expexted4.__str__(), merged_list[3].__str__())

    def test_eniminate_transitive(self):
        algo = Bernstein()
        fds = FDList()
        fds.add_fd(FD(frozenset(['X1', 'X2']), frozenset(['A', 'D'])))
        fds.add_fd(FD(frozenset(['C', 'D']), frozenset(['X1', 'X2'])))
        fds.add_fd(FD(frozenset(['A', 'X1']), frozenset(['B'])))
        fds.add_fd(FD(frozenset(['B', 'X2']), frozenset(['C'])))
        fds.add_fd(FD(frozenset(['C']), frozenset(['A'])))

        algo.compute(fds)

        final = algo.get_final_fds_lists()

        expexted1 = FDList()
        expexted1.add_fd(FD(frozenset(['X1', 'X2']), frozenset(['C'])))
        expexted1.add_fd(FD(frozenset(['X1', 'X2']), frozenset(['D'])))
        expexted1.add_fd(FD(frozenset(['C', 'D']), frozenset(['X2'])))
        expexted1.add_fd(FD(frozenset(['C', 'D']), frozenset(['X1'])))
        expexted2 = FDList()
        expexted2.add_fd(FD(frozenset(['A', 'X1']), frozenset(['B'])))
        expexted3 = FDList()
        expexted3.add_fd(FD(frozenset(['B', 'X2']), frozenset(['C'])))
        expexted4 = FDList()
        expexted4.add_fd(FD(frozenset(['C']), frozenset(['A'])))

        self.assertEqual(4, len(final))
        self.assertEqual(expexted1.__str__(), final[0].__str__())
        self.assertEqual(expexted2.__str__(), final[1].__str__())
        self.assertEqual(expexted3.__str__(), final[2].__str__())
        self.assertEqual(expexted4.__str__(), final[3].__str__())

    def test_construct_relations(self):
        algo = Bernstein()
        fds = FDList()
        fds.add_fd(FD(frozenset(['X1', 'X2']), frozenset(['A', 'D'])))
        fds.add_fd(FD(frozenset(['C', 'D']), frozenset(['X1', 'X2'])))
        fds.add_fd(FD(frozenset(['A', 'X1']), frozenset(['B'])))
        fds.add_fd(FD(frozenset(['B', 'X2']), frozenset(['C'])))
        fds.add_fd(FD(frozenset(['C']), frozenset(['A'])))

        algo.compute(fds)

        relations = algo.get_relations()

        Bernstein.print_relations(relations)

        self.assertEqual(4, len(relations))

    def test_construct_relations_2(self):
        algo = Bernstein()
        fds = FDList()
        fds.add_fd(FD(frozenset(['A', 'B']), frozenset(['C', 'D'])))
        fds.add_fd(FD(frozenset(['A']), frozenset(['C', 'D'])))

        algo.compute(fds)

        relations = algo.get_relations()

        Bernstein.print_relations(relations)

        self.assertEqual(1, len(relations))

    def test_build_lossy_table(self):
        algo = Bernstein()
        fds = FDList()
        fds.add_fd(FD(frozenset(['X1', 'X2']), frozenset(['A', 'D'])))
        fds.add_fd(FD(frozenset(['C', 'D']), frozenset(['X1', 'X2'])))
        fds.add_fd(FD(frozenset(['A', 'X1']), frozenset(['B'])))
        fds.add_fd(FD(frozenset(['B', 'X2']), frozenset(['C'])))
        fds.add_fd(FD(frozenset(['C']), frozenset(['A'])))

        algo.compute(fds)

        attr, table = algo.build_lossy_table(algo.get_relations(), fds)

        print algo.print_lossy_table(attr, table)

    def test_build_lossy_table_2(self):
        algo = Bernstein()
        fds = FDList()
        fds.add_fd(FD(frozenset(['A', 'B']), frozenset(['C', 'D'])))
        fds.add_fd(FD(frozenset(['A']), frozenset(['C', 'D'])))

        algo.compute(fds)

        attr, table = algo.build_lossy_table(algo.get_relations(), fds)

        print algo.print_lossy_table(attr, table)
