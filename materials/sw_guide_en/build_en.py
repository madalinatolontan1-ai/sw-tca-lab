# Builds the SW TCA lab guide (EN) as HTML for import into Google Docs.
# English version of "SW TCA – laborator (RO), structura HW", with the 13 Nov updates (no group field, no grading, consent, feedback).
import html, os
E = html.escape
SHA = os.environ.get("IMG_SHA", "main")
IMG = "https://raw.githubusercontent.com/madalinatolontan1-ai/sw-tca-lab/%s/docs/guide-img/sw-en/" % SHA
APP = "https://madalinatolontan1-ai.github.io/sw-tca-lab/sw/"
REPO = "https://github.com/madalinatolontan1-ai/sw-tca-lab"
out = []
def h(x): out.append('<h2>%s</h2>' % E(x))
def h3(x): out.append('<h3>%s</h3>' % E(x))
def p(x, raw=False): out.append('<p>%s</p>' % (x if raw else E(x)))
def pn(x, raw=False): out.append('<p class="n">%s</p>' % (x if raw else E(x)))
def ol(items, kind="1"): out.append('<ol type="%s">%s</ol>' % (kind, "".join("<li>%s</li>" % E(i) for i in items)))
def table(head, rows, center_cols=(), first_bold=True, size=10):
    th = "".join("<th>%s</th>" % E(x) for x in head)
    trs = []
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            v = E(str(c)); v = "<b>%s</b>" % v if (first_bold and i == 0) else v
            tds.append(("<td align=center>%s</td>" if i in center_cols else "<td>%s</td>") % v)
        trs.append("<tr>%s</tr>" % "".join(tds))
    out.append('<table class="s%d"><tr>%s</tr>%s</table><p></p>' % (size, th, "".join(trs)))
def code(lines):
    out.append('<table style="border-collapse:collapse;width:100%%;border:1px solid #000">%s</table><p></p>' % "".join(
        '<tr><td style="width:5%%;text-align:right;color:#999;font-family:\'Courier New\';font-size:9pt;padding:1pt 4pt;border:none">%s</td><td style="font-family:\'Courier New\';font-size:10pt;color:#1A3F7F;padding:1pt 4pt;border:none;white-space:pre">%s</td></tr>' % (n, E(l).replace(" ", "&nbsp;")) for n, l in lines))
def img(f, w, cap):
    out.append('<p style="text-align:center;text-indent:0"><img src="%s%s" width="%d"></p><p style="text-align:center;text-indent:0;font-size:10pt"><i>%s</i></p>' % (IMG, f, w, E(cap)))

out.append("""<html><head><meta charset="utf-8"><style>
body,p,li,td,th{font-family:'Times New Roman';font-size:12pt}
p{text-align:justify;text-indent:1.25cm;margin:0 0 6pt 0}
p.n{text-indent:0}
li{text-align:justify;margin:0 0 3pt 0}
h1{font-family:Aptos,Arial;font-size:20pt;color:#0F4761;font-weight:normal;text-align:center}
h2{font-family:Aptos,Arial;font-size:14pt;color:#0F4761;font-weight:normal;margin:16pt 0 6pt 0}
h3{font-family:Aptos,Arial;font-size:12pt;color:#156082;font-weight:normal;margin:12pt 0 4pt 0}
table{border-collapse:collapse;width:100%}
th{background:#000000;color:#FFFFFF;font-size:10pt;border:1px solid #000;padding:2pt 4pt}
td{font-size:10pt;border:1px solid #000;padding:2pt 4pt}
</style></head><body>""")
out.append('<h1>Software Test Coverage Analysis (SW TCA)</h1>')

