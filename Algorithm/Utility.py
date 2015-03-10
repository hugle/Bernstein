import copy
from itertools import combinations
from FuncDependency import *


def find_minimal_cover(S):
    """
    Compute the minimum cover
    :param S: A set of FDs
    :return: A new FDs that is minimum cover
    """

    if isinstance(S, type(FDList)):
        raise TypeError('The input argument is not FDList type')

    min_cover = FDList()

    # 1. Make sure all FDs are singleton on RHS
    for fd in S.get_fds():
        rhs = fd.right_attributes
        for attr in rhs:
            temp_fd = FD(fd.left_attributes, frozenset([attr]))
            min_cover.add_fd(temp_fd)

    # 2. Remove extraneous LHS attributes
    is_modified = True  # Repeatably check after each modification on the FDs List

    while is_modified:
        is_modified = False

        for fd in min_cover.get_fds():

            if len(fd) > 1:
                combination_size = len(fd) - 1

                while combination_size > 0:
                    lhs = fd.left_attributes
                    fd_attrs = set()
                    fd_attrs.update(fd.left_attributes)
                    fd_attrs.update(fd.right_attributes)

                    for test_attr_set in combinations(lhs, combination_size):
                        X = compute_closure(frozenset(test_attr_set), min_cover)

                        if X >= fd_attrs:
                            # add new fd
                            new_fd = FD(frozenset(test_attr_set), fd.right_attributes)
                            min_cover.add_fd(new_fd)

                            # remove this fd
                            min_cover.remove_fd(fd)

                            # indicate modified, start from beginning
                            is_modified = True
                            break


                    combination_size -= 1

                    if is_modified:
                        break

            if is_modified:
                break

    # 3. Remove redundant FD
    for fd in min_cover.get_fds():
        min_cover_copy = copy.copy(min_cover)
        min_cover_copy.remove_fd(fd)
        X = compute_closure(fd.left_attributes, min_cover_copy)

        if X >= fd.right_attributes:
            # eliminate this fd
            min_cover = min_cover_copy

    return min_cover


def compute_closure(A, S):
    """
    Compute the closure for the input attributes A = {A1, A2, ...}

    :param A: A set of attributes
    :param S: A set of FD's
    :return: The closure of A
    """

    if type(A) is not frozenset:
        raise TypeError('The first argument is not frozenset type')

    if isinstance(S, type(FDList)):
        raise TypeError('The second argument is not FDList type')

    S_copy = copy.copy(S)

    X = set()

    # By reflexivity
    X.update(A)

    while S_copy.size():
        for idx, fd in enumerate(S_copy.get_fds()):
            B = fd.left_attributes
            if X >= B:
                C = fd.right_attributes
                X.update(C)
                S_copy.remove_fd(fd)
                break

            if (idx+1) == S_copy.size():
                return X

    return X
