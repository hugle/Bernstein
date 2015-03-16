from tabulate import tabulate

from Utility import *
from FuncDependency import *


class Bernstein(object):

    def __init__(self):
        """
        Constructor
        """
        self.G = None   # the original fds
        self.H = None
        self.partitioned_fds_list = None
        self.merged_fds_list = None
        self.final_fds_list = None
        self.relations = None

    def compute(self, G):
        """
        Compute the bernstein algorithm
        :param G: The input functinoal dependencies
        :return: None
        """
        self.G = G
        self.H = find_minimal_cover(self.G)
        self.partitioned_fds_list = self.partition(self.H)
        self.merged_fds_list = self.merge_keys(self.partitioned_fds_list, self.H)
        self.final_fds_list = self.eliminate_transitive_fds(self.merged_fds_list, self.H)
        self.relations = self.construct_relations(self.final_fds_list)

    def get_minimum_cover(self):
        return self.H

    def get_partitioned_fd_lists(self):
        return self.partitioned_fds_list

    def get_merged_fd_lists(self):
        return self.merged_fds_list

    def get_final_fds_lists(self):
        return self.final_fds_list

    def get_relations(self):
        return self.relations

    @staticmethod
    def print_relations(relations):
        printable_list = []
        for idx, rel in enumerate(relations):
            rel_name = 'R%d'%idx
            printable_list.append([rel_name, rel['key'], rel['attr']])

        print tabulate(printable_list, ['Relation', 'Keys', 'Attributes'])

    @staticmethod
    def partition(fds):
        """
        Partition the input functional dependencies list
        :param fds: The input functional dependencies
        :return: The partitioned functional dependency list
        """
        if not isinstance(fds, FDList):
            raise Exception('The input argument is not FDList')

        fds_copy = deepcopy(fds)
        fds_remain = deepcopy(fds)  # Remaining fds
        fds_list = []

        while fds_remain.size():
            H = FDList()
            current_left_side = fds_remain.get_fds()[0].left_attributes
            for fd in fds_copy.get_fds():
                if fd.left_attributes == current_left_side:
                    H.add_fd(fd)
                    fds_remain.remove_fd(fd)
            fds_list.append(H)

        return fds_list

    @staticmethod
    def merge_keys(fds_list, H):
        """
        Merge equivalent keys
        :param fds_list: Functional dependencies
        :param H: The minimum cover
        :return: A merged fds list
        """
        new_fds_list = []
        fds_list_copy = deepcopy(fds_list)
        while len(fds_list_copy):
            found = False
            # get left common attribute
            left_attribute = fds_list_copy[0].get_fds()[0].left_attributes
            check_fds = fds_list_copy[0]
            fds_list_copy.remove(fds_list_copy[0])   # Remove X
            # compute closure
            closure_X = compute_closure(left_attribute, H)

            J = FDList()    # Store bijection
            for fds in fds_list_copy:
                check_left = fds.get_fds()[0].left_attributes
                if check_left <= closure_X:
                    closure_Y = compute_closure(check_left, H)
                    if closure_X == closure_Y:
                        # satisfy to merge
                        for y in check_left:
                            fd = FD(left_attribute, frozenset([y]))
                            J.add_fd(fd)

                        for x in left_attribute:
                            fd = FD(check_left, frozenset([x]))
                            J.add_fd(fd)

                        # merge (merged fds, J)
                        new_fds_list.append((check_fds + fds - J, J))
                        fds_list_copy.remove(fds)   # remove Y
                        found = True
                        break

            if not found:
                new_fds_list.append(check_fds)

        return new_fds_list

    @staticmethod
    def eliminate_transitive_fds(fds_list, H):
        """
        Eliminate transitive fds by checking each groups of
        functional dependencies H_i
        Check when the group is tuple (fds, J), which contains
        J
        :param fds_list: The input fds groups
        :param H: The minimum cover
        :return: The new fds groups by adding J to corresponding group
        """
        new_fds_lists = []
        for idx, item in enumerate(fds_list):
            if type(item) is tuple:
                # Do checking transitive
                check_fds = item[0]
                check_fds_copy = deepcopy(item[0])
                for fd in check_fds.get_fds():
                    left_closure = compute_closure(fd.left_attributes, H)
                    if fd.right_attributes <= left_closure:
                        # found transitive fd
                        check_fds_copy.remove_fd(fd)

                # merge J to this fds
                for fd in item[1].get_fds():
                    check_fds_copy.add_fd(fd)

                new_fds_lists.append(check_fds_copy)
            else:
                new_fds_lists.append(item)

        return new_fds_lists

    @staticmethod
    def construct_relations(fds_lists):
        """
        Construct relations for each group
        :param fds_lists: The fds groups
        :return: The list of relations(set)
        """
        relations = []
        for fds in fds_lists:
            if not isinstance(fds, FDList):
                raise Exception('Not all fds lists are FDList type')

            rel = {'key': [], 'attr': set()}
            for fd in fds.get_fds():
                if not fd.left_attributes in rel['key']:
                    rel['key'].append(fd.left_attributes)

                rel['attr'].update(fd.right_attributes)

            for key in rel['key']:
                rel['attr'] = rel['attr'] - key

            relations.append(rel)

        return relations

    @staticmethod
    def check_lossy(relations, G):
        """

        :param relations:
        :param G:
        :return: the resulting table and flag which indicate yes or no
        """

        return False

