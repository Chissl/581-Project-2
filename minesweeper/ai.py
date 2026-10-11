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
               rule. This is when three revealed cells in a row/col show 1-2-1
               and the only covered cells touching them are on one side. It
               flags the covered cells beside the two 1s (they must be mines)
               and opens the covered cell beside the 2 (it must be safe). When neither hard
               nor medium AI logic applies, pick a random cell to open.


Functions:     hiddenNeighbors(board, row, col)   ->[(row, col)]
               flaggedNeighbors(board, row, col)  -> [(row, col)]
               revealedNumber(board, row, col)    -> Optional[int]
               easyAI(board)                      -> Optional[Move]
               mediumAI(board, isHardAI=False)          -> Optional[Move]
               oneTwoOneMove(board)               -> Optional[Move]
               hardAI(board)                      -> Optional[Move]
               chooseMove(board, mode)            -> Optional[Move]
               doMove(board, move)                -> bool
               autoSolve(mineCount, mode, verbose)-> bool
Classes:       Move(Named Tuple)
                 __init__(action, row, col)
Inputs:        Board, Mine count, Mode(easy/medium/hard), Move(open/flag)
Outputs:       Repective AI mode's move

External Sources:
               Generated with the assistance of Claude (Anthropic, model
               Claude Opus 5) via Claude Code. Also Generated with the 
               assistance of DeepSeek(High-Flyer, model DeepSeek-V4.1-Flash).
               Reviewed by the author.

