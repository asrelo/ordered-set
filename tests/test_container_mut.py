import pytest

from ordered_set import orderedfrozenset, orderedset

from .helpers import move_within_seq
from .helpers.ordered_set_ import check_orderedset_invariants


def smth_test_insertion_data_function_base(data):
    return list(data)


def fixture_test_insertion_data(name='data', **kwargs):
    return pytest.fixture(name=name, **kwargs)


def smth_test_insertion_object_function_base(data):
    return orderedset.from_unique(data)


def fixture_test_insertion_object(name='object_', **kwargs):
    return pytest.fixture(name=name, **kwargs)


def smth_test_insertion_data_and_object_function_base(data, object_):
    return (data, object_)


def fixture_test_insertion_data_and_object(name='data_and_object', **kwargs):
    return pytest.fixture(name=name, **kwargs)


def smth_test_sequence_mutation_synched_add_fixtures(*, data_attr):
    data_getattr = lambda cls: getattr(cls, data_attr)  # noqa: E731

    def wrapper(cls):
        cls.data = classmethod(
            fixture_test_insertion_data()(
                lambda cls: smth_test_insertion_data_function_base(data_getattr(cls))
            )
        )
        cls.object_ = staticmethod(
            fixture_test_insertion_object()(
                lambda data: smth_test_insertion_object_function_base(data)
            )
        )
        #cls.data_and_object = staticmethod(
        #    fixture_test_insertion_data_and_object()(
        #        lambda data, object_: (
        #            smth_test_insertion_data_and_object_function_base(
        #                data, object_,
        #            )
        #        )
        #    )
        #)
        return cls

    return wrapper


@smth_test_sequence_mutation_synched_add_fixtures(data_attr='DATA')
class TestDelSingle:

    DATA = (1, 2, 5, 4, 3)

    @pytest.mark.parametrize('idx', (0, 2, (len(DATA) - 1), -len(DATA), -1))
    @staticmethod
    def test_smth(data, object_, idx):
        assert list(object_) == data
        del data[idx]
        del object_[idx]
        assert list(object_) == data
        check_orderedset_invariants(object_)

    @pytest.mark.parametrize('idx', (len(DATA), (-len(DATA) - 1)))
    @staticmethod
    def test_oob(object_, idx):
        with pytest.raises(IndexError):
            del object_[idx]


@smth_test_sequence_mutation_synched_add_fixtures(data_attr='DATA')
class TestDelSlice:

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
    @staticmethod
    def test_smth(data, object_, slice_):
        assert list(object_) == data
        del data[slice_]
        del object_[slice_]
        assert list(object_) == data
        check_orderedset_invariants(object_)


@smth_test_sequence_mutation_synched_add_fixtures(data_attr='DATA')
class TestInsertOrIgnore:

    DATA = (1, 2, 5, 4, 3)

    @pytest.mark.parametrize(
        'idx', (0, 2, len(DATA), -len(DATA), -2, -1, (len(DATA) * 2), -(len(DATA) * 2)),
    )
    @staticmethod
    def test_absent(data, object_, idx):
        val = 8
        assert val not in data
        data.insert(idx, val)
        object_.insert_or_ignore(idx, val)
        assert list(object_) == data
        check_orderedset_invariants(object_)

    @pytest.mark.parametrize('idx_new', (0, 2, len(DATA), -len(DATA), -2, -1))
    @pytest.mark.parametrize('idx_old', (0, 2, (len(DATA) - 1), -len(DATA), -2, -1))
    @staticmethod
    def test_present(data, object_, idx_old, idx_new):
        val = data[idx_old]
        object_.insert_or_ignore(idx_new, val)
        assert list(object_) == data
        check_orderedset_invariants(object_)


