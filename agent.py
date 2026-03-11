from __future__ import annotations
import math
from typing import Tuple

from engine import BLACK, PASS_MOVE, opponent
from position import Position
from evaluation import evaluate

# Alpha-Beta Minimax Agent: It searches the game tree to a set depth and returns the best move.

class AlphaBetaAgent:

    def __init__(self, game, search_depth: int = 3):
        self.game = game
        self.search_depth = search_depth
        self.perspective: int = BLACK

    def is_terminal(self, pos: Position, depth: int) -> bool:

        if depth <= 0:
            return True
        
        if pos.consecutive_passes >= 2:
            return True
        
        return False

    def get_next_position(self, pos: Position, move: Tuple[int, int]) -> Position:

        prev_board_copy = self.game.copy_board(pos.board)

        if move == PASS_MOVE:
            return Position(
                board=self.game.copy_board(pos.board),
                to_play=opponent(pos.to_play),
                prev_board=prev_board_copy,
                captures_black=pos.captures_black,
                captures_white=pos.captures_white,
                consecutive_passes=pos.consecutive_passes + 1,
            )

        resulting_board, stones_captured = self.game.apply_move(pos.board, move, pos.to_play)

        black_captures = pos.captures_black
        white_captures = pos.captures_white

        if pos.to_play == BLACK:
            black_captures += stones_captured

        else:
            white_captures += stones_captured

        return Position(
            board=resulting_board,
            to_play=opponent(pos.to_play),
            prev_board=prev_board_copy,
            captures_black=black_captures,
            captures_white=white_captures,
            consecutive_passes=0,
        )

    def alphabeta(self, pos: Position, depth: int, alpha: float, beta: float) -> float:

        if self.is_terminal(pos, depth):
            return evaluate(self.game, pos, self.perspective)

        is_maximizing = (pos.to_play == self.perspective)
        legal_moves = self.game.legal_moves(pos.board, pos.to_play, pos.prev_board)

        if is_maximizing:

            best_value = -math.inf

            for move in legal_moves:
                child = self.get_next_position(pos, move)
                best_value = max(best_value, self.alphabeta(child, depth - 1, alpha, beta))
                alpha = max(alpha, best_value)

                if alpha >= beta:
                    break

            return best_value
        
        else:

            best_value = math.inf

            for move in legal_moves:
                child = self.get_next_position(pos, move)
                best_value = min(best_value, self.alphabeta(child, depth - 1, alpha, beta))
                beta = min(beta, best_value)

                if alpha >= beta:
                    break

            return best_value

    def choose_move(self, pos: Position) -> Tuple[int, int]:

        self.perspective = pos.to_play

        best_move = PASS_MOVE
        best_value = -math.inf

        for move in self.game.legal_moves(pos.board, pos.to_play, pos.prev_board):
            child = self.get_next_position(pos, move)
            value = self.alphabeta(child, self.search_depth - 1, -math.inf, math.inf)

            if value > best_value:
                best_value = value
                best_move = move

        return best_move