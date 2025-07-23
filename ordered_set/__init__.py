# noqa: D104

from collections.abc import (
    Callable,
    Hashable,
    Iterable,
    Iterator,
    Sequence,
    Set,
    MutableSequence,
    MutableSet,
)
from copy import copy, deepcopy
from operator import eq, ne, lt, gt, le, ge
from os import PathLike
from pathlib import Path
from reprlib import recursive_repr
from threading import RLock
from typing import Optional, TypeAlias, TypeVar, Generic, overload

from typing_extensions import Self, override

from ordered_set._common import ComparisonResult, coerce_iterable_to_collection

__all__ = ('orderedfrozenset', 'orderedset')

_PACKAGE_PATH: Path = Path(__file__).parent

_VERSION_FILE_PATH: Path = _PACKAGE_PATH / 'VERSION'


def _get_version(path: PathLike = _VERSION_FILE_PATH) -> str:
    with open(path, 'rt') as file:
        return file.readline().strip()


__version__: str = _get_version()


# XXX: `orderedfrozenset` inherits its constructor from `_orderedset_base`.
# That constructor uses a temporary `orderedset` object (which has its own
# independent constructor).


T = TypeVar('T', bound=Hashable)


# XXX: ?
class _orderedset_base(Generic[T]):

    __slots__ = ('_data_lock', '_set', '_list')

    _SET_CTR: type
    _LIST_CTR: type

    def __init__(self):
        self._data_lock: RLock = RLock()    # XXX: RLock
        self._set: Set
        self._list: Sequence

    def _check(self) -> None:
        with self._data_lock:
            # is it optimal?
            if len(self._set ^ self._SET_CTR(self._list)) != 0:  # pragma: no cover
                raise ValueError(
                    'Inconsistency detected: some elements are present only in the set'
                    ' or only in the list'
                )
            if len(self._set) != len(self._list):   # pragma: no cover
                raise ValueError('Inconsistency detected: the list has duplicate elements')
            if set(map(id, self._set)) != set(map(id, self._list)):  # pragma: no cover
                raise RuntimeError(
                    'Inconsistency detected: set and list don\'t refer to same objects'
                )

    @classmethod
    def _from_iterable(cls, it: Iterable[T]) -> Self:
        raise NotImplementedError()

    def __bool__(self) -> bool:
        return (len(self) > 0)

    @recursive_repr()
    def __repr__(self) -> str:
        type_name = type(self).__name__
        init_str = ''
        if len(self) > 0:
            iterable_type = (list if isinstance(self._list, list) else tuple)
            init_str = repr(iterable_type(self))
        return f'{type_name}({init_str})'

    def copy(self) -> Self:
        obj = type(self)()
        with self._data_lock:
            obj._set = copy(self._set)
            obj._list = copy(self._list)
        if __debug__:
            obj._check()
        return obj

    def __copy__(self) -> Self:
        return self.copy()

    def __deepcopy__(self, memo: object) -> Self:
        obj = type(self)()
        with self._data_lock:
            obj._set = deepcopy(self._set, memo)
            obj._list = deepcopy(self._list, memo)
        if __debug__:
            obj._check()
        return obj

    def __contains__(self, value: T) -> bool:
        return (value in self._set)

    def __iter__(self) -> Iterator[T]:
        return iter(self._list)

    def __len__(self) -> int:
        return len(self._set)

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Self:
        ...

    def __getitem__(self, index):
        if isinstance(index, slice):
            if index == slice(None):
                return self.copy()
            return self._from_iterable(self._list[index])
        return self._list[index]

    def __reversed__(self) -> Iterator[T]:
        return reversed(self._list)

    def index(self, value: T, start: int = 0, stop: Optional[int] = None) -> int:
        index_args_extra = []
        if stop is not None:
            index_args_extra.append(stop)
        return self._list.index(value, start, *index_args_extra)

    def count(self, value: T) -> int:
        return int(value in self._set)  # 0 or 1

    ComparisonOpMethod: TypeAlias = Callable[[Self, object], ComparisonResult]

    def __eq__(self, other: object) -> ComparisonResult:
        # "ordered set" in this implementation is not an instance
        # of any built-in collection type.
        # So the cases for built-in collections here are rather arbitrary.
        if isinstance(other, _orderedset_base):
            other_list = other._list
            if not isinstance(other_list, self._LIST_CTR):
                other_list = self._LIST_CTR(other_list)
            return (self._list == other_list)
        # `() != []`:
        if isinstance(other, (list if issubclass(self._LIST_CTR, list) else tuple)):
            return (self._list == other)
        # `frozenset() == set()`:
        if isinstance(other, (frozenset, set)):
            return (self._set == other)
        return NotImplemented

    @override
    def __ne__(self, other: object) -> ComparisonResult:
        return (not self.__eq__(other))

    @overload
    @staticmethod
    def _make_cmp_op(
        op: Callable[[Sequence, Sequence], ComparisonResult],
    ) -> ComparisonOpMethod:
        ...

    @overload
    @staticmethod
    def _make_cmp_op(op: Callable[[Set, Set], ComparisonResult]) -> ComparisonOpMethod:
        ...

    @staticmethod
    def _make_cmp_op(op) -> ComparisonOpMethod:
        def op_new(self, other: object) -> ComparisonResult:
            if isinstance(other, _orderedset_base):
                other = other._list
            # `() != []`:
            if isinstance(other, (list if issubclass(self._LIST_CTR, list) else tuple)):
                return op(self._list, other)
            # `frozenset() == set()`:
            if isinstance(other, (frozenset, set)):
                return op(self._set, other)
            return NotImplemented
        return op_new

    __lt__: ComparisonOpMethod  = override(_make_cmp_op(lt))
    __gt__: ComparisonOpMethod  = override(_make_cmp_op(gt))
    __le__: ComparisonOpMethod  = override(_make_cmp_op(le))
    __ge__: ComparisonOpMethod  = override(_make_cmp_op(ge))

    ComparisonSetOpMethod: TypeAlias = Callable[[Self, Set], ComparisonResult]

    @staticmethod
    def _make_set_cmp_op(
        set_op: Callable[[Set, Set], ComparisonResult],
    ) -> ComparisonSetOpMethod:
        def op(self, other: Set[T]) -> ComparisonResult:
            if isinstance(other, _orderedset_base):
                other = other._set
            return set_op(self._set, other)
        return op

    is_set_equal: ComparisonSetOpMethod = _make_set_cmp_op(eq)
    is_set_not_equal: ComparisonSetOpMethod = _make_set_cmp_op(ne)
    is_strict_subset: ComparisonSetOpMethod = _make_set_cmp_op(lt)
    is_strict_superset: ComparisonSetOpMethod   = _make_set_cmp_op(gt)
    is_subset: ComparisonSetOpMethod    = _make_set_cmp_op(le)
    is_superset: ComparisonSetOpMethod  = _make_set_cmp_op(ge)

    def is_disjoint(self, other: Set[T]) -> bool:
        if isinstance(other, _orderedset_base):
            other = other._set
        return self._set.isdisjoint(other)

    def isdisjoint(self, other: Set[T]) -> bool:
        return self.is_disjoint(other)

    # Reflected methods for binary arithmetic operations are called
    # when in `a X b` `type(b)` is a strict subclass (a different type)
    # of `type(a)`.
    # <https://docs.python.org/3/reference/datamodel.html#object.__radd__>

    def __and__(self, other: Set[T]) -> Self:
        return self._from_iterable(filter(lambda v: v in other, self))

    def __rand__(self, other: Set[T]) -> Self:
        return self.__and__(other)

    def __or__(self, other: Set[T]) -> Self:
        obj = orderedset(self)
        obj |= other    # calls __ior__
        return self._from_iterable(obj)

    def __ror__(self, other: Set[T]) -> Self:
        return self.__or__(other)

    def __xor__(self, other: Set[T]) -> Self:
        obj = orderedset(self)
        obj ^= other    # calls __ixor__
        return self._from_iterable(obj)

    def __rxor__(self, other: Set[T]) -> Self:
        return self.__xor__(other)

    def _difference(self, other: Set[T], *, swap: bool = False) -> Self:
        a, b = self, other
        if swap:
            a, b = b, a
        return self._from_iterable(filter(lambda v: v not in b, a))

    def __sub__(self, other: Set[T]) -> Self:
        return self._difference(other)

    def __rsub__(self, other: Set[T]) -> Self:
        return self._difference(other, swap=True)


