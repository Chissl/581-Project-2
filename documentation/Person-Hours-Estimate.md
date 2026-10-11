# Person-Hours Estimate: EECS 581 Project 2

**Project:** Enhance an inherited Minesweeper system (Python / Tkinter)
**Prepared by:** Will Godderz (Project Manager), with drafting help from Claude (Anthropic)
**Team size:** 7

**Result: about 140 person-hours (≈ 56 use case points × 2.5 hours per point), or about 4 weeks for the team.**

---

## 1. Method

We used the **Use Case Points (UCP)** method from lecture ("SE effort and cost estimation approaches"). It turns the number and complexity of use cases and actors into an effort figure in five steps:

1. **UUCW:** weight each use case by its number of steps (Simple ≤ 3 steps = 5, Average 4–7 = 10, Complex > 7 = 15).
2. **UAW:** weight each actor (Simple, another system = 1; Average, API user = 2; Complex, GUI user = 3).
3. **UUCP** = UUCW + UAW.
4. Adjust for **technical (TCF)** and **environmental (ECF)** factors:
   TCF = 0.6 + 0.01 × Σ(technical rating × weight)
   ECF = 1.4 − 0.03 × Σ(environmental rating × weight)
5. **Effort** = UUCP × TCF × ECF × productivity factor (hours per UCP).

We chose UCP because the Project 2 requirements are stable and already written as player-facing behaviours (game play, AI modes, a custom feature), so they map directly onto use cases. We also cross-checked the result against how many hours the team can actually give the project each week (Section 6).

**Scope counted:** only work Project 2 requires: making the inherited Project 1 features fully work, the AI solver (Easy, Medium, Hard, interactive and auto-solve), our custom feature (board sizes), and documentation. Code we inherited and didn't have to change isn't counted.

---

## 2. Step 1: Use case weights (UUCW)

| # | Use case | Main steps | Steps | Complexity | Weight |
|---|---|---|---|---|---|
| UC1 | **Play a standard game** (verify and fix inherited Project 1 features) | Start game → reveal cell → flag cell | 3 | Simple | 5 |
| UC2 | **Choose a board size** (custom feature) | Open size list → pick Small/Medium/Large → mine range updates → press New Game → grid is rebuilt | 5 | Average | 10 |
| UC3 | **Play against the AI** (interactive mode) | Enable AI → choose mode → player moves → AI waits → AI moves → board redraws → repeat until win/loss | 7 | Average | 10 |
| UC4 | **Watch the AI auto-solve** | Choose mode → press Auto-solve → AI moves on a timer → board redraws → stops on win/loss or Stop | 5 | Average | 10 |
| UC5 | **AI picks an Easy move** | List covered, unflagged cells → pick one at random → open it | 3 | Simple | 5 |
| UC6 | **AI picks a Medium move** | Scan revealed numbers → rule 1 (covered neighbours = number → flag) → rule 2 (flags = number → open) → else random → apply move | 5 | Average | 10 |
| UC7 | **AI picks a Hard move** | Rule 1 → rule 2 → scan rows and columns for 1-2-1 → check only one side is covered → flag outer mine 1 → flag outer mine 2 → open safe middle → else random → apply move | 9 | Complex | 15 |
| | | | | **UUCW** | **65** |

## 3. Step 2: Actor weights (UAW)

| Actor | Type | Complexity | Weight |
|---|---|---|---|
| Player | Uses the graphical window (Tkinter) | Complex | 3 |
| AI solver | Another component of the system acting on the board | Simple | 1 |
| | | **UAW** | **4** |

## 4. Step 3: Unadjusted UCP

**UUCP = UUCW + UAW = 65 + 4 = 69**

---

## 5. Step 4: Technical and environmental factors

Each factor is rated 0 (irrelevant) to 5 (essential) and multiplied by the standard UCP weight for that factor.

### Technical Complexity Factor (TCF)

| No. | Factor | Weight | Rating | Score | Reason |
|---|---|---|---|---|---|
| T1 | Distributed system | 2 | 0 | 0 | Single desktop program |
| T2 | Performance objectives | 1 | 2 | 2 | AI and redraws must stay smooth on a 25×25 board |
| T3 | End-user efficiency | 1 | 3 | 3 | Rubric requires an interface needing no manual |
| T4 | Complex internal processing | 1 | 4 | 4 | AI rule logic and 1-2-1 pattern detection |
| T5 | Reusability | 1 | 2 | 2 | Board and AI should be reusable by future teams |
| T6 | Easy to install | 0.5 | 1 | 0.5 | Standard Python, no extra packages |
| T7 | Easy to use | 0.5 | 4 | 2 | Demo is graded on intuitiveness |
| T8 | Portability | 2 | 2 | 4 | Must run on whichever laptop is used for the demo |
| T9 | Easy to change | 1 | 3 | 3 | Maintenance project; next team must extend it |
| T10 | Concurrency | 1 | 1 | 1 | Timer and timed AI moves share the GUI event loop |
| T11 | Special security features | 1 | 0 | 0 | None |
| T12 | Third-party access | 1 | 0 | 0 | None |
| T13 | Special training needs | 1 | 0 | 0 | None |
| | | | **Σ** | **21.5** | |

