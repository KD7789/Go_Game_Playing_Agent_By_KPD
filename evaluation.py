from __future__ import annotations
from engine import BLACK, EMPTY, opponent

# Heuristic evaluation function: Scores a position from the perspective player's point of view.

def evaluate(game, pos, perspective: int) -> float:

    board = pos.board
    size = game.n

    own_stone_count = 0
    opp_stone_count = 0
    center = (size - 1) / 2.0
    own_center_score = 0.0
    opp_center_score = 0.0

    for row in range(size):

        for col in range(size):

            if board[row][col] == perspective:
                own_stone_count += 1
                own_center_score += -(abs(row - center) + abs(col - center))

            elif board[row][col] == opponent(perspective):
                opp_stone_count += 1
                opp_center_score += -(abs(row - center) + abs(col - center))

    if perspective == BLACK:
        own_captures = pos.captures_black
        opp_captures = pos.captures_white
    else:
        own_captures = pos.captures_white
        opp_captures = pos.captures_black

    visited = set()
    own_liberties = 0
    opp_liberties = 0
    own_groups_in_atari = 0
    opp_groups_in_atari = 0

    for row in range(size):

        for col in range(size):

            if board[row][col] == EMPTY or (row, col) in visited:
                continue

            group = game.get_group(board, row, col)
            visited.update(group)
            liberty_count = game.count_liberties(board, group)

            if board[row][col] == perspective:
                own_liberties += liberty_count

                if liberty_count == 1:
                    own_groups_in_atari += 1

            else:
                opp_liberties += liberty_count

                if liberty_count == 1:
                    opp_groups_in_atari += 1

    return (
        1.0  * (own_stone_count - opp_stone_count)
        + 1.8  * (own_captures - opp_captures)
        + 0.35 * (own_liberties - opp_liberties)
        + 0.9  * (opp_groups_in_atari - own_groups_in_atari)
        + 0.05 * (own_center_score - opp_center_score)
    )