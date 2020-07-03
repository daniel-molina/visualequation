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


def opfunctions(parent, code):
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
        if argabove and argbelow:
            latex_code = code + r"_{{{0}}}^{{{1}}}"
            n_operands = 2
        elif argabove:
            latex_code = code + r"^{{{0}}}"
            n_operands = 1
        elif argbelow:
            latex_code = code + r"_{{{0}}}"
            n_operands = 1
        else:
            latex_code = code
            n_operands = 0
        return Op(n_operands, latex_code, "opfun")
    else:
        return None


def f(code):
    return lambda parent: opfunctions(parent, code)


FUNCTIONS = [
    Symbol('arccos', r'\arccos'),
    Symbol('arcsin', r'\arcsin'),
    Symbol('arctan', r'\arctan'),
    Symbol('arg', r'\arg'),
    Symbol('cos', r'\cos'),
    Symbol('cosh', r'\cosh'),
    Symbol('coth', r'\coth'),
    Symbol('csc', r'\csc'),
    Symbol('deg', r'\deg'),
    Symbol('det', f(r'\det')),
    Symbol('dim', r'\dim'),
    Symbol('exp', r'\exp'),
    Symbol('gcd', f(r'\gcd')),
    Symbol('hom', r'\hom'),
    Symbol('inf', f(r'\inf')),
    Symbol('ker', r'\ker'),
    Symbol('lg', r'\lg'),
    Symbol('lim', f(r'\lim')),
    Symbol('liminf', f(r'\liminf')),
    Symbol('limsup', f(r'\limsup')),
    Symbol('ln', r'\ln'),
    Symbol('log', r'\log'),
    Symbol('max', f(r'\max')),
    Symbol('min', f(r'\min')),
    Symbol('pr', f(r'\Pr')),
    Symbol('sec', r'\sec'),
    Symbol('sin', r'\sin'),
    Symbol('sinh', r'\sinh'),
    Symbol('sup', f(r'\sup')),
    Symbol('tan', r'\tan'),
    Symbol('tanh', r'\tanh'),
    Symbol('upperre', r'\Re'),
    Symbol('upperim', r'\Im'),
    Symbol('wp', r'\wp'),
    Symbol('if', r'\text{if }'),
    Symbol('ow', r'\text{o.w.}'),
    Symbol('otherwise', r'\text{otherwise}'),
]
