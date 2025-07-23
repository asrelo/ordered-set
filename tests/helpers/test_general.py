import pytest

from ._general import move_within_seq


@pytest.mark.parametrize(
    ('universal_indirection_simple', 'idx_from', 'idx_to', 'expected'),
    (
        (lambda: [1, 2, 3, 4, 5],   1,  3,  (1, 3, 2, 4, 5)),
        (lambda: [1, 2, 3, 4, 5],   3,  1,  (1, 4, 2, 3, 5)),
        (lambda: [1, 2, 3, 4, 5],   0,  5,  (2, 3, 4, 5, 1)),
        (lambda: [1, 2, 3, 4, 5],   4,  0,  (5, 1, 2, 3, 4)),
        (lambda: [1, 2, 3, 4, 5],   -5, 2,  (2, 1, 3, 4, 5)),
        (lambda: [1, 2, 3, 4, 5],   -2, 5,  (1, 2, 3, 5, 4)),
        (lambda: [1, 2, 3, 4, 5],   2,  2,  (1, 2, 3, 4, 5)),
        (lambda: [42],  0,  0,  (42,)),
    ),
    indirect=('universal_indirection_simple',),
)
def test_move_within_seq(universal_indirection_simple, idx_from, idx_to, expected):
    seq = universal_indirection_simple
    move_within_seq(seq, idx_from, idx_to)
    if not isinstance(seq, list):
        seq = list(seq)
    if not isinstance(expected, list):
        expected = list(expected)
    assert seq == expected