Sequence.register(_orderedset_base)  # type: ignore
Set.register(_orderedset_base)  # type: ignore


class _orderedset_from_unique_helper_mixin:
    @classmethod
    def _from_unique_make_exception_for_duplicate_values(cls) -> ValueError:
        _ = cls
        return ValueError('Duplicates detected in the collection')


class _orderedset_picklable_mixin(Generic[T]):

    def __getstate__(self) -> tuple[Set[T], Sequence[T]]:
        return (self._set, self._list)

    def __setstate__(self, state: tuple[Set[T], Sequence[T]]):
        set_, list_ = state
        self._set = set_
        self._list = list_
        # An inconsistency can only result from corrupt pickle data,
        # and there is a lot that can result from corrupt pickle data -
        # we don't catch that.
        #self._check()


class orderedfrozenset(
    _orderedset_picklable_mixin,
    _orderedset_from_unique_helper_mixin,
    Hashable,
    _orderedset_base
):

    _SET_CTR = frozenset
    _LIST_CTR = tuple

    def __init__(self, iterable: Optional[Iterable[T]] = None):
        super().__init__()
        if iterable is not None:
            if not isinstance(iterable, _orderedset_base):
                iterable = orderedset(iterable)    # takes care of duplicates
            self._set = self._SET_CTR(iterable._set)
            self._list = self._LIST_CTR(iterable._list)
        else:
            self._set = self._SET_CTR()
            self._list = self._LIST_CTR()

    @classmethod
    def _from_iterable(cls, it: Iterable[T]) -> Self:
        return cls(it)

    @classmethod
    def from_unique(cls, iterable: Iterable[T]) -> Self:
        collection = coerce_iterable_to_collection(iterable)
        obj = cls(collection)
        if len(obj) != len(collection):
            raise cls._from_unique_make_exception_for_duplicate_values()
        return obj

    def __hash__(self) -> int:
        assert (isinstance(self._set, frozenset) and isinstance(self._list, tuple))
        return hash((self._set, self._list))


