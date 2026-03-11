from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

# Dataclass representing the full game state at any point in the game.

@dataclass
class Position:
    
    board: List[List[int]]
    to_play: int
    prev_board: Optional[List[List[int]]] = None
    captures_black: int = 0
    captures_white: int = 0
    consecutive_passes: int = 0