from __future__ import annotations

from typing import Sequence


def format_board(board: Sequence[Sequence[int | None]]) -> str:
    values = [value for row in board for value in row if value is not None]
    width = max(len(str(value)) for value in values) if values else 1

    def render(value: int | None) -> str:
        return ".".rjust(width) if value is None else str(value).rjust(width)

    return "\n".join(" ".join(render(value) for value in row) for row in board)


__all__ = ["format_board"]
