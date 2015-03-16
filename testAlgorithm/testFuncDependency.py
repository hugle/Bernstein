import unittest

from Algorithm.FuncDependency import *


class TestFuncDependency(unittest.TestCase):

    def setUp(self):
        pass

    @unittest.expectedFailure
    def test_null_left(self):
        fd = FD(frozenset([]), frozenset(['A', 'B']))

    @unittest.expectedFailure
    def test_null_null_right(self):
        fd = FD(frozenset(['A', 'B']), frozenset([]))

    @unittest.expectedFailure
    def test_not_str_type_LHS(self):
        fd = FD(frozenset([1, 'A']), frozenset(['B']))

    @unittest.expectedFailure
    def test_not_str_type_RHS(self):
        fd = FD(frozenset(['A']), frozenset([2, 'B']))

    @unittest.expectedFailure
    def test_attribute_contain_space_LHS(self):
        fd = FD(frozenset(['A', 'Student B']), frozenset(['B']))

    @unittest.expectedFailure
    def test_attribute_contain_space_RHS(self):
        fd = FD(frozenset(['A', 'B']), frozenset(['Student C', 'B']))

    @unittest.expectedFailure
    def test_attribute_contain_hyphen_LHS(self):
        fd = FD(frozenset(['A', 'Student-B']), frozenset(['B']))

    @unittest.expectedFailure
    def test_attribute_contain_hyphen_RHS(self):
        fd = FD(frozenset(['A', 'B']), frozenset(['Student-C', 'B']))

    @unittest.expectedFailure
    def test_attribute_contain_gl_LHS(self):
        fd = FD(frozenset(['A', 'Student>B']), frozenset(['B']))

    @unittest.expectedFailure
    def test_attribute_contain_gl_RHS(self):
        fd = FD(frozenset(['A', 'B']), frozenset(['Student>C', 'B']))

    def test_get_right_attributes(self):
        fd = FD(frozenset(['A', 'B']), frozenset(['C']))
        self.assertTrue(frozenset(['C']) >= fd.right_attributes)

    def test_get_left_attributes(self):
        fd = FD(frozenset(['A', 'B']), frozenset(['C']))
        self.assertTrue(frozenset(['A', 'B']) >= fd.left_attributes)

    def test_print_fd_format(self):
        fd = FD(frozenset(['A', 'B']), frozenset(['C']))
        expected_msg = 'Functional Dependency : A B  ->  C '
        self.assertEqual(expected_msg, fd.__str__())

    def test_get_fds(self):
        fds = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fds.add_fd(fd1)
        fds.add_fd(fd2)

        self.assertTrue(type(fds.get_fds()) is list)

    def test_get_fds_size(self):
        fds = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fds.add_fd(fd1)
        fds.add_fd(fd2)

        self.assertEqual(2, fds.size())

    def test_print_fds(self):
        fds = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fds.add_fd(fd1)
        fds.add_fd(fd2)

        expected_msg = '1 : Functional Dependency : A B  ->  C \n' \
                       '2 : Functional Dependency : A D  ->  E \n'

        self.assertEqual(expected_msg, fds.__str__())

    def test_get_attributes_set(self):
        fds = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fds.add_fd(fd1)
        fds.add_fd(fd2)

        self.assertTrue(frozenset(['A', 'B', 'C', 'D', 'E']) >= fds.get_attributes_set())

    def test_failed_get_attributes_set(self):
        fds = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fds.add_fd(fd1)
        fds.add_fd(fd2)

        self.assertFalse(frozenset(['A', 'B', 'D', 'E']) >= fds.get_attributes_set())

    def test_remove_fd(self):
        fds = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fds.add_fd(fd1)
        fds.add_fd(fd2)

        fds.remove_fd(fd1)

        self.assertEqual(1, fds.size())

    @unittest.expectedFailure
    def test_remove_fd_not_exist(self):
        fds = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fd3 = FD(frozenset(['A', 'D']), frozenset(['K']))
        fds.add_fd(fd1)
        fds.add_fd(fd2)

        fds.remove_fd(fd3)

    @unittest.expectedFailure
    def test_modify_LHS(self):
        # namedtuple is immutable
        fd = FD(frozenset(['A', 'B']), frozenset(['C']))
        fd.left_attributes = frozenset(['A'])
        self.assertEqual(frozenset(['A']), fd.left_attributes)


    @unittest.expectedFailure
    def test_subtract_failed(self):
        fds1 = FDList()
        fds2 = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fds1.add_fd(fd1)
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fd3 = FD(frozenset(['A', 'D']), frozenset(['K']))
        fds2.add_fd(fd2)
        fds2.add_fd(fd3)

        result = fds1 - fd2
        return result

    @unittest.expectedFailure
    def test_add_failed(self):
        fds1 = FDList()
        fds2 = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fds1.add_fd(fd1)
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fd3 = FD(frozenset(['A', 'D']), frozenset(['K']))
        fds2.add_fd(fd2)
        fds2.add_fd(fd3)

        result = fds1 + fd2
        return result

    def test_add(self):
        fds1 = FDList()
        fds2 = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fds1.add_fd(fd1)
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fd3 = FD(frozenset(['A', 'D']), frozenset(['K']))
        fd4 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fds2.add_fd(fd2)
        fds2.add_fd(fd3)
        fds2.add_fd(fd4)

        expected = FDList()
        expected.add_fd(fd1)
        expected.add_fd(fd2)
        expected.add_fd(fd3)

        result = fds1 + fds2

        self.assertEqual(expected.__str__(), result.__str__())

    def test_subtract(self):
        fds1 = FDList()
        fds2 = FDList()
        fd1 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fd2 = FD(frozenset(['A', 'D']), frozenset(['E']))
        fds1.add_fd(fd1)
        fds1.add_fd(fd2)
        fd3 = FD(frozenset(['A', 'D']), frozenset(['K']))
        fd4 = FD(frozenset(['A', 'B']), frozenset(['C']))
        fds2.add_fd(fd3)
        fds2.add_fd(fd4)

        expected = FDList()
        expected.add_fd(fd2)

        result = fds1 - fds2

        self.assertEqual(expected.__str__(), result.__str__())
