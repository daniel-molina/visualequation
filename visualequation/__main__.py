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
import sys
import tempfile
import shutil
import os
import argparse
import traceback
import gettext
import locale
import faulthandler
faulthandler.enable()

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import commons
gettext.install('visualequation')
# Check if user language is available for translation
if locale.getlocale()[0] != None:
    if locale.getlocale()[0][0:2] == "es":
        es = gettext.translation('visualequation', commons.LOCALE_DIR,
                                 languages=['es'])
        es.install()

from . import symbolstab
from . import eqlabel
from . import conversions
from . import eqtools
from . import game
from . import latexdialogs
from .errors import ShowError

class MyScrollBar(QScrollBar):
    """
    Class to set focus in equation when moving the scroll bars.
    It also moves the equation correctly when inserting new elements.
    """
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.prev_max = None

    def mouseReleaseEvent(self, event):
        QScrollBar.mouseReleaseEvent(self, event)
        self.equation.setFocus()
            
    def setFocusTo(self, widget):
        self.equation = widget

    def sliderChange(self, change):
        QScrollBar.sliderChange(self, change)
        # Do not use/set prev_max vertically
        if change == QAbstractSlider.SliderRangeChange and \
           self.orientation() == Qt.Horizontal:
            if self.prev_max != None:
                self.setValue(self.value() + self.maximum() - self.prev_max)
            self.prev_max = self.maximum()
            
class MyScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vbar = MyScrollBar(Qt.Vertical, self)
        self.hbar = MyScrollBar(Qt.Horizontal, self)
        self.setVerticalScrollBar(self.vbar)
        self.setHorizontalScrollBar(self.hbar)

    def setWidget(self, widget):
        QScrollArea.setWidget(self, widget)
        self.vbar.setFocusTo(widget)
        self.hbar.setFocusTo(widget)
        
