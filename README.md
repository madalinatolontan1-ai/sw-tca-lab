# SW TCA lab – structural code coverage demo

Demo for the *Software Test Coverage Analysis* lab (UPT, Faculty of Electronics,
Telecommunications and Information Technologies).

The code is part of the firmware of a CAN node that sends front-radar data
(MCP2551 transceiver). It is compiled with **GCC 14** and measured with **gcov /
gcovr**, which report statement, branch and condition (MC/DC) coverage.

## Start (in the browser, nothing to install)

1. Click **Code → Codespaces → Create codespace on main**.
2. Wait until the setup finishes (GCC 14 and gcovr are installed automatically).
3. In the terminal, run one of the commands below.
4. Run `make serve` and click **Open in Browser** in the pop-up (or open the **Ports** tab and click the globe icon next to port 8080). Stop the server with `Ctrl+C` before running the next report.

## Commands

| Command | What you see |
|---|---|
| `make report SET=f1_statement` | 100% statements, but one branch is never taken |
| `make report SET=f1_branch` | statements and branches covered |
| `make report SET=f1_branch BUG=1` | same coverage on code with a planted bug: every test passes |
| `make report SET=f1_limits BUG=1` | boundary tests derived from the requirements find the bug |
| `make report SET=f2_branch` | every decision is true and false, but MC/DC is not reached |
| `make report SET=int_one` | function and call coverage with one integration test |

## Files

- `src/can_node.h`, `src/can_node.c` – code under test
- `test/test_demo.c` – demo test sets
- `Makefile` – build with coverage, run the tests, generate the report

---

### Pe scurt, în română

Demo pentru laboratorul de *Analiza acoperirii testelor software*. Deschide un
Codespace (**Code → Codespaces → Create codespace on main**), rulează în terminal
una dintre comenzile din tabel, apoi `make serve` și apasă **Open in Browser**. Fiecare student
lucrează în propriul Codespace; modificările tale nu afectează repository-ul.
