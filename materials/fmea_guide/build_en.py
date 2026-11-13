"""FMEA lab guide (EN), DFMEA HW + SW, English version of build_ro.py.
Writes fmea_guide_en.html, uploaded to Drive as a Google Doc."""
import html, os
SHA = os.environ.get("IMG_SHA", "main")
IMG = "https://raw.githubusercontent.com/madalinatolontan1-ai/sw-tca-lab/%s/docs/guide-img/fmea-en/" % SHA
APP = "https://madalinatolontan1-ai.github.io/sw-tca-lab/fmea/"
e = html.escape
out = []
def h1(t): out.append("<h1>%s</h1>" % e(t))
def h2(t): out.append("<h2>%s</h2>" % e(t))
def h3(t): out.append("<h3>%s</h3>" % e(t))
def p(t, raw=False): out.append("<p>%s</p>" % (t if raw else e(t)))
def ol(items): out.append("<ol>" + "".join("<li>%s</li>" % e(i) for i in items) + "</ol>")
def ul(items): out.append("<ul>" + "".join("<li>%s</li>" % e(i) for i in items) + "</ul>")
def table(rows, bold_first_col=True):
    s = "<table border='1' style='border-collapse:collapse'>"
    for i, r in enumerate(rows):
        s += "<tr>" + "".join(("<td><b>%s</b></td>" if (i == 0 or (bold_first_col and j == 0)) else "<td>%s</td>") % e(str(c)) for j, c in enumerate(r)) + "</tr>"
    out.append(s + "</table>")
def fig(name, cap, w=600):
    out.append("<p style='text-align:center'><img src='%s%s' width='%d'></p>" % (IMG, name, w))
    out.append("<p style='text-align:center'><i>%s</i></p>" % e(cap))

h1("Failure Mode and Effects Analysis (FMEA): hardware and software DFMEA")

h2("What is FMEA?")
p("FMEA (Failure Mode and Effects Analysis) is a risk analysis done before the failure exists. The team takes every element of the product, writes what it has to do (the functions), asks how it might fail to do it (the failure modes), what happens then (the effects) and why it could happen (the causes). For every effect – mode – cause chain it rates the risk and decides what to do so that the risk drops. FMEA is preventive: it is worth most at the start, when a change is cheap, and less with every phase in which the failure stays undiscovered.")
p("The AIAG-VDA handbook (2019), used in the automotive industry, has three types of FMEA:")
table([["Type", "What it analyses", "Example on the CAN module"],
       ["DFMEA (design)", "The product design: the schematic, the components chosen, the layout, the code, the requirements", "R4 chosen with too low a power rating; SENSOR_MAX written in another unit"],
       ["PFMEA (process)", "The manufacturing and assembly process", "C2 missing after placement; cold solder joint on J2 (the HW TCA lab)"],
       ["FMEA-MSR", "Monitoring and system response in operation, in the vehicle", "The radar detects bus-off and reports the fault to the ADAS ECU"]])
p("In this lab we do a DFMEA on the CAN node of the front radar, on two of its parts: a hardware signal and a software function. The method is the same for both. Only the causes differ: in hardware they are about choosing and dimensioning the components, the schematic and the layout; in software every cause is systematic (requirements, constants, logic, data types, interfaces), because software does not wear out and is not manufactured unit by unit.")
h3("Why, when and on what")
ul(["Why: so that failures are found and removed in the design, not at the customer. A failure found in the field costs much more than one found in design (recalls, warranty, legal liability).",
    "When: the DFMEA starts together with the design (concept, schematic, software architecture) and is updated at every change; it is a living document. The PFMEA starts when the production line is designed.",
    "On what: on the system (the radar), on subsystems and components (the CAN node, the transceiver, the filters), on software (the functions) and on the manufacturing process.",
    "Who: a team, not one person: HW designer, SW developer, test and validation engineer, functional safety engineer, quality engineer. In the lab, you play all these roles."])
