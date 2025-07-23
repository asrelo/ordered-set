BUILTIN_SEQUENCE_TYPES = (tuple, list)
BUILTIN_SET_TYPES = (frozenset, set)


def iterable_as_immut_builtin_sequence(iterable):
    if not isinstance(iterable, BUILTIN_SEQUENCE_TYPES):
        iterable = tuple(iterable)
    return iterable


def move_within_seq(seq, idx_from, idx_to):
    seq_len = len(seq)
    idx_from %= seq_len
    assert idx_from >= 0
    idx_to %= ((seq_len + 1) if idx_to >= 0 else seq_len)
    assert idx_to >= 0
    val = seq.pop(idx_from)
    if idx_to > idx_from:
        idx_to -= 1
    seq.insert(idx_to, val)


def are_all_elements_unique(collection):
    return (len(frozenset(collection)) == len(collection))
