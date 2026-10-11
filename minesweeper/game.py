"""
================================================================================
Module:        minesweeper.game
Description:   Interactive terminal front end for Minesweeper. Asks the player
               for a mine count, then repeatedly draws the board, reads a
               command, and applies it until the player wins, loses, or quits.

Functions:     prompt_mine_count() -> int
               play()              -> None

Inputs:        Keyboard input from the player:
                 - mine count (10-20)
                 - commands: 'r <cell>' reveal, 'f <cell>' flag, 'q' quit
Outputs:       Board drawings and status messages printed to the terminal

External Sources:
               Generated with the assistance of Claude (Anthropic, model
               Claude Opus 5) via Claude Code. Reviewed by the author.

Author:        Caleb Hite & Kai Barnhart
Created:       2026-09-14
================================================================================
"""

from . import config
from .board import Board, parse_coordinate
from .boardsize import BoardSize
from . import ai

def prompt_mine_count() -> int:
    """Ask the player how many mines to use, repeating until the answer is valid.

    Inputs:  Keyboard input (whole number).
    Outputs: int - mine count between BoardSize.SMALL.min_mines and BoardSize.SMALL.max_mines.
    """
    # Sourced: Claude AI
    # Loop until the input is a whole number inside the allowed range.
    while True:
        raw = input(f"Number of mines ({BoardSize.SMALL.min_mines}-{BoardSize.SMALL.max_mines}): ").strip()
        if raw.isdigit() and BoardSize.SMALL.min_mines <= int(raw) <= BoardSize.SMALL.max_mines:
            return int(raw)
        print(f"Please enter a whole number from {BoardSize.SMALL.min_mines} to {BoardSize.SMALL.max_mines}.")


def play() -> None:
    """Run one full game of Minesweeper in the terminal.

    Inputs:  Keyboard commands from the player (see module prologue).
    Outputs: None. Prints the board each turn and a final win/loss message.
    """
    


    # Sourced: Claude AI
    # --- Setup: create a covered, unflagged board (mines placed on first reveal) ---
    # Terminal play always uses the classic 10x10 board.
    board = Board(BoardSize.SMALL, prompt_mine_count())

    #2
    # Default to a solo game so answering "N" still leaves these defined.
    ai_enabled = False
    aiMode = "easy"
    aiInteractive = input("Enable AI Interactive Mode? (Y or N): ")
    if aiInteractive == "Y" or aiInteractive == "y":
        ai_enabled = True
        aiMode = input("Choose A Mode (easy, medium, or hard): ").strip().lower()
        if aiMode not in ("easy", "medium", "hard"):
            print("Entered Invalid Mode. Playing Easy")
            aiMode = "easy"
    
    playerTurn = True

    print("Commands: 'r A1' to reveal, 'f A1' to flag/unflag, 'q' to quit.")
    if ai_enabled:
       print(f"AI opponent enabled in {aiMode} mode.")

    # --- Main game loop: draw, read command, update ---
    while True:
        print()
        print(board.render())
        # Status indicator and remaining mine count, both required by the
        # project specification. Inside this loop the game is always "Playing";
        # the win and loss branches below print the final status.
        #2 status = "Playing" if not board.is_cleared() else "Victory"
        print(f"Status: Playing   Mines remaining: {board.flags_remaining()}")


        #2
        if ai_enabled and not playerTurn:
            move = ai.chooseMove(board, aiMode)
            if move is None:
                print("AI has no moves left.")
                print("Status: Victory- you cleared every safe cell")
                return
            label = f"{move.action} {chr(ord('A') + move.col)}{move.row + 1}"
            hit = ai.doMove(board, move)
            print(f"AI chose {label}.")
            if hit:
                print()
                print(board.render(show_mines=True))
                print("Status: Game Over: Loss - AI uncovered a mine.")
                return
            if board.is_cleared():
                print()
                print(board.render(show_mines=True))
                print("Status: Victory - AI cleared every safe cell!")
                return
            playerTurn = True
            continue

        

        # Split input into [command, coordinate]; ignore blank lines.
        parts = input("> ").strip().split()
        if not parts:
            continue

        # Quit command.
        if parts[0].lower() == "q":
            print("Goodbye!")
            return
 
        # Anything other than 'r <cell>' or 'f <cell>' is a usage error.
        if len(parts) != 2 or parts[0].lower() not in ("r", "f"):
            print("Usage: r <cell> | f <cell> | q")
            continue

        # Convert 'A1'-style text to grid indices; report bad coordinates.
        try:
            row, col = parse_coordinate(parts[1], board)
        except ValueError as exc:
            print(exc)
            continue

        # Flag command: toggle and go back to the top of the loop.
        if parts[0].lower() == "f":
            board.toggle_flag(row, col)
            continue

        # Reveal command: check for a loss first, then a win.
        if board.reveal(row, col):
            print()
            print(board.render(show_mines=True))
            print("Status: Game Over: Loss - you uncovered a mine.")
            return
        if board.is_cleared():
            print()
            print(board.render(show_mines=True))
            print("Status: Victory - you cleared every safe cell!")
            return

        #2
        if aiInteractive:
            playerTurn = False