h3("Standards, laws and industries")
table([["Field", "What requires FMEA"],
       ["Automotive", "The AIAG-VDA FMEA handbook (2019) and SAE J1739 (2021) describe the method. IATF 16949 requires the design risk analysis (DFMEA) among the design outputs and the PFMEA among the process outputs. ISO 26262-9 (clause 8) requires safety analyses, and FMEA is the inductive analysis used most often."],
       ["General", "IEC 60812:2018 describes FMEA and FMECA for any industry."],
       ["Aerospace", "SAE ARP4761A (2023) for the safety assessment; SAE AS13004 for PFMEA and the control plan."],
       ["Medical", "ISO 14971 for risk management of medical devices; FMEA is one of the techniques used."],
       ["Railway", "EN 50126 (RAMS), with FMEA as a basic analysis."],
       ["Telecom", "There is no dedicated FMEA standard. TL 9000 is the quality management system of the ICT sector; for the analysis IEC 60812 is used and, for reliability, Telcordia SR-332."]])
p("What happens if FMEA is not done: at the IATF 16949 audit, its absence is a nonconformity, and the supplier may lose the certification and the customer. If the failure reaches the field, recalls and product liability follow; the new European product liability directive (EU 2024/2853) explicitly includes software.")
h3("Exercise 1 (verbal)")
p("For each situation, say whether it is a DFMEA cause or a PFMEA cause, and why:")
ol(["R4 was chosen with a power rating too low for the dominant state;", "R4 is missing from the board after placement;",
    "SENSOR_MAX was written in degrees, while the rest of the code works in tenths of a degree;", "the solder joint of a J2 pin is cold;",
    "the requirement for the first detection of an object is missing from the software specification."])

h2("The 7 steps of the AIAG-VDA method")
table([["Step", "What you do", "In the app"],
       ["1. Planning", "The intent, timing, team, tasks and tools (the 5T)", "Step 1 · Planning"],
       ["2. Structure analysis", "The structure tree: N1 effect (the radar), N2 the element analysed, N3 the cause categories", "The HW and SW tabs, steps 2–3"],
       ["3. Function analysis", "The functions of every element: verb + object + measurable condition", "Steps 2–3"],
       ["4. Failure analysis", "Effects, failure modes and causes, linked in the failure net", "Step 4"],
       ["5. Risk analysis", "Prevention and detection controls; S, O, D; the action priority AP", "Steps 5–6"],
       ["6. Optimization", "Actions for AP H and M, with a responsible person and a due date; new O and D", "Steps 5–6"],
       ["7. Results documentation", "The report with the results", "Step 7 · Report"]])
h3("Exercise 2 (verbal)")
p("Load the demo variant F0 in the app and read the 5T in Step 1. What is in the scope of the analysis and what is not? Why is the manufacturing process not part of the DFMEA?")

h2("The case study and the app")
p("We work on the same generic automotive front radar as in the TCA labs (lab assumption: ASIL B), which sends the list of detected objects over CAN at 500 kbit/s, about every 72 ms. The CAN node has the hardware part from the HW TCA lab (the module with the MCP2551 transceiver) and the software part from the SW TCA lab (the receive functions).")
p("How you work: you work in the web app <a href='%s'>FMEA Lab</a>, in the browser, with nothing to install. Enter your name and the variant code and press „Load variant”. In the lab you work on the demo variant F0, together with the instructor: the RC filters on CANH / CANL (HW) and the plausibility check of the azimuth angle, the function sensor_value_plausible() (SW). At home you do the same analysis on your own variant (F1–F6) and send the report. The app has a tab for the HW analysis, one for the SW analysis and the Report tab. Each analysis has three stages: steps 2–3 (structure and functions), step 4 (the failure net) and steps 5–6 (risk and optimization). At every stage you find „Context”, „How to do it” (with the example on F0) and the AIAG-VDA reference tables. Your work is saved in the browser you use." % APP, raw=True)
p("Lab simplification: choose a single function per element, at most 3 failure modes, 3 effects and 2 causes per mode. The app warns you when you go past these limits, but does not block you. In industry the analysis covers every function and every failure; here we look at how you rate them, not at a complete analysis.")

