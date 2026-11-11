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

## The same tests with GoogleTest

`test/test_gtest.cpp` holds the lab tests written with GoogleTest: table-driven
(parameterized) tests for F1, F2 and F3, integration tests, and a fault-injection
test for the defensive `default` branch. Every test records the requirement it
verifies, and `tools/trace.py` turns the XML results into a requirement → test table.

| Command | What you see |
|---|---|
| `make gtest` | every suite: line, branch and condition (MC/DC) coverage, traceability table |
| `make gtest FILTER='F1Statement*'` | three extended frames: 100% of `can_frame_is_valid` lines, not every branch |
| `make gtest FILTER='F1Statement*:F1Branch*' BUG=1` | full F1 coverage on the planted bug, every test passes |
| `make gtest FILTER='F1Limits*' BUG=1` | boundary tests at and beyond each limit find it (2 failures) |
| `make gtest FILTER='F2Mcdc*'` | five tests for four conditions: every condition outcome covered |
| `make gtest FI=1` | fault injection forces a corrupted CAN state and reaches the `default` branch: 100% |

Suites: `F1Statement`, `F1Branch`, `F1Limits`, `F2Mcdc`, `F2Limits`, `F3Limits`,
`Integration`, `FaultInjection` (only with `FI=1`). Several suites: separate them with `:`.

## Lab app

The exercises run in the browser. Enter your name, group and the variant code you received in the lab.

- SW TCA (code coverage): **https://madalinatolontan1-ai.github.io/sw-tca-lab/sw/** (source: `docs/sw/index.html`)
- HW TCA (production test coverage): **https://madalinatolontan1-ai.github.io/sw-tca-lab/hw/** (source: `docs/hw/index.html`)
- FMEA (DFMEA, 7 AIAG-VDA steps): **https://madalinatolontan1-ai.github.io/sw-tca-lab/fmea/** (source: `docs/fmea/index.html`)

## Report collection

The apps can send each report to a Google Apps Script collector (Drive folder + Google Sheet). Setup: `tools/report-collector/README.md`; the endpoint goes in `docs/report-config.js`.

## Files

- `src/can_node.h`, `src/can_node.c` – code under test
- `test/test_demo.c` – demo test sets (plain C)
- `test/test_gtest.cpp` – the same tests with GoogleTest; `tools/trace.py` – requirement traceability
- `Makefile` – build with coverage, run the tests, generate the report
- `docs/sw/index.html`, `docs/hw/index.html`, `docs/fmea/index.html` – the lab apps (GitHub Pages); `docs/index.html` links both

---

### Pe scurt, în română

Demo pentru laboratorul de *Analiza acoperirii testelor software*. Deschide un
Codespace (**Code → Codespaces → Create codespace on main**), rulează în terminal
una dintre comenzile din tabel, apoi `make serve` și apasă **Open in Browser**. Fiecare student
lucrează în propriul Codespace; modificările tale nu afectează repository-ul.

Aceleași teste scrise cu GoogleTest: `make gtest` (toate), `make gtest FILTER='F1Limits*' BUG=1`
(testele la limită găsesc greșeala), `make gtest FI=1` (injectarea de defecte atinge ramura default).
Fiecare test are cerința lui, iar la final apare tabelul cerință → test.

Aplicațiile de laborator: SW TCA la `/sw/`, HW TCA la `/hw/`, FMEA la `/fmea/` (linkurile de mai sus).
