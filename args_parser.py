import argparse
import textwrap
import sys


class ConsoleArgsParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(ConsoleArgsParser, self).__init__(*args, **kwargs)
        self.prog = 'Coursera courses'
        self.formatter_class = argparse.RawDescriptionHelpFormatter
        self.description = textwrap.dedent('''\
                      Script creates a XLSX file with information about Coursera courses.
                      In this file you will find the name of the course, it's language and
                      date of beginning, moreover there will be the course length in weeks
                      and average course rating.\n
                      -----------------------------------------------------------------
                      If you want to stop the program press Ctrl+C.
                      ------------------------------------------------------------------
                      This program had been tested on Python 3.5.2.
                      ''')
        self.add_argument('saving_dist', nargs='*',
                          help='Specify the full path to folder and filename\
                              e.g /home/user/documents/courses.xlsx, \
                              else result will be saved at the program\'s folder.',
                          type=argparse.FileType('w'), default=None)

    def error(self, message):
        sys.stderr.write('error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)
