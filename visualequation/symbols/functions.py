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


def fun_accepting_args(parent, code):
    """Functions processed by this function can have arguments and they need
    to be treated as variable-size symbols when scripted.

    Even when they do not have any argument, they are set to Op with 0
    arguments so it is known that they are special when scripting them.
    """
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle(_('Choose arguments'))
            self.argabove = QCheckBox(_("Argument over operator"))
            self.argbelow = QCheckBox(_("Argument under operator"))
            self.argbelow.setChecked(True)
            self.msg = QLabel(
                _("Note: It is also possible to put arguments"
                  " in the corners by surrounding the operator and using keys"
                  " UP and DOWN."))
            self.msg.setWordWrap(True)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            self.buttons.button(QDialogButtonBox.Ok).setFocus()
            vbox = QVBoxLayout(self)
            vbox.addWidget(self.argabove)
            vbox.addWidget(self.argbelow)
            vbox.addWidget(self.msg)
            vbox.addWidget(self.buttons)

            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        @staticmethod
        def get(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return ((dialog.argabove.isChecked(),
                         dialog.argbelow.isChecked()),
                        True)
            else:
                return (None, None), False

    (argabove, argbelow), ok = Dialog.get(parent)
    if ok:
        base = Op(myname, code, 0, "fun_args")
        if argabove and argbelow:
            return [SLUNDEROVER, base], 2
        elif argabove:
            return [SLOVER, base], 1
        elif argbelow:
            return [SLUNDER, base], 1
        else:
            return base
    else:
        return None


def f(code):
    return lambda parent: fun_accepting_args(parent, code)


FUNCTIONS = [
    PanelIcon('arccos', r'\arccos'),
    PanelIcon('arcsin', r'\arcsin'),
    PanelIcon('arctan', r'\arctan'),
    PanelIcon('arg', r'\arg'),
    PanelIcon('cos', r'\cos'),
    PanelIcon('cosh', r'\cosh'),
    PanelIcon('coth', r'\coth'),
    PanelIcon('csc', r'\csc'),
    PanelIcon('deg', r'\deg'),
    PanelIcon('det', f(r'\det')),
    PanelIcon('dim', r'\dim'),
    PanelIcon('exp', r'\exp'),
    PanelIcon('gcd', f(r'\gcd')),
    PanelIcon('hom', r'\hom'),
    PanelIcon('inf', f(r'\inf')),
    PanelIcon('ker', r'\ker'),
    PanelIcon('lg', r'\lg'),
    PanelIcon('lim', f(r'\lim')),
    PanelIcon('liminf', f(r'\liminf')),
    PanelIcon('limsup', f(r'\limsup')),
    PanelIcon('ln', r'\ln'),
    PanelIcon('log', r'\log'),
    PanelIcon('max', f(r'\max')),
    PanelIcon('min', f(r'\min')),
    PanelIcon('pr', f(r'\Pr')),
    PanelIcon('sec', r'\sec'),
    PanelIcon('sin', r'\sin'),
    PanelIcon('sinh', r'\sinh'),
    PanelIcon('sup', f(r'\sup')),
    PanelIcon('tan', r'\tan'),
    PanelIcon('tanh', r'\tanh'),
    PanelIcon('upperre', r'\Re'),
    PanelIcon('upperim', r'\Im'),
    PanelIcon('wp', r'\wp'),
    PanelIcon('if', r'\text{if }'),
    PanelIcon('ow', r'\text{o.w.}'),
    PanelIcon('otherwise', r'\text{otherwise}'),
]
