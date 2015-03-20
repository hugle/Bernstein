from tabulate import tabulate

from Utility import *
from FuncDependency import *


class Bernstein(object):

    def __init__(self):
        """
        Constructor
        """
        self.__G = None   # the original fds
        self.__H = None
        self.__partitioned_fds_list = None
        self.__merged_fds_list = None
        self.__final_fds_list = None
        self.__relations = None
        self.__pnp_table = None
        self.__all_keys = None

    def compute(self, G):
        """
        Compute the bernstein algorithm
        :param G: The input functinoal dependencies
        :return: None
        """
        self.__G = G
        self.__H = find_minimal_cover(self.__G)
        self.__partitioned_fds_list = self.partition(self.__H)
        self.__merged_fds_list = self.merge_keys(self.__partitioned_fds_list, self.__H)
        self.__final_fds_list = self.eliminate_transitive_fds(self.__merged_fds_list)
        self.__relations = self.construct_relations(self.__final_fds_list)
        self.__pnp_table = self.find_p_np_table(self.__G)
        self.__all_keys = self.find_all_keys_based_on_prime_table(self.__pnp_table, self.__G)

    def get_minimum_cover(self):
        return self.__H

    def get_partitioned_fd_lists(self):
        return self.__partitioned_fds_list

    def get_merged_fd_lists(self):
        return self.__merged_fds_list

    def get_final_fds_lists(self):
        return self.__final_fds_list

    def get_relations(self):
        return self.__relations

    def get_p_np_table(self):
        return self.__pnp_table

    def get_all_keys(self):
        return self.__all_keys

    @staticmethod
    def check_print_lossy_table(attributes, table):
        """
        Print lossy table
        :param table: The row list
        :param attributes: The full attributes list
        :return: True is it is lossless
        """
        column_names = ['Schema'] + attributes
        printable_list = []

        for row in table:
            printable_row = []
            printable_row.append(row[0])
            check_row = row[1]
            for a in attributes:
                printable_row.append(check_row[a])
            printable_list.append(printable_row)

        information = tabulate(printable_list, column_names)

        lossless = False
        for row in table:
            check_row = row[1]

            valid = True
            for a in attributes:
                if not check_row[a]:
                    valid = False
                    break
            if valid:
                lossless = True
                break

        return lossless, information

    @staticmethod
    def get_print_relations_info(relations):
        printable_list = []
        for idx, rel in enumerate(relations):
            rel_name = 'R%d'%idx
            printable_list.append([rel_name, rel['key'], rel['attr']])

        info = tabulate(printable_list, ['Relation', 'Keys', 'Attributes'])
        return info

    @staticmethod
    def get_print_n_np_table_info(table):
        """
        Print the table for computing prime and non-prime
        :param table: The dict contains key 'Left', 'Middle', 'Right'
        :return: None
        """
        if not isinstance(table, dict):
            raise Exception('The input table is not dict')

        column_names = ['Left', 'Middle', 'Right']
        printable_list = [table['Left'], table['Middle'], table['Right']]
        info = tabulate([printable_list], column_names)
        return info

    @staticmethod
    def get_print_all_keys_info(keys):
        info = tabulate(keys)
        return info

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
        new_fds_group = []
        fds_list_copy = deepcopy(fds_list)
        while len(fds_list_copy):
            found = False
            # get left common attribute
            left_attribute = fds_list_copy[0].get_fds()[0].left_attributes
            # The fds that is being checking
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
                        new_fds_group.append((check_fds + fds - J, J))
                        fds_list_copy.remove(fds)   # remove Y
                        found = True
                        break

            if not found:
                new_fds_group.append(check_fds)

        return new_fds_group

    @staticmethod
    def eliminate_transitive_fds(fds_list):
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
        removed_fd = FDList()
        for idx, item in enumerate(fds_list):
            if type(item) is tuple:
                # Do checking transitive
                check_fds = item[0]
                check_fds_copy = deepcopy(item[0])
                J = item[1].get_fds()
                for fd in check_fds.get_fds():
                    # construct new H
                    new_H = get_all_fds_from_merged_fds_list(fds_list)
                    for f in removed_fd.get_fds():
                        new_H.remove_fd(f)
                    new_H.remove_fd(fd) # remove this testing fd
                    # construct new H end

                    left_closure = compute_closure(fd.left_attributes, new_H)
                    if fd.right_attributes <= left_closure:
                        # Check whether C -> A, if found, not transitive fd
                        found = False
                        for f in new_H.get_fds():
                            temp_left = f.left_attributes
                            if temp_left <= left_closure - fd.right_attributes - fd.left_attributes:
                                test_closure = compute_closure(temp_left, new_H)
                                # core checking transitive definition
                                if (not fd.left_attributes <= test_closure) and test_closure >= fd.right_attributes:
                                    found = True
                                    break

                        if found:
                            # found transitive fd
                            removed_fd.add_fd(fd)
                            check_fds_copy.remove_fd(fd)
                    else:
                        # the fd can't be removed
                        continue

                # merge J to this fds
                for fd in J:
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
    def build_lossy_table(relations, G):
        """

        :param relations:
        :param G:
        :return: the resulting table and flag which indicate yes or no
        """
        all_attr = list(get_fds_attributes(G))
        table = []

        for rel in relations:
            key_list = rel['key']
            attr_set = rel['attr']
            rel_attr = set()
            rel_attr.update(attr_set)
            for key in key_list:
                rel_attr.update(key)

            check_row = {}
            for attr in all_attr:
                check_row[attr] = False

            for attr in rel_attr:
                check_row[attr] = True

            table.append((list(rel_attr), check_row))

        for fd in G.get_fds():
            left = fd.left_attributes
            right = fd.right_attributes
            for row in table:
                check_row = row[1]
                valid = True   # check update condition satisfied
                for a in left:
                    if not check_row[a]:
                        valid = False

                if valid:
                    for a in right:
                        check_row[a] = True

        return all_attr, table

    @staticmethod
    def find_p_np_table(fds):
        """
        Find Prime and None-Prime table
        :param fds: The input functional dependencies
        :return: The resulting table
        """
        table = {'Left': [], 'Middle': [], 'Right': []}
        attributes = get_fds_attributes(fds)
        for attr in attributes:
            exist_left = False
            exist_right = False
            for fd in fds.get_fds():
                if set([attr]) <= fd.left_attributes:
                    exist_left = True
                if set([attr]) <= fd.right_attributes:
                    exist_right = True

                if exist_left and exist_right:
                    break

            if exist_left and not exist_right:
                table['Left'].append(attr)
            elif not exist_left and exist_right:
                table['Right'].append(attr)
            elif exist_left and exist_right:
                table['Middle'].append(attr)

        return table

    @staticmethod
    def find_all_keys_based_on_prime_table(p_np_table, G):
        """
        Find all keys, but not including superkeys
        :param p_np_table: The left, middle and right table
        :param G: The original dependencies
        :return: Set of keys including explicit and hidden
        """
        if not isinstance(p_np_table, dict):
            raise Exception('The input p_np_table is not dict')

        if not isinstance(G, FDList):
            raise Exception('The input G is not a instance of FDList')

        all_keys = []

        left_list = p_np_table['Left']
        middle_list = p_np_table['Middle']

        # Get full set of attributes in fds
        A = get_fds_attributes(G)

        # For left side
        left_size = len(left_list)
        combination_size = 0
        while combination_size <= left_size:
            combination_size += 1
            for s in combinations(left_list, combination_size):
                found_key = [key for key in all_keys if key <= frozenset(s)]
                if len(found_key) == 0:
                    s_closure = compute_closure(frozenset(s), G)
                    if s_closure == A and frozenset(s) not in all_keys:
                        all_keys.append(frozenset(s))
                else:
                    continue

        # For middle attributes with fixed left attributes
        middle_size = len(middle_list)
        combination_size = 0
        while combination_size <= middle_size:
            combination_size += 1
            for s in combinations(middle_list, combination_size):
                com_s = list(s) + left_list
                found_key = [key for key in all_keys if key <= frozenset(com_s)]
                if len(found_key) == 0:
                    s_closure = compute_closure(frozenset(com_s), G)
                    if s_closure == A and frozenset(com_s) not in all_keys:
                        all_keys.append(frozenset(com_s))
                else:
                    continue

        return all_keys

    @staticmethod
    def superfluous_attribute_detection_algorithm(relations, G, test_relation, test_attribute):

        if not isinstance(test_relation, dict):
            raise Exception('test_relation is not dict')

        if not isinstance(test_attribute, set):
            raise Exception('test_attribute is not set')

        if len(test_attribute) != 1:
            raise Exception('test_attribute must have only one attribute')

        if not isinstance(relations, list):
            raise Exception('relations must be a list')

        if not isinstance(G, FDList):
            raise Exception('G must be a instance of FDList')

        isSuperfluous = True

        # compute attribute set in test_relation
        A = get_all_attributes_in_relation(test_relation)

        # test attribute must in test relation
        if not test_attribute <= A:
            raise Exception('test_attribute must be subset of test_relation')

        # whether test_attribute is superfluous in test_relation
        # Step 1
        all_keys = get_all_keys_in_relation(test_relation)

        Ki_prime = deepcopy(all_keys)

        for key in all_keys:
            if test_attribute <= key:
                Ki_prime.remove(key)

        # Step 1.1
        Gi_prime = FDList()

        # construct test relation(k -> A - k - test_attribute)
        test_relation_keys = test_relation['key']

        for k in test_relation_keys:
            Gi_prime.add_fd(FD(k, frozenset(A - k - test_attribute)))

        for rel in relations:
            if rel is not test_relation:
                A_i = get_all_attributes_in_relation(rel)
                for k in rel['key']:
                    Gi_prime.add_fd(FD(k, frozenset(A_i - k)))

        # Step 2
        if len(Ki_prime) == 0:
            print '---------------------------------'
            print test_attribute, ' is not superfluous.'
            print '---------------------------------'
            isSuperfluous = False
            return isSuperfluous
        else:
            go_step3 = False
            for k in Ki_prime:
                k_closure = compute_closure(k, Gi_prime)
                if test_attribute <= k_closure:
                    # go to step3
                    go_step3 = True
                    break
                else:
                    continue

        if not go_step3:
            print '---------------------------------'
            print test_attribute, ' is not superfluous.'
            print '---------------------------------'
            isSuperfluous = False
            return isSuperfluous

        # Step 3
        test_attribute_key_set = [key for key in all_keys if key not in Ki_prime]

        for key in test_attribute_key_set:
            while isSuperfluous:
                key_closure = compute_closure(key, Gi_prime)
                if A <= key_closure:
                    break
                else:
                    # next
                    M = key_closure
                    temp_set = M & A - test_attribute

                    G_plus = compute_closure(temp_set, G)

                    if A <= G_plus:
                        Ki_prime = [key for key in all_keys if key in temp_set and key not in Ki_prime] + Ki_prime
                        print Ki_prime
                    else:
                        isSuperfluous = False

        # output
        if isSuperfluous:
            print '---------------------------------'
            print test_attribute, ' is superfluous.'
            print 'Ki_prime is', Ki_prime
            print '---------------------------------'
            return True
        else:
            print '---------------------------------'
            print test_attribute, ' is not superfluous.'
            print '---------------------------------'
            return False