h2("Structure and functions (steps 2–3)")
p("The structure tree has three levels. N1 is the effect level: the radar, seen from the vehicle. N2 is the element analysed: the hardware signal or the software function of your variant; this is where the failure modes appear. N3 is the cause level: the design cause categories.")
table([["Level", "HW analysis", "SW analysis"],
       ["N1 (effect)", "The front radar (ASIL B)", "The front radar (ASIL B)"],
       ["N2 (mode)", "The signal of the variant (e.g. the RC filters on CANH / CANL)", "The function of the variant (e.g. sensor_value_plausible() for the azimuth angle)"],
       ["N3 (cause)", "Component selection, Component dimensioning, Signal definition, Schematic, PCB layout", "Software requirements (SWR), Constants and parameters (#define), Decision logic, Data types and value ranges, Interface (calls, return values)"]])
p("A good function has a verb, an object and a measurable condition, for example „Provides 120 Ω ±1 % between CANH and CANL at the end of the bus”. You write the N2 functions starting from the requirements shown (HWR for hardware, SWR for software). The suggestion list in the app is the same for every level: you decide where each function fits.")
h3("Exercise 3 (on paper)")
p("The power indicator LED1 + R5 is not in any variant. Write one function for it at N2, with a measurable condition, and one function for the „Component dimensioning” category at N3.")
h3("Exercise 4 (in the app)")
p("On F0, in the HW tab, write one function each for N1, N2 and the „Component dimensioning” category. Then do the same in the SW tab, with the „Constants and parameters (#define)” category. Follow the example in „How to do it”.")
fig("hw_s23c.png", "F0, HW analysis: the structure tree, the function of the „Component dimensioning” category and the board with the signal analysed.")

h2("The failure net (step 4)")
p("Failures are the negation of the functions: the function is missing, partial, intermittent, unwanted or out of limits. At N1 you write the effects (what the vehicle or the ADAS ECU sees), at N2 the failure modes of the element, at N3 the causes. Then link every mode to at least one effect and at least one cause. Severity is rated on the effect, and the mode takes the highest severity of the effects linked to it.")
p("On every cause you choose the culprit: in HW, the component (those on the signal are highlighted on the board and in the schematic); in SW, the requirement, if the cause is in the requirements category. Mind the level: „C2 has too wide a tolerance” is a cause (N3), not a mode; the mode is what the filter does wrong (asymmetry between CANH and CANL).")
h3("Exercise 5 (on paper)")
p("For the function you wrote in exercise 3, write a complete chain: the effect at N1, with S from the table below, the failure mode at N2, a cause at N3, its category and the culprit component.")
table([["S", "Criterion (table D1, summary)"],
       ["10", "Affects the safe operation of the vehicle or the health of people"], ["9", "Noncompliance with regulations"],
       ["8", "Loss of a primary vehicle function"], ["7", "Degradation of a primary vehicle function"],
       ["6", "Loss of a secondary vehicle function"], ["5", "Degradation of a secondary vehicle function"],
       ["4", "Very objectionable appearance, sound or vibration"], ["3", "Moderately objectionable appearance, sound or vibration"],
       ["2", "Slightly objectionable appearance, sound or vibration"], ["1", "No discernible effect"]])
h3("Exercise 6 (in the app)")
p("On F0, build the failure net from „How to do it”. HW: the effect „Electromagnetic emissions above the regulated limits (EMC)”, S 9; the mode „Asymmetry between the CANH and CANL filters”; the cause „Tolerance too wide for the function”, under „Component dimensioning”, culprit C2. SW: the effect „A real object is not reported (missed detection, no braking)”, S 8, at sensor level; the mode „Rejects a valid value”; the cause „Wrong unit of the constant”, under „Constants and parameters (#define)”: SENSOR_MAX written in degrees (60) instead of tenths of a degree (600), so objects beyond 6° are rejected.")
fig("hw_s4c.png", "F0, HW analysis: effect – mode – cause, with the culprit C2 chosen on the cause.")
fig("sw_s4c.png", "F0, SW analysis: the chain for the constant SENSOR_MAX written in another unit.")