**TCF = 0.6 + 0.01 × 21.5 = 0.815**

### Environmental Complexity Factor (ECF)

| No. | Factor | Weight | Rating | Score | Reason |
|---|---|---|---|---|---|
| E1 | Familiarity with UCP / the process | 1.5 | 1 | 1.5 | First time using UCP |
| E2 | Application experience | 0.5 | 3 | 1.5 | All of us built Minesweeper in Project 1, but not this codebase |
| E3 | Object-oriented experience | 1 | 3 | 3 | Comfortable with Python classes |
| E4 | Lead analyst capability | 0.5 | 3 | 1.5 | Technical lead knows the AI requirements well |
| E5 | Motivation | 1 | 4 | 4 | Graded project with a demo |
| E6 | Stable requirements | 2 | 4 | 8 | Requirements are fixed in the assignment |
| E7 | Part-time staff | −1 | 5 | −5 | Every member is a part-time student |
| E8 | Difficult programming language | −1 | 1 | −1 | Python is familiar |
| | | | **Σ** | **13.5** | |

**ECF = 1.4 − 0.03 × 13.5 = 0.995**

---

## 6. Step 5: Final effort

**Adjusted UCP = UUCP × TCF × ECF = 69 × 0.815 × 0.995 ≈ 56.0 UCP**

### Productivity factor: 2.5 person-hours per UCP

The lecture example uses 20 hours per UCP, a figure meant for a professional team building a new system across its whole life cycle (requirements through deployment). Ours is much lower because:

- **Most of the system already exists.** We inherited a working game (~2,000 lines including tests), so much of each use case is reading and changing code rather than writing it.
- **Small scope and simple environment.** It's one Python program with no database, network or deployment.
- **Cross-check against team capacity (top-down).** Seven members giving about 5 hours a week over the four working weeks of the project is 7 × 5 × 4 = 140 hours. 140 ÷ 56 UCP = 2.5 hours per UCP, so the UCP size and the team's capacity agree.

**Estimated effort = 56.0 UCP × 2.5 hours/UCP ≈ 140 person-hours**

---

## 7. Breakdown

### By use case
Each use case's share of the 140 hours is proportional to its weight. Actor effort is spread across all use cases.

| Use case | Weight | Hours |
|---|---|---|
| UC1 Play a standard game (verify/fix) | 5 | 11 |
| UC2 Choose a board size | 10 | 21.5 |
| UC3 Play against the AI | 10 | 21.5 |
| UC4 Watch the AI auto-solve | 10 | 21.5 |
| UC5 Easy AI move | 5 | 11 |
| UC6 Medium AI move | 10 | 21.5 |
| UC7 Hard AI move | 15 | 32 |
| **Total** | **65** | **140** |

### By activity

| Activity | Hours | Basis |
|---|---|---|
| Coding | 50 | AI modes, board sizes, GUI controls, bug fixes |
| Testing | 30 | Unit tests, AI correctness checks, stress testing before the demo |
| Meetings | 28 | 4 weekly team meetings × 1 hour × 7 members |
| Documentation | 32 | Code prologues and comments, architecture, UML, estimate, hours log |
| **Total** | **140** | |

### By team member (planned)

| Member | Role | Main work | Planned hours |
|---|---|---|---|
| Will Godderz | Project Manager | Planning, coordination, estimate and hours tracking, merging work | 20 |
| Jaydee Brown | Frontend Developer | GUI controls for board size, AI opponent and Auto-solve | 22 |
| Lea Syed | Quality Testing (UI & Input) | UI and input testing, stress testing, bug reports | 20 |
| Aidan Bergeman | Version Control & Code Quality | Branches and merges, code review, comments and prologues | 18 |
| Zackary Rhodes | Backend Developer | AI rule logic (Medium / Hard) | 20 |
| Ethan Gao | Backend Developer | Board and board-size logic, AI support code | 20 |
| Didier Carrillo | Technical Lead | AI design and integration, technical decisions | 20 |
| | | **Total** | **140** |

---

## 8. Duration and cost

**Duration.** Team capacity is 7 members × ~5 hours/week = 35 person-hours per week, so 140 ÷ 35 = **4 weeks**. That fits the window between receiving the project (September 20, 2026) and the code freeze.

**Cost** (for completeness, using the lecture's blended rate of $75/hour): 140 × $75 = **$10,500**.

---

## 9. Assumptions and risks

- **Availability.** Each member averages about 5 hours a week. Exams in other courses are the biggest risk to this.
- **Inherited code quality.** We assumed the Project 1 code mostly works. Hidden bugs in it would push UC1 above its estimate.
- **Merge problems.** Several people work on the same files (`gui.py`, `ai.py`), so merges may take extra time.
- **Lecture hours aren't counted.** EECS 581 lectures are excluded, as the assignment requires.

Actual hours are recorded day by day in a separate document in this folder.