h("What is SW TCA?")
p("In HW TCA the board is designed correctly, but every manufactured unit can come out with its own defect (a missing part, an open solder joint), so every board goes through the production tests. Software is not manufactured unit by unit: every module shipped contains exactly the same program. If a programmer wrote >= instead of >, the mistake is in every module, from day one. ISO 26262 calls these mistakes systematic faults; for software, all faults are systematic.")
p("A software fault cannot be caught in production, because all units are identical. The code is verified once, during development, and again at every change (regression testing). Software Test Coverage Analysis (SW TCA) answers the question: how completely have the tests exercised the code and the requirements? Is there a line that no test has executed? If there is, any mistake in it is certain to reach the customer.")
p("ISO 26262 does not set a percentage: it asks for a defined and justified target value (ISO 26262-6, 9.4.4, NOTE 1: a missing or too low target without a justification is insufficient). In industrial practice the usual target is 100%, required by vehicle manufacturers in their customer-specific requirements and by the aviation standard DO-178C. In the lab we also work with 100%. What cannot be covered by tests is justified in writing: why it cannot be reached and why that is acceptable. It is the counterpart of the residual risk in HW TCA.")
p("Coverage is measured with metrics. The ones used in the lab are:")
table(["Metric", "What it checks", "Good at finding", "Limits"], [
    ["Statement coverage", "Every statement has been executed at least once.", "code never executed (a return, a branch with statements)", "does not see the false branch of an if without else"],
    ["Branch coverage", "Every decision (if, switch) has been both true and false.", "untested outcomes of a decision", "does not see the conditions inside a decision with && or ||"],
    ["MC/DC", "Every condition in a decision changes the result on its own.", "conditions with no effect or written wrongly", "does not choose boundary values"],
    ["Function / call coverage", "Every function has been called; every call site has been executed.", "functions or calls not tested at integration", "says nothing about the inside of the function"]])
p("None of the metrics says whether the result is correct. Only the expected result of the test, taken from the requirement, does that.")
h3("Exercise 1 (verbal)")
p("For each problem below, say which metric reveals it, or whether none can see it:")
ol(["a return that no test has executed;", "an if without else, tested only with the condition true;", "a condition in a decision with || that never changed the result;",
    "a function that no integration test calls;", "a comparison written >= instead of >, tested only with values far from the boundary."], "a")

h("What the standards require")
p("The functional safety standard for road vehicles, ISO 26262 (2018 edition), part 6, recommends the metrics according to the ASIL (Automotive Safety Integrity Level, from A to D, D being the strictest). ++ means highly recommended (in practice mandatory; if it is not applied, a justification is written), + means recommended.")
table(["Metric", "ASIL A", "ASIL B", "ASIL C", "ASIL D"], [
    ["Statement coverage (unit, table 9)", "++", "++", "+", "+"], ["Branch coverage (unit, table 9)", "+", "++", "++", "++"],
    ["MC/DC (unit, table 9)", "+", "+", "+", "++"], ["Function coverage (integration, table 12)", "+", "+", "++", "++"],
    ["Call coverage (integration, table 12)", "+", "+", "++", "++"]], center_cols=(1, 2, 3, 4))
p("Entries 1a, 1b and 1c of table 9 are alternatives: a combination suited to the ASIL is chosen, with a justification. At ASIL B, statement and branch coverage are ++, while MC/DC is only +. Structural coverage at integration (clause 10.4.5, table 12) applies to ASIL A and B only as a recommendation: the standard writes „ASIL (A), (B), C and D”, and the brackets mean a recommendation. In the lab we practise it as good practice. If the coverage reached is considered insufficient, the standard requires either additional tests or a justification based on other methods (clause 9.4.4). Tests are written from the requirements, and Automotive SPICE, the model vehicle manufacturers use to assess their suppliers, requires every test to be linked to the requirement it verifies.")
h3("Exercise 2 (verbal)")
p("The radar in the lab is ASIL B. Which metrics are ++ at ASIL B? And at ASIL A and ASIL D? Why does statement coverage drop to + at ASIL C and D? What happens if, at ASIL D, MC/DC does not reach 100%?")

