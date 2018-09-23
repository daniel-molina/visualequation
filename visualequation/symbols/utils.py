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
    """ Class for LaTeX operator (that has arguments)"""
    def __init__(self, n_args, latex_code):
        self.n_args = n_args
        self.latex_code = latex_code

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
        return "Op(" + repr(self.n_args) + ", " + repr(self.latex_code) + ")"

LatexSymb = namedtuple('LatexSymb', 'tag code expr')
MenuItemData = namedtuple('MenuItem', 'tag symb_l expr')

# Use these operators in the code, so it will be easy to change their value
# in next releases
SELARG = r'\cdots'
NEWARG = r'\square'
REDIT = Op(1, r'\left\lmoustache{{{0}}}\right\rgroup')
LEDIT = Op(1, r'\left\lgroup{{{0}}}\right\rmoustache')
JUXT = Op(2, r'{0} {1}')

# It does NOT include ' ', '^', '\\' and '~'
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
    "'": r"'",
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

class Symb(QLabel):
    def __init__(self, parent, symb):
        super().__init__('')
        self.parent = parent
        self.symb = symb
        self.setPixmap(QPixmap(os.path.join(commons.SYMBOLS_DIR,
                                           symb.tag + ".png")))
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        self.parent.symb_chosen = self.symb
        self.parent.accept()

class ChooseSymbDialog(QDialog):
    def __init__(self, parent, caption, symb_list, n_columns):
        super().__init__(parent)
        self.setWindowTitle(caption)
        self.setMinimumSize(QSize(300, 300))
        layout = QGridLayout(self)
        row = 1
        column = 1
        for symb in symb_list:
            symb = Symb(self, symb)
            layout.addWidget(symb, row, column)
            column += 1
            if column > n_columns:
                column = 1
                row += 1
        self.setLayout(layout)   

LSUB = Op(2, r'{{}}_{{{1}}}{0}')
SUB = Op(2, r'{0}_{{{1}}}')
SUP = Op(2, r'{0}^{{{1}}}')
LSUP = Op(2, r'{{}}^{{{1}}}{0}')
LSUBSUB = Op(3, r'{{}}_{{{1}}}{0}_{{{2}}}')
SUBSUP = Op(3, r'{0}_{{{1}}}^{{{2}}}')
SUPLSUP = Op(3, r'{{}}^{{{2}}}{0}^{{{1}}}')
LSUBLSUP = Op(3, r'{{}}_{{{1}}}^{{{2}}}{0}')
LSUBSUP = Op(3, r'{{}}_{{{1}}}{0}^{{{2}}}')
SUBLSUP = Op(3, r'{{}}^{{{2}}}{0}_{{{1}}}')
LSUBSUBSUP = Op(4, r'{{}}_{{{1}}}{0}^{{{3}}}_{{{2}}}')
LSUBSUBLSUP = Op(4, r'{{}}_{{{1}}}^{{{3}}}{0}_{{{2}}}')
LSUBSUPLSUP = Op(4, r'{{}}^{{{3}}}_{{{1}}}{0}^{{{2}}}')
SUBSUPLSUP = Op(4, r'{{}}^{{{3}}}{0}^{{{2}}}_{{{1}}}')
LSUBSUBSUPLSUP = Op(5, r'{{}}_{{{1}}}^{{{4}}}{0}_{{{2}}}^{{{3}}}')

# First elements are the most common
INDEX_OPS = [
    SUP, SUB, SUBSUP, LSUP, LSUB,
    LSUBSUB, SUPLSUP, LSUBLSUP, LSUBSUP, SUBLSUP,
    LSUBSUBSUP, LSUBSUBLSUP, LSUBSUPLSUP, SUBSUPLSUP,
    LSUBSUBSUPLSUP,
]

#INDICES = [
#    LatexSymb('lsub', LSUB, r'{{}}_{{\square}}\cdot'),
#    LatexSymb('sub', SUB, r'\cdot_{{\square}}'),
#    LatexSymb('super', SUP, r'\cdot^{{\square}}'),
#    LatexSymb('lsup', LSUP, r'{{}}^{{\square}}\cdot'),
#    LatexSymb('lsubsub', LSUBSUB, r'{{}}_{{\square}}\cdot_{{\square}}'),
#    LatexSymb('subsup', SUBSUP, r'\cdot^{{\square}}_{{\square}}'),
#    LatexSymb('suplsup', SUPLSUP, r'{{}}^{{\square}}\cdot^{{\square}}'),
#    LatexSymb('lsublsup', LSUBLSUP, r'{{}}^{{\square}}_{{\square}}\cdot'),
#    LatexSymb('lsubsup', LSUBSUP, r'{{}}_{{\square}}\cdot^{{\square}}'),
#    LatexSymb('sublsup', SUBLSUP, r'{{}}^{{\square}}\cdot_{{\square}}'),
#    LatexSymb('lsubsubsup', LSUBSUBSUP,
#              r'{{}}_{{\square}}\cdot^{{\square}}_{{\square}}'),
#    LatexSymb('lsubsublsup', LSUBSUBLSUP,
#              r'{{}}_{{\square}}^{{\square}}\cdot_{{\square}}'),
#    LatexSymb('lsubsuplsup', LSUBSUPLSUP,
#              r'{{}}^{{\square}}_{{\square}}\cdot^{{\square}}'),
#    LatexSymb('subsuplsup', SUBSUPLSUP,
#              r'{{}}^{{\square}}\cdot^{{\square}}_{{\square}}'),
#    LatexSymb('lsubsubsuplsup', LSUBSUBSUPLSUP,
#              r'{{}}^{{\square}}_{{\square}}\cdot^{{\square}}_{{\square}}'),
#]

#    ('binomial', (Op(2, r'\binom{{{0}}}{{{1}}}'),
#     [r'\binom{{\cdot}}{{\square}}'])),

#MENUITEMSDATA.append(MenuItemData(
#    tag="tab_indices",
#    symb_l=INDICES, clickable_size=(60, 60), dpi=200, expr=r'a^b'))
