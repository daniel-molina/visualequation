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

            self.setWindowTitle('Function operator')
            self.argabove = QCheckBox("Argument over operator")
            self.argbelow = QCheckBox("Argument under operator")
            self.argbelow.setChecked(True)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            self.buttons.button(QDialogButtonBox.Ok).setFocus()
            vbox = QVBoxLayout(self)
            vbox.addWidget(self.argabove)
            vbox.addWidget(self.argbelow)
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
                return ((None, None), False)
            
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
    LatexSymb('arccos', r'\arccos'),
    LatexSymb('arcsin', r'\arcsin'),
    LatexSymb('arctan', r'\arctan'),
    LatexSymb('arg', r'\arg'),
    LatexSymb('cos', r'\cos'),
    LatexSymb('cosh', r'\cosh'),
    LatexSymb('coth', r'\coth'),
    LatexSymb('csc', r'\csc'),
    LatexSymb('deg', r'\deg'),
    LatexSymb('det', f(r'\det')),
    LatexSymb('dim', r'\dim'),
    LatexSymb('exp', r'\exp'),
    LatexSymb('gcd', f(r'\gcd')),
    LatexSymb('hom', r'\hom'),
    LatexSymb('inf', f(r'\inf')),
    LatexSymb('ker', r'\ker'),
    LatexSymb('lg', r'\lg'),
    LatexSymb('lim', f(r'\lim')),
    LatexSymb('liminf', f(r'\liminf')),
    LatexSymb('limsup', f(r'\limsup')),
    LatexSymb('ln', r'\ln'),
    LatexSymb('log', r'\log'),
    LatexSymb('max', f(r'\max')),
    LatexSymb('min', f(r'\min')),
    LatexSymb('pr', f(r'\Pr')),
    LatexSymb('sec', r'\sec'),
    LatexSymb('sin', r'\sin'),
    LatexSymb('sinh', r'\sinh'),
    LatexSymb('sup', f(r'\sup')),
    LatexSymb('tan', r'\tan'),
    LatexSymb('tanh', r'\tanh'),
    LatexSymb('upperre', r'\Re'),
    LatexSymb('upperim', r'\Im'),
    LatexSymb('wp', r'\wp'),
    LatexSymb('if', r'\text{if }'),
    LatexSymb('ow', r'\text{o.w.}'),
    LatexSymb('otherwise', r'\text{otherwise}'),
]
