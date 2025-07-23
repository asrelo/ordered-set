from .helpers.ordered_set_ import parametrize_ordered_set_types
from .helpers.pickle_ import pickle_roundtrip


@parametrize_ordered_set_types('class_')
def test_pickle_empty(class_):
    obj = class_()
    assert pickle_roundtrip(obj) == obj


@parametrize_ordered_set_types('class_')
def test_pickle(class_):
    obj = class_('abracadabra')
    assert pickle_roundtrip(obj) == obj
