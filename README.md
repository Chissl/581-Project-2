# Minesweeper — EECS 581 Project 2

A single-player Minesweeper game with preset grid sizes: Small (10\*10), Medium (15\*15), Large (25*25) with a
user-selected mine count. Ships with a clickable graphical window (Tkinter) and a
terminal version.

**Course:** EECS 581 Software Engineering II, Fall 2026 — Professor Hossein Saiedian

---

## Running the game

Requires Python 3.9+ (developed and tested on 3.11). No third-party packages.

```bash
python main.py            # graphical window (default)
python main.py --text     # terminal version
python main.py --aiAS --hard   # watch the AI solve a game by itself (--easy / --medium / --hard)
```

If Tkinter is missing from your Python installation, `main.py` explains how to install it
and falls back to the terminal version rather than crashing.

### Running the tests

```bash
python -m unittest discover -s tests -t .
```

---

## How to play

### Graphical version

| Action | Effect |
| --- | --- |
| Left-click | Uncover a cell |
| Right-click (or Ctrl-click on macOS) | Place / remove a flag |
| Double-click a number | "Chord" — open all unflagged neighbors once the flag count matches the number |
| **Mines** spinner | Choose 10–20 mines (enforced by the control, so an invalid count can never be entered) |
| **Board Size** list | Small (10x10), Medium (15x15) or Large (25x25); takes effect on **New Game** |
| **AI opponent** checkbox | Turn the AI on or off (starts a new game) |
| AI mode menu | Pick **easy**, **medium** or **hard**; takes effect on **New Game** |
| **Auto-solve** | The AI plays the current board by itself in the chosen mode; press **Stop** (or **New Game**) to take over again |
| **New Game** | Start a fresh board |

The window shows **Mines remaining** (total mines minus flags placed), an elapsed timer, and
a status indicator reading **Playing**, **Victory**, or **Game Over: Loss**.

### Terminal version

```
Commands: 'r A1' to reveal, 'f A1' to flag/unflag, 'q' to quit.
```

Coordinates are case-insensitive (`A1`, `a1`, and ` A1 ` are all accepted). Invalid
coordinates and malformed commands print an explanation and re-prompt instead of exiting.

Board symbols: `#` covered · `F` flagged · `.` uncovered with zero adjacent mines ·
`1`–`8` adjacent mine count · `*` mine (shown at game over).

---

## AI solver

The AI lives in `minesweeper/ai.py`. It plays on the same board as the player and can run in
two ways:

- **Interactive mode**: you and the AI take turns on the same board.
  - In the window, tick **AI opponent** and pick a mode. After each cell you uncover, the AI
    makes one move about half a second later. Clicks are ignored while it is the AI's turn.
  - In the terminal (`python main.py --text`), answer `Y` to "Enable AI Interactive Mode?" and
    type a mode. The AI's move is printed after each of yours (e.g. `AI chose flag F1.`).
- **Auto-solve mode**: the AI plays the whole game with no player.
  - In the window, pick a mode and press **Auto-solve**. It works on any board size and mine
    count, makes a move every fraction of a second so you can watch, and ends on a win or a
    mine. The button turns into **Stop**; you can stop it and finish the game yourself. Your
    clicks are ignored while it runs.
  - From the command line, `python main.py --aiAS --easy|--medium|--hard` plays a 10x10,
    10-mine game, prints the board after every AI move, then prints `AI won!` or `AI lost.`

Each move is either *open* a cell or *flag* a cell. If the AI opens a mine, the game is lost;
if it uncovers the last safe cell, the game is won.

| Mode | How it picks a move |
| --- | --- |
| **Easy** | Opens a random cell that is still covered and not flagged. |
| **Medium** | Looks at every uncovered number and applies two rules. **Rule 1:** if the number equals its covered neighbors (flagged ones included), all of them are mines, so flag one. **Rule 2:** if the number equals its flagged neighbors, the rest are safe, so open one. If neither rule applies, it falls back to a random open like Easy. |
| **Hard** | Tries Medium's two rules first. If neither applies, it looks for three uncovered cells in a row reading **1-2-1**: it flags the two outer covered cells beside the row and opens the covered cell beside the middle. If there is no such pattern, it falls back to a random open. |

