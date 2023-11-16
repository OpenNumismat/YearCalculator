import argparse
import sys
from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtWidgets import QApplication, QDialog
from YearCalculator import YearCalculatorDialog


def main():
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--lang", choices=('en', 'bg', 'de', 'es', 'pt', 'ru', 'sl', 'uk'),
        help="UI language. If not specified, the system language is used"
    )

    args = parser.parse_args()

    if args.lang:
        locale = QLocale(args.lang)
    else:
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
    import resources
    main()
