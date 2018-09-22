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
            label_combo = QLabel('Matrix type:')
            self.combo = QComboBox()
            for mtype in MATRIXTYPES:
                self.combo.addItem(QIcon(os.path.join(commons.SYMBOLS_DIR,
                                                      mtype.tag + '.png')), '')
            self.combo.setIconSize(self.combo.minimumSizeHint())
            #self.combo.setSizePolicy(QSizePolicy.Expanding,
            #                         QSizePolicy.Maximum)
            #self.combo.setSizeAdjustPolicy(0) 
            #self.combo.setMinimumHeight(50)
            #self.combo.SizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
            #self.combo.setView(QListView())
            #self.combo.setStyleSheet('''
            #QComboBox QAbstractItemView::item { min-height: 50px;}
            #''')
            
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label_rows)
            vbox.addWidget(self.ledit_rows)
            vbox.addWidget(label_cols)
            vbox.addWidget(self.ledit_cols)
            vbox.addWidget(label_combo)
            vbox.addWidget(self.combo)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit_rows.setFocus()

            self.ledit_rows.textChanged.connect(self.check_state)
            self.ledit_cols.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

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
                         MATRIXTYPES[dialog.combo.currentIndex()].code),
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
            label_l = QLabel('Left delimiter:')
            self.combo_l = QComboBox()
            self.combo_l.setIconSize(self.combo_l.minimumSizeHint())
            for delim in SINGLEDELIMITERS:
                self.combo_l.addItem(QIcon(os.path.join(commons.SYMBOLS_DIR,
                                                        delim.tag + '.png')),
                                     '')
            label_r = QLabel('Right delimiter:')
            self.combo_r = QComboBox()
            self.combo_r.setIconSize(self.combo_l.minimumSizeHint())
            for delim in SINGLEDELIMITERS:
                self.combo_r.addItem(QIcon(os.path.join(commons.SYMBOLS_DIR,
                                                        delim.tag + '.png')),
                                     '')
            self.combo_r.setCurrentIndex(1)
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
            vbox.addWidget(self.combo_l)
            vbox.addWidget(label_r)
            vbox.addWidget(self.combo_r)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit_align.setDisabled(True)
            self.ledit_rows.setFocus()

            self.ledit_rows.textChanged.connect(self.check_state)
            self.ledit_cols.textChanged.connect(self.check_state)
            self.ledit_align.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

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
                         SINGLEDELIMITERS[dialog.combo_l.currentIndex()].code,
                         SINGLEDELIMITERS[dialog.combo_r.currentIndex()].code,
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
