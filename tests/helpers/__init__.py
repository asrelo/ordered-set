# noqa: D104

import itertools
from typing import NamedTuple

from ._general import *  # noqa: F403,F401


def fixture_params_product(*args):
    return list(itertools.product(*args))


class FixtureRequestMockObj(NamedTuple):
    param:  object


def combine_parametrize_id_strings(*ids):
    return '-'.join(ids)


def product_parametrize_ids_strings(*ids_lists):
    return list(combine_parametrize_id_strings(*t) for t in itertools.product(*ids_lists))


def product_parametrize_ids_callables(*id_callables):
    def id_callable(params):
        return tuple(
            callable_(param)
            for param, callable_ in zip(params, id_callables, strict=True)
        )
    return id_callable


def product_parametrize_ids(*ids):
    if all(map(callable, ids)):
        return product_parametrize_ids_callables(*ids)
    if all(isinstance(id_, (str, bytes)) for id_ in ids):
        return product_parametrize_ids_strings(*ids)
    raise TypeError(
        'The ids objects must either all be sequences of equal lengths of strings,'
        ' or all be callables. With pytest, it is impossible to make proper composite'
        ' IDs another way.'
    )
