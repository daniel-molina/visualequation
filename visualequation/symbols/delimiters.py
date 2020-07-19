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
    PanelIcon('lparenthesis', '('),
    PanelIcon('rparenthesis', ')'),
    PanelIcon('vert', '|'),
    PanelIcon('uppervert', r'\|'),
    PanelIcon('lbracket', r'\{{'),  # {{: It will be part of an operator
    PanelIcon('rbracket', r'\}}'),  # }}: Idem
    PanelIcon('langle', r'\langle'),
    PanelIcon('rangle', r'\rangle'),
    PanelIcon('lfloor', r'\lfloor'),
    PanelIcon('rfloor', r'\rfloor'),
    PanelIcon('lceil', r'\lceil'),
    PanelIcon('rceil', r'\rceil'),
    PanelIcon('slash', '/'),
    PanelIcon('backslash', r'\backslash'),
    PanelIcon('lsqbracket', '['),
    PanelIcon('rsqbracket', ']'),
    PanelIcon('llcorner', r'\llcorner'),
    PanelIcon('lrcorner', r'\lrcorner'),
    PanelIcon('ulcorner', r'\ulcorner'),
    PanelIcon('urcorner', r'\urcorner'),
    PanelIcon('uparrow', r'\uparrow'),
    PanelIcon('upperuparrow', r'\Uparrow'),
    PanelIcon('downarrow', r'\downarrow'),
    PanelIcon('upperdownarrow', r'\Downarrow'),
    PanelIcon('blankdelimiter', r'.'),
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
                commons.ICONS_DIR, self.symb_l.name + ".png")))
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
                commons.ICONS_DIR, self.symb_r.name + ".png")))
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
            dialog = ChooseElemDialog(self, _("Left delimiter"),
                                      SINGLEDELIMITERS, 4)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                self.symb_l = dialog.symb_chosen
                self.repr_l.setPixmap(QPixmap(os.path.join(
                    commons.ICONS_DIR, self.symb_l.name + ".png")))

        def handle_click_r(self):
            dialog = ChooseElemDialog(self, _("Right delimiter"),
                                      SINGLEDELIMITERS, 4)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                self.symb_r = dialog.symb_chosen
                self.repr_r.setPixmap(QPixmap(os.path.join(
                    commons.ICONS_DIR, self.symb_r.name + ".png")))

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
    PanelIcon('parenthesisb', Op(1, r'\left( {0} \right)')),
    PanelIcon('sqbracketsb', Op(1, r'\left[ {0} \right]')),
    PanelIcon('vertb', Op(1, r'\left| {0} \right|')),
    PanelIcon('uppervertb', Op(1, r'\left\| {0} \right\|')),
    PanelIcon('bracketsb', Op(1, r'\left\{{ {0} \right\}}')),
    PanelIcon('angleb', Op(1, r'\left\langle {0} \right\rangle')),
    PanelIcon('floorb', Op(1, r'\left\lfloor {0} \right\rfloor')),
    PanelIcon('ceilb', Op(1, r'\left\lceil {0} \right\rceil')),
    PanelIcon('lcornerb', Op(1, r'\left\llcorner {0} \right\lrcorner')),
    PanelIcon('ucornerb', Op(1, r'\left\ulcorner {0} \right\urcorner')),
    PanelIcon('freedelimiters', free_delimiters),
]
