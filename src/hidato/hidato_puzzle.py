from __future__ import annotations

from typing import Iterable, List, Sequence

from .grid import BLOCKED, Coordinate, Grid, are_adjacent, chebyshev_distance

BoardInput = Sequence[Sequence[int | None]]
BoardOutput = List[List[int]]


class HidatoSolver:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.max_value = grid.total_slots

    def solve(self) -> BoardOutput | None:
        if not self._validate_fixed_pairs():
            return None
        if self._backtrack(1):
            return self.grid.snapshot()
        return None

    def _validate_fixed_pairs(self) -> bool:
        for value, position in self.grid.positions.items():
            next_value = value + 1
            if next_value in self.grid.positions and not are_adjacent(
                position, self.grid.positions[next_value]
            ):
                return False
        return True

    def _next_fixed_after(self, value: int) -> tuple[int, Coordinate] | None:
        future_values = [candidate for candidate in self.grid.fixed_values if candidate > value]
        if not future_values:
            return None
        next_value = min(future_values)
        return next_value, self.grid.positions[next_value]

    def _candidate_cells(self, value: int) -> list[Coordinate]:
        previous = self.grid.positions.get(value - 1)
        next_pos = self.grid.positions.get(value + 1)

        if previous is None:
            candidates = [cell for cell in self.grid.empty_cells()]
        else:
            candidates = [cell for cell in self.grid.neighbors(previous) if self.grid.is_free(cell)]

        if next_pos is not None:
            candidates = [cell for cell in candidates if are_adjacent(cell, next_pos)]

        future = self._next_fixed_after(value)
        if future is not None:
            future_value, future_pos = future
            steps_available = future_value - value
            candidates = [
                cell for cell in candidates if chebyshev_distance(cell, future_pos) <= steps_available
            ]

        return sorted(candidates, key=self._neighboring_free_cells)

    def _neighboring_free_cells(self, cell: Coordinate) -> int:
        return sum(1 for neighbor in self.grid.neighbors(cell) if self.grid.is_free(neighbor))

    def _backtrack(self, value: int) -> bool:
        if value > self.max_value:
            return True

        if value in self.grid.positions:
            return self._backtrack(value + 1)

        for cell in self._candidate_cells(value):
            self.grid.set_value(cell, value)

            if self._backtrack(value + 1):
                return True

            self.grid.clear_value(value)

        return False


def hidato_puzzle(board: BoardInput) -> BoardOutput | None:
    """
    Resolve um Hidato usando backtracking.

    O tabuleiro pode conter inteiros positivos já fixos, células vazias (None ou 0) e células
    bloqueadas marcadas com -1. Retorna o tabuleiro completo ou None se não houver solução.
    """

    grid = Grid(board)
    solver = HidatoSolver(grid)
    return solver.solve()
