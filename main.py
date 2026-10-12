"""
================================================================================
Module:        main
Description:   Entry point for the Minesweeper game. Run `python main.py` from
               the project root to open the clickable game window, or
               `python main.py --text` to play the original terminal version.
               If Tkinter is missing from the Python installation, the game
               explains how to fix it and falls back to the terminal version.

Functions:     main() -> None

Inputs:        One optional command-line flag: --text (or -t) for terminal play
Outputs:       A game window, or terminal output in text mode

External Sources:
               Generated with the assistance of Claude (Anthropic, model
               Claude Opus 5) via Claude Code.
               Also Generated with the assistance of DeepSeek(High-Flyer,
               model DeepSeek-V4.1-Flash).
               Reviewed by the author.

================================================================================
"""

import sys
from minesweeper.ai import autoSolve

def main() -> None:
    """Start the graphical game, or the terminal game if --text is given.

    Inputs:  Command-line arguments from sys.argv.
    Outputs: None. Runs until the player quits or closes the window.
    """
    #Sourced: DeepSeek AI
    #Text mode; Add --aiAS flag to turn on the Auto Solver
    if "--aiAS" in sys.argv[1:]:
        mode = "easy" #default to easy mode
        mineAmount = 10 #default to 10 mines
        if "--easy" in sys.argv[1:]: #if add "--easy" flag set mode to easy
            mode = "easy"
        if "--medium" in sys.argv[1:]: #if add "--medium" flag set mode to medium
            mode = "medium"
        if "--hard" in sys.argv[1:]: #if add "--hard" flag set mode to hard
            mode = "hard"
        if "--mines=15" in sys.argv[1:]:
            mineAmount = 15
        if "--mines=20" in sys.argv[1:]:
            mineAmount = 20

        won = autoSolve(mineCount = mineAmount, mode=mode, verbose=True) #run autoSolve
        #If won returns True, print victory message else print loss message
        print("AI won!" if won else "AI lost.") 
        return #Exit out of main
    
    # Sourced: Claude AI
    # Text mode is opt-in; the clickable window is the default experience.
    if any(arg in ("--text", "-t") for arg in sys.argv[1:]):
        from minesweeper.game import play

        play()
        return

    # Tkinter ships with most Python builds but can be missing (for example a
    # Homebrew Python without python-tk). Explain the fix instead of crashing.
    try:
        from minesweeper.gui import run
    except ImportError:
        print("Tkinter is not available in this Python installation.")
        print("Install it (macOS: 'brew install python-tk', Ubuntu: "
              "'sudo apt install python3-tk') or run 'python main.py --text'.")
        print("Falling back to the terminal version.\n")
        from minesweeper.game import play
        play()
        return

    run()


# Sourced: Claude AI
# Only start the game when this file is run directly, not when it is imported.
if __name__ == "__main__":
    main()
