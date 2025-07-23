from copy import copy, deepcopy

from .helpers.ordered_set_ import parametrize_ordered_set_types


DATA = (1, 2, 3, 8, 4)


def check_ordered_set_shallow_copy(orig, copy_):
    assert copy_ is not orig
    assert set(map(id, copy_)) == set(map(id, orig))
    #assert copy_ == orig


@parametrize_ordered_set_types('class_')
def test_copy_method(class_):
    orig = class_.from_unique(DATA)
    copy_ = orig.copy()
    check_ordered_set_shallow_copy(orig, copy_)


@parametrize_ordered_set_types('class_')
def test_copy_shallow(class_):
    orig = class_.from_unique(DATA)
    copy_ = copy(orig)
    check_ordered_set_shallow_copy(orig, copy_)


# ordered_set types only operate on Hashable values, which are supposed
# to be immutable; for immutable object (at least for built-in objects),
# deepcopy may return the same object.
@parametrize_ordered_set_types('class_')
def test_copy_deep(class_):
    orig = class_.from_unique(DATA)
    copy_ = deepcopy(orig)
    assert copy_ is not orig