@smth_test_sequence_mutation_synched_add_fixtures(data_attr='DATA')
class TestUpsert:

    DATA = (1, 2, 5, 4, 3)

    @pytest.mark.parametrize(
        'idx', (0, 2, len(DATA), -len(DATA), -2, -1, (len(DATA) * 2), -(len(DATA) * 2)),
    )
    @staticmethod
    def test_absent(data, object_, idx):
        val = 8
        assert val not in data
        data.insert(idx, val)
        object_.upsert(idx, val)
        assert list(object_) == data
        check_orderedset_invariants(object_)

    @pytest.mark.parametrize('idx_new', (0, 2, len(DATA), -len(DATA), -2, -1))
    @pytest.mark.parametrize('idx_old', (0, 2, (len(DATA) - 1), -len(DATA), -2, -1))
    @staticmethod
    def test_present(data, object_, idx_old, idx_new):
        val = data[idx_old]
        move_within_seq(data, idx_old, idx_new)
        object_.upsert(idx_new, val)
        assert list(object_) == data
        check_orderedset_invariants(object_)


@smth_test_sequence_mutation_synched_add_fixtures(data_attr='DATA')
class TestAppendOrIgnore:

    DATA = (1, 2, 5, 4, 3)

    @staticmethod
    def test_absent(data, object_):
        val = 8
        assert val not in data
        data.append(val)
        object_.append_or_ignore(val)
        assert list(object_) == data
        check_orderedset_invariants(object_)

    @pytest.mark.parametrize('idx_old', (0, 2, (len(DATA) - 1), -len(DATA), -2, -1))
    @staticmethod
    def test_present(data, object_, idx_old):
        val = data[idx_old]
        object_.append_or_ignore(val)
        assert list(object_) == data
        check_orderedset_invariants(object_)


@smth_test_sequence_mutation_synched_add_fixtures(data_attr='DATA')
class TestUppend:

    DATA = (1, 2, 5, 4, 3)

    @staticmethod
    def test_absent(data, object_):
        val = 8
        assert val not in data
        data.append(val)
        object_.uppend(val)
        assert list(object_) == data
        check_orderedset_invariants(object_)

    @pytest.mark.parametrize('idx_old', (0, 2, (len(DATA) - 1), -len(DATA), -2, -1))
    @staticmethod
    def test_present(data, object_, idx_old):
        val = data[idx_old]
        move_within_seq(data, idx_old, len(data))
        object_.uppend(val)
        assert list(object_) == data
        check_orderedset_invariants(object_)


def test_clear():
    data = (1, 2, 3, 1, 3)
    obj = orderedset(data)
    assert len(obj) > 0
    obj.clear()
    assert len(obj) == 0
    check_orderedset_invariants(obj)


def test_reverse():
    data = (1, 2, 5, 4, 3)
    data_rev = list(reversed(data))
    obj = orderedset.from_unique(data)
    obj.reverse()
    assert list(obj) == data_rev
    check_orderedset_invariants(obj)


class TestExtendOrIgnore:

    @pytest.mark.parametrize('update_transform', (None, orderedfrozenset))
    @pytest.mark.parametrize(
        ('data', 'update', 'expected'),
        (
            ((), (), ()),
            ((), (1, 2), (1, 2)),
            ((1, 2), (), (1, 2)),
            ((1, 2), (2, 3, 4), (1, 2, 3, 4)),
            ((1, 2, 3), (3, 4, 5, 1), (1, 2, 3, 4, 5)),
            ((1, 2, 3), (4, 4, 3, 5, 5, 1), (1, 2, 3, 4, 5)),
        ),
    )
    @staticmethod
    def test_update_ordered(data, update, expected, update_transform):
        if update_transform is not None:
            update = update_transform(update)
        obj = orderedset.from_unique(data)
        obj.extend_or_ignore(update)
        if not isinstance(expected, list):
            expected = list(expected)
        assert list(obj) == expected
        check_orderedset_invariants(obj)

    @pytest.mark.parametrize(
        ('data', 'update'),
        (
            ((), {}),
            ((), {1, 2}),
            ((1, 2), {}),
            ((1, 2), {2, 3, 4}),
            ((1, 2, 3), {4, 3, 5, 1}),
        ),
    )
    @staticmethod
    def test_update_unordered(data, update):
        if not isinstance(update, set):
            update = set(update)
        expected_tail = update - set(data)
        obj = orderedset.from_unique(data)
        obj.extend_or_ignore(update)
        obj_list = list(obj)
        if not isinstance(data, list):
            data = list(data)
        assert obj_list[:len(data)] == data
        assert set(obj_list[len(data):]) == expected_tail
        check_orderedset_invariants(obj)


