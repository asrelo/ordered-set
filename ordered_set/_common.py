from collections.abc import Iterable, Collection
from types import NotImplementedType
from typing import TypeAlias, TypeVar


ComparisonResult: TypeAlias = bool | NotImplementedType


T = TypeVar('T')


def coerce_iterable_to_collection(
    iterable: Iterable[T]
) -> Collection[T]:  # pragma: no cover
    if not isinstance(iterable, Collection):
        iterable = list(iterable)
    return iterable
