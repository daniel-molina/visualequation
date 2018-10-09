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

def text(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Text')
            label = QLabel('Text:')
            self.ledit = QLineEdit()
            regexp = QRegExp("^[a-zA-Z\d\s|!\\$%&/()=?'@#\\[\\]{}*+-<>,.;:_]+$")
            self.validator = QRegExpValidator(regexp)
            self.ledit.setValidator(self.validator)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label)
            vbox.addWidget(self.ledit)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit.setFocus()

            self.ledit.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        def check_state(self, *args, **kargs):
            state = self.validator.validate(self.ledit.text(), 0)[0]
            if state == QValidator.Acceptable:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)

        @staticmethod
        def get_text(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (dialog.ledit.text(), True)
            else:
                return (None, False)
            
    text, ok = Dialog.get_text(parent)
    if ok:
        # Correct string
        for key in ASCII_LATEX_TRANSLATION:
            text = text.replace(key, ASCII_LATEX_TRANSLATION[key])
        return r'\text{{' + text + '}}'
    else:
        return None

def special_format(latex_command, label_text, only_capital=False):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle(label_text + " characters")
            label = QLabel(label_text + ':')
            self.ledit = QLineEdit()
            if only_capital:
                regexp = QRegExp("^[A-Z]+$")
            else:
                regexp = QRegExp("^[a-zA-Z\d]+$")
            self.validator = QRegExpValidator(regexp)
            self.ledit.setValidator(self.validator)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label)
            vbox.addWidget(self.ledit)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit.setFocus()

            self.ledit.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        def check_state(self, *args, **kargs):
            state = self.validator.validate(self.ledit.text(), 0)[0]
            if state == QValidator.Acceptable:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)

        @staticmethod
        def get_text(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (dialog.ledit.text(), True)
            else:
                return (None, False)

    def fun(parent):
        text, ok = Dialog.get_text(parent)
        if ok:
            return latex_command + text + '}'
        else:
            return None

    return fun

COLORS = [
    LatexSymb('black', 'black'),
    LatexSymb('blue', 'blue'),
    LatexSymb('brown', 'brown'),
    LatexSymb('cyan', 'cyan'),
    LatexSymb('darkgray', 'darkgray'),
    LatexSymb('gray', 'gray'),
    LatexSymb('green', 'green'),
    LatexSymb('lightgray', 'lightgray'),
    LatexSymb('lime', 'lime'),
    LatexSymb('magenta', 'magenta'),
    LatexSymb('olive', 'olive'),
    LatexSymb('orange', 'orange'),
    LatexSymb('pink', 'pink'),
    LatexSymb('purple', 'purple'),
    LatexSymb('red', 'red'),
    LatexSymb('teal', 'teal'),
    LatexSymb('violet', 'violet'),
    LatexSymb('white', 'white'),
    LatexSymb('yellow', 'yellow'),
]


def color(parent):
    dialog = ChooseSymbDialog(parent, "Choose color", COLORS, 3)
    result = dialog.exec_()
    if result == QDialog.Accepted:
        return Op(1, r'\begingroup\color{{' + dialog.symb_chosen.code
                  + r'}}{0}\endgroup')
    else:
        return None

def colorbox(parent):
    dialog = ChooseSymbDialog(parent, "Choose color", COLORS, 3)
    result = dialog.exec_()
    if result == QDialog.Accepted:
        return Op(1, r'\colorbox{{' + dialog.symb_chosen.code
                  + r'}}{{$\displaystyle {0}$}}')
    else:
        return None

TEXT = [
    LatexSymb('text', text),
    LatexSymb('mathcal', special_format(r'\mathcal{', 'Caligraphic', True)),
    LatexSymb('mathbb', special_format(r'\mathbb{', 'Mathbb', True)),
    LatexSymb('mathfrak', special_format(r'\mathfrak{', 'Fraktur')),
    LatexSymb('mathsf', special_format(r'\mathsf{', 'Sans serif')),
    LatexSymb('mathbf', special_format(r'\mathbf{', 'Bold')),
    LatexSymb('textbfem', special_format(r'\textbf{\em ', 'Bold Italic')),
    LatexSymb('color', color),
    LatexSymb('colorbox', colorbox),
]
