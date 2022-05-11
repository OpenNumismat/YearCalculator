# coding: utf-8

from cx_Freeze import setup, Executable

executables = [Executable('src/main.py',
                          targetName='YearCalculator.exe',
                          base='Win32GUI',
                          icon='src/icons/date.ico')]

options = {
    'build_exe': {
        'include_msvcr': True,
        'build_exe': 'build_windows',
        'include_files': ['src/resources.py', 'src/YearCalculator.py'],
    }
}

setup(name='YearCalculator',
      version='0.1',
      description='YearCalculator',
      executables=executables,
      options=options)
