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

""" The module that manages the user interaction with LaTeX code."""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import eqtools
from . import commons

class ShowLatexDialog(QDialog):
    def __init__(self, eq, parent=None):
        super().__init__(parent)
        self.eq = eq.eq
        self.index = eq.eqsel.index
        self.setWindowTitle('LaTeX code')
        self.text = QTextEdit(self)
        self.text.insertPlainText(eqtools.eqblock2latex(self.eq,
                                                        self.index)[0])
        self.text.moveCursor(QTextCursor.Start)
        self.text.setReadOnly(True)
        copybutton = QPushButton('Copy to Clipboard')
        msg = QLabel('Tip: If you pretend to copy it, do\n'
                     + 'not close the program before\n'
                     + 'pasting.')
        copybutton.clicked.connect(self.handlecopy)
        self.onlysel = QCheckBox('Only selection')
        self.onlysel.setChecked(True)
        self.onlysel.stateChanged.connect(self.settext)
        self.fullcode = QCheckBox('Full code')
        self.fullcode.setChecked(False)
        self.fullcode.stateChanged.connect(self.settext)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok, Qt.Horizontal,
                                        self)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.text)
        vbox.addWidget(self.onlysel)
        vbox.addWidget(self.fullcode)
        vbox.addWidget(copybutton)
        vbox.addWidget(msg)
        vbox.addWidget(self.buttons)
        self.buttons.accepted.connect(self.accept)

    def handlecopy(self):
        self.text.selectAll()
        self.text.copy()

    def settext(self):
        self.text.clear()
        if self.onlysel.isChecked():
            formulalatex = eqtools.eqblock2latex(self.eq, self.index)[0]
        else:
            formulalatex = eqtools.eqblock2latex(self.eq, 0)[0]
        if self.fullcode.isChecked():
            with open(commons.LATEX_TEMPLATE, "r") as ftempl:
                for line in ftempl:
                    self.text.insertPlainText(
                        line.replace('%EQ%', formulalatex))
        else:
            self.text.insertPlainText(formulalatex)
            
    @staticmethod
    def showlatex(eq, parent=None):
        dialog = ShowLatexDialog(eq, parent)
        dialog.exec_()
        return None
