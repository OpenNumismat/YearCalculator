import argparse
import sys
from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox
from YearCalculator import YearCalculatorDialog


def main():
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--lang", choices=('en', 'bg', 'de', 'es', 'pt', 'ru', 'sl', 'uk'),
        help="UI language. If not specified, the system language is used"
    )
    parser.add_argument(
        "-g", "--gregorian", type=int,
        help="Initial gregorian year"
    )
    parser.add_argument(
        "-n", "--native",
        help="Initial year in native calendar"
    )
    parser.add_argument(
        "-c", "--calendar",
        choices=('hebrew', 'islamic', 'iranian', 'japanese', 'roman', 'nepal', 'thai', 'burmese')
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

    if args.gregorian:
        gregorian_year = str(args.gregorian)
    else:
        gregorian_year = ''

    if args.native:
        native_year = args.native
    else:
        native_year = ''

    if args.calendar == 'hebrew':
        calendar_type = YearCalculatorDialog.CALENDARS.HEBREW
    elif args.calendar == 'islamic':
        calendar_type = YearCalculatorDialog.CALENDARS.ISLAMIC
    elif args.calendar == 'iranian':
        calendar_type = YearCalculatorDialog.CALENDARS.IRANIAN
    elif args.calendar == 'japanese':
        calendar_type = YearCalculatorDialog.CALENDARS.JAPANESE
    elif args.calendar == 'roman':
        calendar_type = YearCalculatorDialog.CALENDARS.ROMAN
    elif args.calendar == 'nepal':
        calendar_type = YearCalculatorDialog.CALENDARS.NEPAL
    elif args.calendar == 'thai':
        calendar_type = YearCalculatorDialog.CALENDARS.THAI
    elif args.calendar == 'burmese':
        calendar_type = YearCalculatorDialog.CALENDARS.BURMESE
    else:
        calendar_type = YearCalculatorDialog.CALENDARS.DEFAULT

    dlg = YearCalculatorDialog(gregorian_year, native_year, calendar_type)
    dlg.buttonBox.clear()
    dlg.buttonBox.addButton(QDialogButtonBox.Close)
    dlg.exec()


if __name__ == "__main__":
    import resources
    main()