Easy is pure guessing and almost always loses. Medium and Hard win most 10x10 games and
roughly a third of games on the larger boards, where more random guesses are needed.

---

## Requirement coverage

| Requirement | Where it is implemented |
| --- | --- |
| 10x10 grid, columns A–J, rows 1–10 | `minesweeper/config.py` (`ROWS`, `COLS`, `COL_LABELS`) |
| Mine count user-specified, 10–20 | GUI spinner (`gui.py::_build_control_bar`); terminal prompt (`game.py::prompt_mine_count`); enforced in `Board.__init__` |
| Mines randomly placed at game start | `Board.place_mines` via `random.Random.sample` |
| First clicked cell (and neighbors) guaranteed mine-free | `Board.place_mines` builds a safe set; mines are placed lazily on the first real reveal. Neighbor safety toggled by `config.SAFE_NEIGHBORS_ON_FIRST_CLICK` |
| All cells start covered, no flags | `Cell` dataclass defaults |
| Uncovering a mine ends the game (loss) | `Board.reveal` returns `True`; handled by `gui.py::finish` / `game.py::play` |
| Number 0–8 of adjacent mines | `Cell.adjacent_mines`, computed in `Board.place_mines` |
| Zero-adjacent cells recursively uncover neighbors | Iterative flood fill in `Board.reveal` |
| Toggle flags on covered cells | `Board.toggle_flag` |
| Flagged cells cannot be uncovered until unflagged | Guard at the top of `Board.reveal` |
| Display remaining flag/mine count | `Board.flags_remaining`, shown in both front ends |
| Grid display of covered / flagged / uncovered states | `gui.py::_draw_cell`; `Cell.symbol` + `Board.render` |
| Status indicator | Status label in the GUI; `Status:` line in the terminal version |
| Loss reveals all mines | `refresh(show_mines=True)` / `render(show_mines=True)` |
| Win by uncovering all non-mine cells | `Board.is_cleared` |

---

## Repository contents

```
main.py                     Entry point; picks the GUI or terminal front end
minesweeper/
  __init__.py               Package marker
  config.py                 Column labels and the first-click rule
  boardsize.py              Small / Medium / Large board sizes and their mine limits
  ai.py                     AI solver: Easy, Medium and Hard move choice, auto-solve mode
  cell.py                   Cell dataclass (one square's state + display symbol)
  board.py                  Board Manager + Game Logic: grid, mines, reveal, flags, win check
  game.py                   Terminal front end (UI + input handler)
  gui.py                    Tkinter front end (UI + input handler)
tests/
  test_board.py             Coordinate parsing, board setup, first-click safety
  test_game_logic.py        Gameplay, flagging, win/loss, bounds, randomized stress test
EECS 581 P1 Team Meeting Log.docx
EECS 581 Project 1 Estimated Person Hours.pages
```

---

## Source attribution

Portions of this project were generated with the assistance of **Claude (Anthropic, model
Claude Opus 5)** via Claude Code, prompted with the project requirements, and reviewed by the
authors. Every source file carries a prologue comment naming its author, creation date, and
external sources; in-code comments marked `# Sourced: Claude AI` indicate AI-assisted blocks.

Standard-library documentation referenced: [`random`](https://docs.python.org/3/library/random.html),
[`dataclasses`](https://docs.python.org/3/library/dataclasses.html),
[`tkinter`](https://docs.python.org/3/library/tkinter.html),
[`unittest`](https://docs.python.org/3/library/unittest.html).
The flood-fill reveal uses the standard iterative depth-first search technique (common
algorithm; no specific source copied). The cell number colors follow the classic Minesweeper
palette.

## Project 2 Team
Will Godderz
Jaydee Brown
Zackary Rhodes
Didier Carrillo
Aidan Bergeman
Ethan Gao
Lea Sulthana Syed


