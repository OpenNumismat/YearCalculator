import sys
from PyQt5.QtWidgets import QApplication, QDialog
from YearCalculator import YearCalculatorDialog
import resources


def main():
    app = QApplication(sys.argv)

    dlg = YearCalculatorDialog('2022', '')
    if dlg.exec_() == QDialog.Accepted:
        print(dlg.year(), '=', dlg.nativeYear())


if __name__ == "__main__":
    main()
