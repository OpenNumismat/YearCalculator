# -*- coding: utf-8 -*-

import math

from PyQt5.QtCore import Qt, QMargins, QT_TRANSLATE_NOOP
from PyQt5.QtGui import QFont, QValidator, QIcon
from PyQt5.QtWidgets import *


class YearCalculatorDialog(QDialog):
    class CALENDARS():
        HEBREW = 0
        ISLAMIC = 1
        SOLAR_HIJRI = 2
        JAPAN = 3
        ROMAN = 4
        NEPAL = 5
        THAI = 6
        BURMESE = 7
        DEFAULT = HEBREW
    
    def __init__(self, year, native_year, default_calendar=CALENDARS.DEFAULT, parent=None):
        super().__init__(parent,
                         Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint)
        self.setWindowTitle(self.tr("Year calculator"))
        self.setWindowIcon(QIcon(':/date.png'))

        self.buttonBox = QDialogButtonBox(Qt.Horizontal)
        self.buttonBox.addButton(QDialogButtonBox.Save)
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.calendars = (HebrewCalendar(), IslamicCalendar(), SolarHijriCalendar(),
                          JapanCalendar(), RomanCalendar(), NepalCalendar(),
                          ThaiCalendar(), BurmeseCalendar())
        self.national_layouts = []

        combo = QComboBox()
        for calendar in self.calendars:
            combo.addItem(QApplication.translate("YearCalculatorDialog", calendar.TITLE))
        combo.activated.connect(self.calendarChanged)

        hlayout = QHBoxLayout()
        year_layout = self.gregoryanLayout(year)
        hlayout.addLayout(year_layout)
        hlayout.setAlignment(year_layout, Qt.AlignTop)
        hlayout.addSpacing(20)

        for calendar in self.calendars:
            layout = self.nationalCalc(calendar, native_year)
            self.national_layouts.append(layout)

            hlayout.addWidget(layout)
            hlayout.setAlignment(layout, Qt.AlignTop)

        layout = QVBoxLayout()
        layout.addWidget(combo)
        layout.addLayout(hlayout)
        layout.addWidget(self.buttonBox)
        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.setLayout(layout)
        
        calendar_index = default_calendar
        for i, calendar in enumerate(self.calendars):
            if native_year and native_year[0] in calendar.SYMBOLS:
                calendar_index = i

        combo.setCurrentIndex(calendar_index)
        self.calendarChanged(calendar_index)
    
    def calendarChanged(self, index):
        self.nationalYearEditor = self.national_layouts[index].EDITOR
        for i, layout in enumerate(self.national_layouts):
            if i == index:
                layout.show()
            else:
                layout.hide()

    def gregoryanLayout(self, year):
        layout = QGridLayout()
        layout.setContentsMargins(QMargins())

        edit = QLineEdit(year)
        validator = GregorianValidator(self)
        edit.setValidator(validator)
        edit.setFont(QFont("serif", 16))
        layout.addWidget(edit, 0, 0, 1, 5)
        
        btn = ClearButton(edit)
        layout.addWidget(btn, 1, 0)
        btn = BackButton(edit)
        layout.addWidget(btn, 1, 1)
        btn = ConvertButton()
        btn.clicked.connect(self.convertGregorian)
        layout.addWidget(btn, 1, 2, 1, 3)

        self.yearEditor = edit

        digits = (("1", "2", "3", "4", "5"), ("6", "7", "8", "9", "0"))
        
        for row, line in enumerate(digits):
            for col, dig in enumerate(line):
                btn = CalcButton(dig, edit)
                layout.addWidget(btn, row+2, col)

        return layout
    
    def nationalCalc(self, calendar, year):
        layout = QGridLayout()
        layout.setContentsMargins(QMargins())

        edit = QLineEdit(year)
        edit.setValidator(calendar)
        edit.setFont(QFont("serif", 16))
        layout.addWidget(edit, 0, 0, 1, 5)

        btn = ClearButton(edit)
        layout.addWidget(btn, 1, 0)
        btn = BackButton(edit)
        layout.addWidget(btn, 1, 1)
        btn = ConvertButton()
        btn.clicked.connect(self.convertToGregorian)
        layout.addWidget(btn, 1, 2, 1, 3)
        
        digits = calendar.CALC
        
        for row, line in enumerate(digits):
            for col, dig in enumerate(line):
                if dig:
                    btn = CalcButton(dig[0], edit)
                    btn.setToolTip(QApplication.translate("YearCalculatorDialog", dig[1]))
                    if len(dig[0]) > 1:
                        layout.addWidget(btn, row+2, col*2, 1, 2)
                    else:
                        layout.addWidget(btn, row+2, col)

        widget = QWidget()
        widget.setLayout(layout)
        widget.EDITOR = edit

        return widget

    def convertGregorian(self):
        text = self.yearEditor.text()
        res, _, _ = self.yearEditor.validator().validate(text, 0)
        if res == QValidator.Acceptable:
            text = self.nationalYearEditor.validator().fromGregorian(int(text))
            self.nationalYearEditor.setText(text)
    
    def convertToGregorian(self):
        text = self.nationalYearEditor.text()
        res, _, _ = self.nationalYearEditor.validator().validate(text, 0)
        if res == QValidator.Acceptable:
            text = self.nationalYearEditor.validator().toGregorian(text)
            self.yearEditor.setText(str(text))
    
    def year(self):
        text = self.yearEditor.text()
        res, _, _ = self.yearEditor.validator().validate(text, 0)
        if res == QValidator.Acceptable:
            return text
        else:
            return ''
    
    def nativeYear(self):
        text = self.nationalYearEditor.text()
        res, _, _ = self.nationalYearEditor.validator().validate(text, 0)
        if res == QValidator.Acceptable:
            return text
        else:
            return ''