h("Case study: the firmware of the front radar's CAN node")
p("We work on the same generic automotive front radar as in HW TCA (lab assumption: ASIL B), which sends the list of detected objects over CAN at 500 kbit/s, every measurement cycle (about 72 ms). The firmware of the CAN node has four C functions. The code was written for the lab, following real rules: the CAN limits come from ISO 11898-1, and the sensor ranges are typical values for a long-range automotive radar. The app shows, for every value, where it comes from. One exception to keep in mind: in classic CAN a DLC of 9…15 is valid at protocol level and still means 8 data bytes. Rejecting a DLC greater than 8 (SWR-F1-01) is therefore a requirement of our application, chosen for robustness, not a rule of the CAN protocol.")
table(["Function", "What it does", "Inputs", "Output", "Requirements"], [
    ["F1 can_frame_is_valid", "Checks whether a CAN frame is valid: DLC at most 8 and the identifier within the 11-bit (standard) or 29-bit (extended) range.", "id, dlc, extended", "true / false", "SWR-F1-01…04"],
    ["F2 sensor_value_plausible", "Checks whether the radar value is within range and does not jump too much from the previous cycle.", "value, previous, first_sample", "true / false", "SWR-F2-01…04"],
    ["F3 can_error_state", "Determines the CAN controller state from the TEC and REC error counters.", "tec, rec", "ERROR_ACTIVE / ERROR_PASSIVE / BUS_OFF", "SWR-F3-01…03"],
    ["can_rx_handler (integration)", "Receives a frame and calls F3, F1 and F2.", "frame, sensor context, tec, rec", "RX_ACCEPTED / RX_REJECTED / RX_BUS_OFF", "SWR-INT-01…03"]])
p('How you work: you work in the web app <a href="%s">SW TCA Lab</a>, in the browser, with nothing to install. Enter your name and the variant code and press „Load variant”. In the lab you work on the demo variant V0. At home you do the same analysis on your own variant (V1–V6) and send the report, as described in the homework at the end. Every tab (F1, F2, F3, Integration) has the requirements, the code and the test table. Write the tests (the inputs, the expected result from the requirement and the requirement verified) and press „Run tests”. The code is coloured like a coverage report: the number next to a line shows how many times it ran, ##### means a line not executed, and the T and F labels show whether the decision was true or false. Every tab also has three aids: „Context: what the function does”, „How to do it” (the steps) and „Where the values come from” (where every constant in the code comes from). If you hold the mouse over a column name, a percentage or a #define line, the app explains what it means. Under the percentages, the lists „Statements not executed”, „Missing decision outcomes”, „Requirements without a valid test” and „Boundary values (BVA)” tell you which test is still missing. The app also checks every test against the requirements: if a test does not exercise the requirement it declares, or if the expected result contradicts the requirement, a warning appears under the test, and the warnings go into the report. A failing test is an incident (the term from ISO/IEC/IEEE 29119-1; ISO 26262-2, 5.4.3.2 requires a process for resolving anomalies). The app shows the probable cause: „the test”, if the expected result contradicts the requirement, or „the code”, if the test follows the requirement and is therefore a fault to analyse in the incident report.' % APP, raw=True)
p("The app is a teaching simulator, not a qualified tool. In a real project, coverage comes from a commercial coverage tool assessed according to ISO 26262-8, clause 11. First the tool impact (TI) is determined: a coverage tool does not insert mistakes into the code, but it can report coverage wrongly and so hide a missing test, so it is TI2. Then the likelihood that a tool error is detected is determined (TD1–TD3). The two give the tool confidence level (TCL1–TCL3); for TCL2 and TCL3 the tool is qualified, usually with the qualification kit offered by the vendor. Tests run on instrumented code, and ISO 26262-6, 9.4.4, NOTE 4 requires showing that the instrumentation does not change the results.")
img("f1_three_tests.png", 520, "F1 on V0, after three tests: the red F label at line 8 shows that the decision was never false.")
h3("Exercise 3 (in the app)")
p("Load variant V0. In F1 and F2, count the decisions and the conditions in the code and say which requirement each decision implements.")

h("Statement coverage and branch coverage")
p("A test follows a single path through the function. In F3, every return is the end of a different path, so 100% statement coverage needs at least three tests:")
code([(1, "if (tec > CAN_BUSOFF_LIMIT) {                    /* 255 */"), (2, "    return CAN_STATE_BUS_OFF;"), (3, "}"),
      (4, "if ((tec > CAN_PASSIVE_LIMIT) || (rec > CAN_PASSIVE_LIMIT)) {  /* 127 */"), (5, "    return CAN_STATE_ERROR_PASSIVE;"), (6, "}"), (7, "return CAN_STATE_ERROR_ACTIVE;")])
