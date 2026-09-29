from enum import Enum

class BoardSize(Enum): 
    # rows, col, min mines, max mines, default mines, cell size
    SMALL = (10, 10, 10, 20, 10, 3)
    MEDIUM = (15, 15, 25, 50, 40, 1)
    LARGE = (25, 25, 50, 120, 100, 1)

    def __init__(self, rows: int, cols: int, min_mines: int, max_mines: int, default_mines: int, cell_size: float):
        self.rows = rows
        self.cols = cols
        self.min_mines = min_mines
        self.max_mines = max_mines
        self.default_mines = default_mines
        self.cell_size = cell_size