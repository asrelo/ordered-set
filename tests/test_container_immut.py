import itertools

import pytest

from ordered_set import orderedfrozenset

from .helpers import (
    iterable_as_immut_builtin_sequence,
    fixture_params_product,
    product_parametrize_ids,
)
from .helpers.ordered_set_ import (
    ORDERED_SET_TYPES,
    parametrize_ordered_set_types,
    ordered_set_type_parametrize_id,
)


class TestContainer:

    DATA = 'abracadabra'

    @pytest.fixture(scope='class', params=tuple(ORDERED_SET_TYPES))
    @classmethod
    def object_(cls, request):
        return request.param(cls.DATA)

    @pytest.mark.parametrize('element', ('a', 'r', 'c'))
    @staticmethod
    def test_present(object_, element):
        assert element in object_

    @pytest.mark.parametrize('element', ('z',))
    @staticmethod
    def test_absent(object_, element):
        assert element not in object_


def test_frozen_hashable_empty():
    obj = orderedfrozenset()
    _ = hash(obj)


def test_frozen_hashable():
    obj = orderedfrozenset((1, 3, 2, 2))
    _ = hash(obj)


@parametrize_ordered_set_types('class_')
def test_iterable_empty(class_):
    obj = class_()
    assert tuple(obj) == ()


@parametrize_ordered_set_types('class_')
def test_iterable(class_):
    data = (1, 2, 5, 4, 3)
    obj = class_.from_unique(data)
    assert tuple(obj) == data


@parametrize_ordered_set_types('class_')
def test_sized_empty(class_):
    obj_empty = class_()
    assert len(obj_empty) == 0


@parametrize_ordered_set_types('class_')
def test_sized(class_):
    data = (1, 2, 5, 4, 3)
    obj = class_.from_unique(data)
    assert len(obj) == len(data)


@parametrize_ordered_set_types('class_')
def test_bool_empty(class_):
    obj_empty = class_()
    assert not bool(obj_empty)


@parametrize_ordered_set_types('class_')
def test_bool(class_):
    data = (1, 3, 2, 2)
    obj = class_(data)
    assert bool(obj)


@parametrize_ordered_set_types('class_')
def test_reversible(class_):
    data = (1, 2, 5, 4, 3)
    data_rev = tuple(reversed(data))
    obj = class_.from_unique(data)
    assert tuple(reversed(obj)) == data_rev


def smth_test_indexing_object_function_base(data, request):
    return request.param.from_unique(data)


# XXX: ?
# Designed to create a fixture from an optionally parametrized fixture
# function.
def fixture_test_indexing_object(
    name='object_', *, scope='function', params=None, autouse=False, ids=None,
):
    # Writing it with a single `product` for all cases is unreasonably
    # complex.
    params_class = tuple(ORDERED_SET_TYPES)
    params = (
        fixture_params_product(params, params_class)
        if params is not None
        else list(params_class)
    )
    if ids is not None:
        ids_class = (
            ordered_set_type_parametrize_id
            if callable(ids)
            else tuple(map(ordered_set_type_parametrize_id, params_class))
        )
        ids = product_parametrize_ids(ids, ids_class)
    return pytest.fixture(
        scope=scope, params=params, autouse=autouse, ids=ids, name=name,
    )


def smth_test_indexing_add_fixtures(*, data_attr, object_scope_class=True):
    data_getattr = lambda cls: getattr(cls, data_attr)  # noqa: E731

    def wrapper(cls):
        cls.object_ = classmethod(
            fixture_test_indexing_object(
                scope=('class' if object_scope_class else 'function')
            )(
                lambda cls, request: (
                    smth_test_indexing_object_function_base(data_getattr(cls), request)
                )
            )
        )
        return cls

    return wrapper


@smth_test_indexing_add_fixtures(data_attr='DATA')
class TestIndexingSingle:

    DATA = (1, 2, 5, 4, 3)

    @pytest.mark.parametrize('idx', (0, 2, (len(DATA) - 1), -len(DATA), -2, -1))
    @classmethod
    def test_smth(cls, object_, idx):
        assert object_[idx] == cls.DATA[idx]

    @pytest.mark.parametrize('idx', (len(DATA), (-len(DATA) - 1)))
    @staticmethod
    def test_oob(object_, idx):
        with pytest.raises(IndexError):
            _ = object_[idx]


