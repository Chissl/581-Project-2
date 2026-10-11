import random
from . import config
from .board import Board, parse_coordinate

from typing import NamedTuple, Optional

class Move(NamedTuple):
    action: str
    row: int
    col: int

def hiddenNeighbors(board: Board, row: int, col:int):
    return [
        (nr, nc)
        for nr, nc in board.neighbors(row, col)
        if not board.grid[nr][nc].is_revealed
        and not board.grid[nr][nc].is_flagged
    ]

def flaggedNeighbors(board: Board, row: int, col: int):
    return[
        (nr, nc)
        for nr, nc in board.neighbors(row, col)
        if board.grid[nr][nc].is_flagged
    ]

def revealedNumber(board: Board, row: int, col: int) -> Optional[int]:
    if not board.in_bounds(row, col):
        return None
    cell = board.grid[row][col]

    if cell.is_revealed and not cell.is_mine and cell.adjacent_mines > 0:
        return cell.adjacent_mines
    return None

def easyAI(board: Board) -> Optional[Move]:
    candidates = []
    for r in range(board.rows):
        for c in range(board.cols):
            coveredCell = board.grid[r][c]
            if coveredCell.is_revealed is False and coveredCell.is_flagged is False:
                candidates.append((r, c)) #"yield" source: deepseek; maybe replace with return

    if candidates is False:
        return None
    row, col = board.rng.choice(candidates)
    return Move("open", row, col)

def mediumAI(board: Board) ->Optional[Move]:
    for r in range(board.rows):
        for c in range(board.cols):
            cell = board.grid[r][c]
            if not cell.is_revealed or cell.adjacent_mines == 0:
                continue

            hidden = hiddenNeighbors(board, r, c)
            if hidden and len(hidden) == cell.adjacent_mines:
                nr, nc = hidden[0]
                return Move("flag", nr, nc)

    #rule 2
    for r in range(board.rows):
        for c in range(board.cols):
            cell = board.grid[r][c]
            if not cell.is_revealed or cell.adjacent_mines == 0:
                continue
            flagged = flaggedNeighbors(board, r, c)
            hidden = hiddenNeighbors(board, r, c)
            if hidden and len(flagged) == cell.adjacent_mines:
                nr, nc = hidden[0]
                return Move("open", nr, nc)

    return easyAI(board) #fallback (random open)

def hardAI(board: Board) ->Optional[Move]:
    candidates = []
    for r in range(board.rows):
        for c in range(board.cols):
            coveredCell = board.grid[r][c]
            if coveredCell.is_revealed is False and coveredCell.is_flagged is False:
                candidates.append((r, c)) #"yield" source: deepseek; maybe replace with return
    
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        for r in range(board.rows):
            for c in range(board.cols):
                mr, mc = r + dr, c + dc
                er, ec = r + 2 * dr, c + 2 * dc
                if not (board.in_bounds(mr, mc) and board.in_bounds(er, ec)):
                    continue

                # if first cell isn't 1 or middle cell isn't 2 or end cell isn't 1 continue
                if revealedNumber(board, r, c) != 1 or revealedNumber(board, mr, mc) != 2 or revealedNumber(board, er, ec) != 1:
                    continue

def chooseMove(board: Board, mode: str) -> Optional[Move]:
    mode = mode.lower()
    if mode == "easy":
        return easyAI(board)
    if mode == "medium":
        return mediumAI(board)
    raise ValueError(f"Unknown AI mode: {mode!r}")

def doMove(board: Board, move: Optional[Move]) -> bool:
    if move is None:
        return False
    if move.action == "flag":
        board.toggle_flag(move.row, move.col)
        return False
    
    
    if move.action == "open":
        return board.reveal(move.row, move.col)
    raise ValueError(f"Unknown move action: {move.action!r}")

def autoSolve(mineCount: int, mode: str, verbose: bool = True) -> bool:
    board = Board(mineCount)

    first = easyAI(board)
    board.reveal(first.row, first.col)

    while not board.is_cleared():
        move = chooseMove(board, mode)
        if move is None:
            break
        hit = doMove(board, move)
        if verbose:
            print(board.render(show_mines=hit))
            print()
        if hit:
            return False

    return board.is_cleared()