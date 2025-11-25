from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, List, Sequence, Tuple

Coordinate = Tuple[int, int]
CellValue = int | None

BLOCKED = -1


def _validate_dimensions(board: Sequence[Sequence[object]]) -> tuple[int, int]:
    if not board:
        raise ValueError("Board must contain at least one row.")
    width = len(board[0])
    if width == 0:
        raise ValueError("Board rows must contain at least one column.")
    for row in board:
        if len(row) != width:
            raise ValueError("All board rows must have the same length.")
    return len(board), width


def _normalize_cell(raw: object) -> int | None:
    if raw is None:
        return None
    if isinstance(raw, bool):
        raise ValueError("Boolean values are not valid cell contents.")
    if not isinstance(raw, int):
        raise TypeError(f"Unsupported cell type: {type(raw)!r}")
    if raw == BLOCKED:
        return BLOCKED
    if raw <= 0:
        return None
    return raw


def chebyshev_distance(a: Coordinate, b: Coordinate) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def are_adjacent(a: Coordinate, b: Coordinate) -> bool:
    return chebyshev_distance(a, b) == 1


@dataclass
class Grid:
    cells: List[List[CellValue]]
    height: int
    width: int
    positions: dict[int, Coordinate]
    fixed_values: set[int]

    def __init__(self, board: Sequence[Sequence[object]]) -> None:
        height, width = _validate_dimensions(board)
        self.height = height
        self.width = width

        self.cells: List[List[CellValue]] = []
        self.positions: dict[int, Coordinate] = {}
        self.fixed_values: set[int] = set()

        for row_idx, row in enumerate(board):
            normalized_row: List[CellValue] = []
            for col_idx, raw_value in enumerate(row):
                value = _normalize_cell(raw_value)
                normalized_row.append(value)
                if value is None or value == BLOCKED:
                    continue
                if value in self.positions:
                    raise ValueError(f"Duplicate value {value} on the board.")
                coord = (row_idx, col_idx)
                self.positions[value] = coord
                self.fixed_values.add(value)
            self.cells.append(normalized_row)

        self._total_slots = sum(1 for row in self.cells for value in row if value != BLOCKED)
        if any(
            value is not None and value != BLOCKED and (value < 1 or value > self._total_slots)
            for row in self.cells
            for value in row
        ):
            raise ValueError("Board contains values outside the valid range for its size.")

    @property
    def total_slots(self) -> int:
        return self._total_slots

    def value_at(self, cell: Coordinate) -> CellValue:
        row, col = cell
        return self.cells[row][col]

    def is_blocked(self, cell: Coordinate) -> bool:
        return self.value_at(cell) == BLOCKED

    def is_free(self, cell: Coordinate) -> bool:
        return self.value_at(cell) is None

    def set_value(self, cell: Coordinate, value: int) -> None:
        if value in self.positions:
            # Attempting to overwrite an existing placement is a bug in the solver.
            raise ValueError(f"Value {value} already placed at {self.positions[value]}.")
        if not self.is_free(cell):
            raise ValueError(f"Cell {cell} is not available.")
        row, col = cell
        self.cells[row][col] = value
        self.positions[value] = cell

    def clear_value(self, value: int) -> None:
        if value in self.fixed_values:
            raise ValueError(f"Cannot clear fixed value {value}.")
        cell = self.positions.pop(value)
        row, col = cell
        self.cells[row][col] = None

    def neighbors(self, cell: Coordinate) -> Iterator[Coordinate]:
        row, col = cell
        for d_row in (-1, 0, 1):
            for d_col in (-1, 0, 1):
                if d_row == 0 and d_col == 0:
                    continue
                new_row, new_col = row + d_row, col + d_col
                if 0 <= new_row < self.height and 0 <= new_col < self.width:
                    neighbor = (new_row, new_col)
                    if not self.is_blocked(neighbor):
                        yield neighbor

    def empty_cells(self) -> Iterable[Coordinate]:
        for row_idx, row in enumerate(self.cells):
            for col_idx, value in enumerate(row):
                if value is None:
                    yield (row_idx, col_idx)

    def snapshot(self) -> List[List[int]]:
        result: List[List[int]] = []
        for row in self.cells:
            if any(value is None for value in row):
                raise ValueError("Grid is not completely filled.")
            result.append([int(value) for value in row if value is not None])
        return result

    def copy_positions(self) -> dict[int, Coordinate]:
        return dict(self.positions)
