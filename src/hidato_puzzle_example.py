from __future__ import annotations

from hidato.hidato_puzzle import hidato_puzzle
from hidato.utils import format_board


EXAMPLE_PUZZLE = [
    [2, None, None, 5],
    [None, 1, None, 6],
    [None, None, None, None],
    [11, None, None, None],
]


def main() -> None:
    print("Puzzle inicial:\n")
    print(format_board(EXAMPLE_PUZZLE))
    print()

    solution = hidato_puzzle(EXAMPLE_PUZZLE)
    if solution is None:
        print("Nenhuma solução encontrada.")
        return

    print("Solução encontrada:\n")
    print(format_board(solution))


if __name__ == "__main__":
    main()

