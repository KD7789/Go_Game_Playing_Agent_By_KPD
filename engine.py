from __future__ import annotations
from typing import List, Tuple, Set, Optional

BLACK = 1
WHITE = -1
EMPTY = 0
PASS_MOVE = (-1, -1)


def opponent(player: int) -> int:
    return -player


def is_on_board(size: int, row: int, col: int) -> bool:

    if row >= 0 and row < size and col >= 0 and col < size:
        return True
    
    else:
        return False


def get_neighbors(size: int, row: int, col: int):

    for row_delta, col_delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:

        neighbor_row, neighbor_col = row + row_delta, col + col_delta

        if is_on_board(size, neighbor_row, neighbor_col):
            yield neighbor_row, neighbor_col

# Core game engine for a 5x5 Go board. It handles stone placement, captures, Ko, and legal move generation.

class GoGame:

    def __init__(self, size: int = 5):
        self.n = size

    def empty_board(self) -> List[List[int]]:
        board = []

        for _ in range(self.n):

            new_row = []

            for _ in range(self.n):
                new_row.append(EMPTY)

            board.append(new_row)

        return board

    def board_to_tuple(self, board: List[List[int]]) -> Tuple[int, ...]:

        flattened = []

        for row in range(self.n):

            for col in range(self.n):
                flattened.append(board[row][col])

        return tuple(flattened)

    def copy_board(self, board: List[List[int]]) -> List[List[int]]:
        new_board = []

        for row in board:
            new_row = []

            for cell in row:
                new_row.append(cell)

            new_board.append(new_row)

        return new_board

    def get_group(self, board: List[List[int]], row: int, col: int) -> Set[Tuple[int, int]]:

        stone_color = board[row][col]
        stack = [(row, col)]
        visited = {(row, col)}

        while stack:

            current_row, current_col = stack.pop()

            for neighbor_row, neighbor_col in get_neighbors(self.n, current_row, current_col):

                if (neighbor_row, neighbor_col) not in visited and board[neighbor_row][neighbor_col] == stone_color:

                    visited.add((neighbor_row, neighbor_col))
                    stack.append((neighbor_row, neighbor_col))

        return visited

    def count_liberties(self, board: List[List[int]], group: Set[Tuple[int, int]]) -> int:

        open_points = set()

        for row, col in group:

            for neighbor_row, neighbor_col in get_neighbors(self.n, row, col):

                if board[neighbor_row][neighbor_col] == EMPTY:
                    open_points.add((neighbor_row, neighbor_col))

        return len(open_points)

    def remove_group(self, board: List[List[int]], group: Set[Tuple[int, int]]) -> int:

        stones_removed = 0

        for row, col in group:

            board[row][col] = EMPTY
            stones_removed += 1

        return stones_removed

    def apply_move(self, board: List[List[int]], move: Tuple[int, int], player: int) -> Tuple[List[List[int]], int]:

        if move == PASS_MOVE:
            return self.copy_board(board), 0

        row, col = move

        if not is_on_board(self.n, row, col):
            raise ValueError("Illegal: out of bounds")
        
        if board[row][col] != EMPTY:
            raise ValueError("Illegal: occupied")

        new_board = self.copy_board(board)
        new_board[row][col] = player
        total_captures = 0

        opp = opponent(player)

        for neighbor_row, neighbor_col in get_neighbors(self.n, row, col):

            if new_board[neighbor_row][neighbor_col] == opp:
                opp_group = self.get_group(new_board, neighbor_row, neighbor_col)

                if self.count_liberties(new_board, opp_group) == 0:
                    total_captures += self.remove_group(new_board, opp_group)

        placed_group = self.get_group(new_board, row, col)

        if self.count_liberties(new_board, placed_group) == 0:
            raise ValueError("Illegal: suicide")

        return new_board, total_captures

    def legal_moves(
        self,
        board: List[List[int]],
        player: int,
        prev_board: Optional[List[List[int]]] = None
    ) -> List[Tuple[int, int]]:
        
        all_moves = [PASS_MOVE]
        prev_board_tuple = self.board_to_tuple(prev_board) if prev_board is not None else None

        for row in range(self.n):

            for col in range(self.n):

                if board[row][col] != EMPTY:
                    continue

                try:
                    resulting_board, _ = self.apply_move(board, (row, col), player)

                    if prev_board_tuple is not None and self.board_to_tuple(resulting_board) == prev_board_tuple:
                        continue

                    all_moves.append((row, col))

                except ValueError:
                    continue

        return all_moves

    def print_board(self, board: List[List[int]]) -> None:

        symbols = {BLACK: "X", WHITE: "O", EMPTY: "."}
        print("   " + " ".join(str(col) for col in range(self.n)))

        for row in range(self.n):
            print(f"{row:2d} " + " ".join(symbols[board[row][col]] for col in range(self.n)))