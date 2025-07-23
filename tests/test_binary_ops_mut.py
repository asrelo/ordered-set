import dataclasses

import pytest

from ordered_set import orderedfrozenset, orderedset

from .helpers import BUILTIN_SET_TYPES, fixture_params_product, FixtureRequestMockObj
from .helpers.ordered_set_ import ORDERED_SET_TYPES


@dataclasses.dataclass(frozen=True, kw_only=True)
class SetsBinaryOpsResults:
    and_:   object
    or_:    object
    xor:    object
    sub:    object


def smth_test_ordered_set_ops_object_function_base(data, request):
    return request.param.from_unique(data)


# WARN: The tests assert order of elements in results.
class TestOrderedSetOps:

    DATA_FOR_TEST_ORDERED_SET = (
        ((),    (), SetsBinaryOpsResults(and_=(), or_=(), xor=(), sub=())),
        ((),    (1, 2), SetsBinaryOpsResults(and_=(), or_=(1, 2), xor=(1, 2), sub=())),
        (
            (1, 2),    (),
            SetsBinaryOpsResults(and_=(), or_=(1, 2), xor=(1, 2), sub=(1, 2)),
        ),
        (
            (1, 2, 3), (1, 2, 3),
            SetsBinaryOpsResults(and_=(1, 2, 3), or_=(1, 2, 3), xor=(), sub=()),
        ),
        (
            (1, 2, 3), (3, 2, 1),
            SetsBinaryOpsResults(and_=(1, 2, 3), or_=(3, 2, 1), xor=(), sub=()),
        ),
        (
            (1, 2),    (3, 4),
            SetsBinaryOpsResults(
                and_=(), or_=(1, 2, 3, 4), xor=(1, 2, 3, 4), sub=(1, 2),
            ),
        ),
        (
            (1, 2),    (1, 4),
            SetsBinaryOpsResults(and_=(1,), or_=(2, 1, 4), xor=(2, 4), sub=(2,)),
        ),
        (
            (2, 3),    (3, 0),
            SetsBinaryOpsResults(and_=(3,), or_=(2, 3, 0), xor=(2, 0), sub=(2,)),
        ),
        (
            (1, 2, 3), (3, 1),
            SetsBinaryOpsResults(and_=(1, 3), or_=(2, 3, 1), xor=(2,), sub=(2,)),
        ),
        (
            (3, 1), (1, 2, 3),
            SetsBinaryOpsResults(and_=(3, 1), or_=(1, 2, 3), xor=(2,), sub=()),
        ),
    )

    @pytest.fixture(
        params=fixture_params_product(DATA_FOR_TEST_ORDERED_SET, ORDERED_SET_TYPES),
    )
    @classmethod
    def fixture_objects_pair_and_expected(cls, request):
        data, obj_class = request.param
        assert len(data) == 3
        return (
            smth_test_ordered_set_ops_object_function_base(
                data[0], FixtureRequestMockObj(orderedset),
            ),
            smth_test_ordered_set_ops_object_function_base(
                data[1], FixtureRequestMockObj(obj_class),
            ),
            data[2],
        )

    @staticmethod
    def test_and(fixture_objects_pair_and_expected):
        obj_a, obj_b, expected = fixture_objects_pair_and_expected
        obj_a &= obj_b
        assert obj_a == orderedfrozenset.from_unique(expected.and_)

    @staticmethod
    def test_or(fixture_objects_pair_and_expected):
        obj_a, obj_b, expected = fixture_objects_pair_and_expected
        obj_a |= obj_b
        assert obj_a == orderedfrozenset.from_unique(expected.or_)

    @staticmethod
    def test_xor(fixture_objects_pair_and_expected):
        obj_a, obj_b, expected = fixture_objects_pair_and_expected
        obj_a ^= obj_b
        assert obj_a == orderedfrozenset.from_unique(expected.xor)

    @staticmethod
    def test_sub(fixture_objects_pair_and_expected):
        obj_a, obj_b, expected = fixture_objects_pair_and_expected
        obj_a -= obj_b
        assert obj_a == orderedfrozenset.from_unique(expected.sub)


def smth_test_set_ops_data_pair_function_base(request):
    data_a, data_b, data_class = request.param
    if not isinstance(data_a, BUILTIN_SET_TYPES):
        data_a = frozenset(data_a)
    if not isinstance(data_b, data_class):
        data_b = data_class(data_b)
    return (data_a, data_b)


def smth_test_set_ops_object_function_base(data, request):
    return request.param(data)


class TestSetOps:

    @pytest.fixture(
        params=fixture_params_product(
            (
                (frozenset(),   frozenset()),
                (frozenset(),   frozenset({1, 2})),
                (frozenset({1, 2}),  frozenset()),
                (frozenset({1, 2, 3}),  frozenset({1, 2, 3})),
                (frozenset({1, 2}), frozenset({1, 2, 3})),
                (frozenset({1, 2, 3}),  frozenset({2, 3})),
                (frozenset({1, 2}), frozenset({3, 4})),
                (frozenset({1, 2}), frozenset({2, 3})),
            ),
            BUILTIN_SET_TYPES,
        ),
    )
    @classmethod
    def fixture_data_pair_and_object(cls, request):
        data, data_class = request.param
        assert len(data) == 2
        return (
            *smth_test_set_ops_data_pair_function_base(
                FixtureRequestMockObj((*data, data_class)),
            ),
            smth_test_set_ops_object_function_base(
                data[0], FixtureRequestMockObj(orderedset),
            ),
        )

    @staticmethod
    def test_and(fixture_data_pair_and_object):
        data_a, data_b, obj = fixture_data_pair_and_object
        data_a &= data_b
        obj &= data_b
        assert obj == data_a

    @staticmethod
    def test_or(fixture_data_pair_and_object):
        data_a, data_b, obj = fixture_data_pair_and_object
        data_a |= data_b
        obj |= data_b
        assert obj == data_a

    @staticmethod
    def test_xor(fixture_data_pair_and_object):
        data_a, data_b, obj = fixture_data_pair_and_object
        data_a ^= data_b
        obj ^= data_b
        assert obj == data_a

    @staticmethod
    def test_sub(fixture_data_pair_and_object):
        data_a, data_b, obj = fixture_data_pair_and_object
        data_a -= data_b
        obj -= data_b
        assert obj == data_a
