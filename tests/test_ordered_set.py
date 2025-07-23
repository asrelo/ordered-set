import pytest

from ordered_set import orderedfrozenset, orderedset

from .helpers.ordered_set_ import parametrize_ordered_set_types


@pytest.mark.parametrize(
    ('input_', 'result'),
    (
        ((), ()),
        ('abdc', 'abdc'),
        ('abracadabra', 'cdbra'),
        (((1, 'b'), (3, 'a'), (2, 'c')), ((1, 'b'), (3, 'a'), (2, 'c'))),
    ),
)
@parametrize_ordered_set_types('class_')
def test_order_after_init(class_, input_, result):
    obj = class_(input_)
    if not isinstance(result, tuple):
        result = tuple(result)
    assert tuple(obj) == result


@pytest.mark.parametrize(
    ('input_', 'result'),
    (
        ((), ()),
        ((2, 1), (2, 1)),
        ('abdc', 'abdc'),
    ),
)
@parametrize_ordered_set_types('class_')
def test_order_after_init_from_unique(class_, input_, result):
    obj = class_.from_unique(input_)
    if not isinstance(result, tuple):
        result = tuple(result)
    assert tuple(obj) == result


@pytest.mark.parametrize('input_', ((1, 1), (1, 2, 4, 2, 5),))
@parametrize_ordered_set_types('class_')
def test_order_init_from_unique_with_duplicates(class_, input_):
    with pytest.raises(ValueError):  # noqa: PT011
        _ = class_.from_unique(input_)


@pytest.mark.parametrize(
    'input_', ((), 'abdc', 'abracadabra', ((1, 'b'), (3, 'a'), (2, 'c'))),
)
@parametrize_ordered_set_types('class_')
def test_repr_no_error(class_, input_):
    _ = repr(class_(input_))


@parametrize_ordered_set_types('class_')
def test_binary_ops_immut_maintain_order(class_):
    os1 = orderedfrozenset((1, 2, 3, 4))
    os2 = orderedfrozenset((3, 4, 5, 6))
    assert tuple(os1 & os2) == (3, 4)
    assert tuple(os1 | os2) == (1, 2, 3, 4, 5, 6)
    assert tuple(os1 ^ os2) == (1, 2, 5, 6)
    assert tuple(os1 - os2) == (1, 2)


def test_workflow_with_mixed_operations():
    raw_data = ['apple', 'banana', 'apple', 'cherry', 'banana', 'date']
    processed = orderedset(raw_data)
    additional_items = ['elderberry', 'apple', 'fig']
    for item in additional_items:
        processed.uppend(item)
    to_remove = list(filter(lambda s: s.startswith('a'), processed))
    for item in to_remove:
        processed.discard(item)
    assert list(processed) == ['cherry', 'banana', 'date', 'elderberry', 'fig']


@parametrize_ordered_set_types('class_')
def test_indexing_and_slicing(class_):
    data = ('x', 'y', 'z', 'a', 'b', 'c')
    os = class_.from_unique(data)
    assert os[0] == 'x'
    assert os[-1] == 'c'
    assert os[2] == 'z'
    assert tuple(os[1:4]) == ('y', 'z', 'a')
    assert tuple(os[::2]) == ('x', 'z', 'b')
    assert tuple(os[::-1]) == ('c', 'b', 'a', 'z', 'y', 'x')
    middle_items = os[1:-1]
    assert 'y' in middle_items
    assert 'x' not in middle_items
    assert 'c' not in middle_items


def test_maintaining_insertion_order_on_modification():
    os = orderedset()
    insertion_sequence = [5, 1, 9, 3, 7, 2, 8, 4, 6]
    for item in insertion_sequence:
        os.uppend(item)
    assert list(os) == insertion_sequence
    os.remove(1)
    os.remove(7)
    os.discard(999)  # non-existent item
    assert list(os) == [5, 9, 3, 2, 8, 4, 6]
    os.uppend(1)
    assert list(os) == [5, 9, 3, 2, 8, 4, 6, 1]


def test_frozen_vs_mutable_usage_patterns():
    mutable_os = orderedset()
    data_sources = [(1, 2, 3), (3, 4, 5), (5, 6, 7)]
    for source in data_sources:
        mutable_os.update(source)
    immutable_os = orderedfrozenset(mutable_os)
    cache = {immutable_os: 'processed_result'}
    container_of_sets = {immutable_os, orderedfrozenset((8, 9, 10))}
    assert len(cache) == 1
    assert len(container_of_sets) == 2
    assert cache[immutable_os] == 'processed_result'
    mutable_os.uppend(8)
    assert 8 not in immutable_os
    assert 8 in mutable_os


#@parametrize_ordered_set_types('class_')
#def test_performance_critical_membership_testing(class_):
#    large_os = class_(range(10000))
#    assert 0 in large_os
#    assert 5000 in large_os
#    assert 9999 in large_os
#    assert 10000 not in large_os
#    assert -1 not in large_os


@parametrize_ordered_set_types('class_')
def test_builtin_sequence_ops(class_):
    data = (3, 1, 4, 1, 5, 9)
    data_dedup = (3, 4, 1, 5, 9)
    os = orderedset(data)
    sorted_items = sorted(os)
    assert sorted_items == sorted(set(data))
    reversed_items = list(reversed(os))
    assert reversed_items == list(reversed(data_dedup))


@parametrize_ordered_set_types('class_')
def test_with_complex_values_1(class_):
    tuple_os = class_(((1, 2), (3, 4), (1, 2), (5, 6)))
    assert tuple(tuple_os) == ((3, 4), (1, 2), (5, 6))


@parametrize_ordered_set_types('class_')
def test_with_complex_values_2(class_):
    data = (1, '1', (1,))
    mixed_os = class_(data)
    for val in data:
        assert val in mixed_os


def test_complex_workflow():
    viewing_history = ['a', 'b', 'a', 'c', 'd', 'd']
    unique_viewed = orderedset(viewing_history)
    recommendations = orderedset(['e', 'f', 'a', 'g'])
    new_recommendations = recommendations - unique_viewed
    assert list(new_recommendations) == ['e', 'f', 'g']
    popular_movies = ['h', 'i', 'e']
    final_recommendations = new_recommendations.copy()
    for movie in popular_movies:
        final_recommendations.append_or_ignore(movie)
    assert 'f' in final_recommendations
    assert 'a' not in final_recommendations
    assert list(final_recommendations) == ['e', 'f', 'g', 'h', 'i']
