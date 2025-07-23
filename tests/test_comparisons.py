import dataclasses
import itertools
from operator import eq, ne

import pytest

from ordered_set import orderedfrozenset, orderedset

from .helpers import BUILTIN_SET_TYPES
from .helpers.ordered_set_ import ORDERED_SET_TYPES, parametrize_ordered_set_types


def assert_comparison_op_value(op, a, b, res, *, both_directions=True):
    assert op(a, b) == res
    if both_directions:
        assert op(b, a) == res


def assert_comparison_method_by_name_value(
    method_name, a, b, res, *, both_directions=True,
):
    assert getattr(a, method_name)(b) == res
    if both_directions:
        assert getattr(b, method_name)(a) == res


class TestOrderedSetEquality:

    DATA_FOR_TEST_ORDERED_SET = (
        ((),    ()),
        ((1, 2, 3), (1, 2, 3)),
        ((1, 2, 3), (3, 2, 1)),
        ((1, 2, 3), (1, 2)),
    )

    @pytest.mark.parametrize(('data_a', 'data_b'), DATA_FOR_TEST_ORDERED_SET)
    @parametrize_ordered_set_types('class_b')
    @parametrize_ordered_set_types('class_a')
    @staticmethod
    def test_smth(class_a, class_b, data_a, data_b):
        assert type(data_a) is type(data_b)
        are_equal = (data_a == data_b)
        obj_a = class_a.from_unique(data_a)
        obj_b = class_b.from_unique(data_b)
        assert_comparison_op_value(eq, obj_a, obj_b, are_equal)
        assert_comparison_op_value(ne, obj_a, obj_b, not are_equal)


@dataclasses.dataclass(frozen=True, kw_only=True)
class BuiltinSetsComparisonResults:
    equal:  bool
    subset: bool
    superset:   bool
    disjoint:   bool


def compare_builtin_sets(a, b, /):
    return BuiltinSetsComparisonResults(
        equal=(a == b),
        subset=a.issubset(b),
        superset=a.issuperset(b),
        disjoint=a.isdisjoint(b),
    )


class TestSetComparisons:

    DATA_FOR_TEST_SETS = (
        (frozenset(),   frozenset()),
        (frozenset(),   frozenset({1, 2})),
        (frozenset({1, 2}),  frozenset()),
        (frozenset({1, 2, 3}),  frozenset({1, 2, 3})),
        (frozenset({1, 2}), frozenset({1, 2, 3})),
        (frozenset({1, 2, 3}),  frozenset({2, 3})),
        (frozenset({1, 2}), frozenset({3, 4})),
        (frozenset({1, 2}), frozenset({2, 3})),
    )

    @parametrize_ordered_set_types('obj_class')
    @pytest.mark.parametrize('data_class', BUILTIN_SET_TYPES)
    @pytest.mark.parametrize(('data_a', 'data_b'), DATA_FOR_TEST_SETS)
    @staticmethod
    def test_sets_ops(data_a, data_b, data_class, obj_class):
        obj = obj_class(data_a)
        if not isinstance(data_a, BUILTIN_SET_TYPES):
            data_a = frozenset(data_a)
        if not isinstance(data_b, data_class):
            data_b = data_class(data_b)
        comparison_res = compare_builtin_sets(data_a, data_b)
        assert_comparison_op_value(eq, obj, data_b, comparison_res.equal)
        assert_comparison_op_value(ne, obj, data_b, not comparison_res.equal)
        assert (obj <= data_b)  == comparison_res.subset
        assert (data_b >= obj)  == comparison_res.subset
        assert (obj < data_b)   == (
            comparison_res.subset and (not comparison_res.equal)
        )
        assert (data_b > obj)   == (
            comparison_res.subset and (not comparison_res.equal)
        )
        assert (obj >= data_b)  == comparison_res.superset
        assert (data_b <= obj)  == comparison_res.superset
        assert (obj > data_b)   == (
            comparison_res.superset and (not comparison_res.equal)
        )
        assert (data_b < obj)   == (
            comparison_res.superset and (not comparison_res.equal)
        )

    @pytest.mark.parametrize(
        ('data_class', 'obj_class'), tuple((cls, cls) for cls in ORDERED_SET_TYPES),
    )
    @pytest.mark.parametrize(('data_a', 'data_b'), DATA_FOR_TEST_SETS)
    @staticmethod
    def test_ordered_sets_methods(data_a, data_b, data_class, obj_class):
        obj = obj_class(data_a)
        if not isinstance(data_a, BUILTIN_SET_TYPES):
            data_a = frozenset(data_a)
        if not isinstance(data_b, data_class):
            data_b = data_class(data_b)
        comparison_res = compare_builtin_sets(data_a, data_b)
        assert (obj.is_set_equal(data_b))   == comparison_res.equal
        assert (obj.is_set_not_equal(data_b))   == (not comparison_res.equal)
        assert (obj.is_subset(data_b))  == comparison_res.subset
        assert (data_b.is_superset(obj))    == comparison_res.subset
        assert (obj.is_strict_subset(data_b))   == (
            comparison_res.subset and (not comparison_res.equal)
        )
        assert (data_b.is_strict_superset(obj)) == (
            comparison_res.subset and (not comparison_res.equal)
        )
        assert (obj.is_superset(data_b))    == comparison_res.superset
        assert (data_b.is_subset(obj))  == comparison_res.superset
        assert (obj.is_strict_superset(data_b)) == (
            comparison_res.superset and (not comparison_res.equal)
        )
        assert (data_b.is_strict_subset(obj))   == (
            comparison_res.superset and (not comparison_res.equal)
        )
        assert (obj.is_disjoint(data_b))    == comparison_res.disjoint
        assert (obj.isdisjoint(data_b)) == comparison_res.disjoint
        assert (data_b.is_disjoint(obj))    == comparison_res.disjoint
        assert (data_b.isdisjoint(obj)) == comparison_res.disjoint

    @pytest.mark.parametrize(
        ('data_class', 'obj_class'),
        tuple(itertools.product(BUILTIN_SET_TYPES, ORDERED_SET_TYPES)),
    )
    @pytest.mark.parametrize(('data_a', 'data_b'), DATA_FOR_TEST_SETS)
    @staticmethod
    def test_sets_methods(data_a, data_b, data_class, obj_class):
        obj = obj_class(data_a)
        if not isinstance(data_a, BUILTIN_SET_TYPES):
            data_a = frozenset(data_a)
        if not isinstance(data_b, data_class):
            data_b = data_class(data_b)
        comparison_res = compare_builtin_sets(data_a, data_b)
        assert (obj.is_set_equal(data_b))   == comparison_res.equal
        assert (obj.is_set_not_equal(data_b))   == (not comparison_res.equal)
        assert (obj.is_subset(data_b))  == comparison_res.subset
        assert (data_b.issuperset(obj)) == comparison_res.subset
        assert (obj.is_strict_subset(data_b))   == (
            comparison_res.subset and (not comparison_res.equal)
        )
        assert (obj.is_superset(data_b))    == comparison_res.superset
        assert (data_b.issubset(obj))   == comparison_res.superset
        assert (obj.is_strict_superset(data_b)) == (
            comparison_res.superset and (not comparison_res.equal)
        )
        assert (obj.is_disjoint(data_b))    == comparison_res.disjoint
        assert (obj.isdisjoint(data_b)) == comparison_res.disjoint
        assert (data_b.isdisjoint(obj)) == comparison_res.disjoint


