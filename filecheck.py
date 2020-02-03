from openpyxl import load_workbook
from picheck import PICheck
import os
import sys
import time

piCheck = PICheck()
inputFileName = sys.argv[1]
writeConsole = True

report = open(time.strftime("%Y%m%d-%H%M%S")+"_phi_report.txt", "w")
report.write("Deltas for" + inputFileName + os.linesep)

uniqueDeltas = []

wb = load_workbook(filename=inputFileName, read_only=True)
for ws in wb.worksheets:
    deltas = []
    row_number = 0

    print("Worksheet title:" + ws.title + os.linesep)
    report.write(os.linesep + "worksheet title:" + ws.title + os.linesep)
    for row in ws.rows:
        row_number += 1
        cell_number = 0
        for cell in row:
            cell_number += 1
            if cell.value:
                piCheckedValue = piCheck.annotate_value(str(cell.value)).strip()
                if piCheckedValue:
                    deltas.append("ROW:" + str(row_number) + " CELL:" + str(cell_number) + " DELTA:" + piCheckedValue)
                    uniqueDeltas.append(piCheckedValue);

    uniqueDeltas = list(set(uniqueDeltas))
    uniqueDeltas.sort()
    report.write(os.linesep + "Unique Deltas:" + os.linesep)
    for uniqueDelta in uniqueDeltas:
        print(uniqueDelta)
        report.write(uniqueDelta + os.linesep)

    for delta in deltas:
        print(delta)
        report.write(delta + os.linesep)

sys.exit()
