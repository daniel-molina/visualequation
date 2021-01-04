#!/usr/bin/env python3

# visualequation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# visualequation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""This is the file to execute the program."""
import gettext
import locale
import argparse
import faulthandler
import shutil
import sys
import tempfile
import traceback

from PyQt5.QtWidgets import QApplication

from visualequation import commons

gettext.install('visualequation')
# Check if user language is available for translation
if locale.getlocale()[0] is not None:
    if locale.getlocale()[0][0:2] == "es":
        es = gettext.translation('visualequation', commons.LOCALE_DIR,
                                 languages=['es'])
        es.install()
    # New languages here...

from visualequation.errors import ShowError
from visualequation import gui

faulthandler.enable()


def main():
    """ This the main function of the program."""
    # Command line options
    parser = argparse.ArgumentParser(
        description=_("Create equations visually."),
        prog="visualequation")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + commons.VERSION)
    parser.add_argument('--debug', action="store_true",
                        help="send debug information to stdout")
    args = parser.parse_args()

    # Catch all exceptions by installing a global exception hook
    # sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback_error):
        # sys._excepthook(exctype, value, traceback_error)
        ShowError('Unhandled exception. Feel free to report this incident'
                  ' with the following traceback code:\n\n'
                  + str(value) + '\n\n'
                  + ''.join(traceback.format_tb(traceback_error)),
                  True)

    sys.excepthook = exception_hook

    # Use global for app to be destructed at the end
    # http://pyqt.sourceforge.net/Docs/PyQt5/gotchas.html#crashes-on-exit
    global app
    app = QApplication(sys.argv)
    # QApplication does a setlocale(LC_ALL, '') under GNU/Linux.
    # That affects vedvipng's calls to sstrtod, e.g.. As explained here:
    # https://stackoverflow.com/questions/25661295/why-does-qcoreapplication
    # -call-setlocalelc-all-by-default-on-unix-linux
    # recommended solution is to use the following instruction
    locale.setlocale(locale.LC_NUMERIC, 'C')

    # Prepare a temporal directory to manage all intermediate files
    temp_dirpath = tempfile.mkdtemp()

    win = gui.MainWindow(temp_dirpath, args)

    win.show()

    exit_code = app.exec_()
    shutil.rmtree(temp_dirpath)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
