from enum import Enum

class BoardSize(Enum): 
    # rows, col, min mines, max mines
    SMALL = (10, 10, 10, 20)
    MEDIUM = (15, 15, 25, 50)
    LARGE = (25, 25, 40, 100)

    def __init__(self, rows: int, cols: int, min_mines: int, max_mines: int):
        self.rows = rows
        self.cols = cols
        self.min_mines = min_mines
        self.max_mines = max_mines