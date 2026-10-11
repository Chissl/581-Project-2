"""
================================================================================
Module:        tests.test_ai
Description:   Unit tests for the AI solver's 1-2-1 pattern rule (hard mode).
               Each test builds a board with hand-placed mines so the pattern
               is known, then checks the AI flags the two mines and opens the
               safe cell, and that it does not use the rule when it isn't safe.

Classes:       TestOneTwoOne - oneTwoOneMove / hardAI pattern tests
Functions:     make_board(mines, covered) -> Board

Inputs:        None (run with: python -m unittest discover -s tests -t .)
Outputs:       unittest pass/fail report

External Sources:
               Generated with the assistance of Claude (Anthropic, model
               Claude Opus 5.5) via Claude Code. Uses Python's standard-library
               unittest module (https://docs.python.org/3/library/unittest.html).
               Reviewed by the author.

Author:        Will Godderz
Created:       2026-10-11
================================================================================
"""

import unittest

from minesweeper import ai
from minesweeper.board import Board
from minesweeper.boardsize import BoardSize


def make_board(mines, covered):
    """Build a 10x10 board with mines at fixed spots.

    Inputs:  mines (set of (row, col)) - where the mines go.
             covered (set of (row, col)) - cells left covered; all others
             start revealed.
    Outputs: Board ready for the AI to read.
    """
    # Sourced: Claude AI
    board = Board(BoardSize.SMALL)
    board.mines_placed = True  # stop the first reveal from re-placing mines
    for r in range(board.rows):
        for c in range(board.cols):
            board.grid[r][c].is_mine = (r, c) in mines
    for r in range(board.rows):
        for c in range(board.cols):
            cell = board.grid[r][c]
            cell.adjacent_mines = sum(board.grid[nr][nc].is_mine for nr, nc in board.neighbors(r, c))
            cell.is_revealed = (r, c) not in covered
    return board


# Row 0 is covered and rows 1-9 are revealed. Mines at A1 and C1 make row 2
# read 1 1 2 1 1 across columns A-E, so B2 C2 D2 hold a 1-2-1.
TOP_ROW = {(0, c) for c in range(10)}
ROW_MINES = {(0, 1), (0, 3)}


class TestOneTwoOne(unittest.TestCase):
    def test_flags_both_mines_then_opens_middle(self):
        # Applying the rule's moves flags the cells beside the 1s and opens the one beside the 2.
        board = make_board(ROW_MINES, TOP_ROW)
        moves = []
        while (move := ai.oneTwoOneMove(board)) is not None:
            moves.append((move.action, move.row, move.col))
            self.assertFalse(ai.doMove(board, move), "the rule opened a mine")
        self.assertEqual(moves, [("flag", 0, 1), ("flag", 0, 3), ("open", 0, 2)])

    def test_vertical_pattern(self):
        # Same pattern turned on its side: column 0 covered, mines at rows 1 and 3.
        board = make_board({(1, 0), (3, 0)}, {(r, 0) for r in range(10)})
        moves = []
        while (move := ai.oneTwoOneMove(board)) is not None:
            moves.append((move.action, move.row, move.col))
            ai.doMove(board, move)
        self.assertEqual(moves, [("flag", 1, 0), ("flag", 3, 0), ("open", 2, 0)])

    def test_not_used_when_other_side_is_covered(self):
        # A covered cell on the far side means the mines could be there instead,
        # so the rule must not guess.
        board = make_board(ROW_MINES, TOP_ROW | {(2, 2)})
        self.assertIsNone(ai.oneTwoOneMove(board))

    def test_hard_ai_solves_pattern_safely(self):
        # Hard mode (medium rules first, then 1-2-1) clears the whole covered row
        # without opening a mine. Medium rules may add moves in between once the
        # first flag is down, so loop until the row is done instead of counting.
        board = make_board(ROW_MINES, TOP_ROW)
        for _ in range(20):
            if all(board.grid[0][c].is_flagged or board.grid[0][c].is_revealed for c in range(10)):
                break
            move = ai.hardAI(board)
            self.assertFalse(ai.doMove(board, move), f"hard AI hit a mine at {move.row},{move.col}")
        self.assertTrue(board.grid[0][1].is_flagged and board.grid[0][3].is_flagged)
        self.assertTrue(board.grid[0][2].is_revealed)


if __name__ == "__main__":
    unittest.main()