table(["Test", "tec", "rec", "Result", "Covers"], [["T1", "300", "0", "BUS_OFF", "line 2"], ["T2", "200", "0", "ERROR_PASSIVE", "line 5"], ["T3", "0", "0", "ERROR_ACTIVE", "line 7"]], center_cols=(1, 2))
p("Branch coverage requires every decision to be true once and false once. In F1, if (extended) { max_id = …; } has no else. If every test has extended = true, every statement runs (100% statement), but the standard frame has not been tested at all: the false branch has no statement of its own, so statement coverage does not see it. That is why branch coverage includes statement coverage, but not the other way round.")
p("Two details of F3 matter for coverage. The order: bus-off is checked before error passive; otherwise tec = 300 would come out ERROR_PASSIVE. The type: tec and rec are uint16_t. If they were uint8_t (0…255), the condition tec > 255 could never be true, and line 2 would be dead code: no test suite could cover it. The coverage analysis would reveal a problem in the requirements or in the design, not a missing test (ISO 26262-6, 9.4.4, EXAMPLE 1). The thresholds come from the CAN specification: error passive when a counter reaches 128, bus-off when TEC reaches 256.")
h3("Exercise 4 (verbal)")
p("For the function below, how many tests are needed, at least, for 100% statement coverage? And for 100% branch coverage? Which values of temp do you choose? Which case remains untested, even with 100% branch?")
code([(1, "int fan_level(int16_t temp)"), (2, "{"), (3, "    int level = 0;"), (4, "    if (temp > 60) {"), (5, "        level = 1;"), (6, "    }"), (7, "    if (temp > 90) {"), (8, "        level = 2;"), (9, "    }"), (10, "    return level;"), (11, "}")])
h3("Exercise 5 (in the app)")
p("On V0, in the F1 tab, answer the ISO 26262 question. Write one test for each of the requirements SWR-F1-01, SWR-F1-03 and SWR-F1-04, all with extended = true, and run them: watch statement and branch. Then add the missing test (the „Missing decision outcomes” list) and say which requirement it covers. Write in the notes why 100% statement was not enough.")

h("MC/DC")
p("A decision can have several conditions joined by && or ||. The decision at line 4 of F3 has two: A = (tec > 127) and B = (rec > 127). Branch coverage only looks at the result of the decision: with tests T2 and T3, B was never true, and a mistake in B (for example rec > 1270) would go unnoticed. MC/DC requires every condition to show that, on its own, it changes the result: for every condition there is a pair of tests in which only that condition changes, and the result changes too.")
table(["Test", "tec", "rec", "A", "B", "A || B"], [["T3", "0", "0", "false", "false", "false"], ["T2", "200", "0", "true", "false", "true"], ["T4", "0", "200", "false", "true", "true"]], center_cols=(1, 2, 3, 4, 5))
p("The pair T3–T2 shows A, the pair T3–T4 shows B. For N conditions, the theoretical minimum is N + 1 tests (unique-cause MC/DC, FAA report DOT/FAA/AR-01/18), instead of all 2^N combinations. It is not an ISO 26262 requirement: the standard only lists MC/DC in table 9 and does not define a particular form. For AND (&&) start from „all true” and make one condition false at a time; for OR (||) start from „all false” and make one true at a time. In C, && and || stop when the result is certain (short-circuit evaluation): in the app's truth table, a condition that was not evaluated is shown as „–”, and a pair is also valid if it differs only in conditions that were not evaluated. The form used by the app, unique-cause with short-circuit evaluation, is called unique-cause + masking MC/DC in the FAA terminology.")
img("f2_mcdc.png", 420, "The MC/DC truth table for F2 on V0 and the pair that demonstrates each condition.")
h3("Exercise 6 (verbal)")
p("For each decision, give the true / false combinations for MC/DC (the minimum of N + 1 tests) and the pair that demonstrates each condition:")
ol(["if ((v >= 2) && (v <= 2500))", "if (a || b || c)", "if (a && (b || c))"])
h3("Exercise 7 (in the app)")
p("On V0, in the F2 tab, reach 100% MC/DC with at most 5 tests. The decision is A && B && (C || D): A and B check the range, C is the first detection of the object, D checks the jump from the previous cycle. Write down the pair that demonstrates each condition and explain the pair for C.")