class TestUpdate:

    @pytest.mark.parametrize('update_transform', (None, orderedfrozenset))
    @pytest.mark.parametrize(
        ('data', 'update', 'expected'),
        (
            ((), (), ()),
            ((), (1, 2), (1, 2)),
            ((1, 2), (), (1, 2)),
            ((1, 2), (2, 3, 4), (1, 2, 3, 4)),
            ((1, 2, 3), (3, 4, 5, 1), (2, 3, 4, 5, 1)),
            ((1, 2, 3), (4, 4, 3, 5, 5, 1), (2, 4, 3, 5, 1)),
        ),
    )
    @staticmethod
    def test_update_ordered(data, update, expected, update_transform):
        if update_transform is not None:
            update = update_transform(update)
        obj = orderedset.from_unique(data)
        obj.update(update)
        if not isinstance(expected, list):
            expected = list(expected)
        assert list(obj) == expected
        check_orderedset_invariants(obj)

    @pytest.mark.parametrize(
        ('data', 'update'),
        (
            ((), {}),
            ((), {1, 2}),
            ((1, 2), {}),
            ((1, 2), {2, 3, 4}),
            ((1, 2, 3), {4, 3, 5, 1}),
        ),
    )
    @staticmethod
    def test_update_unordered(data, update):
        if not isinstance(update, set):
            update = set(update)
        head_length = len(data) - len(update & set(data))
        expected_head = list(filter(lambda x: x not in update, data))
        assert head_length == len(expected_head)
        obj = orderedset.from_unique(data)
        obj.update(update)
        obj_list = list(obj)
        if not isinstance(data, list):
            data = list(data)
        assert obj_list[:head_length] == expected_head
        assert set(obj_list[head_length:]) == update
        check_orderedset_invariants(obj)


@smth_test_sequence_mutation_synched_add_fixtures(data_attr='DATA')
class TestPop:

    DATA = (1, 2, 5, 4, 3)

    @pytest.mark.parametrize('idx', (0, 2, (len(DATA) - 1), -len(DATA), -2, -1))
    @staticmethod
    def test_present(data, object_, idx):
        val = data.pop(idx)
        val_popped = object_.pop(idx)
        assert val_popped == val
        assert list(object_) == data
        check_orderedset_invariants(object_)

    @pytest.mark.parametrize('idx', ((len(DATA) * 2), -(len(DATA) * 2)))
    @staticmethod
    def test_absent(data, object_, idx):
        with pytest.raises(IndexError):
            _ = object_.pop(idx)
        check_orderedset_invariants(object_)


@smth_test_sequence_mutation_synched_add_fixtures(data_attr='DATA')
class TestRemove:

    DATA = (1, 2, 5, 4, 3)

    @pytest.mark.parametrize('val', (1, 5, 3))
    @classmethod
    def test_present(cls, data, object_, val):
        data.remove(val)
        object_.remove(val)
        assert val not in object_
        assert list(object_) == data
        check_orderedset_invariants(object_)

    @pytest.mark.parametrize('val', (0, 8))
    @staticmethod
    def test_absent(data, object_, val):
        with pytest.raises(KeyError):
            object_.remove(val)
        assert list(object_) == data
        check_orderedset_invariants(object_)


@smth_test_sequence_mutation_synched_add_fixtures(data_attr='DATA')
class TestDiscard:

    DATA = (1, 2, 5, 4, 3)

    @pytest.mark.parametrize('val', (1, 5, 3))
    @classmethod
    def test_present(cls, data, object_, val):
        data.remove(val)
        object_.discard(val)
        assert val not in object_
        assert list(object_) == data
        check_orderedset_invariants(object_)

    @pytest.mark.parametrize('val', (0, 8))
    @classmethod
    def test_absent(cls, object_, val):
        object_.discard(val)
        assert tuple(object_) == cls.DATA
        check_orderedset_invariants(object_)
