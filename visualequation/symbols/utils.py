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

"""
A module that contains main structures used by operators and symbols.
"""
import os
from collections import namedtuple

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from .. import commons


class Op(object):
    """Class for an equation operator"""

    def __init__(self, n_args, latex_code, type_=None):
        self.n_args = n_args
        self.latex_code = latex_code
        self.type_ = type_ if type_ is not None else ""

    def __call__(self, *args):
        return self.latex_code.format(*args)

    def __eq__(self, other):
        if type(self) is type(other):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "Op(" + repr(self.n_args) + ", " + repr(self.latex_code) \
               + ", " + repr(self.type_) + ")"


PanelIcon = namedtuple('PanelIcon', 'name code')
MenuItemData = namedtuple('MenuItemData', 'name symb_l')

# Use these operators in the code, so it will be easy to change their value
# in next releases
SELARG = r'\cdots'
NEWARG = r'\begingroup\color{purple}\oblong\endgroup'
REDIT = Op(1, r'\left\lmoustache {0} \right\rgroup')        # right
LEDIT = Op(1, r'\left\lgroup {0} \right\rmoustache')        # left
NEDIT = Op(1, r'\left\lmoustache {0} \right\rmoustache')    # new
SEDIT = Op(1, r'\left\rmoustache {0} \right\lmoustache')    # substitute
JUXT = Op(2, r'{0} {1}')
# The initial space is needed to distinguish from GROUP operator
TEMPGROUP = Op(1, r' {0}')
GROUP = Op(1, r'{0}')
SOLIDGROUP = Op(1, r'{0} ')

# It does NOT include ' ', "'", '^', '\\' and '~'
# so it is valid for both text and math environments
ASCII_LATEX_TRANSLATION = {
    '|': r'|',
    '!': r'!',
    '$': r'\$',
    '%': r'\%',
    '&': r'\&',
    '/': r'/',
    '(': r'(',
    ')': r')',
    '=': r'=',
    '?': r'?',
    '@': r'@',
    '#': r'\#',
    '[': r'[',
    ']': r']',
    '{': r'\{',
    '}': r'\}',
    '*': r'*',
    '+': r'+',
    '-': r'-',
    '<': r'<',
    '>': r'>',
    ',': r',',
    '.': r'.',
    ';': r';',
    ':': r':',
    '_': r'\_',
}


class PanelElem(QLabel):
    def __init__(self, parent, pelem):
        super().__init__('')
        self.parent = parent
        self.pelem = pelem
        self.setPixmap(QPixmap(os.path.join(commons.ICONS_DIR,
                                            pelem.name + ".png")))
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        self.parent.pelem_chosen = self.pelem
        self.parent.accept()


class ChooseElemDialog(QDialog):
    def __init__(self, parent, caption, pelem_list, n_columns):
        super().__init__(parent)
        self.setWindowTitle(caption)
        self.setMinimumSize(QSize(300, 300))
        layout = QGridLayout(self)
        row = 1
        column = 1
        for pelem in pelem_list:
            pelem = PanelElem(self, pelem)
            layout.addWidget(pelem, row, column)
            column += 1
            if column > n_columns:
                column = 1
                row += 1
        self.setLayout(layout)
