from collections import namedtuple


class FDList:

    def __init__(self):
        self.FDs = []

    def remove_fd(self, fd):
        """
        Remove a fd object from FDs list
        :param fd: The fd object in self
        """
        if type(fd) is not FD:
            raise "The input type is not FD"

        if fd not in self.FDs:
            raise "The input FD is not in the FDs List"

        self.FDs.remove(fd)

    def add_fd(self, fd):
        """
        Add FD to FD list
        :param fd: The FD object
        """
        if type(fd) is not FD:
            raise "The input type is not FD"

        self.FDs.append(fd)

    def get_fds(self):
        """
        Get all function dependencies
        :return: The FD list
        """
        return self.FDs

    def size(self):
        """
        Get the size of the FD list
        :return: The size
        """
        return len(self.FDs)

    def get_attributes_set(self):
        """
        Get attributes tuple in the FD list
        :return: The attribute tuple
        """
        attributes = set()

        for fd in self.FDs:
            attributes.update(fd.left_attributes)
            attributes.update(fd.right_attributes)

        return frozenset(attributes)

    def __str__(self):
        """
        Print the FD list
        :return: The information need to be printed
        """
        msg = ''
        for idx, fd in enumerate(self.FDs):
            msg += str(idx+1) + ' : ' + fd.__str__() + '\n'

        return msg


class FD(namedtuple('FD', 'left_attributes right_attributes')):

    __slots__ = ()

    def __init__(self, left, right):
        """
        Constructor of functional dependency
        by taking LHS attributes and RHS attributes
        :param left: The left hand side attributes list
        :param right: The right hand side attributes list
        """

        if type(left) is not frozenset:
            raise TypeError('Left attribute is not a list object')

        for x in left:
            if type(x) is not str:
                raise TypeError('The attribute in LHS list is not str')

            if (' ' in x) or ('-' in x) or ('>' in x):
                raise ValueError('Attribute name must not contain space \'-\' or \'>\'')

        if type(right) is not frozenset:
            raise TypeError('Right attribute is not a list object')

        for y in right:
            if type(y) is not str:
                raise TypeError('The attribute in RHS list is not str')

            if (' ' in y) or ('-' in y) or ('>' in y):
                raise ValueError('Attribute name must not contain space \'-\' or \'>\'')

        if len(left) is 0 or len(right) is 0:
            raise IndexError('List must not have empty list')

    def __str__(self):
        msg = 'Functional Dependency : '

        for x in self.left_attributes:
            msg += x + ' '

        msg += ' ->  '

        for y in self.right_attributes:
            msg += y + ' '

        return msg