# MutableSequence-like, MutableSet-like
class orderedset(
    _orderedset_picklable_mixin,
    _orderedset_from_unique_helper_mixin,
    _orderedset_base
):

    _SET_CTR = set
    _LIST_CTR = list

    def __init__(self, iterable: Optional[Iterable[T]] = None):
        super().__init__()
        # XXX: Types?? This is kinda broken.
        self._set: MutableSet
        self._list: MutableSequence
        if isinstance(iterable, _orderedset_base):
            self._set = self._SET_CTR(iterable._set)
            self._list = self._LIST_CTR(iterable._list)
            return
        self._set = self._SET_CTR()
        self._list = self._LIST_CTR()
        if iterable is not None:
            self.update(iterable)

    @classmethod
    def _from_iterable(cls, it: Iterable[T]) -> Self:
        return cls(it)

    @classmethod
    def from_unique(cls, iterable: Iterable[T]) -> Self:
        collection = coerce_iterable_to_collection(iterable)
        obj = cls(collection)
        if len(obj) != len(collection):
            raise cls._from_unique_make_exception_for_duplicate_values()
        return obj

    # __setitem__ does not make sense

    @overload
    def __delitem__(self, index: int) -> None:
        ...

    @overload
    def __delitem__(self, index: slice) -> None:
        ...

    def __delitem__(self, index):
        with self._data_lock:
            if isinstance(index, slice):
                self._set -= frozenset(self._list[index])
            else:
                self._set.remove(self._list[index])
            del self._list[index]

    # insert makes little sense and significantly increases complexity

    def insert_or_ignore(self, index: int, value: Hashable) -> None:
        with self._data_lock:
            if value in self._set:
                return
            self._set.add(value)
            self._list.insert(index, value)

    def upsert(self, index: int, value: Hashable) -> None:
        with self._data_lock:
            if value in self._set:
                self_len = len(self._list)
                index_old = self._list.index(value)
                _ = self._list.pop(index_old)
                index %= ((self_len + 1) if index >= 0 else self_len)
                if index > index_old:
                    index -= 1
            else:
                self._set.add(value)
            self._list.insert(index, value)

    # append makes little sense and significantly increases complexity

    def append_or_ignore(self, value: Hashable) -> None:
        with self._data_lock:
            if value in self._set:
                return
            self._set.add(value)
            self._list.append(value)

    def uppend(self, value: Hashable) -> None:
        with self._data_lock:
            if value in self._set:
                self._list.remove(value)
            else:
                self._set.add(value)
            self._list.append(value)

    def clear(self) -> None:
        with self._data_lock:
            self._set.clear()
            self._list.clear()

    def reverse(self) -> None:
        self._list.reverse()

    # extend makes little sense and greatly increases complexity
    # (you've been warned)

    def extend_or_ignore(self, other: Iterable[T]) -> None:
        # This algorithm works in O(n_new).
        with self._data_lock:
            for item in other:
                self.append_or_ignore(item)

    def update(self, other: Iterable[T]) -> None:
        if not isinstance(other, Set):
            # This algorithm works in O(n_new n_common).
            with self._data_lock:
                for item in other:
                    self.uppend(item)
            return
        # This algorithm works in O(n_old + n_new).
        # O(n_new) (or O(n_old)?) (or O(n_old + n_new), if we consider
        # the copying):
        intersection = self._set & other
        with self._data_lock:
            # O(n_old):
            self._list = self._LIST_CTR(
                filter(lambda v: v not in intersection, self._list)
            )
            self._list.extend(other)    # all values in `other` must be unique
            # O(n_new):
            self._set |= other

    def pop(self, index: int = -1) -> Hashable:
        with self._data_lock:
            value = self._list.pop(index)   # may raise IndexError
            self._set.remove(value)
        return value

    def remove(self, value: Hashable) -> None:
        with self._data_lock:
            self._set.remove(value)  # may raise KeyError
            self._list.remove(value)

    # add makes no sense

    def discard(self, value: Hashable) -> None:
        with self._data_lock:
            try:
                self._set.remove(value)
            except KeyError:
                return
            self._list.remove(value)

    # When an in-place method for a binary arithmetic operation
    # is not available, a functional method is called instead. So in `a X= b`
    # a new object is created via `a X b` and it is then assigned to `a`.
    # <https://docs.python.org/3/reference/datamodel.html#object.__iadd__>

    def __iand__(self, other: Set[T]) -> Self:
        with self._data_lock:
            self._set &= other  # may raise TypeError
            self._list = self._LIST_CTR(filter(lambda v: v in other, self._list))
        return self

    def __or__(self, other: Set[T]) -> Self:
        obj = self.copy()
        obj |= other    # calls __ior__
        return obj

    #def __ror__(self, other: Set[T]) -> Self:
    #    return self.__or__(other)

    def __ior__(self, other: Set[T]) -> Self:
        self.update(other)
        return self

    def __xor__(self, other: Set[T]) -> Self:
        obj = self.copy()
        obj ^= other    # calls __ixor__
        return obj

    #def __rxor__(self, other: Set[T]) -> Self:
    #    return self.__xor__(other)

    def _symmetric_difference_update(self, other: Set[T]) -> None:
        if isinstance(other, _orderedset_base):
            # This algorithm works in O(n_new n_common).
            with self._data_lock:
                for item in other:
                    try:
                        self._set.remove(item)
                    except KeyError:
                        self._set.add(item)
                        self._list.append(item)
                    else:
                        self._list.remove(item)
            return
        if isinstance(other, Set):  # pragma: no branch
            # This algorithm works in O(n_old + n_new). But it disregards
            # the order the elements are retrieved from the `other` set.
            # O(n_old) (or O(n_old + n_new), if we consider the copying):
            new_difference = other - self._set
            with self._data_lock:
                # O(n_new):
                self._set ^= other
                # O(n_old):
                self._list = self._LIST_CTR(
                    filter(lambda v: v not in other, self._list)
                )
                # Here we disregard the order of iteration of `other`,
                # using `new_difference` instead:
                self._list.extend(new_difference)
            return
        raise TypeError(    # pragma: no cover
            f'Cannot XOR a {type(self).__name__} with a {type(other).__name__},'
            ' a set type is required'
        )

    def __ixor__(self, other: Set[T]) -> Self:
        self._symmetric_difference_update(other)
        return self

    def __sub__(self, other: Set[T]) -> Self:
        return self._from_iterable(filter(lambda v: v not in other, self))

    #def __rsub__(self, other: Set[T]) -> Self:
    #    return self.__sub__(other)

    def __isub__(self, other: Set[T]) -> Self:
        with self._data_lock:
            self._set -= other  # may raise TypeError   # type: ignore
            self._list = self._LIST_CTR(
                filter(lambda v: v not in other, self._list)
            )   # type: ignore
        return self
