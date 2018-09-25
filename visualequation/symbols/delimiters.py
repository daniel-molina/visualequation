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

SINGLEDELIMITERS = [
    LatexSymb('lparenthesis', '(', '('),
    LatexSymb('rparenthesis', ')', ')'),
    LatexSymb('vert', '|', '|'),
    LatexSymb('uppervert', r'\|', r'\|'),
    LatexSymb('lbracket', r'\{{', r'\{'), # {{: It will be part of an operator
    LatexSymb('rbracket', r'\}}', r'\}'), # }}: Idem
    LatexSymb('langle', r'\langle', r'\langle'),
    LatexSymb('rangle', r'\rangle', r'\rangle'),
    LatexSymb('lfloor', r'\lfloor', r'\lfloor'),
    LatexSymb('rfloor', r'\rfloor', r'\rfloor'),
    LatexSymb('lceil', r'\lceil', r'\lceil'),
    LatexSymb('rceil', r'\rceil', r'\rceil'),
    LatexSymb('slash', '/', '/'),
    LatexSymb('backslash', r'\backslash', r'\backslash'),
    LatexSymb('lsqbracket', '[', '['),
    LatexSymb('rsqbracket', ']', ']'),
    LatexSymb('llcorner', r'\llcorner', r'\llcorner'),
    LatexSymb('lrcorner', r'\lrcorner', r'\lrcorner'),
    LatexSymb('ulcorner', r'\ulcorner', r'\ulcorner'),
    LatexSymb('urcorner', r'\urcorner', r'\urcorner'),
    LatexSymb('uparrow', r'\uparrow', r'\uparrow'),
    LatexSymb('upperuparrow', r'\Uparrow', r'\Uparrow'),
    LatexSymb('downarrow', r'\downarrow', r'\downarrow'),
    LatexSymb('upperdownarrow', r'\Downarrow', r'\Downarrow'),
    LatexSymb('blankdelimiter', r'.', r'\text{None}'),
]

def free_delimiters(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle('Free delimiters')

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

            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label_l)
            vbox.addLayout(hbox_l)
            vbox.addWidget(label_r)
            vbox.addLayout(hbox_r)
            vbox.addWidget(self.buttons)

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

        @staticmethod
        def get_delimiter(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return ((dialog.symb_l.code, dialog.symb_r.code), True)
            else:
                return ((None, None), False)
            
    (delim_l, delim_r), ok = Dialog.get_delimiter(parent)
    if ok:
        return Op(1, r'\left' + delim_l + r' {0} ' + r'\right' +  delim_r)
    else:
        return None

DELIMITERS = [
    LatexSymb('parenthesisb', Op(1, r'\left( {0} \right)'),
              r'\left(\cdots\right)'),
    LatexSymb('vertb', Op(1, r'\left| {0} \right|'),
              r'\left|\cdots\right|'),
    LatexSymb('uppervertb', Op(1, r'\left\| {0} \right\|'),
              r'\left\|\cdots\right\|'),
    LatexSymb('bracketsb', Op(1, r'\left\{{ {0} \right\}}'),
              r'\left\{\cdots\right\}'),
    LatexSymb('angleb', Op(1, r'\left\langle {0} \right\rangle'),
              r'\left\langle\cdots\right\rangle'),
    LatexSymb('floorb', Op(1, r'\left\lfloor {0} \right\rfloor'),
              r'\left\lfloor\cdots\right\rfloor'),
    LatexSymb('ceilb', Op(1, r'\left\lceil {0} \right\rceil'),
              r'\left\lceil\cdots\right\rceil'),
    LatexSymb('sqbracketsb', Op(1, r'\left[ {0} \right]'),
              r'\left[\cdots\right]'),
    LatexSymb('lcornerb', Op(1, r'\left\llcorner {0} \right\lrcorner'),
              r'\left\llcorner\cdots\right\lrcorner'),
    LatexSymb('ucornerb', Op(1, r'\left\ulcorner {0} \right\urcorner'),
              r'\left\ulcorner\cdots\right\urcorner'),
    LatexSymb('freedelimiters', free_delimiters, r'?_1\cdots ?_2'),
]
