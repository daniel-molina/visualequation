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

            self.setWindowTitle(_('Variable-size operator'))
            self.suplimit = QCheckBox(_("Limit over the sign"))
            self.suplimit.setChecked(True)
            self.inflimit = QCheckBox(_("Limit under the sign"))
            self.inflimit.setChecked(True)
            self.msg = QLabel(
                _("Note: It is also possible to put arguments"
                  " in the corners of the operator by"
                  " surrounding the operator and using keys"
                  " UP and DOWN."))
            self.msg.setWordWrap(True)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            self.buttons.button(QDialogButtonBox.Ok).setFocus()
            vbox = QVBoxLayout(self)
            vbox.addWidget(self.suplimit)
            vbox.addWidget(self.inflimit)
            vbox.addWidget(self.msg)
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
                return (None, None), False

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

            self.setWindowTitle(_('Integral operator'))
            self.suplimit = QCheckBox(_("Argument over the integral sign"))
            self.inflimit = QCheckBox(_("Argument under the integral sign"))
            self.msg = QLabel(
                _("Note: Leaving boxes unchecked will allow"
                  " to put the limits in the corners of the"
                  " integral by surrounding the integral and"
                  " using keys UP and DOWN."))
            self.msg.setWordWrap(True)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            self.buttons.button(QDialogButtonBox.Ok).setFocus()
            vbox = QVBoxLayout(self)
            vbox.addWidget(self.suplimit)
            vbox.addWidget(self.inflimit)
            vbox.addWidget(self.msg)
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
                return (None, None), False

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
    Symbol('sum', f(r'\sum')),
    Symbol('prod', f(r'\prod')),
    Symbol('coprod', f(r'\coprod')),
    Symbol('int', fint(r'\int')),
    Symbol('iint', fint(r'\iint')),
    Symbol('iiint', fint(r'\iiint')),
    Symbol('iiiint', fint(r'\iiiint')),
    Symbol('dotsint', fint(r'\dotsint')),
    Symbol('oint', fint(r'\oint')),
    Symbol('oiint', fint(r'\oiint')),
    Symbol('sqint', fint(r'\sqint')),
    Symbol('sqiint', fint(r'\sqiint')),
    Symbol('ointctrclockwise', fint(r'\ointctrclockwise')),
    Symbol('ointclockwise', fint(r'\ointclockwise')),
    Symbol('biguplus', f(r'\biguplus')),
    Symbol('bignplus', f(r'\bignplus')),
    Symbol('bigcup', f(r'\bigcup')),
    Symbol('bigcap', f(r'\bigcap')),
    Symbol('bigoplus', f(r'\bigoplus')),
    Symbol('bigotimes', f(r'\bigotimes')),
    Symbol('bigodot', f(r'\bigodot')),
    Symbol('bigvee', f(r'\bigvee')),
    Symbol('bigwedge', f(r'\bigwedge')),
    Symbol('bigsqcup', f(r'\bigsqcup')),
    Symbol('bigsqcap', f(r'\bigsqcap')),
]