h("How tests are written, and why 100% does not mean free of mistakes")
p("Tests are written from the requirements, not from the code (ISO 26262-6, table 8). At ASIL B, requirements analysis, equivalence classes and boundary values are all ++. The techniques are:")
table(["Technique", "What you do", "Example on F3 (bus-off when TEC > 255)"], [
    ["Requirements analysis", "At least one test per requirement; the expected result comes from the requirement.", "tec = 300 → BUS_OFF"],
    ["Equivalence classes", "Split the range into groups that are handled the same way and take one value from each.", "TEC 0…127, 128…255, 256…65535"],
    ["Boundary values", "Test the value exactly at the boundary and the one just past it: ISO 26262-6, table 8, note b asks for values that approach and cross the boundary, so a boundary is fully tested only with both. This is where > instead of >= mistakes live.", "TEC 127 / 128 and 255 / 256; REC 127 / 128"],
    ["Error guessing", "Values chosen from experience.", "0, 65535, a difference of exactly zero"]])
p("Coverage shows that a line ran, not that it gave the correct result. You can go through every branch with „middle” values and never touch the wrong boundary. The right order is: tests from the requirements, then the coverage, then the gaps.")
p("Boundary values are mandatory in this lab. It is the same technique as in general software testing, called boundary value analysis (BVA): you find it in the ISTQB syllabus and in ISO/IEC/IEEE 29119-4; it is not specific to the automotive industry. The recipe has three steps: (1) find the number in the requirement; (2) ask yourself which is the last value with one answer and the first value with the other answer; (3) those two are the tests. Example: „ERROR_PASSIVE when REC > 127” gives REC = 127 (ERROR_ACTIVE) and REC = 128 (ERROR_PASSIVE). Values far from the boundary, such as 0 or 200, go through all the code, but do not see whether the programmer wrote >= instead of >: both versions of the code give the same result. In the app, the „Boundary values (BVA)” metric shows how many boundaries have both tests and must reach 100% in F1, F2 and F3, and the list under it shows which boundary and which test is missing.")
p("Here is an example from variant V0 (you redo it in exercise 9). With four tests, F1 has 100% statement, branch, MC/DC and requirements, and every test passes. Requirement SWR-F1-02 says that an identifier greater than 0x7FF is rejected, so 0x7FF itself must be accepted. The test with id = 0x7FF, standard frame, fails: the function returns false. A failing test is an incident. Its analysis shows that the expected result follows the requirement, so the cause is in the code: line 14 says id >= max_id instead of id > max_id. The incident report looks like this:")
table(["Failing test", "Line", "Fix", "Description"], [["T5: id = 0x7FF, dlc = 8, extended = false", "14", "if (id > max_id) {",
    "SWR-F1-02 rejects only identifiers greater than 0x7FF, so 0x7FF must be accepted (SWR-F1-04). Got false, expected true. The >= comparison also rejects the largest valid value."]])
h3("Exercise 8 (verbal)")
p("Requirement: „The temperature sensor is faulty if the temperature read is below −40 °C or above 125 °C.” Which equivalence classes and which boundary values do you test? What is the minimum number of tests?")
h3("Exercise 9 (in the app)")
p("On V0, in the F1 tab, add the boundary tests for the standard and the extended frame (0x7FF and 0x1FFFFFFF). Which test fails? Fill in the incident report: the test, the line, the fix and the description (the requirement, the result obtained, the result expected).")
h3("Exercise 10 (in the app)")
p("On V0, in the F3 tab, write the tests from requirements SWR-F3, with every boundary value (TEC 127 / 128 and 255 / 256, REC 127 / 128). What coverage do you get? Does any test fail? At home, the mistake in your variant is in F3.")

h("Integration and code that cannot be reached")
p("At integration, the function can_rx_handler calls the other three. Here we track function coverage (every function called) and call coverage (every call site executed). What remains uncovered is analysed: a test is missing, a requirement is missing, or the code cannot be reached. Code that cannot be reached is not deleted if it has a role (for example defensive code, required by the MISRA C coding rules); it is justified: why it cannot be reached, why that is acceptable and how it could still be verified. For the default branch of a switch, ISO 26262-6, 9.4.4 accepts two ways. The first is the justification: it is defensive code, required by MISRA C:2012 rule 16.4 (every switch has a default), and ISO 26262-6, table 1, note d even gives default as an example of a defensive technique. The second is a test by fault injection (table 7, 1l, recommended at ASIL B): a stub of the function can_error_state() or the debugger forces state to an invalid value, for example 0xFF, and the test checks that the function returns RX_FAULT.")
h3("Exercise 11 (verbal)")
p("In the app, in F3, after the tests (tec = 300, rec = 0), (0, 0) and (10, 5), line 42 shows ##### and the „Missing decision outcomes” list shows „line 41: true”. What does it mean? Which tests do you add, and from which requirement? Think about MC/DC too.")
h3("Exercise 12 (in the app)")
p("On V0, in the Integration tab, reach 100% functions called and 100% calls executed. Which lines remain uncovered, and why? In the „Justification of uncovered code” field, write the justification or describe the fault-injection test that would reach them.")

