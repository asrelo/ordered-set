import pytest

from ordered_set import orderedfrozenset, orderedset


ORDERED_SET_TYPES = (orderedfrozenset, orderedset)


def check_orderedset_invariants(obj):
    obj._check()


def parametrize_ordered_set_types(argname):
    return pytest.mark.parametrize(argname, tuple(ORDERED_SET_TYPES))


def ordered_set_type_parametrize_id(class_):
    return class_.__name__
