import copy
from FuncDependency import *

def find_minimal_cover(FDs):
    min_cover = []
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
