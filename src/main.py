import sys
from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtWidgets import QApplication, QDialog
from YearCalculator import YearCalculatorDialog
import resources


def main():
    app = QApplication(sys.argv)

    locale = QLocale()

    translator = QTranslator(app)
    if translator.load(locale, 'lang', '_', ':/i18n'):
        app.installTranslator(translator)

    path = QLibraryInfo.path(QLibraryInfo.TranslationsPath)
    translator = QTranslator(app)
    if translator.load(locale, 'qtbase', '_', path):
        app.installTranslator(translator)

    dlg = YearCalculatorDialog('2022', '')
    if dlg.exec() == QDialog.Accepted:
        print(dlg.year(), '=', dlg.nativeYear())


if __name__ == "__main__":
    main()
