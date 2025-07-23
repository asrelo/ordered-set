from collections.abc import Sequence

from .helpers.ordered_set_ import ORDERED_SET_TYPES, ordered_set_type_parametrize_id


def pytest_make_parametrize_id(config, val, argname):
    _ = config
    _ = argname
    if isinstance(val, type) and issubclass(val, ORDERED_SET_TYPES):
        return ordered_set_type_parametrize_id(val)
    return None


# Writing a `pytest_assertrepr_compare` hook for `orderedset` specifically
# was considered.
# However, as of 8.4, pytest actually detects that `orderedset` inherits
# from `Sequence` and treats this class as a list-like class. This is
# good enough. Also, properly implementing (and maintaining) this hook
# is quite a bit of work.
assert all(issubclass(cls, Sequence) for cls in ORDERED_SET_TYPES)