h("Homework (the report)")
p("At home you do the complete analysis on your own variant. Two things are different from V0. The „Boundary values (BVA)” list shows which boundary and which test is missing, but without values: you take the values from the requirements. The report also contains the work history: how many times you ran the tests, how many test versions got a warning along the way and how many warnings remain. What matters most in the report is what you write (the incident report, the notes, the justification) and how correctly you wrote the tests the first time, from the requirements. The steps are the ones you did in the lab on V0:")
ol(["in the app press „Start over”, then load your variant (V1–V6), with your name;",
    "redo exercises 5, 7, 9, 10 and 12 on your variant (careful: in F2 the signal limits are different from V0);",
    "in F3, the failing boundary test shows you the mistake in your variant: fill in the incident report;",
    "in F1, F2 and F3, the „Boundary values (BVA)” metric must reach 100%; in every tab, write in the notes the techniques used (equivalence classes, boundary values) and the conclusion;",
    "in the Report tab, check the report and send it. By sending it you agree that the data in the report may be used for a case study; your name is not used anywhere, only the results from the app. After sending, an anonymous 5-question questionnaire about the app and the exercise appears; you can fill it in or close it with „Not now”. If the sending is not confirmed, download the report (.html) and keep it."])

h("Resources")
for t, u in [("The SW TCA Lab app", APP), ("The lab repository (the code, the gcov demo in Codespaces)", REPO),
             ("K. J. Hayhurst, D. S. Veerhusen, J. J. Chilenski, L. K. Rierson, „A Practical Tutorial on Modified Condition/Decision Coverage”, NASA/TM-2001-210876, 2001", "https://shemesh.larc.nasa.gov/fm/papers/Hayhurst-2001-tm210876-MCDC.pdf"),
             ("ISO 26262-6:2018, Road vehicles — Functional safety — Part 6: Product development at the software level (through the university library)", "https://www.iso.org/standard/68388.html")]:
    pn('<a href="%s">%s</a>' % (u, E(t)), raw=True)

h("Annex. Variant V0 solved in the app: what goes in each field")
p("The values below were run in the app on V0. With them, every tab has 0 warnings, and F1, F2 and F3 have „Boundary values (BVA)” 3/3. The app puts an example test in every tab (T1 or I1, labelled „example”); keep it, it is part of the solution. The texts for the notes, the incident report and the justification are models: any wording that says the same thing is correct.")
h3("Start and the ISO 26262 question (F1 tab)")
p("Start: your name, the variant code V0, then „Load variant”. In F1, at „Before testing: what does ISO 26262-6 require for ASIL B?”, choose: Statement coverage = ++ highly recommended; Branch coverage = ++ highly recommended; MC/DC = + recommended (ISO 26262-6, table 9, ASIL B column).")
h3("F1: tests")
table(["Test", "id", "dlc", "extended", "Expected result", "Requirement", "Verdict"], [
    ["T1 (example)", "0x100", "9", "true", "false", "SWR-F1-01", "PASS"], ["T2", "0x20000000", "8", "true", "false", "SWR-F1-03", "PASS"],
    ["T3", "0x100", "8", "true", "true", "SWR-F1-04", "PASS"], ["T4", "0x800", "8", "false", "false", "SWR-F1-02", "PASS"],
    ["T5", "0x7FF", "8", "false", "true", "SWR-F1-04", "FAIL · probable cause: the code"], ["T6", "0x1FFFFFFF", "8", "true", "true", "SWR-F1-04", "FAIL · probable cause: the code"]])
