"""
================================================================================
Module:        minesweeper.ai
Description:   Implements the easy, medium, and hard AI modes additions and 
               helper functions that choose and apply the computer's chosen moves.
               The default run is interactive mode, where human and computer 
               alternate turns, but players can toggle the auto-solving AI on 
               by running the text version. The same board as the player is used
               for the computer and it can also flag or reveal uncovered cells.

               The easy AI uncovered and unflagged cells at random.

               The medium AI first checks if the amount of hidden neighbors of an
               equals uncovered cell equals the number on that cell and flags the
               them if true. Second, if the amount of flagged neighbors equals an
               uncovered cell's number, the AI opens all other hidden neighbors.

               The hard AI uses the medium AI's logic but adds the 1-2-1 pattern
               rule. This is when three reveals cells in a row/col show 1-2-1 then
               it flags the two outer hidden neighbors since it deduces them as
               mines. It then opens the middle hidden neighbor. When neither hard
               nor medium AI logic applies, pick a random cell to open.


Functions:     hiddenNeighbors(board, row, col)   ->[(row, col)]
               flaggedNeighbors(board, row, col)  -> [(row, col)]
               revealedNumber(board, row, col)    -> Optional[int]
               easyAI(board)                      -> Optional[Move]
               mediumAI(board, isHardAI)          -> Optional[Move]
               hardAI(board)                      -> Optional[Move]
               chooseMove(board, mode)            -> Optional[Move]
               doMove(board, move)                -> bool
               autoSolve(mineCount, mode, verbose)-> bool
Classes:       Move(Named Tuple)
                 action: str
                 row:    int
                 col:    int

Inputs:        Board, Mine count, Mode(easy/medium/hard), Move(open/flag)
Outputs:       Repective AI mode's move

External Sources:
               Generated with the assistance of Claude (Anthropic, model
               Claude Opus 5) via Claude Code. Also Generated with the 
               assistance of DeepSeek(High-Flyer, model DeepSeek-V4.1-Flash).
               Uses Python's standard-library typing module
               (https://docs.python.org/3/library/typing.html).
               Reviewed by the author.

Author:        Didier Carrillo
Created:       2026-10-10 ***Created earlier, but moved to this new file.
================================================================================
"""

from .board import Board
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

def mediumAI(board: Board, isHardAI=False) ->Optional[Move]:
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

    if isHardAI is True:
        return None
    return easyAI(board) #fallback (random open)

def hardAI(board: Board) ->Optional[Move]:
    move = mediumAI(board, isHardAI=True)
    if move is not None: #if AI found move using mediumAI, just use that
        return move
    #if move is None, mediumAI didn't find valid move so use 1-2-1 rule
    
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

                outer_a = (r - dr, c - dc)
                outer_b = (er + dr, ec + dc)
                middleN = (mr - dc * 0, mc + 0) #place holder for hidden middle neighbor

                perpendicular_dr, perpendicular_dc = -dc, dr #coordinate(dr,dc) is shifted 90 degrees

                for sign in (1, -1):
                    mid_r = mr + sign * perpendicular_dr
                    mid_c = mc + sign * perpendicular_dc

                    #if any cell generated is not in bounds, continue
                    if not (board.in_bounds(mid_r, mid_c) and board.in_bounds(*outer_a) and board.in_bounds(*outer_b)):
                        continue

                    #if cell is revealed or flagged, continue
                    if board.grid[mid_r][mid_c].is_revealed is True or board.grid[mid_r][mid_c].is_flagged is True:
                        continue

                    #checks that outer_a is hidden and unflagged so that actions can be taken on it
                    a_ok = (not board.grid[outer_a[0]][outer_a[1]].is_revealed and not board.grid[outer_a[0]][outer_a[1]].is_flagged)
                    #checks that outer_b is hidden and unflagged so that actions can be taken on it
                    b_ok = (not board.grid[outer_b[0]][outer_b[1]].is_revealed and not board.grid[outer_b[0]][outer_b[1]].is_flagged)
                    if not (a_ok and b_ok):
                        continue

                    if not board.grid[outer_a[0]][outer_a[1]].is_flagged:
                        return Move("flag", outer_a[0], outer_a[1])
                    if not board.grid[outer_b[0]][outer_b[1]].is_flagged:
                        return Move("flag", outer_b[0], outer_b[1])
                    return Move("open", mid_r, mid_c)

    
    return easyAI(board)

                    

def chooseMove(board: Board, mode: str) -> Optional[Move]:
    mode = mode.lower()
    if mode == "easy":
        return easyAI(board)
    if mode == "medium":
        return mediumAI(board)
    if mode == "hard":
        return hardAI(board)
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