h2("Risk analysis (step 5)")
p("For every mode – cause link you add the existing controls and rate the risk:")
ul(["S comes from the effects linked to the mode (the highest), from table D1.",
    "O is rated on the cause, taking into account the prevention controls (what keeps the cause from occurring: calculations, design rules, reviews, approved components, coding rules), from table D2. Note: in HW TCA you used table P2 of the process FMEA; the DFMEA uses D2, the design table.",
    "D is rated on the detection controls (the test or analysis that finds the cause or the mode before release), from table D3. D depends on how proven the method is and on how early it is done: a good test, done after tooling release, still has D 5–7.",
    "AP (action priority) follows from S, O and D, from the AP table: H means action needed, M action recommended, L action optional. We do not use RPN = S × O × D."])
table([["O", "Criterion (table D2, summary)", "D", "Criterion (table D3, summary)"],
       ["10", "New technology, no experience and no prevention", "10", "No test procedure yet"],
       ["9", "First use in the company, new innovations, no validation", "9", "The test does not target the failure mode or the cause"],
       ["8", "New innovations in a new application, no validation", "8", "New, unproven test method"],
       ["7", "New design on similar technology, limited prevention", "7", "Proven test, done late, pass / fail"],
       ["6", "Similar design, changed operating conditions, partial prevention", "6", "Proven test, done late, test to failure"],
       ["5", "Detail changes, proven technology, lessons learned applied", "5", "Proven test, done late, degradation test"],
       ["4", "Almost identical design, follows standards and best practices", "4", "Proven test, done in time, pass / fail"],
       ["3", "Known design, tested in comparable conditions", "3", "Proven test, done in time, test to failure"],
       ["2", "Mature design, long field exposure", "2", "Proven test, done in time, degradation test"],
       ["1", "The cause cannot occur by design", "1", "Detects reliably, or the cause cannot occur"]], bold_first_col=False)
p("The AP table (AIAG-VDA), by S, O and D bands:")
AP = {"9-10": {"8-10": "HHHH", "6-7": "HHHH", "4-5": "HHHM", "2-3": "HMLL", "1": "LLLL"},
      "7-8": {"8-10": "HHHH", "6-7": "HHHM", "4-5": "HMMM", "2-3": "MMLL", "1": "LLLL"},
      "4-6": {"8-10": "HHMM", "6-7": "MMML", "4-5": "MLLL", "2-3": "LLLL", "1": "LLLL"},
      "2-3": {"8-10": "MMLL", "6-7": "LLLL", "4-5": "LLLL", "2-3": "LLLL", "1": "LLLL"}}
rows = [["S", "O", "D 7–10", "D 5–6", "D 2–4", "D 1"]]
for sb in ["9-10", "7-8", "4-6", "2-3"]:
    for ob in ["8-10", "6-7", "4-5", "2-3", "1"]:
        rows.append([sb.replace("-", "–"), ob.replace("-", "–")] + list(AP[sb][ob]))
rows.append(["1", "1–10", "L", "L", "L", "L"])
table(rows)
h3("Exercise 7 (on paper)")
p("Read AP from the table for the rows below. For every H or M row, say what you would change first: the prevention (O) or the detection (D)?")
table([["Row", "S", "O", "D", "AP"], ["a", "9", "4", "7", ""], ["b", "9", "2", "4", ""], ["c", "8", "4", "3", ""], ["d", "6", "5", "2", ""]])
h3("Exercise 8 (in the app)")
p("On F0, at steps 5–6, fill in the initial state. HW: prevention „RC filter calculation” and „Components from the approved list”, O 4; detection „EMC test (emissions and immunity)”, at design validation, after tooling release, D 7. SW: prevention „Code review against the sensor specification”, O 4; detection „Requirements-based testing” and „Boundary value tests”, D 3. What AP do you get in each case, and why does the EMC test have D 7, although it is a proven method?")