class HebrewCalendar(QValidator):
    TITLE = QT_TRANSLATE_NOOP("YearCalculatorDialog", "Hebrew")
    CALC = ((("??", "1"), ("??", "2"), ("??", "3"), ("??", "4"), ("??", "5"),
             ("??", "6"), ("??", "7"), ("??", "8"), ("??", "9")),
            (("??", "10"), ("??", "20"), ("??", "30"), ("??", "40"), ("??", "50"),
             ("??", "60"), ("??", "70"), ("??", "80"), ("??", "90")),
            (None, ("??", "20"), None, ("??", "40"), ("??", "50"),
             None, None, ("??", "80"), ("??", "90")),
            (("??", "100"), ("??", "200"), ("??", "300"), ("??", "400"), None,
             None, None, None, ("??", QT_TRANSLATE_NOOP("YearCalculatorDialog", "Units"))))
    SYMBOLS = "??????????????????????????????????????????????????????????????"

    def validate(self, input_, pos):
        for c in input_:
            if c not in self.SYMBOLS:
                return QValidator.Invalid, input_, pos
        if input_.count('??') > 1:
            return QValidator.Invalid, input_, pos

        if len(input_) > 6:
            return QValidator.Invalid, input_, pos
        
        if len(input_) < 3:
            return QValidator.Intermediate, input_, pos

        if '??' not in input_ or input_[-1] == '??':
            return QValidator.Intermediate, input_, pos

        if input_[-2] != '??':
            return QValidator.Invalid, input_, pos

        return QValidator.Acceptable, input_, pos
    
    def toGregorian(self, year):
        _DIGITS = {"??": 1, "??": 2, "??": 3, "??": 4, "??": 5, "??": 6, "??": 7, "??": 8, "??": 9,
                  "??": 10, "??": 20, "??": 20, "??": 30, "??": 40, "??": 40, "??": 50, "??": 50,
                  "??": 60, "??": 70, "??": 80, "??": 80, "??": 90, "??": 90,
                  "??": 100, "??": 200, "??": 300, "??": 400, "??": 0}
        
        result = 5000
        
        for i in range(len(year)):
            if i == 0 and year[i] == "??":
                continue
            result += _DIGITS[year[i]]
        
        return result - 3760

    def fromGregorian(self, year):
        _GEMATRIOS = {
            1: '??', 2: '??', 3: '??', 4: '??', 5: '??', 6: '??', 7: '??', 8: '??', 9: '??',
            10: '??', 20: '??', 30: '??', 40: '??', 50: '??', 60: '??', 70: '??', 80: '??',
            90: '??', 100: '??', 200: '??', 300: '??', 400: '??'
        }
        
        num = year + 3760
        
        ones = num % 10
        tens = num % 100 - ones
        hundreds = num % 1000 - tens - ones
        four_hundreds = ''.join(['??' for _ in range(hundreds // 400)])
        ones = _GEMATRIOS.get(ones, '')
        tens = _GEMATRIOS.get(tens, '')
        hundreds = _GEMATRIOS.get(hundreds % 400, '')
        if 5708 > num or num > 5740:
            thousands = num // 1000
            thousands = _GEMATRIOS.get(thousands, '')
        else:
            thousands = ''
        letters = thousands + four_hundreds + hundreds + tens + ones
        
        letters = letters.replace('????', '????').replace('????', '????')
        
        if len(letters) > 1:
            letters = letters[:-1] + '??' + letters[-1]
        
        return letters


class IslamicCalendar(QValidator):
    TITLE = QT_TRANSLATE_NOOP("YearCalculatorDialog", "Islamic")
    CALC = ((("??", "1"), ("??", "2"), ("??", "3"), ("??", "4"), ("??", "5"),
             ("??", "6"), ("??", "7"), ("??", "8"), ("??", "9"), ("??", "0")),
            (None, None, None, ("??", "4"), ("??", "5"),
             ("??", "6"), None, None, None, None))
    SYMBOLS = "??????????????????????????"

    def validate(self, input_, pos):
        for c in input_:
            if c not in self.SYMBOLS:
                return QValidator.Invalid, input_, pos

        if len(input_) < 3:
            return QValidator.Intermediate, input_, pos

        if len(input_) > 4:
            return QValidator.Invalid, input_, pos
        
        return QValidator.Acceptable, input_, pos
    
    def toGregorian(self, year):
        _DIGITS = {"??": 1, "??": 2, "??": 3, "??": 4, "??": 4, "??": 5, "??": 5,
                   "??": 6, "??": 6, "??": 7, "??": 8, "??": 9, "??": 0}
        
        result = 0
        for c in year:
            result *= 10
            result += _DIGITS[c]
        
        return math.ceil(0.969697 * result + 622)
    
    def fromGregorian(self, year):
        _DIGITS = {1: "??", 2: "??", 3: "??", 4: "??", 5: "??",
                   6: "??", 7: "??", 8: "??", 9: "??", 0: "??"}
        
        num = int(1.03125 * (year - 622))
        
        ones = num % 10
        tens = (num // 10)  % 10
        hundreds = (num // 100)  % 10
        thousands = (num // 1000)  % 10
        
        letters = _DIGITS[hundreds] + _DIGITS[tens] + _DIGITS[ones]
        if thousands:
            letters = _DIGITS[thousands] + letters
        
        return letters


class SolarHijriCalendar(QValidator):
    TITLE = QT_TRANSLATE_NOOP("YearCalculatorDialog", "Solar hijri")
    CALC = ((("??", "1"), ("??", "2"), ("??", "3"), ("??", "4"), ("??", "5")),
            (("??", "6"), ("??", "7"), ("??", "8"), ("??", "9"), ("??", "0")))
    SYMBOLS = "????????????????????"

    def validate(self, input_, pos):
        for c in input_:
            if c not in self.SYMBOLS:
                return QValidator.Invalid, input_, pos

        if len(input_) < 3:
            return QValidator.Intermediate, input_, pos

        if len(input_) > 4:
            return QValidator.Invalid, input_, pos
        
        return QValidator.Acceptable, input_, pos
    
    def toGregorian(self, year):
        _DIGITS = {"??": 1, "??": 2, "??": 3, "??": 4, "??": 5,
                   "??": 6, "??": 7, "??": 8, "??": 9, "??": 0}
        
        result = 0
        for c in year:
            result *= 10
            result += _DIGITS[c]
        
        return result + 621
    
    def fromGregorian(self, year):
        _DIGITS = {1: "??", 2: "??", 3: "??", 4: "??", 5: "??",
                   6: "??", 7: "??", 8: "??", 9: "??", 0: "??"}
        
        num = year - 621

        ones = num % 10
        tens = (num // 10)  % 10
        hundreds = (num // 100)  % 10
        thousands = (num // 1000)  % 10
        
        letters = _DIGITS[hundreds] + _DIGITS[tens] + _DIGITS[ones]
        if thousands:
            letters = _DIGITS[thousands] + letters
        
        return letters


class JapanCalendar(QValidator):
    TITLE = QT_TRANSLATE_NOOP("YearCalculatorDialog", "Japan")
    CALC = ((("1", ""), ("2", ""), ("3", ""), ("4", ""), ("5", ""),
             ("6", ""), ("7", ""), ("8", ""), ("9", ""), ("0", "")),
            (("???", "1"), ("???", "2"), ("???", "3"), ("???", "4"), ("???", "5"),
             ("???", "6"), ("???", "7"), ("???", "8"), ("???", "9")),
            (("???", "1"), ("???", "10"), ("???", QT_TRANSLATE_NOOP("YearCalculatorDialog", "Year"))),
            (("??????", "1868"), ("??????", "1912"), ("??????", "1926"), ("??????", "1989"), ("??????", "2019")))
    SYMBOLS = "1234567890??????????????????????????????????????????????????????????????????"

    def validate(self, input_, pos):
        for c in input_:
            if c not in self.SYMBOLS:
                return QValidator.Invalid, input_, pos
        if input_.count('???') > 1:
            return QValidator.Invalid, input_, pos

        if len(input_) < 4:
            return QValidator.Intermediate, input_, pos

        if len(input_) > 6:
            return QValidator.Invalid, input_, pos
        
        if "???" in input_:
            letters = input_
            if letters[0] == "???":
                letters = input_[::-1]
    
            if letters[-1] != "???":
                return QValidator.Invalid, input_, pos
    
            if letters[:2] not in ("??????", "??????", "??????", "??????", "??????"):
                return QValidator.Intermediate, input_, pos
            
            for c in letters[2:-1]:
                if c not in "1234567890" and c not in "?????????????????????????????????":
                    return QValidator.Intermediate, input_, pos
        else:
            return QValidator.Intermediate, input_, pos
        
        return QValidator.Acceptable, input_, pos
    
    def toGregorian(self, year):
        if year[0] == "???":
            year = year[::-1]
        
        _DIGITS = {"1": 1, "???": 1, "???": 1, "2": 2, "???": 2, "3": 3, "???": 3,
                   "4": 4, "???": 4, "5": 5, "???": 5, "6": 6, "???": 6, "7": 7,
                   "???": 7, "8": 8, "???": 8, "9": 9, "???": 9, "0": 0, "???": 0}
        
        result = 0
        if year[2] in "1234567890":
            for c in year[2:-1]:
                result *= 10
                result += _DIGITS[c]
        else:
            for c in year[2:-1]:
                if c == "???":
                    if result == 0:
                        result = 10
                    else:
                        result *= 10
                result += _DIGITS[c]
        
        if year[:2] == "??????":
            result += 1868
        elif year[:2] == "??????":
            result += 1912
        elif year[:2] == "??????":
            result += 1926
        elif year[:2] == "??????":
            result += 1989
        elif year[:2] == "??????":
            result += 2019

        return result - 1
    
    def fromGregorian(self, year):
        _DIGITS = {1: "???", 2: "???", 3: "???", 4: "???", 5: "???",
                   6: "???", 7: "???", 8: "???", 9: "???"}
        
        if year >= 2019:
            result = "??????"
            year -= 2019
        elif year >= 1989:
            result = "??????"
            year -= 1989
        elif year >= 1926:
            result = "??????"
            year -= 1926
        elif year >= 1912:
            result = "??????"
            year -= 1912
        else:
            result = "??????"
            year -= 1868
        year += 1
        
        ones = year % 10
        tens = (year // 10)  % 10
        
        if tens > 1:
            result += _DIGITS[tens]
        if tens > 0:
            result += "???"
        if ones:
            result += _DIGITS[ones]

        result += "???"
        
        if year < 1948:
            result[::-1]
        
        return result


class RomanCalendar(QValidator):
    TITLE = QT_TRANSLATE_NOOP("YearCalculatorDialog", "Roman")
    CALC = ((("I", "1"), ("V", "5"), ("X", "10"), ("L", "50"),
             ("C", "100"), ("D", "500"), ("M", "1000")),)
    SYMBOLS = "IVXLCDMivxlcdm"

    def validate(self, input_, pos):
        for c in input_:
            if c not in self.SYMBOLS:
                return QValidator.Invalid, input_, pos

        if len(input_) < 1:
            return QValidator.Intermediate, input_, pos
        
        return QValidator.Acceptable, input_, pos
    
    def toGregorian(self, year):
        trans = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000,
                 'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000}
        values = [trans[r] for r in year]
        return sum(
            val if val >= next_val else -val
            for val, next_val in zip(values[:-1], values[1:])
        ) + values[-1]
    
    def fromGregorian(self, year):
        num = int(year)
        return (
            'M' * (num // 1000) +
            self.encode_digit((num // 100) % 10, 'C', 'D', 'CM') +
            self.encode_digit((num //  10) % 10, 'X', 'L', 'XC') +
            self.encode_digit( num         % 10, 'I', 'V', 'IX') 
        )

    def encode_digit(self, digit, one, five, nine):
        return (
            nine                     if digit == 9 else
            five + one * (digit - 5) if digit >= 5 else
            one + five               if digit == 4 else
            one * digit              
        )


class NepalCalendar(QValidator):
    TITLE = QT_TRANSLATE_NOOP("YearCalculatorDialog", "Nepal")
    CALC = ((("???", "1"), ("???", "2"), ("???", "3"), ("???", "4"), ("???", "5"),
             ("???", "6"), ("???", "7"), ("???", "8"), ("???", "9"), ("???", "0")),
            (("???", "1"), ("???", "2"), ("???", "3"), ("???", "4"), ("???", "5"),
             ("???", "6"), ("???", "7"), ("???", "8"), ("???", "9"), ("???", "0")))
    SYMBOLS = "????????????????????????????????????????????????????????????"

    def validate(self, input_, pos):
        for c in input_:
            if c not in self.SYMBOLS:
                return QValidator.Invalid, input_, pos

        if len(input_) < 4:
            return QValidator.Intermediate, input_, pos

        if len(input_) > 4:
            return QValidator.Invalid, input_, pos

        return QValidator.Acceptable, input_, pos
    
    def toGregorian(self, year):
        _DIGITS = {"???": 0, "???": 1, "???": 2, "???": 3, "???": 4,
                   "???": 5, "???": 6, "???": 7, "???": 8, "???": 9,
                   "???": 0, "???": 1, "???": 2, "???": 3, "???": 4,
                   "???": 5, "???": 6, "???": 7, "???": 8, "???": 9}
        
        result = 0
        for c in year:
            result *= 10
            result += _DIGITS[c]
        
        if result < 1823:
            return result + 78
        return result - 57
    
    def fromGregorian(self, year):
        _DIGITS = {1: "???", 2: "???", 3: "???", 4: "???", 5: "???",
                   6: "???", 7: "???", 8: "???", 9: "???", 0: "???"}
        
        if year < 1901:
            num = year - 78
        else:
            num = year + 57
        
        ones = num % 10
        tens = (num // 10)  % 10
        hundreds = (num // 100)  % 10
        thousands = (num // 1000)  % 10
        
        letters = _DIGITS[hundreds] + _DIGITS[tens] + _DIGITS[ones]
        if thousands:
            letters = _DIGITS[thousands] + letters
        
        return letters


class ThaiCalendar(QValidator):
    TITLE = QT_TRANSLATE_NOOP("YearCalculatorDialog", "Thai")
    CALC = ((("???", "1"), ("???", "2"), ("???", "3"), ("???", "4"), ("???", "5")),
            (("???", "6"), ("???", "7"), ("???", "8"), ("???", "9"), ("???", "0")))
    SYMBOLS = "??????????????????????????????"

    def validate(self, input_, pos):
        for c in input_:
            if c not in self.SYMBOLS:
                return QValidator.Invalid, input_, pos

        if len(input_) < 3:
            return QValidator.Intermediate, input_, pos

        if len(input_) > 4:
            return QValidator.Invalid, input_, pos

        return QValidator.Acceptable, input_, pos
    
    def toGregorian(self, year):
        _DIGITS = {"???": 0, "???": 1, "???": 2, "???": 3, "???": 4,
                   "???": 5, "???": 6, "???": 7, "???": 8, "???": 9}
        
        result = 0
        for c in year:
            result *= 10
            result += _DIGITS[c]
        
        if 1197 <= result and result <= 1249:
            return result + 638
        elif result <= 131:
            return result + 1781
        return result - 543
    
    def fromGregorian(self, year):
        _DIGITS = {1: "???", 2: "???", 3: "???", 4: "???", 5: "???",
                   6: "???", 7: "???", 8: "???", 9: "???", 0: "???"}
        
        if 1835 <= year and year <= 1887:
            num = year - 638
        elif year <= 1912:
            num = year - 1781
        else:
            num = year + 543
        
        ones = num % 10
        tens = (num // 10)  % 10
        hundreds = (num // 100)  % 10
        thousands = (num // 1000)  % 10
        
        letters = _DIGITS[hundreds] + _DIGITS[tens] + _DIGITS[ones]
        if thousands:
            letters = _DIGITS[thousands] + letters
        
        return letters


class BurmeseCalendar(QValidator):
    TITLE = QT_TRANSLATE_NOOP("YearCalculatorDialog", "Burmese")
    CALC = ((("???", "1"), ("???", "2"), ("???", "3"), ("???", "4"), ("???", "5")),
            (("???", "6"), ("???", "7"), ("???", "8"), ("???", "9"), ("???", "0")))
    SYMBOLS = "??????????????????????????????"

    def validate(self, input_, pos):
        for c in input_:
            if c not in self.SYMBOLS:
                return QValidator.Invalid, input_, pos

        if len(input_) < 4:
            return QValidator.Intermediate, input_, pos

        if len(input_) > 4:
            return QValidator.Invalid, input_, pos

        return QValidator.Acceptable, input_, pos
    
    def toGregorian(self, year):
        _DIGITS = {"???": 0, "???": 1, "???": 2, "???": 3, "???": 4,
                   "???": 5, "???": 6, "???": 7, "???": 8, "???": 9}
        
        result = 0
        for c in year:
            result *= 10
            result += _DIGITS[c]
        
        if result <= 1247:
            return result + 638
        return result
    
    def fromGregorian(self, year):
        _DIGITS = {1: "???", 2: "???", 3: "???", 4: "???", 5: "???",
                   6: "???", 7: "???", 8: "???", 9: "???", 0: "???"}
        
        if 1852 <= year and year <= 1885:
            num = year - 638
        else:
            num = year
        
        ones = num % 10
        tens = (num // 10)  % 10
        hundreds = (num // 100)  % 10
        thousands = (num // 1000)  % 10
        
        letters = _DIGITS[hundreds] + _DIGITS[tens] + _DIGITS[ones]
        if thousands:
            letters = _DIGITS[thousands] + letters
        
        return letters


class GregorianValidator(QValidator):
    def validate(self, input_, pos):
        if len(input_) == 0:
            return QValidator.Intermediate, input_, pos

        try:
            val = int(input_)
        except ValueError:
            return QValidator.Invalid, input_, pos

        if 0 > val or val > 2500:
            return QValidator.Invalid, input_, pos

        return QValidator.Acceptable, input_, pos


class CalcButton(QPushButton):
    def __init__(self, text, editor, parent=None):
        super().__init__(text, parent)
        
        self.editor = editor
        
        font = QFont("serif", 20)
        self.setFont(font)

        if len(text) > 1:
            self.setFixedWidth(80)
        else:
            self.setFixedWidth(40)
        self.setFixedHeight(40)
        
        self.clicked.connect(self.onClicked)

    def onClicked(self):
        new_text = self.editor.text() + self.text()
        res, new_text, _ = self.editor.validator().validate(new_text, 0)
        if res != QValidator.Invalid:
            self.editor.setText(new_text)


class ClearButton(QPushButton):
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        
        self.editor = editor
        
        self.setFixedWidth(40)
        self.setFixedHeight(40)
        self.setToolTip(self.tr("Clear"))
        self.setIcon(QIcon(':/cross.png'))
        
        self.clicked.connect(self.onClicked)

    def onClicked(self):
        self.editor.clear()


class BackButton(QPushButton):
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        
        self.editor = editor
        
        self.setFixedWidth(40)
        self.setFixedHeight(40)
        self.setToolTip(self.tr("Backspace"))
        self.setIcon(QIcon(':/backspace.png'))
        
        self.clicked.connect(self.onClicked)

    def onClicked(self):
        text = self.editor.text()
        if text:
            self.editor.setText(text[:-1])


class ConvertButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        font = QFont("serif", 16)
        self.setFont(font)

        self.setFixedHeight(40)
        self.setToolTip(self.tr("Convert"))
        self.setText("  " + self.tr("Convert"))
        self.setIcon(QIcon(':/tick.png'))
