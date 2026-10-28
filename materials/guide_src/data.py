# Shared data for the HW TCA lab guide (RO / EN), taken from the HW app (docs/hw/index.html)
IMG = "https://raw.githubusercontent.com/madalinatolontan1-ai/sw-tca-lab/main/materials/img/"
APP = "https://madalinatolontan1-ai.github.io/sw-tca-lab/hw/"

RULES = [  # category, mode, AOI, AXI, ICT with TP, ICT without TP
    ("PAS-SMD (R, C)", "Missing", 1, 3, 1, 5), ("PAS-SMD (R, C)", "Short", 5, 5, 1, 5), ("PAS-SMD (R, C)", "Open", 1, 5, 1, 5), ("PAS-SMD (R, C)", "Wrong value", 10, 10, 1, 5),
    ("DIODE (LED)", "Missing", 1, 3, 1, 5), ("DIODE (LED)", "Short", 5, 5, 1, 5), ("DIODE (LED)", "Open", 1, 5, 1, 5), ("DIODE (LED)", "Wrong value", 10, 10, 5, 10), ("DIODE (LED)", "Wrong polarity", 1, 10, 1, 5),
    ("IC-LEADED (U1)", "Missing", 1, 1, 1, 5), ("IC-LEADED (U1)", "Pin open", 1, 5, 1, 10), ("IC-LEADED (U1)", "Pin short", 1, 1, 1, 10), ("IC-LEADED (U1)", "Pin wrong functionality", 10, 10, 10, 10),
    ("CONN-THT (J1, J2, JP1)", "Missing", 1, 1, 1, 10), ("CONN-THT (J1, J2, JP1)", "Pin open", 10, 3, 1, 10), ("CONN-THT (J1, J2, JP1)", "Pin short", 10, 1, 1, 10),
    ("CONN-THT (J1, J2, JP1)", "Wrong value", 1, 10, 1, 5), ("CONN-THT (J1, J2, JP1)", "Short", 1, 10, 1, 5), ("CONN-THT (J1, J2, JP1)", "Open", 10, 3, 1, 5),
]

AP = {  # S band -> O band -> D 7-10, 5-6, 2-4, 1
    "9–10": {"8–10": "HHHH", "6–7": "HHHH", "4–5": "HHHM", "2–3": "HMLL", "1": "LLLL"},
    "7–8": {"8–10": "HHHH", "6–7": "HHHM", "4–5": "HMMM", "2–3": "MMLL", "1": "LLLL"},
    "4–6": {"8–10": "HHMM", "6–7": "MMML", "4–5": "MLLL", "2–3": "LLLL", "1": "LLLL"},
    "2–3": {"8–10": "MMLL", "6–7": "LLLL", "4–5": "LLLL", "2–3": "LLLL", "1": "LLLL"},
    "1": {"8–10": "LLLL", "6–7": "LLLL", "4–5": "LLLL", "2–3": "LLLL", "1": "LLLL"},
}