h2("Optimization (step 6)")
p("Where AP is H or M you propose actions, in the revised state. An action has a type, a text, a responsible person, a due date and a status. Type P (prevention) changes the design and lowers O; type D (detection) adds or moves a test and lowers D. After the actions you rate the new O and the new D; the revised AP shows whether the risk went down.")
ul(["When an action is done, you choose its result: PASS or FAIL.",
    "FAIL means the test found the failure: the detection worked, but the failure exists. Add a corrective design action (P) and re-rate O. A better test alone does not lower the risk.",
    "If after the revision the risk is still H or M, propose an additional action (P, which lowers O, or D, which lowers D) and justify the residual risk. At S 9 with O 4–5, D 2–4 leaves AP H: in practice only prevention lowers the risk."])
h3("Exercise 9 (in the app)")
p("On F0, propose the actions. HW: [P] „Tolerance analysis on the C1 / C2 pair (C0G, 1 %)” and [D] „EMC pre-compliance test on the prototype, before tooling release”, with new O 2 and new D 4. SW: [P] „Constants generated automatically from the sensor specification”, with new O 2. What AP do you get? Then, in HW, mark the pre-compliance test as done, with the result FAIL: what does the app ask you to do, and why?")
fig("hw_s56c.png", "F0, HW analysis: the initial state (AP H) and the revised state, with one P action and one D action (AP L).")
fig("sw_s56c.png", "F0, SW analysis: the initial state (AP M) and the P action that lowers O (AP L).")

h2("The link with testing")
p("FMEA and testing work together. The detection controls in the DFMEA are in fact the tests in the design verification and validation plan: the EMC test, the measurements on the prototype, the requirements-based software tests. When a test FAILs, the result goes back into the FMEA. The previous labs cover the test side of the same elements:")
ul(["HW TCA: the same components, but the causes are manufacturing causes (PFMEA), and the question is whether AOI, AXI, ICT and FT catch the defect before the board leaves the plant.",
    "SW TCA: shows how complete the software tests used as detection in the SW DFMEA are. A low D on „Requirements-based testing” only makes sense if the tests cover the code and the boundaries."])
h3("Exercise 10 (verbal)")
p("The cause in the SW demo is SENSOR_MAX = 60 instead of 600. Which test from the SW TCA lab would have found it: which angle values do you choose, which expected result and from which requirement? Why is D 3 and not 1?")

h2("Homework (the report)")
p("At home you do the analysis on your own variant, for the HW signal and for the SW function. The steps are the ones from the lab, on F0:")
ol(["in the app press „Start over”, then load your variant (F1–F6), with your name;",
    "for HW and for SW: redo exercises 4, 6, 8 and 9 (one function per element, at most 3 modes, 3 effects and 2 causes per mode);",
    "on every cause choose the culprit (the component in HW, the requirement for SW causes in the requirements category);",
    "for AP H or M propose actions with a responsible person and a due date, and rate the new O and D; if the risk is still H or M, propose the additional action and justify the residual risk;",
    "write the conclusions, check the „Checks” list of each analysis, then, in the Report tab, press „Send report”. By sending it you agree that the data in the report may be used for a case study; your name is not used anywhere, only the results from the app. After sending, an anonymous 5-question questionnaire about the app and the exercise appears; you can fill it in or close it with „Not now”. If the sending is not confirmed, download the report (.html) and keep it."])

h2("Resources")
out.append("<ul><li><a href='%s'>The FMEA Lab app</a></li>" % APP +
           "<li>AIAG & VDA, FMEA Handbook, 1st ed., 2019 (tables D1, D2, D3 and AP).</li>"
           "<li>SAE J1739:2021, Potential Failure Mode and Effects Analysis (FMEA).</li>"
           "<li>IEC 60812:2018, Failure modes and effects analysis (FMEA and FMECA).</li>"
           "<li>ISO 26262-9:2018, Road vehicles — Functional safety — Part 9 (clause 8, safety analyses); IATF 16949:2016.</li>"
           "<li><a href='https://www.microchip.com/en-us/product/MCP2551'>Microchip, MCP2551 High-Speed CAN Transceiver (datasheet)</a></li></ul>")

doc = "<html><head><meta charset='utf-8'></head><body>" + "\n".join(out) + "</body></html>"
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fmea_guide_en.html"), "w", encoding="utf-8").write(doc)
print(len(doc))
