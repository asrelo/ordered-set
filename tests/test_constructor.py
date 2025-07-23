import enum

import pytest

from ordered_set import orderedfrozenset, orderedset

from .helpers import are_all_elements_unique
from .helpers.ordered_set_ import (
    check_orderedset_invariants,
    parametrize_ordered_set_types,
)


DATA_NUMS_1_TUPLE = (1, 2, 5, 4, 3)
assert are_all_elements_unique(DATA_NUMS_1_TUPLE)


def build_data_nums_1_list():
    return list(DATA_NUMS_1_TUPLE)


def build_data_nums_1_orderedfrozenset():
    return orderedfrozenset(DATA_NUMS_1_TUPLE)


def build_data_nums_1_orderedset():
    return orderedset(DATA_NUMS_1_TUPLE)


DATA_INPUT_NUMS_2_TUPLE = (1, 2, 3, -2, 1, 4, 5, 4)


def build_data_input_nums_2_list():
    return list(DATA_INPUT_NUMS_2_TUPLE)


DATA_INPUT_NUMS_3_TUPLE = (-1,) * 10


def build_data_input_nums_3_list():
    return list(DATA_INPUT_NUMS_3_TUPLE)


_DATA_NUMS_4_SET = {1, 5, 22, -303, 444}
DATA_NUMS_4_FROZENSET = frozenset(_DATA_NUMS_4_SET)


def build_data_nums_4_set():
    return set(_DATA_NUMS_4_SET)


_DATA_NUMS_5_DICT = {1: 'a', 5: 'e', 22: 'v', -303: 'kp', 444: 'qb'}


def build_data_nums_5_dict():
    return _DATA_NUMS_5_DICT.copy()


def build_data_nums_5_keys_view():
    return build_data_nums_5_dict().keys()


DATA_INPUT_STR_1 = 'abdcef'
assert are_all_elements_unique(DATA_INPUT_STR_1)


DATA_INPUT_STR_2 = 'abracadabra'


@parametrize_ordered_set_types('class_')
def test_init_empty(class_):
    obj = class_()
    check_orderedset_invariants(obj)


class TestInitCollection:

    class DataKey(enum.Enum):
        NUMS_1_TUPLE    = enum.auto()
        NUMS_1_LIST = enum.auto()
        NUMS_1_ORDEREDFROZENSET = enum.auto()
        NUMS_1_ORDEREDSET   = enum.auto()
        INPUT_NUMS_2_TUPLE  = enum.auto()
        INPUT_NUMS_2_LIST   = enum.auto()
        INPUT_NUMS_3_TUPLE  = enum.auto()
        INPUT_NUMS_3_LIST   = enum.auto()
        NUMS_4_SET  = enum.auto()
        NUMS_4_FROZENSET    = enum.auto()
        NUMS_5_DICT = enum.auto()
        NUMS_5_KEYS_VIEW    = enum.auto()
        STR_1   = enum.auto()
        INPUT_STR_2 = enum.auto()

    KEYED_DATA = {
        DataKey.NUMS_1_TUPLE:   DATA_NUMS_1_TUPLE,
        DataKey.NUMS_1_LIST:    build_data_nums_1_list,
        DataKey.NUMS_1_ORDEREDFROZENSET:    build_data_nums_1_orderedfrozenset,
        DataKey.NUMS_1_ORDEREDSET:  build_data_nums_1_orderedset,
        DataKey.INPUT_NUMS_2_TUPLE: DATA_INPUT_NUMS_2_TUPLE,
        DataKey.INPUT_NUMS_2_LIST:  build_data_input_nums_2_list,
        DataKey.INPUT_NUMS_3_TUPLE: DATA_INPUT_NUMS_3_TUPLE,
        DataKey.INPUT_NUMS_3_LIST:  build_data_input_nums_3_list,
        DataKey.NUMS_4_SET: build_data_nums_4_set,
        DataKey.NUMS_4_FROZENSET:   DATA_NUMS_4_FROZENSET,
        DataKey.NUMS_5_DICT:    build_data_nums_5_dict,
        DataKey.NUMS_5_KEYS_VIEW:   build_data_nums_5_keys_view,
        DataKey.STR_1:  DATA_INPUT_STR_1,
        DataKey.INPUT_STR_2:    DATA_INPUT_STR_2,
    }

    @pytest.mark.parametrize(
        'universal_indirection_simple',
        KEYED_DATA.values(),
        ids=KEYED_DATA.keys(),
        indirect=True,
    )
    @parametrize_ordered_set_types('class_')
    @staticmethod
    def test_init(universal_indirection_simple, class_):
        obj = class_(universal_indirection_simple)
        check_orderedset_invariants(obj)


class TestInitCollectionUnique:

    class DataKey(enum.Enum):
        NUMS_1_TUPLE    = enum.auto()
        NUMS_1_LIST = enum.auto()
        NUMS_1_ORDEREDFROZENSET = enum.auto()
        NUMS_1_ORDEREDSET   = enum.auto()
        NUMS_4_SET  = enum.auto()
        NUMS_4_FROZENSET    = enum.auto()
        NUMS_5_DICT = enum.auto()
        NUMS_5_KEYS_VIEW    = enum.auto()
        STR_1   = enum.auto()

    KEYED_DATA = {
        DataKey.NUMS_1_TUPLE:   DATA_NUMS_1_TUPLE,
        DataKey.NUMS_1_LIST:    build_data_nums_1_list,
        DataKey.NUMS_1_ORDEREDFROZENSET:    build_data_nums_1_orderedfrozenset,
        DataKey.NUMS_1_ORDEREDSET:  build_data_nums_1_orderedset,
        DataKey.NUMS_4_SET: build_data_nums_4_set,
        DataKey.NUMS_4_FROZENSET:   DATA_NUMS_4_FROZENSET,
        DataKey.NUMS_5_DICT:    build_data_nums_5_dict,
        DataKey.NUMS_5_KEYS_VIEW:   build_data_nums_5_keys_view,
        DataKey.STR_1:  DATA_INPUT_STR_1,
    }

    @pytest.mark.parametrize(
        'universal_indirection_simple',
        KEYED_DATA.values(),
        ids=KEYED_DATA.keys(),
        indirect=True,
    )
    @parametrize_ordered_set_types('class_')
    @staticmethod
    def test_init_from_unique(universal_indirection_simple, class_):
        obj = class_.from_unique(universal_indirection_simple)
        check_orderedset_invariants(obj)


class TestInitIterator:

    class DataKey(enum.Enum):
        NUMS_1_TUPLE    = enum.auto()
        INPUT_NUMS_2_TUPLE  = enum.auto()

    KEYED_DATA = {
        DataKey.NUMS_1_TUPLE:   DATA_NUMS_1_TUPLE,
        DataKey.INPUT_NUMS_2_TUPLE: DATA_INPUT_NUMS_2_TUPLE,
    }

    @pytest.mark.parametrize(
        'universal_indirection_simple',
        KEYED_DATA.values(),
        ids=KEYED_DATA.keys(),
        indirect=True,
    )
    @parametrize_ordered_set_types('class_')
    @staticmethod
    def test_smth(universal_indirection_simple, class_):
        data_it = iter(universal_indirection_simple)
        obj = class_(data_it)
        check_orderedset_invariants(obj)
