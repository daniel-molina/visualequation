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
from .delimiters import *

MATRIXTYPES = [
    LatexSymb('pmatrix', 'pmatrix', r'\begin{pmatrix}\square\end{pmatrix}'),
    LatexSymb('vmatrix', 'vmatrix', r'\begin{vmatrix}\square\end{vmatrix}'),
    LatexSymb('Vmatrix', 'Vmatrix', r'\begin{Vmatrix}\square\end{Vmatrix}'),
    LatexSymb('bmatrix', 'bmatrix', r'\begin{bmatrix}\square\end{bmatrix}'),
    LatexSymb('Bmatrix', 'Bmatrix', r'\begin{Bmatrix}\square\end{Bmatrix}'),
    LatexSymb('matrix', 'matrix', r'\begin{matrix}\square\end{matrix}'),
]

def matrix_type(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Matrix')
            label_rows = QLabel('Number of rows:')
            self.ledit_rows = QLineEdit()
            label_cols = QLabel('Number of columns:')
            self.ledit_cols = QLineEdit()
            regexp = QRegExp('^[1-9]$')
            self.validator = QRegExpValidator(regexp)
            self.ledit_rows.setValidator(self.validator)
            self.ledit_cols.setValidator(self.validator)

            self.symb = MATRIXTYPES[0]
            label_type = QLabel('Matrix type:')
            hbox_type = QHBoxLayout()
            button_type = QPushButton('Choose')
            button_type.clicked.connect(self.handle_click)
            self.repr_type = QLabel('')
            self.repr_type.setPixmap(QPixmap(os.path.join(
                commons.SYMBOLS_DIR, self.symb.tag + ".png")))
            self.repr_type.setAlignment(Qt.AlignCenter)
            hbox_type.addWidget(button_type)
            hbox_type.addWidget(self.repr_type)
            
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label_rows)
            vbox.addWidget(self.ledit_rows)
            vbox.addWidget(label_cols)
            vbox.addWidget(self.ledit_cols)
            vbox.addWidget(label_type)
            vbox.addLayout(hbox_type)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit_rows.setFocus()

            self.ledit_rows.textChanged.connect(self.check_state)
            self.ledit_cols.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        def handle_click(self):
            dialog = ChooseSymbDialog(self, "Matrix type", MATRIXTYPES, 3)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                self.symb = dialog.symb_chosen
                self.repr_type.setPixmap(QPixmap(os.path.join(
                    commons.SYMBOLS_DIR, self.symb.tag + ".png")))

        def check_state(self, *args, **kargs):
            state1 = self.validator.validate(self.ledit_rows.text(), 0)[0]
            state2 = self.validator.validate(self.ledit_cols.text(), 0)[0]
            if state1 == state2 == QValidator.Acceptable:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)

        @staticmethod
        def get_matrix_def(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return ((int(dialog.ledit_rows.text()),
                         int(dialog.ledit_cols.text()),
                         dialog.symb.code),
                        True)
            else:
                return ((None, None, None), False)

    (n_rows, n_cols, mtype), ok = Dialog.get_matrix_def(parent)
    if ok:
        row_code = r'{}' + r'&{}'*(n_cols-1) + r'\\'
        latex_code = r'\begin{{' + mtype + r'}}' + row_code*n_rows \
                     + r'\end{{' + mtype + r'}}'
        return Op(n_rows*n_cols, latex_code)
    else:
        return None

def cases(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Cases')
            label = QLabel('Number of cases:')
            self.ledit = QLineEdit()
            regexp = QRegExp('^[1-9]$')
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
        def get_n_cases(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (int(dialog.ledit.text()), True)
            else:
                return (None, False)
            
    n_cases, ok = Dialog.get_n_cases(parent)
    if ok:
        case_code = r'{}&{}\\'
        latex_code = r'\begin{{cases}}' + case_code*n_cases + r'\end{{cases}}'
        return Op(n_cases*2, latex_code)
    else:
        return None

def equation_system(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Equation system')
            label = QLabel('Number of equations:')
            self.ledit = QLineEdit()
            regexp = QRegExp('^[1-9]$')
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
        def get_n_equations(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (int(dialog.ledit.text()), True)
            else:
                return (None, False)
            
    n_equations, ok = Dialog.get_n_equations(parent)
    if ok:
        case_code = r'{}\\'
        latex_code = r'\begin{{cases}}' + case_code*n_equations \
                     + r'\end{{cases}}'
        return Op(n_equations, latex_code)
    else:
        return None

def array(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('General Array')
            label_rows = QLabel('Number of rows:')
            self.ledit_rows = QLineEdit()
            label_cols = QLabel('Number of columns:')
            self.ledit_cols = QLineEdit()
            regexp = QRegExp('^[1-9]$')
            self.validator = QRegExpValidator(regexp)
            self.ledit_rows.setValidator(self.validator)
            self.ledit_cols.setValidator(self.validator)
            label_align = QLabel('Alignment of columns (eg. lc|r):\n'+
                                 '(l: left, c: center, r: right, |: v. line)')
            self.ledit_align = QLineEdit()
            # Left delimiter
            self.symb_l = SINGLEDELIMITERS[0]
            label_l = QLabel('Left delimiter:')
            hbox_l = QHBoxLayout()
            button_l = QPushButton('Choose')
            button_l.clicked.connect(self.handle_click_l)
            self.repr_l = QLabel('')
            self.repr_l.setPixmap(QPixmap(os.path.join(
                commons.SYMBOLS_DIR, self.symb_l.tag + ".png")))
            self.repr_l.setAlignment(Qt.AlignCenter)
            hbox_l.addWidget(button_l)
            hbox_l.addWidget(self.repr_l)
            # Right delimiter
            self.symb_r = SINGLEDELIMITERS[1]
            label_r = QLabel('Right delimiter:')
            hbox_r = QHBoxLayout()
            button_r = QPushButton('Choose')
            button_r.clicked.connect(self.handle_click_r)
            self.repr_r = QLabel('')
            self.repr_r.setPixmap(QPixmap(os.path.join(
                commons.SYMBOLS_DIR, self.symb_r.tag + ".png")))
            self.repr_r.setAlignment(Qt.AlignCenter)
            hbox_r.addWidget(button_r)
            hbox_r.addWidget(self.repr_r)
            # Buttons
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label_rows)
            vbox.addWidget(self.ledit_rows)
            vbox.addWidget(label_cols)
            vbox.addWidget(self.ledit_cols)
            vbox.addWidget(label_align)
            vbox.addWidget(self.ledit_align)
            vbox.addWidget(label_l)
            vbox.addLayout(hbox_l)
            vbox.addWidget(label_r)
            vbox.addLayout(hbox_r)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit_align.setDisabled(True)
            self.ledit_rows.setFocus()
            # Connect
            self.ledit_rows.textChanged.connect(self.check_state)
            self.ledit_cols.textChanged.connect(self.check_state)
            self.ledit_align.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        def handle_click_l(self):
            dialog = ChooseSymbDialog(self, "Left delimiter",
                                      SINGLEDELIMITERS, 4)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                self.symb_l = dialog.symb_chosen
                self.repr_l.setPixmap(QPixmap(os.path.join(
                    commons.SYMBOLS_DIR, self.symb_l.tag + ".png")))

        def handle_click_r(self):
            dialog = ChooseSymbDialog(self, "Right delimiter",
                                      SINGLEDELIMITERS, 4)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                self.symb_r = dialog.symb_chosen
                self.repr_r.setPixmap(QPixmap(os.path.join(
                    commons.SYMBOLS_DIR, self.symb_r.tag + ".png")))

        def check_state(self, *args, **kargs):
            state1 = self.validator.validate(self.ledit_rows.text(), 0)[0]
            state2 = self.validator.validate(self.ledit_cols.text(), 0)[0]
            if state2 == QValidator.Acceptable:
                self.ledit_align.setEnabled(True)
                n_cols = self.ledit_cols.text()
                regexp = QRegExp("^" + "(\\|*[lcr]\\|*){" + n_cols + '}' + "$")
                val_align = QRegExpValidator(regexp)
                self.ledit_align.setValidator(val_align)
                state3 = val_align.validate(self.ledit_align.text(), 0)[0]
            else:
                self.ledit_align.setDisabled(True)
                state3 = QValidator.Invalid
            if state1 == state2 == state3 == QValidator.Acceptable:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)

        @staticmethod
        def get_array(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return ((int(dialog.ledit_rows.text()),
                         int(dialog.ledit_cols.text()),
                         dialog.symb_l.code,
                         dialog.symb_r.code,
                         dialog.ledit_align.text()),
                        True)
            else:
                return ((None, None, None, None, None), False)

    (n_rows, n_cols, delim_l, delim_r, align), ok = Dialog.get_array(parent)
    if ok:
        row_code = r'{}' + r'&{}'*(n_cols-1) + r'\\'
        latex_code = r'\left' + delim_l \
                     + r'\begin{{array}}' \
                     + '{{' + align + '}}' \
                     + row_code*n_rows \
                     + r'\end{{array}}' \
                     + r'\right' + delim_r
        return Op(n_rows*n_cols, latex_code)
    else:
        return None

MANYLINES = [
    LatexSymb('matrix_type', matrix_type,
              r"\begin{pmatrix}\cdots&\square\\\square&\square\end{pmatrix}"),
    LatexSymb('cases', cases,
              r'\begin{cases}\cdots &\text{if }x>0\\b&\text{ow.}\end{cases}'),
    LatexSymb('equations_system', equation_system,
                          r'\begin{cases}\cdots\\x-y=8\end{cases}'),
    LatexSymb('array', array,
              r'\left(\begin{array}{l|r}\cdots&\square\\\square&\square\end{array}\right]')
]
