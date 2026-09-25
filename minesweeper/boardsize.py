from enum import Enum

class BoardSize(Enum): 
    # Board size, min mines, max mines
    SMALL = (10, 10, 20)
    MEDIUM = (15, 25, 50)
    LARGE = (25, 40, 100)

    def __init__(self, board_size: int, min_mines: int, max_mines: int):
        self.board_size = board_size
        self.min_mines = min_mines
        self.max_mines = max_mines