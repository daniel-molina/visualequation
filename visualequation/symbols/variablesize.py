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
from visualequation.eqlib.ops import *


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
        base = Op(myname, code, 0, "vs")
        if sup and inf:
            return [SLUNDEROVER, base], 2
        elif sup:
            return [SLOVER, base], 1
        elif inf:
            return [SLUNDER, base], 1
        else:
            return base
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
        base = Op(myname, code, 0, "int")
        if sup and inf:
            return [LIMUNDEROVER, base], 2
        elif sup:
            return [LIMOVER, base], 1
        elif inf:
            return [LIMUNDER, base], 1
        else:
            return base
    else:
        return None


def fint(code):
    return lambda parent: integrals(parent, code)


VARIABLESIZE = [
    PanelIcon('sum', f(r'\sum')),
    PanelIcon('prod', f(r'\prod')),
    PanelIcon('coprod', f(r'\coprod')),
    PanelIcon('int', fint(r'\int')),
    PanelIcon('iint', fint(r'\iint')),
    PanelIcon('iiint', fint(r'\iiint')),
    PanelIcon('iiiint', fint(r'\iiiint')),
    PanelIcon('dotsint', fint(r'\dotsint')),
    PanelIcon('oint', fint(r'\oint')),
    PanelIcon('oiint', fint(r'\oiint')),
    PanelIcon('sqint', fint(r'\sqint')),
    PanelIcon('sqiint', fint(r'\sqiint')),
    PanelIcon('ointctrclockwise', fint(r'\ointctrclockwise')),
    PanelIcon('ointclockwise', fint(r'\ointclockwise')),
    PanelIcon('biguplus', f(r'\biguplus')),
    PanelIcon('bignplus', f(r'\bignplus')),
    PanelIcon('bigcup', f(r'\bigcup')),
    PanelIcon('bigcap', f(r'\bigcap')),
    PanelIcon('bigoplus', f(r'\bigoplus')),
    PanelIcon('bigotimes', f(r'\bigotimes')),
    PanelIcon('bigodot', f(r'\bigodot')),
    PanelIcon('bigvee', f(r'\bigvee')),
    PanelIcon('bigwedge', f(r'\bigwedge')),
    PanelIcon('bigsqcup', f(r'\bigsqcup')),
    PanelIcon('bigsqcap', f(r'\bigsqcap')),
]
