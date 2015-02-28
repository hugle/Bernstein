import unittest

from Algorithm.FuncDependency import *


class TestFuncDependency(unittest.TestCase):

    def setUp(self):
        pass

    @unittest.expectedFailure
    def test_null_left(self):
        fd = FD([], ['A', 'B'])

    @unittest.expectedFailure
    def test_null_null_right(self):
        fd = FD(['A', 'B'], [])

    @unittest.expectedFailure
    def test_not_str_type_LHS(self):
        fd = FD([1, 'A'], ['B'])

    @unittest.expectedFailure
    def test_not_str_type_RHS(self):
        fd = FD(['A'], [2, 'B'])

    @unittest.expectedFailure
    def test_attribute_contain_space_LHS(self):
        fd = FD(['A', 'Student B'], ['B'])

    @unittest.expectedFailure
    def test_attribute_contain_space_RHS(self):
        fd = FD(['A', 'B'], ['Student C', 'B'])

    @unittest.expectedFailure
    def test_attribute_contain_hyphen_LHS(self):
        fd = FD(['A', 'Student-B'], ['B'])

    @unittest.expectedFailure
    def test_attribute_contain_hyphen_RHS(self):
        fd = FD(['A', 'B'], ['Student-C', 'B'])

    @unittest.expectedFailure
    def test_attribute_contain_gl_LHS(self):
        fd = FD(['A', 'Student>B'], ['B'])

    @unittest.expectedFailure
    def test_attribute_contain_gl_RHS(self):
        fd = FD(['A', 'B'], ['Student>C', 'B'])

    def test_get_right_attributes(self):
        fd = FD(['A', 'B'], ['C'])
        self.assertEqual(['C'], fd.right_attributes)

    def test_get_left_attributes(self):
        fd = FD(['A', 'B'], ['C'])
        self.assertEqual(['A', 'B'], fd.left_attributes)

    def test_print_fd_format(self):
        fd = FD(['A', 'B'], ['C'])
        expected_msg = 'Functional Dependency : A B  ->  C '
        self.assertEqual(expected_msg, fd.__str__())

    def test_get_fds(self):
        fds = FDList()
        fd1 = FD(['A', 'B'], ['C'])
        fd2 = FD(['A', 'D'], ['E'])
        fds.add_fd(fd1)
        fds.add_fd(fd2)

        self.assertTrue(type(fds.get_fds()) is list)

    def test_get_fds_size(self):
        fds = FDList()
        fd1 = FD(['A', 'B'], ['C'])
        fd2 = FD(['A', 'D'], ['E'])
        fds.add_fd(fd1)
        fds.add_fd(fd2)

        self.assertEqual(2, fds.size())

    def test_print_fds(self):
        fds = FDList()
        fd1 = FD(['A', 'B'], ['C'])
        fd2 = FD(['A', 'D'], ['E'])
        fds.add_fd(fd1)
        fds.add_fd(fd2)

        expected_msg = '1 : Functional Dependency : A B  ->  C \n' \
                       '2 : Functional Dependency : A D  ->  E \n'

        self.assertEqual(expected_msg, fds.__str__())