@smth_test_indexing_add_fixtures(data_attr='DATA')
class TestIndexingSlice:

    DATA = (1, 2, 3, 7, 6, 5, 4)

    @pytest.mark.parametrize(
        'slice_',
        (
            slice(None, None),
            slice(2, 5),
            slice(-3, None),
            slice(None, -2),
            slice(-4, -1),
            slice(None, None, 2),
            slice(None, None, -1),
            slice((len(DATA) * 2), None),
            slice(None, -(len(DATA) * 2)),
            slice(2, (len(DATA) * 2)),
            slice(-(len(DATA) * 2), -3),
            slice(5, 2),
            slice(2, 5, -1),
        ),
    )
    @classmethod
    def test_values(cls, object_, slice_):
        sliced = object_[slice_]
        assert isinstance(sliced, type(object_))
        assert tuple(sliced) == cls.DATA[slice_]


def smth_test_index_data_as_builtin_function_base(data):
    return iterable_as_immut_builtin_sequence(data)


# XXX: ?
def fixture_test_index_data_as_builtin(
    name='data_as_builtin', *, scope='function', params=None, autouse=False, ids=None,
):
    return pytest.fixture(
        scope=scope, params=params, autouse=autouse, ids=ids, name=name,
    )


def smth_test_index_add_fixtures(
    *, data_attr, data_as_builtin_scope_class=True, **kwargs,
):
    data_getattr = lambda cls: getattr(cls, data_attr)  # noqa: E731

    def wrapper(cls):
        cls = smth_test_indexing_add_fixtures(data_attr=data_attr, **kwargs)(cls)
        cls.data_as_builtin = classmethod(
            fixture_test_index_data_as_builtin(
                scope=('class' if data_as_builtin_scope_class else 'function')
            )(
                lambda cls, request: smth_test_index_data_as_builtin_function_base(
                    data_getattr(cls)
                )
            )
        )
        return cls

    return wrapper


@smth_test_index_add_fixtures(data_attr='DATA')
class TestIndex:

    DATA = (1, 2, 5, 4, 3)

    @pytest.mark.parametrize('val', (1, 5, 3))
    @classmethod
    def test_present(cls, object_, val):
        assert object_.index(val) == cls.DATA.index(val)

    @pytest.mark.parametrize('val', (0, 8))
    @staticmethod
    def test_absent(object_, val):
        with pytest.raises(ValueError):  # noqa: PT011
            _ = object_.index(val)

    @pytest.mark.parametrize(
        ('val', 'range_'),
        (
            (1, (0, 2)),
            (2, (0, -2)),
            (3, (2, None)),
            (4, (2, 4)),
            (5, (2, -2)),
            (3, (-3, None)),
            (5, (-3, 3)),
            (4, (-3, -1)),
        ),
    )
    @classmethod
    def test_present_in_range(cls, data_as_builtin, object_, val, range_):
        start, stop = range_
        index_extra_args = []
        if start is not None:
            index_extra_args.append(start)
        if stop is not None:
            index_extra_args.append(stop)
        assert (
            object_.index(val, *index_extra_args)
            == data_as_builtin.index(val, *index_extra_args)
        )

    @pytest.mark.parametrize(
        ('val', 'range_'),
        tuple(zip(
            itertools.repeat(8),
            (
                (0, 2),
                (0, -2),
                (2, None),
                (2, 4),
                (2, -2),
                (-3, None),
                (-3, 3),
                (-3, -1),
            ),
        )),
    )
    @classmethod
    def test_absent_in_range(cls, object_, val, range_):
        start, stop = range_
        index_extra_args = []
        if start is not None:
            index_extra_args.append(start)
        if stop is not None:
            index_extra_args.append(stop)
        with pytest.raises(ValueError):  # noqa: PT011
            _ = object_.index(val, *index_extra_args)

    @pytest.mark.parametrize(
        ('val', 'range_'),
        (
            (5, (0, 2)),
            (3, (0, -2)),
            (1, (2, None)),
            (1, (2, 4)),
            (1, (2, -2)),
            (2, (-3, None)),
            (4, (-3, 3)),
            (2, (-3, -1)),
        ),
    )
    @classmethod
    def test_present_but_absent_in_range(cls, object_, val, range_):
        start, stop = range_
        index_extra_args = []
        if start is not None:
            index_extra_args.append(start)
        if stop is not None:
            index_extra_args.append(stop)
        with pytest.raises(ValueError):  # noqa: PT011
            _ = object_.index(val, *index_extra_args)


@smth_test_indexing_add_fixtures(data_attr='DATA')
class TestCount:

    DATA = (1, 2, 5, 4, 3)

    @pytest.mark.parametrize('val', (1, 5, 3))
    @staticmethod
    def test_present(object_, val):
        assert val in object_
        assert object_.count(val) == 1

    @pytest.mark.parametrize('val', (0, 8))
    @staticmethod
    def test_absent(object_, val):
        assert val not in object_
        assert object_.count(val) == 0
