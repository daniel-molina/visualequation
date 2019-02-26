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

import os
import subprocess

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import eqtools
from . import commons
from . import conversions

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
        copybutton = QPushButton(_('Copy to Clipboard'))
        copybutton.clicked.connect(self.handlecopy)
        msg = QLabel(_('Tip: If you pretend to copy the code, do'
                       ' not close the program before'
                       ' pasting.'))
        msg.setWordWrap(True)
        self.onlysel = QCheckBox(_('Only selection'))
        self.onlysel.setChecked(True)
        self.onlysel.stateChanged.connect(self.settext)
        self.fullcode = QCheckBox(_('Full code'))
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
        
class EditLatexDialog(QDialog):
    def __init__(self, latexblock, temp_dir, parent=None):
        super().__init__(parent)
        self.temp_dir = temp_dir
        self.setWindowTitle(_('Edit LaTeX code'))
        self.resize(600, 600)
        self.eqblock = QLabel(self)
        self.eqblock.setAlignment(Qt.AlignCenter)
        eqblock_im = conversions.eq2png(latexblock, 300, None, self.temp_dir)
        self.eqblock.setPixmap(QPixmap(eqblock_im))
        self.scrollarea = QScrollArea(self)
        self.scrollarea.setWidget(self.eqblock)
        self.scrollarea.setWidgetResizable(True)
        
        self.text = QTextEdit(self)
        self.text.insertPlainText(latexblock)
        self.text.moveCursor(QTextCursor.Start)
        self.text.setFocus()
        self.text.textChanged.connect(self.ontextchanged)
        regexp = QRegExp(
            "^[a-zA-Z\d\s|!\\$%&/()=?'@#\\[\\]{}*+-<>,.;:_\n\t\\^\\\\]*$")
        self.validator = QRegExpValidator(regexp)
        self.checkbutton = QPushButton(_('Check LaTeX code'))
        self.checkbutton.clicked.connect(self.handlecheck)
        self.checkbutton.setDisabled(True)
        self.compilationmsg = QLabel(_('Change LaTeX code as desired'))
        self.compilationmsg.setWordWrap(True)
        warnmsg = QLabel(
            _('Note: It will not be possible to select individual elements'
              ' of this block if it is edited.'))
        warnmsg.setWordWrap(True)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Cancel |
                                        QDialogButtonBox.Ok,
                                        Qt.Horizontal,
                                        self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.scrollarea)
        vbox.addWidget(self.text)
        vbox.addWidget(self.checkbutton)
        vbox.addWidget(self.compilationmsg)
        vbox.addWidget(warnmsg)
        vbox.addWidget(self.buttons)

    def ontextchanged(self):
        self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
        self.compilationmsg.setText(_('Press Check button when code is ready'))
        state = self.validator.validate(self.text.toPlainText(), 0)[0]
        if state != QValidator.Acceptable:
            self.compilationmsg.setText(
                _('LaTeX code contains invalid characters'))
            self.checkbutton.setDisabled(True)
        else:
            self.checkbutton.setEnabled(True)


        
    def handlecheck(self):
        self.compilationmsg.setText(_('Checking LateX code...'))
        latex_file = os.path.join(self.temp_dir, "edit.tex")
        conversions.eq2latex_file(self.text.toPlainText(), latex_file,
                                  commons.LATEX_TEMPLATE)
        try:
            subprocess.check_output(["latex", "-interaction=nonstopmode",
                                     "-halt-on-error",
                                     "-output-directory=" + self.temp_dir,
                                     latex_file])
        except subprocess.CalledProcessError as error:
            self.compilationmsg.setText(_('LaTex code is not valid'))
            self.checkbutton.setDisabled(True)
            self.text.setFocus()
            return
        dvi_file = os.path.join(self.temp_dir, "edit.dvi")
        dvi_log = os.path.join(self.temp_dir, "edit.log")
        png_file = os.path.join(self.temp_dir, "edit.png")
        conversions.dvi2png(dvi_file, png_file, dvi_log, 300, None)
        self.eqblock.setPixmap(QPixmap(png_file))
        self.compilationmsg.setText(_('LaTex code is valid'))
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
        self.text.setFocus()

    @staticmethod
    def editlatex(latexblock, temp_dir, parent=None):
        dialog = EditLatexDialog(latexblock, temp_dir, parent)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            return dialog.text.toPlainText()
        else:
            return None