p("What the app shows along the way. Only T1: statement 63%, decisions 33%. T1–T3: statement 100%, decisions 83%, the „Missing decision outcomes” list shows „line 8: false”, and SWR-F1-02 is under „Requirements without a valid test”. With T4: statement, decisions, MC/DC and requirements 100%, but „Boundary values (BVA)” 1/3 (0x7FF and 0x1FFFFFFF „on the boundary” are missing). With T5 and T6: BVA 3/3, and T5 and T6 fail with „FAIL · incident – probable cause: the code”.")
h3("F1: the incident report")
table(["Field in the app", "What you write"], [["Failing test", "T5 (and T6)"], ["Suspect line", "14"], ["Proposed fix (C code)", "if (id > max_id) {"],
    ["Description: requirement, result obtained, result expected", "SWR-F1-02 rejects only identifiers greater than 0x7FF, so 0x7FF must be accepted (SWR-F1-04). For id = 0x7FF, standard frame, the function returns false; true was expected. The comparison at line 14 uses >= instead of >, so it also rejects the largest valid value. The same mistake appears for the extended frame (T6, 0x1FFFFFFF)."]])
h3("F1: notes")
p("With T1–T3, all with extended = true, statement reached 100%, but branch only 83%: the decision at line 8 was never false, so the standard frame (SWR-F1-02) was not tested. The false branch of an if without else has no statements of its own, which is why statement coverage does not see it; T4 (0x800, standard frame) completed branch coverage. Techniques: requirements analysis (one test per requirement), equivalence classes (valid / invalid DLC, standard / extended frame, identifier within range / above range) and boundary values (DLC 8 / 9, 0x7FF / 0x800, 0x1FFFFFFF / 0x20000000). Conclusion: coverage was 100% before T5 and T6; the mistake at line 14 (>= instead of >) was found only by the boundary tests, written from the requirement.")
h3("F2: tests")
table(["Test", "value", "previous", "first_sample", "Expected result", "Requirement", "Role"], [
    ["T1 (example)", "1251", "0", "true", "true", "SWR-F2-03", "C: first detection (pair T1–T3)"], ["T2", "1000", "1050", "false", "true", "SWR-F2-04", "base: tracked object, jump 50"],
    ["T3", "1000", "1100", "false", "false", "SWR-F2-04", "D: jump 100 (pair T2–T3)"], ["T4", "1", "0", "true", "false", "SWR-F2-01", "A: below minimum (pair T1–T4)"],
    ["T5", "2501", "2500", "true", "false", "SWR-F2-02", "B: above maximum (pair T1–T5)"], ["T6", "2", "2", "true", "true", "SWR-F2-01", "minimum boundary: 2 (1 is in T4)"],
    ["T7", "2500", "2500", "false", "true", "SWR-F2-02", "maximum boundary: 2500 (2501 is in T5)"], ["T8", "1080", "1000", "false", "true", "SWR-F2-04", "step boundary: 80"],
    ["T9", "1081", "1000", "false", "false", "SWR-F2-04", "step boundary: 81"]])
p("What the app shows: statement, decisions, MC/DC (5/5), requirements and BVA (3/3) 100%, every test PASS; on V0, F2 has no mistake. The pairs shown: A T1–T4, B T1–T5, C T1–T3, D T2–T3. The decision at line 25 (delta < 0) is true in T2 (1000 − 1050 < 0) and false in T1. T1–T5 are the MC/DC set (N + 1 = 5 tests for 4 conditions), T6–T9 are the boundaries. In T7 first_sample is false, but the jump is 0, so D is true and the test checks only the maximum.")
h3("F2: notes")
p("The decision at line 28 is A && B && (C || D), with A = value >= 2, B = value <= 2500, C = first_sample, D = delta <= 80. I started from T2 (tracked object, small jump, accepted) and changed one condition at a time: D in T3 (jump 100, rejected), A in T4 (1, rejected), B in T5 (2501, rejected). The pair for C is T1–T3: in T3, C and D are false and the result is false; in T1, C is true, and D is no longer evaluated (|| stops at the first true), so the result becomes true only because of C. D differs between the two tests, but does not affect the result: this is unique-cause + masking MC/DC. Techniques: MC/DC, equivalence classes (below the range, within the range, above the range; small / large jump; first detection / tracked object) and boundary values (2 / 1, 2500 / 2501, jump 80 / 81). Every test passes: on V0, F2 has no mistake.")
h3("F3: tests")
table(["Test", "tec", "rec", "Expected result", "Requirement", "Role"], [
    ["T1 (example)", "0", "0", "ERROR_ACTIVE", "SWR-F3-03", "normal class"], ["T2", "256", "0", "BUS_OFF", "SWR-F3-01", "TEC just after 255"],
    ["T3", "255", "0", "ERROR_PASSIVE", "SWR-F3-02", "TEC on the bus-off boundary"], ["T4", "128", "0", "ERROR_PASSIVE", "SWR-F3-02", "TEC just after 127"],
    ["T5", "127", "0", "ERROR_ACTIVE", "SWR-F3-03", "TEC on the passive boundary"], ["T6", "0", "128", "ERROR_PASSIVE", "SWR-F3-02", "REC just after 127"],
    ["T7", "0", "127", "ERROR_ACTIVE", "SWR-F3-03", "REC on the passive boundary"]])
