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
    Symbol('lparenthesis', '('),
    Symbol('rparenthesis', ')'),
    Symbol('vert', '|'),
    Symbol('uppervert', r'\|'),
    Symbol('lbracket', r'\{{'),  # {{: It will be part of an operator
    Symbol('rbracket', r'\}}'),  # }}: Idem
    Symbol('langle', r'\langle'),
    Symbol('rangle', r'\rangle'),
    Symbol('lfloor', r'\lfloor'),
    Symbol('rfloor', r'\rfloor'),
    Symbol('lceil', r'\lceil'),
    Symbol('rceil', r'\rceil'),
    Symbol('slash', '/'),
    Symbol('backslash', r'\backslash'),
    Symbol('lsqbracket', '['),
    Symbol('rsqbracket', ']'),
    Symbol('llcorner', r'\llcorner'),
    Symbol('lrcorner', r'\lrcorner'),
    Symbol('ulcorner', r'\ulcorner'),
    Symbol('urcorner', r'\urcorner'),
    Symbol('uparrow', r'\uparrow'),
    Symbol('upperuparrow', r'\Uparrow'),
    Symbol('downarrow', r'\downarrow'),
    Symbol('upperdownarrow', r'\Downarrow'),
    Symbol('blankdelimiter', r'.'),
]


def free_delimiters(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle(_('Free delimiters'))

            self.symb_l = SINGLEDELIMITERS[0]
            label_l = QLabel(_('Left delimiter:'))
            hbox_l = QHBoxLayout()
            button_l = QPushButton(_('Choose'))
            button_l.clicked.connect(self.handle_click_l)
            self.repr_l = QLabel('')
            self.repr_l.setPixmap(QPixmap(os.path.join(
                commons.ICONS_DIR, self.symb_l.tag + ".png")))
            self.repr_l.setAlignment(Qt.AlignCenter)
            hbox_l.addWidget(button_l)
            hbox_l.addWidget(self.repr_l)

            self.symb_r = SINGLEDELIMITERS[1]
            label_r = QLabel(_('Right delimiter:'))
            hbox_r = QHBoxLayout()
            button_r = QPushButton(_('Choose'))
            button_r.clicked.connect(self.handle_click_r)
            self.repr_r = QLabel('')
            self.repr_r.setPixmap(QPixmap(os.path.join(
                commons.ICONS_DIR, self.symb_r.tag + ".png")))
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
            dialog = ChooseSymbDialog(self, _("Left delimiter"),
                                      SINGLEDELIMITERS, 4)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                self.symb_l = dialog.symb_chosen
                self.repr_l.setPixmap(QPixmap(os.path.join(
                    commons.ICONS_DIR, self.symb_l.tag + ".png")))

        def handle_click_r(self):
            dialog = ChooseSymbDialog(self, _("Right delimiter"),
                                      SINGLEDELIMITERS, 4)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                self.symb_r = dialog.symb_chosen
                self.repr_r.setPixmap(QPixmap(os.path.join(
                    commons.ICONS_DIR, self.symb_r.tag + ".png")))

        @staticmethod
        def get_delimiter(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (dialog.symb_l.code, dialog.symb_r.code), True
            else:
                return (None, None), False

    (delim_l, delim_r), ok = Dialog.get_delimiter(parent)
    if ok:
        return Op(1, r'\left' + delim_l + r' {0} ' + r'\right' + delim_r)
    else:
        return None


DELIMITERS = [
    Symbol('parenthesisb', Op(1, r'\left( {0} \right)')),
    Symbol('sqbracketsb', Op(1, r'\left[ {0} \right]')),
    Symbol('vertb', Op(1, r'\left| {0} \right|')),
    Symbol('uppervertb', Op(1, r'\left\| {0} \right\|')),
    Symbol('bracketsb', Op(1, r'\left\{{ {0} \right\}}')),
    Symbol('angleb', Op(1, r'\left\langle {0} \right\rangle')),
    Symbol('floorb', Op(1, r'\left\lfloor {0} \right\rfloor')),
    Symbol('ceilb', Op(1, r'\left\lceil {0} \right\rceil')),
    Symbol('lcornerb', Op(1, r'\left\llcorner {0} \right\lrcorner')),
    Symbol('ucornerb', Op(1, r'\left\ulcorner {0} \right\urcorner')),
    Symbol('freedelimiters', free_delimiters),
]