class MainWindow(QMainWindow):
    def __init__(self, temp_dir):
        super().__init__()
        self.temp_dir = temp_dir
        ShowError.default_parent = self
        self.init_center_widget()
        self.statusBar()
        self.init_menu()

        self.setWindowTitle('Visual Equation')
        self.setWindowIcon(QIcon(commons.ICON))
        self.resize(900, 600)

    def init_menu(self):
        # File
        new_act = QAction(_('&New'), self)
        new_act.setShortcut('Ctrl+N')
        new_act.setStatusTip(_('Create a new equation'))
        new_act.triggered.connect(self.maineq.eq.new_eq)
        open_act = QAction(_('&Open'), self)
        open_act.setShortcut('Ctrl+O')
        open_act.setStatusTip(_('Open equation from image'))
        open_act.triggered.connect(self.maineq.eq.open_eq)
        save_act = QAction(_('&Save'), self)
        save_act.setShortcut('Ctrl+S')
        save_act.setStatusTip(_('Save image'))
        save_act.triggered.connect(self.maineq.eq.save_eq)
        exit_act = QAction(_('&Exit'), self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip(_('Exit application'))
        exit_act.triggered.connect(qApp.quit)
        # Edit
        undo_act = QAction(_('&Undo'), self)
        undo_act.setShortcut('Ctrl+Z')
        undo_act.setStatusTip(_('Return equation to previous state'))
        undo_act.triggered.connect(self.maineq.eq.recover_prev_eq)
        redo_act = QAction(_('&Redo'), self)
        redo_act.setShortcut('Ctrl+Y')
        redo_act.setStatusTip(_('Recover next equation state'))
        redo_act.triggered.connect(self.maineq.eq.recover_next_eq)
        copy_act = QAction(_('&Copy'), self)
        copy_act.setShortcut('Ctrl+C')
        copy_act.setStatusTip(_('Copy selection'))
        copy_act.triggered.connect(self.maineq.eq.sel2eqbuffer)
        def cut():
            self.maineq.eq.sel2eqbuffer()
            self.maineq.eq.remove_sel()
        cut_act = QAction(_('C&ut'), self)
        cut_act.setShortcut('Ctrl+X')
        cut_act.setStatusTip(_('Cut selection'))
        cut_act.triggered.connect(cut)
        paste_act = QAction(_('&Paste'), self)
        paste_act.setShortcut('Ctrl+V')
        paste_act.setStatusTip(_('Paste previous cut or copied selection'))
        paste_act.triggered.connect(self.maineq.eq.eqbuffer2sel)
        def editlatex():
            oldlatexcode = eqtools.eqblock2latex(self.maineq.eq.eq,
                                                 self.maineq.eq.eqsel.index)[0]
            newlatexcode = latexdialogs.EditLatexDialog.editlatex(
                oldlatexcode, self.temp_dir, self)
            if newlatexcode:
                self.maineq.eq.insert_substituting(newlatexcode)
        editlatex_act = QAction(_('Edit LaTeX'), self)
        editlatex_act.setStatusTip(_('Edit LaTeX code of selected block'))
        editlatex_act.triggered.connect(editlatex)
        def selectall():
            self.maineq.eq.eqsel.index = 0
            self.maineq.eq.eqsel.display()
        selectall_act = QAction('&Select all', self)
        selectall_act.setShortcut('Ctrl+A')
        selectall_act.setStatusTip(_('Select the entire equation'))
        selectall_act.triggered.connect(selectall)
        # View
        def zoomin():
            if self.maineq.eq.eqsel.dpi < 1000:
               self.maineq.eq.eqsel.dpi += 50
               self.maineq.eq.eqsel.display()
            else:
                ShowError(_('Equation will no be increased.'), False)
        zoomin_act = QAction(_('Zoom &In'), self)
        zoomin_act.setShortcut('Ctrl++')
        zoomin_act.setStatusTip(_('Increase size of the equation'))
        zoomin_act.triggered.connect(zoomin)
        def zoomout():
            if self.maineq.eq.eqsel.dpi >= 100:
               self.maineq.eq.eqsel.dpi -= 50
               self.maineq.eq.eqsel.display()
            else:
                ShowError(_('Equation will no be decreased.'), False)
        zoomout_act = QAction(_('Zoom &Out'), self)
        zoomout_act.setShortcut('Ctrl+-')
        zoomout_act.setStatusTip(_('Decrease size of the equation'))
        zoomout_act.triggered.connect(zoomout)
        def showlatex():
            latexdialogs.ShowLatexDialog.showlatex(self.maineq.eq, self)
        showlatex_act = QAction(_('Show &LaTeX code'), self)
        showlatex_act.setStatusTip(
            _('Show the LaTeX code generating the equation'))
        showlatex_act.triggered.connect(showlatex)
        # Games
        def alice():
            state = activate_game_act.isChecked()
            game.Game.activate(state)
            self.maineq.eq.eqsel.display(self.maineq.eq.eq,
                                         self.maineq.eq.eqsel.right)
        activate_game_act = QAction(_('Invite &Alice'), self, checkable=True)
        activate_game_act.triggered.connect(alice)
        activate_game_act.setStatusTip(_('Let Alice to be with you while '
                                         'building the equation'))
        # Help
        usage_act = QAction(_('Basic &usage'), self)
        usage_act.setShortcut('Ctrl+H')
        usage_act.setStatusTip(_('Basic usage of the program'))
        usage_act.triggered.connect(self.usage)
        about_act = QAction(_('About &Visual Equation'), self)
        about_act.triggered.connect(self.about)
        aboutQt_act = QAction(_('About &Qt'), self)
        aboutQt_act.triggered.connect(QApplication.aboutQt)

        # Define menuBar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        file_menu = menubar.addMenu(_('&File'))
        file_menu.addAction(new_act)
        file_menu.addAction(open_act)
        file_menu.addAction(save_act)      
        file_menu.addSeparator()
        file_menu.addAction(exit_act)
        edit_menu = menubar.addMenu(_('&Edit'))
        edit_menu.addAction(undo_act)
        edit_menu.addAction(redo_act)
        edit_menu.addSeparator()
        edit_menu.addAction(copy_act)
        edit_menu.addAction(cut_act)
        edit_menu.addAction(paste_act)
        edit_menu.addSeparator()
        edit_menu.addAction(editlatex_act)
        edit_menu.addSeparator()
        edit_menu.addAction(selectall_act)
        view_menu = menubar.addMenu(_('&View'))
        view_menu.addAction(zoomin_act)
        view_menu.addAction(zoomout_act)
        view_menu.addSeparator()
        view_menu.addAction(showlatex_act)
        game_menu = menubar.addMenu(_('&Games'))
        game_menu.addAction(activate_game_act)
        help_menu = menubar.addMenu(_('&Help'))
        help_menu.addAction(usage_act)
        help_menu.addAction(aboutQt_act)
        help_menu.addAction(about_act)

    def init_center_widget(self):
        # Create central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        # Create the equation
        self.maineq = eqlabel.EqLabel(self.temp_dir, self)
        self.maineq.setAlignment(Qt.AlignCenter)
        self.scrollarea = MyScrollArea(self)
        self.scrollarea.setWidget(self.maineq)
        self.scrollarea.setWidgetResizable(True)
        # Create the symbols TabWidget
        self.tabs = symbolstab.TabWidget(self, self.maineq)
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Add everything to the central widget
        layout.addWidget(self.scrollarea)
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)
        self.maineq.setFocus()

    def usage(self):

        usagestr = _("<p>Visual Equation is expected to be user-friendly "
        "and intuitive, so it should not be difficult to use if you "
        "understand its usage. Basically:</p>"
        "<p>Instead of a cursor, you navigate with a \"ghost\" that "
        "surrounds blocks of the equation, from single symbols to arguments, "
        "operators and the entire equation. Change the ghost's selection and "
        "insert characters at the direction in which the ghost is facing "
        "by pressing keys on the keyboard or clicking symbols "
        "in the bottom panel. If the ghost surrounds a square, "
        "as when you open the program, you overwrite the square.</p>"
        "<p>These are the main keys:</p>"
        "<ul>"
        "<li><b>LEFT</b>: "
        "Change the direction of the ghost to the left or "
        "navigate backwards.</li>"
        "<li><b>RIGHT</b> or <b>TAB</b>: "
        "Change the direction of the ghost to right or "
        "navigate forwards.</li>"
        "<li><b>UP</b> and <b>DOWN</b>: "
        "Put a superindex or subindex in the direction "
        "pointed by the ghost.</li>"
        "<li><b>DELETE</b> or <b>BACKSPACE</b>: "
        "Remove current selection. If it was the entire argument "
        "of an operator, a square will remain so you can change it "
        "by something else.</li>"
        "<li><b>Left-click</b> on an element of the symbols panel: "
        "Insert the element where the ghost is facing.</li>"
        "<li><b>SHIFT + Left-click</b> on an element of the symbols panel "
        "(<b>VERY handy</b>): "
        "If the element is an operator, the selection is replaced "
        "by the operator and its first argument is set to previous selection. "
        "(The first argument is the one represented by dots) "
        "If the element is a symbol, the selection is replaced "
        "by the symbol.</li>"
        "</ul>"
        "<p>You may learn also the short-cuts noted in the menu.</p>")

        class Dialog(QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setWindowTitle(_('Basic usage'))
                text = QTextEdit(self)
                text.setReadOnly(True)
                text.insertHtml(usagestr)
                text.moveCursor(QTextCursor.Start)
                buttons = QDialogButtonBox(QDialogButtonBox.Ok, self)
                vbox = QVBoxLayout(self)
                vbox.addWidget(text)
                vbox.addWidget(buttons)
                buttons.accepted.connect(self.accept)
        dialog = Dialog(self)
        dialog.exec_()

    def about(self):
        msg = _("<p>Visual Equation</p>"
            "<p><em>Version:</em> %s </p>"
            "<p><em>Author:</em> Daniel Molina Garcia</P>"
            '<p><em>Sources:</em> '
            '<a href="https://github.com/daniel-molina/visualequation">'
            "Webpage</a></p>"
            "<p><em>License:</em> GPLv3 or above</p>") % commons.VERSION
        QMessageBox.about(self, _("About"), msg)


def main():
    """ This the main function of the program."""
    # Command line options
    parser = argparse.ArgumentParser(
        description=_("Create equations visually."),
        prog="visualequation")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + commons.VERSION)
    parser.parse_args()

    # Catch all exceptions by installing a global exception hook
    #sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback_error):
        #sys._excepthook(exctype, value, traceback_error)
        ShowError('Unhandled exception. Feel free to report this incident'
                  " with the following traceback code:\n"
                  + ''.join(traceback.format_tb(traceback_error)),
                  True)
    sys.excepthook = exception_hook

    # Use global for app to be destructed at the end
    # http://pyqt.sourceforge.net/Docs/PyQt5/gotchas.html#crashes-on-exit
    global app 
    app = QApplication(sys.argv)

    # Prepare a temporal directory to manage all intermediate files
    temp_dirpath = tempfile.mkdtemp()

    win = MainWindow(temp_dirpath)

    win.show()

    exit_code = app.exec_()
    shutil.rmtree(temp_dirpath)
    sys.exit(exit_code)
   
if __name__ == '__main__':
    main()
