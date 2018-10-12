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

from .utils import *

def variablesize(parent, code):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Variable-size operator')
            self.suplimit = QCheckBox("Limit over the sign")
            self.suplimit.setChecked(True)
            self.inflimit = QCheckBox("Limit under the sign")
            self.inflimit.setChecked(True)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            self.buttons.button(QDialogButtonBox.Ok).setFocus()
            vbox = QVBoxLayout(self)
            vbox.addWidget(self.suplimit)
            vbox.addWidget(self.inflimit)
            vbox.addWidget(self.buttons)

            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        @staticmethod
        def get(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return ((dialog.suplimit.isChecked(),
                         dialog.inflimit.isChecked()),
                        True)
            else:
                return ((None, None), False)
            
    (sup, inf), ok = Dialog.get(parent)
    if ok:
        if sup and inf:
            latex_code = code + r"_{{{0}}}^{{{1}}}"
            n_operands = 2
        elif sup:
            latex_code = code + r"^{{{0}}}"
            n_operands = 1
        elif inf:
            latex_code = code + r"_{{{0}}}"
            n_operands = 1
        else:
            latex_code = code
            n_operands = 0
        return Op(n_operands, latex_code, "vsize")
    else:
        return None

def f(code):
    return lambda parent: variablesize(parent, code)

def integrals(parent, code):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Integral operator')
            self.suplimit = QCheckBox("Argument over the integral sign")
            self.inflimit = QCheckBox("Argument under the integral sign")
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            self.buttons.button(QDialogButtonBox.Ok).setFocus()
            vbox = QVBoxLayout(self)
            vbox.addWidget(self.suplimit)
            vbox.addWidget(self.inflimit)
            vbox.addWidget(self.buttons)

            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        @staticmethod
        def get(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return ((dialog.suplimit.isChecked(),
                         dialog.inflimit.isChecked()),
                        True)
            else:
                return ((None, None), False)
            
    (sup, inf), ok = Dialog.get(parent)
    if ok:
        if sup and inf:
            latex_code = code + r"\limits_{{{0}}}^{{{1}}}"
            n_operands = 2
        elif sup:
            latex_code = code + r"\limits^{{{0}}}"
            n_operands = 1
        elif inf:
            latex_code = code + r"\limits_{{{0}}}"
            n_operands = 1
        else:
            return Op(0, code, "int_empty")
        return Op(n_operands, latex_code, "int_with_args")
    else:
        return None

def fint(code):
    return lambda parent: integrals(parent, code)


VARIABLESIZE = [
    LatexSymb('sum', f(r'\sum')),
    LatexSymb('prod', f(r'\prod')),
    LatexSymb('coprod', f(r'\coprod')),
    LatexSymb('int', fint(r'\int')),
    LatexSymb('iint', fint(r'\iint')),
    LatexSymb('iiint', fint(r'\iiint')),
    LatexSymb('iiiint', fint(r'\iiiint')),
    LatexSymb('dotsint', fint(r'\dotsint')),
    LatexSymb('oint', fint(r'\oint')),
    LatexSymb('oiint', fint(r'\oiint')),
    LatexSymb('sqint', fint(r'\sqint')),
    LatexSymb('sqiint', fint(r'\sqiint')),
    LatexSymb('ointctrclockwise', fint(r'\ointctrclockwise')),
    LatexSymb('ointclockwise', fint(r'\ointclockwise')),
    LatexSymb('biguplus', f(r'\biguplus')),
    LatexSymb('bignplus', f(r'\bignplus')),
    LatexSymb('bigcup', f(r'\bigcup')),
    LatexSymb('bigcap', f(r'\bigcap')),
    LatexSymb('bigoplus', f(r'\bigoplus')),
    LatexSymb('bigotimes', f(r'\bigotimes')),
    LatexSymb('bigodot', f(r'\bigodot')),
    LatexSymb('bigvee', f(r'\bigvee')),
    LatexSymb('bigwedge', f(r'\bigwedge')),
    LatexSymb('bigsqcup', f(r'\bigsqcup')),
    LatexSymb('bigsqcap', f(r'\bigsqcap')),
]