@dataclasses.dataclass(frozen=True, kw_only=True)
class BuiltinSequencesComparisonResults:
    equal:  bool
    follows:    bool

    @property
    def precedes(self):
        return (not (self.equal or self.follows))

    @classmethod
    def create(cls, **kwargs):
        try:
            precedes = kwargs.pop('precedes')
        except KeyError:
            pass
        else:
            if precedes:
                kwargs.setdefault('follows', False)
                kwargs.setdefault('equal', False)
                if not (
                    kwargs.get('follows', False)
                    and (not kwargs.get('equal', False))
                ):
                    raise ValueError(
                        f'Conflicting arguments about precedes: **{kwargs!r}'
                    )
        return cls(**kwargs)


def compare_builtin_sequences(a, b, /):
    return BuiltinSequencesComparisonResults(
        equal=(a == b),
        follows=(a > b),
    )


class TestSequenceComparisons:

    DATA_FOR_TEST_SEQUENCES = (
        ((),    ()),
        ((),    (1, 2)),
        ((1, 2),    ()),
        ((1, 2, 3), (1, 2, 3)),
        ((1, 2),    (1, 4)),
        ((1, 4),    (1, 2)),
        ((2, 3),    (3, 0)),
        ((3, 0),    (2, 3)),
        ((5, 0),    (5, 0, 3)),
        ((5, 0, 3), (5, 0)),
    )

    @pytest.mark.parametrize(
        ('data_class', 'obj_class'),
        (
            (tuple, orderedfrozenset),
            (list, orderedset),
            *tuple((cls, cls) for cls in ORDERED_SET_TYPES),
        ),
    )
    @pytest.mark.parametrize(('data_a', 'data_b'), DATA_FOR_TEST_SEQUENCES)
    @staticmethod
    def test_sequences_ops(data_a, data_b, data_class, obj_class):
        obj = obj_class.from_unique(data_a)
        if not isinstance(data_a, data_class):
            data_a = data_class(data_a)
        if not isinstance(data_b, data_class):
            data_b = data_class(data_b)
        comparison_res = compare_builtin_sequences(data_a, data_b)
        assert_comparison_op_value(eq, obj, data_b, comparison_res.equal)
        assert_comparison_op_value(ne, obj, data_b, not comparison_res.equal)
        assert (obj <= data_b)  == (comparison_res.equal or comparison_res.precedes)
        assert (data_b >= obj)  == (comparison_res.equal or comparison_res.precedes)
        assert (obj < data_b)   == comparison_res.precedes
        assert (data_b > obj)   == comparison_res.precedes
        assert (obj >= data_b)  == (comparison_res.equal or comparison_res.follows)
        assert (data_b <= obj)  == (comparison_res.equal or comparison_res.follows)
        assert (obj > data_b)   == comparison_res.follows
        assert (data_b < obj)   == comparison_res.follows