SEVERITY = {
    "ro": [("E9", 9, "Neconformitate cu reglementările (EMC: emisii sau imunitate)"), ("E8", 8, "Pierderea funcției principale (fără comunicație CAN sau fără funcționare)"),
           ("E7", 7, "Degradarea funcției principale (comunicație coruptă sau intermitentă)"), ("E6", 6, "Pierderea unei funcții secundare (indicatorul LED nu funcționează)"),
           ("E5", 5, "Degradarea unei funcții secundare (indicație LED greșită)"), ("E2", 2, "Efect ușor deranjant, fără efect funcțional sau EMC"), ("E1", 1, "Niciun efect perceptibil")],
    "en": [("E9", 9, "Noncompliance with regulations (EMC: emissions or immunity)"), ("E8", 8, "Loss of the primary function (no CAN communication or no operation)"),
           ("E7", 7, "Degradation of the primary function (corrupted or intermittent communication)"), ("E6", 6, "Loss of a secondary function (the LED indicator does not work)"),
           ("E5", 5, "Degradation of a secondary function (wrong LED indication)"), ("E2", 2, "Slightly objectionable effect, no functional or EMC effect"), ("E1", 1, "No discernible effect")],
}
SEV_SCALE = {
    "ro": ["Afectează siguranța vehiculului, a ocupanților sau a altor participanți la trafic", "Neconformitate cu reglementările", "Pierderea unei funcții principale", "Degradarea unei funcții principale",
           "Pierderea unei funcții secundare", "Degradarea unei funcții secundare", "Aspect, zgomot, vibrații sau haptică foarte deranjante", "Aspect, zgomot, vibrații sau haptică moderat deranjante",
           "Aspect, zgomot, vibrații sau haptică ușor deranjante", "Niciun efect perceptibil"],
    "en": ["Affects safe operation of the vehicle, occupants or other road users", "Noncompliance with regulations", "Loss of a primary function", "Degradation of a primary function",
           "Loss of a secondary function", "Degradation of a secondary function", "Very objectionable appearance, sound, vibration or haptics", "Moderately objectionable appearance, sound, vibration or haptics",
           "Slightly objectionable appearance, sound, vibration or haptics", "No discernible effect"],
}
OCC = {
    "ro": ["Prima aplicare a unei tehnologii noi; fără experiență, standarde sau bune practici; prevenția nu poate prezice performanța", "Prima utilizare în firmă a unor inovații sau materiale noi; prevenția nu țintește cerințele",
           "Inovații folosite într-o aplicație nouă; puține standarde aplicabile; prevenția nu e un indicator fiabil", "Design nou pe tehnologie similară, aplicație nouă; prevenția dă o indicație limitată",
           "Similar cu designuri anterioare, condiții de utilizare modificate; standardele nu sunt suficiente", "Modificări de detaliu pe un design dovedit; lecțiile învățate sunt aplicate, dar nedovedite",
           "Design aproape identic, expunere scurtă în teren; conform bunelor practici", "Modificări de detaliu pe un design cunoscut, cu experiență de test sau teren comparabilă",
           "Design matur, aproape identic, cu expunere lungă în teren", "Cauza e eliminată prin prevenție; nu e posibilă prin design"],
    "en": ["First application of new technology; no experience, standards or best practices; prevention cannot predict performance", "First use in the company of innovations or new materials; prevention not targeted to the requirements",
           "Innovations used in a new application; few applicable standards; prevention is not a reliable indicator", "New design on similar technology, new application; prevention gives a limited indication",
           "Similar to previous designs, changed duty cycle or conditions; standards not sufficient", "Detail changes to a proven design; lessons learned applied but not proven",
           "Almost identical design, short field exposure; conforms to best practices", "Detail changes to a known design with comparable test or field experience",
           "Almost identical mature design with long field exposure", "Cause eliminated by prevention; not possible by design"],
}
FT = {
    "ro": [("FT1", "Consum de curent", "IDD pe VDD (J1), în stare recesivă și dominantă", "Recesiv ≤ 10 mA; dominant ≤ 75 mA", "Short pe C3, short / wrong polarity LED1, pin short U1 (VDD–GND), U1 missing, wrong functionality VDD"),
           ("FT2", "Indicator de alimentare", "LED1 aprins, verificat automat cu un senzor optic", "Aprins la VDD nominal", "LED1 open / missing / wrong polarity, R5 open / missing"),
           ("FT3", "Tensiuni pe bus în recesiv", "VCANH, VCANL fără sarcină, TXD = 1", "2,0 – 3,0 V", "Short R1/C1, R2/C2 (linie la GND), pin open / short U1 pe CANH / CANL"),
           ("FT4", "Tensiune diferențială în dominant", "VCANH – VCANL cu sarcină 40–60 Ω, TXD = 0", "1,5 – 3,0 V", "Driver defect (wrong functionality CANH / CANL), R3 wrong value (mod standby)"),
           ("FT5", "Loopback TXD → RXD", "Se comută TXD; RXD trebuie să urmeze starea bus-ului", "RXD = 0 în dominant, 1 în recesiv", "Pin open TXD / RXD pe U1 și J1, wrong functionality TXD / RXD, mod standby greșit (R3)"),
           ("FT6", "Rezistență de terminație", "Rezistența CAN_H–CAN_L pe J2, cu JP1 montat și nemontat", "≈ 120 Ω cu JP1; ≥ 20 kΩ fără JP1", "R4 open / missing / wrong value, JP1 missing / open / short"),
           ("FT7", "Transmisie CAN prin conectori", "Testerul trimite cadre pe TXD (J1); un nod de referință pe J2 le recepționează și le confirmă (ACK), la 500 kbit/s", "Toate cadrele recepționate corect, fără error frames", "Pin open / short pe J1 (VDD, TXD, GND) și J2 (CAN_H, CAN_L), U1 TXD / CANH / CANL / RS, R3 open / missing / wrong value (standby), short R1/C1, R2/C2"),
           ("FT8", "Recepție CAN prin conectori", "Nodul de referință trimite cadre pe J2; testerul citește RXD pe J1, la 500 kbit/s", "Toate cadrele citite corect pe RXD, fără error frames", "Pin open / short pe J1 (RXD) și J2 (CAN_H, CAN_L), U1 RXD / CANH / CANL, wrong functionality RXD")],
    "en": [("FT1", "Supply current", "IDD on VDD (J1), in the recessive and the dominant state", "Recessive ≤ 10 mA; dominant ≤ 75 mA", "C3 short, LED1 short / wrong polarity, U1 pin short (VDD–GND), U1 missing, VDD wrong functionality"),
           ("FT2", "Power indicator", "LED1 on, checked automatically with an optical sensor", "On at nominal VDD", "LED1 open / missing / wrong polarity, R5 open / missing"),
           ("FT3", "Recessive bus voltages", "VCANH, VCANL without load, TXD = 1", "2.0 – 3.0 V", "R1/C1, R2/C2 short (line to GND), U1 pin open / short on CANH / CANL"),
           ("FT4", "Dominant differential voltage", "VCANH – VCANL with a 40–60 Ω load, TXD = 0", "1.5 – 3.0 V", "Faulty driver (CANH / CANL wrong functionality), R3 wrong value (standby mode)"),
           ("FT5", "Loopback TXD → RXD", "TXD is toggled; RXD has to follow the bus state", "RXD = 0 in dominant, 1 in recessive", "TXD / RXD pin open on U1 and J1, TXD / RXD wrong functionality, wrong standby mode (R3)"),
           ("FT6", "Termination resistance", "CAN_H–CAN_L resistance on J2, with JP1 fitted and removed", "≈ 120 Ω with JP1; ≥ 20 kΩ without JP1", "R4 open / missing / wrong value, JP1 missing / open / short"),
           ("FT7", "CAN transmission through the connectors", "The tester sends frames on TXD (J1); a reference node on J2 receives and acknowledges them (ACK), at 500 kbit/s", "All frames received correctly, no error frames", "Pin open / short on J1 (VDD, TXD, GND) and J2 (CAN_H, CAN_L), U1 TXD / CANH / CANL / RS, R3 open / missing / wrong value (standby), R1/C1, R2/C2 short"),
           ("FT8", "CAN reception through the connectors", "The reference node sends frames on J2; the tester reads RXD on J1, at 500 kbit/s", "All frames read correctly on RXD, no error frames", "Pin open / short on J1 (RXD) and J2 (CAN_H, CAN_L), U1 RXD / CANH / CANL, RXD wrong functionality")],
}
COMPONENTS = {  # ref, nets, role
    "ro": [("J1", "VDD, TXD, RXD, GND", "conector spre senzor (alimentare și date de la microcontroler)"), ("U1", "TXD, GND, VDD, RXD, VREF (neconectat), CANL, CANH, RS", "transceiver CAN MCP2551 (SOIC-8)"),
           ("C3", "VDD – GND", "decuplarea alimentării"), ("R3", "RS – GND", "alege modul de lucru al lui U1 (high-speed, slope control, standby)"),
           ("R4 + JP1", "CANH – N_TERM – CANL", "terminația de 120 Ω a bus-ului, activată cu jumperul JP1"), ("R1 / C1", "CANH – N_F1 – GND", "filtru RC pe CANH (EMC)"),
           ("R2 / C2", "CANL – N_F2 – GND", "filtru RC pe CANL (EMC)"), ("J2", "CANH, CANL, GND", "conector spre bus-ul CAN"), ("LED1 + R5", "VDD – N_LED – GND", "indicator de alimentare")],
    "en": [("J1", "VDD, TXD, RXD, GND", "connector to the sensor (supply and data from the microcontroller)"), ("U1", "TXD, GND, VDD, RXD, VREF (not connected), CANL, CANH, RS", "MCP2551 CAN transceiver (SOIC-8)"),
           ("C3", "VDD – GND", "supply decoupling"), ("R3", "RS – GND", "selects the operating mode of U1 (high-speed, slope control, standby)"),
           ("R4 + JP1", "CANH – N_TERM – CANL", "120 Ω bus termination, enabled with jumper JP1"), ("R1 / C1", "CANH – N_F1 – GND", "RC filter on CANH (EMC)"),
           ("R2 / C2", "CANL – N_F2 – GND", "RC filter on CANL (EMC)"), ("J2", "CANH, CANL, GND", "connector to the CAN bus"), ("LED1 + R5", "VDD – N_LED – GND", "power indicator")],
}
# worked example H0 (values the app gives for AOI/AXI/ICT; S, O, FT are the example's choices)
H0 = [  # ref, mode, class, S, O, AOI, AXI, ICT, FT test, FT D, D, AP, D after, AP after
    ("R2", "Missing", "E9", 9, 2, 1, 3, 5, "NONE", 10, 1, "L", 1, "L"),
    ("J2", "Missing", "E8", 8, 2, 1, 1, 10, "FT7", 5, 1, "L", 1, "L"),
    ("J2 · pin 2 CAN_L", "Pin open", "E8", 8, 2, 10, 3, 10, "FT7", 5, 3, "L", 1, "L"),
    ("LED1", "Short", "E6", 6, 2, 5, 5, 5, "FT2", 5, 5, "L", 5, "L"),
    ("R5", "Missing", "E6", 6, 2, 1, 3, 5, "FT2", 1, 1, "L", 1, "L"),
    ("R5", "Wrong value", "E5", 5, 2, 5, 10, 5, "NONE", 10, 5, "L", 1, "L"),
]