p("What the app shows: statement, decisions, MC/DC (3/3), requirements and BVA (3/3) 100%, every test PASS. The MC/DC pairs at line 41: tec > 127 through T1–T3, rec > 127 through T1–T6. On V0, F3 has no mistake (the V0 mistake is in F1).")
h3("F3: notes")
p("I wrote the tests from requirements SWR-F3, with the boundary values for every threshold: TEC 255 / 256 (bus-off), TEC 127 / 128 and REC 127 / 128 (error passive). The equivalence classes: TEC 0…127, 128…255, 256 and above; REC 0…127, 128 and above. Bus-off is checked first, otherwise tec = 256 would come out ERROR_PASSIVE. For MC/DC at line 41, T3 shows the effect of tec > 127 and T6 that of rec > 127, both against T1. Every test passes and every metric is 100%: on V0, F3 has no mistake.")
h3("Integration: tests")
table(["Test", "id, dlc, extended", "value, previous, first_sample", "tec, rec", "Expected result", "Requirement"], [
    ["I1 (example)", "0x100, 8, false", "1251, 1251, false", "300, 0", "RX_BUS_OFF", "SWR-INT-01"], ["I2", "0x100, 8, false", "1000, 1050, false", "0, 0", "RX_ACCEPTED", "SWR-INT-02"],
    ["I3", "0x100, 9, false", "1000, 1050, false", "0, 0", "RX_REJECTED", "SWR-INT-03"], ["I4", "0x100, 8, false", "3000, 1050, false", "0, 0", "RX_REJECTED", "SWR-INT-03"]])
p("What the app shows: functions called 100% (4/4), calls executed 100% (3/3), MC/DC 100% (can_frame_is_valid through I2–I3, sensor_value_plausible through I2–I4), requirements 100%, but statement 82% (9/11) and decisions 80% (4/5). Lines 67 and 68 remain, and „Missing decision outcomes” shows „line 54: default”. Every test passes.")
h3("Integration: justification of the uncovered code")
p("Lines 67–68 (default) cannot be reached by tests: can_error_state() returns only ERROR_ACTIVE, ERROR_PASSIVE and BUS_OFF, all handled explicitly. The code is defensive, required by MISRA C:2012 rule 16.4 (every switch has a default), and handles a corrupted value of state (for example a memory error) by returning RX_FAULT. It can be verified by fault injection (ISO 26262-6, table 7, 1l): a stub of can_error_state() returns 0xFF, and the test expects RX_FAULT. The code is accepted as uncovered, with this justification (ISO 26262-6, 9.4.4).")
h3("Integration: notes")
p("I1 covers the BUS_OFF branch (SWR-INT-01), I2 the acceptance path and all three calls C1, C2, C3 (SWR-INT-02), I3 an invalid frame, for which C3 is no longer called, and I4 an implausible value (SWR-INT-03). Functions and calls are 100%. Statement and decisions cannot reach 100% because of the default branch, which is defensive code: it is not deleted, it is justified.")
h3("Report")
p("In the Report tab check that the ISO answer, the four test tables with the coverage, the incident report for F1, the integration justification and the notes appear. „Work history” shows, for every function, the runs, the test versions with a warning and the warnings remaining (0 at the end). On V0 the report is not sent: it is only an exercise.")
out.append("</body></html>")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sw_guide_en.html"), "w", encoding="utf-8").write("\n".join(out))
print(len("\n".join(out)))
