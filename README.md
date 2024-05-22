[![GitHub release](https://img.shields.io/github/release/opennumismat/YearCalculator.svg)](https://github.com/opennumismat/YearCalculator/releases/)
[![GitHub release (latest by date)](https://img.shields.io/github/downloads/opennumismat/YearCalculator/latest/total.svg)](https://hanadigital.github.io/grev/?user=OpenNumismat&repo=YearCalculator)
[![GitHub all releases](https://img.shields.io/github/downloads/opennumismat/YearCalculator/total.svg)](https://hanadigital.github.io/grev/?user=OpenNumismat&repo=YearCalculator)
[![GitHub license](https://img.shields.io/github/license/opennumismat/YearCalculator.svg)](https://github.com/opennumismat/YearCalculator/blob/master/LICENSE)

# YearCalculator

With YearCalculator you can convert Gregorian year to other calendar system (Hebrew, Islamic, Solar hijri, Japan, Roman, Nepal, Thai, Burmese) and Vice Versa.

YearCalculator is a part of [OpenNumismat](https://opennumismat.github.io/) project, so it aims to convert years on coins.

![Screenshot](https://opennumismat.github.io/images/YearCalculator.png)

#### Download
[Latest version for Windows 10 and later](https://github.com/OpenNumismat/YearCalculator/releases/latest)

[Version 0.1 for Windows XP and later](https://github.com/OpenNumismat/YearCalculator/releases/download/0.1/YearCalculator.zip)

#### Usage
    YearCalculator.exe [-h] [-l {en,bg,de,es,pt,ru,sl,uk}] [-g GREGORIAN] [-n NATIVE]
                       [-c {hebrew,islamic,iranian,japanese,roman,nepal,thai,burmese}]

    options:
      -l {en,bg,de,es,pt,ru,sl,uk}, --lang {en,bg,de,es,pt,ru,sl,uk}
                            UI language. If not specified, the system language is used
      -g GREGORIAN, --gregorian GREGORIAN
                            Initial gregorian year
      -n NATIVE, --native NATIVE
                            Initial year in native calendar
      -c {hebrew,islamic,iranian,japanese,roman,nepal,thai,burmese}, --calendar {hebrew,islamic,iranian,japanese,roman,nepal,thai,burmese}

#### For run from source code
    pip3 install -r requirements.txt
    python3 src/run.py
