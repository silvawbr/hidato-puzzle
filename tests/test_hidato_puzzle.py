from __future__ import annotations

from hidato.grid import chebyshev_distance
from hidato.hidato_puzzle import hidato_puzzle


def _assert_valid_solution(puzzle: list[list[int | None]], solution: list[list[int]]) -> None:
    rows = len(puzzle)
    cols = len(puzzle[0])
    assert len(solution) == rows
    assert all(len(row) == cols for row in solution)

    total_slots = sum(1 for row in puzzle for value in row if value != -1)
    positions: dict[int, tuple[int, int]] = {}

    for row_idx in range(rows):
        for col_idx in range(cols):
            expected = puzzle[row_idx][col_idx]
            solved_value = solution[row_idx][col_idx]

            if expected == -1:
                assert solved_value == -1
                continue

            assert solved_value >= 1
            positions[solved_value] = (row_idx, col_idx)

            if expected not in (None, 0):
                assert solved_value == expected

    assert set(positions.keys()) == set(range(1, total_slots + 1))

    for value in range(1, total_slots):
        assert chebyshev_distance(positions[value], positions[value + 1]) == 1


def test_solves_simple_3x3_board() -> None:
    puzzle = [
        [1, None, None],
        [None, None, None],
        [None, None, 9],
    ]

    solution = hidato_puzzle(puzzle)
    assert solution is not None
    _assert_valid_solution(puzzle, solution)


def test_solves_board_with_blocked_cells() -> None:
    puzzle = [
        [1, None, None, 4],
        [None, -1, None, 5],
        [None, None, None, None],
        [10, None, None, None],
    ]

    solution = hidato_puzzle(puzzle)
    assert solution is not None
    _assert_valid_solution(puzzle, solution)


def test_detects_impossible_fixed_pair() -> None:
    puzzle = [
        [1, None, None],
        [None, None, None],
        [None, None, 2],
    ]

    assert hidato_puzzle(puzzle) is None
