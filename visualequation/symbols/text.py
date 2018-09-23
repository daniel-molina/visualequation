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
    LatexSymb('black', 'black', r'\textcolor{black}{\text{black}}'),
    LatexSymb('blue', 'blue', r'\textcolor{blue}{\text{blue}}'),
    LatexSymb('brown', 'brown', r'\textcolor{brown}{\text{brown}}'),
    LatexSymb('cyan', 'cyan', r'\textcolor{cyan}{\text{cyan}}'),
    LatexSymb('darkgray', 'darkgray',
              r'\textcolor{darkgray}{\text{darkgray}}'),
    LatexSymb('gray', 'gray', r'\textcolor{gray}{\text{gray}}'),
    LatexSymb('green', 'green', r'\textcolor{green}{\text{green}}'),
    LatexSymb('lightgray', 'lightgray',
              r'\textcolor{lightgray}{\text{lightgray}}'),
    LatexSymb('lime', 'lime', r'\textcolor{lime}{\text{lime}}'),
    LatexSymb('magenta', 'magenta', r'\textcolor{magenta}{\text{magenta}}'),
    LatexSymb('olive', 'olive', r'\textcolor{olive}{\text{olive}}'),
    LatexSymb('orange', 'orange', r'\textcolor{orange}{\text{orange}}'),
    LatexSymb('pink', 'pink', r'\textcolor{pink}{\text{pink}}'),
    LatexSymb('purple', 'purple', r'\textcolor{purple}{\text{purple}}'),
    LatexSymb('red', 'red', r'\textcolor{red}{\text{red}}'),
    LatexSymb('teal', 'teal', r'\textcolor{teal}{\text{teal}}'),
    LatexSymb('violet', 'violet', r'\textcolor{violet}{\text{violet}}'),
    LatexSymb('white', 'white', r'\textcolor{white}{\text{white}}'),
    LatexSymb('yellow', 'yellow', r'\textcolor{yellow}{\text{yellow}}'),
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
    LatexSymb('text', text, r"\text{Text}"),
    LatexSymb('mathcal', special_format(r'\mathcal{', 'Caligraphic', True),
              r"\mathcal{ABC}"),
    LatexSymb('mathbb', special_format(r'\mathbb{', 'Mathbb', True),
              r"\mathbb{ABC}"),
    LatexSymb('mathfrak', special_format(r'\mathfrak{', 'Fraktur'),
              r"\mathfrak{Ab1}"),
    LatexSymb('mathsf', special_format(r'\mathsf{', 'Sans serif'),
              r"\mathsf{Ab1}"),
    LatexSymb('mathbf', special_format(r'\mathbf{', 'Bold'),
              r"\mathbf{Ab1}"),
    LatexSymb('textbfem', special_format(r'\textbf{\em ', 'Bold Italic'),
              r"\textbf{\em Ab1}"),
    LatexSymb('color', color, r'\textcolor{red}{C}\textcolor{blue}'
              + r'{o}\textcolor{olive}{|}\textcolor{pink}{0}'
              + r'\textcolor{purple}{r}'),
    LatexSymb('colorbox', colorbox, r'\colorbox{yellow}{$x^2$}/2'),
]