Author:        Didier Carrillo
Created:       2026-10-10 ***Created earlier, but moved to this new file.
================================================================================
"""

from .board import Board
from .boardsize import BoardSize
from typing import Optional

#Holds the AI's chosen action and coordinate.
class Move:
    def __init__(self, action, row, col): #class constructor for Move
        self.action = action #stores action (which should be "open" or "flag" or None)
        self.row = row #stores row
        self.col = col #stores column

'''
Get list of uncovered and unflagged(hidden) neighbors for mediumAI.

Inputs: board(Board)- the board object being played on.
        row(int)- row of coordinate
        col(int)- column of coordinate
Outputs: List of uncovered and unflagged neighbor coordinates
'''
def hiddenNeighbors(board: Board, row: int, col:int):
    #return list of (neighbor_row, neighbor_col) when cell (nr, nc) is not revealed and not flagged
    return [
        (nr, nc) 
        for nr, nc in board.neighbors(row, col)
        if not board.grid[nr][nc].is_revealed and not board.grid[nr][nc].is_flagged
    ]

'''
Get list of flagged neighbors for mediumAI.

Inputs: board(Board)- the board object being played on.
        row(int)- row of coordinate
        col(int)- column of coordinate
Outputs: List of flagged neighbor coordinates
'''
def flaggedNeighbors(board: Board, row: int, col: int):
    #return list of (neighbor_row, neighbor_col) when cell (nr, nc) is flagged
    return[
        (nr, nc)
        for nr, nc in board.neighbors(row, col)
        if board.grid[nr][nc].is_flagged
    ]

'''
Get list of flagged neighbors for mediumAI.

Inputs: board(Board)- the board object being played on.
        row(int)- row of coordinate
        col(int)- column of coordinate
Outputs: Number of adjacent mines
'''
def revealedNumber(board: Board, row: int, col: int) -> Optional[int]:
    #Sourced: DeepSeek AI
    #if coordinate provided is not in the board, return None, otherwise save it in variable cell
    if not board.in_bounds(row, col):
        return None
    cell = board.grid[row][col] 

    #if the cell is uncovered, not a mine, and has any adjacent mines return the number of adjacent mines
    if cell.is_revealed and not cell.is_mine and cell.adjacent_mines > 0:
        return cell.adjacent_mines
    return None #Return None if any condition above failed

    

'''
Program computer to solve minesweeper game by uncovering cells at random.

Inputs: board(Board)- the board object being played on.
Outputs: AI's Move("open" and randomly selected cell); None if cannot find fitting cell
'''
def easyAI(board: Board) -> Optional[Move]:
    candidates = [] #list to hold valid cells, will later pick at random from these
    #Going through board, checks each cell for if it's covered or flagged
    for r in range(board.rows):
        for c in range(board.cols):
            coveredCell = board.grid[r][c]
            #if the cell is not revealed and is unflagged, append it to candidates list
            if coveredCell.is_revealed is False and coveredCell.is_flagged is False:
                candidates.append((r, c))

    #If could not find valid candidates, return False
    if not candidates:
        return None
    #Otherwise set row and col to a random coordinate from candidates list(using board's random.Random() instance)
    row, col = board.rng.choice(candidates)
    return Move("open", row, col) #Return Move(always "open") with the picked coordinates

'''
Program computer to play minesweeper using 2 rules.
    1. If a revealed cell's amount of hidden neighbors matches it's number, flag it's hidden
        neighbors
    2. Then if a revealed cell's amount of flagged neighbors matches it's number, open it's 
        unflagged and hidden neighbors.
    Otherwise call easyAI and open a random cell.
Inputs: board(Board)- the board object being played on.
        isHardAI- defaults to False; Only for when hardAI calls mediumAI
Outputs: AI's Move("open"/"flag" and selected cell); Calls easyAI when neither rule applies
         None when isHardAI=True (to stop mediumAI from calling easyAI)
'''
def mediumAI(board: Board, isHardAI=False) ->Optional[Move]:
    #Sourced: DeepSeek AI
    #Go through every cell and check if it's covered or has any adjacent mines
    for r in range(board.rows):
        for c in range(board.cols):
            cell = board.grid[r][c]
            if not cell.is_revealed or cell.adjacent_mines == 0:
                continue #When is not revealed or has no adjacent mines, continue to rule 2

            hidden = hiddenNeighbors(board, r, c)
            # Count flagged cells as hidden too, so an already-flagged mine
            # doesn't make the AI flag a safe neighbor by mistake.
            flagged = flaggedNeighbors(board, r, c)
            if hidden and len(hidden) + len(flagged) == cell.adjacent_mines:
                nr, nc = hidden[0]
                return Move("flag", nr, nc)

    #rule 2; Sourced: DeepSeek AI
    #Go through every cell and check if it is revealed or has any adjacent mines
    for r in range(board.rows):
        for c in range(board.cols):
            cell = board.grid[r][c]
            if not cell.is_revealed or cell.adjacent_mines == 0:
                continue #When is not revealed and has no adjacent mines, rule 2 does not apply

            flagged = flaggedNeighbors(board, r, c)
            hidden = hiddenNeighbors(board, r, c)
            if hidden and len(flagged) == cell.adjacent_mines:
                nr, nc = hidden[0]
                #Open hidden neighbors when number of flagged neighbors equals number of adjacent mines
                return Move("open", nr, nc)  

    #When neither rule applies, check if mediumAI was called by hardAI
    if isHardAI is True:
        return None #Return None if mediumAI was called by hardAI(to not call easyAI)
    return easyAI(board) #fallback (random open)


def oneTwoOneMove(board: Board) -> Optional[Move]:
    """Find a 1-2-1 pattern and return the move it proves is right.

    Inputs:  board (Board) - the current game board.
    Outputs: Move to flag one of the two mines, or to open the safe cell, or
             None if no 1-2-1 pattern on the board gives a new move.

    The pattern: three revealed cells side by side read 1, 2, 1, and the only
    covered cells touching them are in the row (or column) on one side. The
    2 needs two mines among the three covered cells beside it. If the cell
    beside the 2 were a mine, the second mine would sit beside one of the 1s,
    giving that 1 two mines - impossible. So the cells beside the two 1s are
    mines and the cell beside the 2 is safe.
    """
    # Sourced: Combined (pattern rule from the project spec; Didier Carrillo's
    # original layout, corrected with Claude AI to check the side cells)
    # Side by side means along a row (0, 1) or down a column (1, 0).
    for dr, dc in ((0, 1), (1, 0)):
        for r in range(board.rows):
            for c in range(board.cols):
                line = [(r, c), (r + dr, c + dc), (r + 2 * dr, c + 2 * dc)]
                numbers = [revealedNumber(board, lr, lc) for lr, lc in line]
                if numbers != [1, 2, 1]:
                    continue

                # The covered side can be either side of the line.
                for sr, sc in ((dc, dr), (-dc, -dr)):
                    side = [(lr + sr, lc + sc) for lr, lc in line]
                    if not all(board.in_bounds(*cell) for cell in side):
                        continue
                    if not _onlyCoveredOnSide(board, line, sr, sc):
                        continue

                    outer_a, middle, outer_b = side
                    # Flag the two mines first, then open the safe middle cell.
                    for mr, mc in (outer_a, outer_b):
                        cell = board.grid[mr][mc]
                        if not cell.is_revealed and not cell.is_flagged:
                            return Move("flag", mr, mc)
                    cell = board.grid[middle[0]][middle[1]]
                    if not cell.is_revealed and not cell.is_flagged:
                        return Move("open", middle[0], middle[1])
    return None


def _onlyCoveredOnSide(board: Board, line, sr: int, sc: int) -> bool:
    """True if every covered neighbor of the three line cells is on the given side.

    Inputs:  board (Board), line (three (row, col) cells), sr/sc (int) - the
             step from the line to the side being checked.
    Outputs: bool - False if a covered or flagged cell touches the pattern
             anywhere else, because then the 1-2-1 deduction is not safe.
    """
    # Sourced: Claude AI
    side_cells = set()
    for lr, lc in line:
        for step in (-1, 0, 1):
            # The three cells on the side row next to each line cell.
            side_cells.add((lr + sr + step * abs(sc), lc + sc + step * abs(sr)))
    for lr, lc in line:
        for nr, nc in board.neighbors(lr, lc):
            if not board.grid[nr][nc].is_revealed and (nr, nc) not in side_cells:
                return False
    return True

'''
Program computer to solve minesweeper game by performing 1-2-1 rule when mediumAI rules do not apply.
    When three uncovered cells are side-by-side in the pattern of 1-2-1, flag the two outer
    hidden neighbors as they are probably mines. Then, open the inner hidden neighbor.

Inputs: board(Board)- the board object being played on.
Outputs: AI's Move("open"/"flag" and selected cell)
         Call easyAI() when the neither of the mediumAI() rules nor the 1-2-1 rule applies
'''
def hardAI(board: Board) ->Optional[Move]:
    move = mediumAI(board, isHardAI=True)
    if move is not None: #if AI found move using mediumAI, just use that
        return move
    #if move is None, mediumAI didn't find valid move so use 1-2-1 rule
    move = oneTwoOneMove(board)
    if move is not None:
        return move
    #no rule applies, so fall back to a random open
    return easyAI(board)

'''
Program computer to solve minesweeper game by uncovering cells at random.

Inputs: board(Board)- the board object being played on.
        mode(str)- "easy", "medium", or "hard"
Outputs: Move of chosen AI mode
'''
def chooseMove(board: Board, mode: str) -> Optional[Move]:
    mode = mode.lower() #Make mode text lowercase,so ValueError isn't raised for capitalization
    #Call corresponding AI mode depending on which mode argument was passed through
    if mode == "easy":
        return easyAI(board)
    if mode == "medium":
        return mediumAI(board)
    if mode == "hard":
        return hardAI(board)
    
    #Sourced: DeepSeek AI
    #raise a ValueError when mode argument isn't one of the above 
    raise ValueError(f"Unknown AI mode: {mode!r}")

'''
Program computer to solve minesweeper game by uncovering cells at random.

Inputs: board(Board)- the board object being played on.
        move(Move)- "open"/"flag" and coordinates; Can also be None
Outputs: Boolean Value- whether revealed cell was a mine
'''
def doMove(board: Board, move: Optional[Move]) -> bool:
    #Sourced: DeepSeek
    #If Move was None return False; no cell revealed
    if move is None:
        return False

    #if Move was "flag", flag the Move's coordinate
    if move.action == "flag":
        board.toggle_flag(move.row, move.col)
        return False #no cell revealed

    #If Move was "open", call board.reveal() to uncover Move's coordinate;
    if move.action == "open":
        return board.reveal(move.row, move.col) #True if hit a mine
    #Raise Value Error if the move's action was not "open" or "flag"
    raise ValueError(f"Unknown move action: {move.action!r}")

'''
The computer solves the minesweeper by itself.

Inputs: mineCount(int)- Number of mines
        mode(str)- AI mode ("easy"/"medium"/"hard")
        verbose(bool)- Default to True; Render the board for each action the AI takes
        boardSize: BoardSize; Defaulted to SMALL board

Outputs: Boolean
         Prints board renders
'''
def autoSolve(mineCount: int, mode: str, verbose: bool = True, boardSize: BoardSize = BoardSize.SMALL) -> bool:
    board = Board(boardSize, mineCount) #Set up board

    first = easyAI(board) #Perform easyAI move so that it picks a random cell to uncover
    board.reveal(first.row, first.col) #Reveal the randomly chosen cell

    #Sourced: DeepSeek AI
    #While the board isn't cleared, the AI performs a move and renders the updated board
    while not board.is_cleared():
        move = chooseMove(board, mode)
        if move is None: #If move is None, break out of while loop
            break
        hit = doMove(board, move) #Move is not None, call doMove
        if verbose: #Default True, so render updated board
            print(board.render(show_mines=hit))
            print()
        if hit: #If doMove returned True, hit a mine and AI lost
            return False

    return board.is_cleared() #Never hit a mine, and ran out of other valid options so AI won