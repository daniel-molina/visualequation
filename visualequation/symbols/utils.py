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


# Standard script operators
LSUB = Op(2, r'\tensor*[_{{{1}}}]{{{0}}}{{}}', 'script')
SUB = Op(2, r'{0}_{{{1}}}', 'script')
SUP = Op(2, r'{0}^{{{1}}}', 'script')
LSUP = Op(2, r'\tensor*[^{{{1}}}]{{{0}}}{{}}', 'script')
LSUBSUB = Op(3, r'\tensor*[_{{{1}}}]{{{0}}}{{_{{{2}}}}}', 'script')
SUBSUP = Op(3, r'{0}_{{{1}}}^{{{2}}}', 'script')
LSUPSUP = Op(3, r'\tensor*[^{{{2}}}]{{{0}}}{{^{{{1}}}}}', 'script')
LSUBLSUP = Op(3, r'\tensor*[_{{{1}}}^{{{2}}}]{{{0}}}{{}}', 'script')
LSUBSUP = Op(3, r'\tensor*[_{{{1}}}]{{{0}}}{{^{{{2}}}}}', 'script')
SUBLSUP = Op(3, r'\tensor*[^{{{2}}}]{{{0}}}{{_{{{1}}}}}', 'script')
LSUBSUBSUP = Op(4, r'\tensor*[_{{{1}}}]{{{0}}}{{^{{{3}}}_{{{2}}}}}', 'script')
LSUBSUBLSUP = Op(4, r'\tensor*[_{{{1}}}^{{{3}}}]{{{0}}}{{_{{{2}}}}}', 'script')
LSUBLSUPSUP = Op(4, r'\tensor*[^{{{3}}}_{{{1}}}]{{{0}}}{{^{{{2}}}}}', 'script')
SUBLSUPSUP = Op(4, r'\tensor*[^{{{3}}}]{{{0}}}{{^{{{2}}}_{{{1}}}}}', 'script')
LSUBSUBLSUPSUP = Op(5,
                    r'\tensor*[_{{{1}}}^{{{4}}}]{{{0}}}{{_{{{2}}}^{{{3}}}}}',
                    'script')

# Script operators used when we want to force the use of parenthesis for the
# base. "P" stands for "parenthesis" or "protected".
PLSUB = Op(2, r'\tensor*[_{{{1}}}]\left({0}\right){{}}', 'pscript')
PSUB = Op(2, r'\left({0}\right)_{{{1}}}', 'pscript')
PSUP = Op(2, r'\left({0}\right)^{{{1}}}', 'pscript')
PLSUP = Op(2, r'\tensor*[^{{{1}}}]\left({0}\right){{}}', 'pscript')
PLSUBSUB = Op(3, r'\tensor*[_{{{1}}}]\left({0}\right){{_{{{2}}}}}', 'pscript')
PSUBSUP = Op(3, r'\left({0}\right)_{{{1}}}^{{{2}}}', 'pscript')
PSUPLSUP = Op(3, r'\tensor*[^{{{2}}}]\left({0}\right){{^{{{1}}}}}', 'pscript')
PLSUBLSUP = Op(3, r'\tensor*[_{{{1}}}^{{{2}}}]\left({0}\right){{}}', 'pscript')
PLSUBSUP = Op(3, r'\tensor*[_{{{1}}}]\left({0}\right){{^{{{2}}}}}', 'pscript')
PSUBLSUP = Op(3, r'\tensor*[^{{{2}}}]\left({0}\right){{_{{{1}}}}}', 'pscript')
PLSUBSUBSUP = Op(4, r'\tensor*[_{{{1}}}]\left({0}\right){{^{{{3}}}_{{{2}}}}}',
                 'pscript')
PLSUBSUBLSUP = Op(4, r'\tensor*[_{{{1}}}^{{{3}}}]\left({0}\right){{_{{{2}}}}}',
                  'pscript')
PLSUBSUPLSUP = Op(4, r'\tensor*[^{{{3}}}_{{{1}}}]\left({0}\right){{^{{{2}}}}}',
                  'pscript')
PSUBSUPLSUP \
    = Op(4, r'\tensor*[^{{{3}}}]\left({0}\right){{^\left({2}}}_{{{1}}}}}',
         'pscript')
PLSUBSUBSUPLSUP \
    = Op(5, r'\tensor*[_{{{1}}}^{{{4}}}]\left({0}\right){{_{{{2}}}^{{{3}}}}}',
         'pscript')

# Script operators with "\sideset". Valid only for variable-size and fun-args
LOLSUB = Op(2, r'\sideset{{_{{{1}}}}}{{}}{0}', 'sideset')
LOSUB = Op(2, r'\sideset{{}}{{_{{{1}}}}}{0}', 'sideset')
LOSUP = Op(2, r'\sideset{{}}{{^{{{1}}}}}{0}', 'sideset')
LOLSUP = Op(2, r'\sideset{{^{{{1}}}}}{{}}{0}', 'sideset')
LOLSUBSUB = Op(3, r'\sideset{{_{{{1}}}}}{{_{{{2}}}}}{0}', 'sideset')
LOSUBSUP = Op(3, r'\sideset{{}}{{_{{{1}}}^{{{2}}}}}{0}', 'sideset')
LOLSUPSUP = Op(3, r'\sideset{{^{{{2}}}}}{{^{{{1}}}}}{0}', 'sideset')
LOLSUBLSUP = Op(3, r'\sideset{{_{{{1}}}^{{{2}}}}}{{}}{0}', 'sideset')
LOLSUBSUP = Op(3, r'\sideset{{_{{{1}}}}}{{^{{{2}}}}}{0}', 'sideset')
LOSUBLSUP = Op(3, r'\sideset{{^{{{2}}}}}{{_{{{1}}}}}{0}', 'sideset')
LOLSUBSUBSUP = Op(4, r'\sideset{{_{{{1}}}}}{{^{{{3}}}_{{{2}}}}}{0}',
                  'sideset')
LOLSUBSUBLSUP = Op(4, r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}}}{0}',
                   'sideset')
LOLSUBLSUPSUP = Op(4, r'\sideset{{^{{{3}}}_{{{1}}}}}{{^{{{2}}}}}{0}',
                   'sideset')
LOSUBLSUPSUP = Op(4, r'\sideset{{^{{{3}}}}}{{^{{{2}}}_{{{1}}}}}{0}',
                  'sideset')
LOLSUBSUBLSUPSUP = Op(5,
                      r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{2}}}^{{{3}}}}}{0}',
                      'sideset')

SCRIPT_TYPES = ('script', 'pscript', 'sideset')

# First elements are the most common
SCRIPT_OPS = (
    SUP, SUB, SUBSUP, LSUP, LSUB,
    LSUBSUB, LSUPSUP, LSUBLSUP, LSUBSUP, SUBLSUP,
    LSUBSUBSUP, LSUBSUBLSUP, LSUBLSUPSUP, SUBLSUPSUP,
    LSUBSUBLSUPSUP,
)

PSCRIPT_OPS = (
    PSUP, PSUB, PSUBSUP, PLSUP, PLSUB,
    PLSUBSUB, PSUPLSUP, PLSUBLSUP, PLSUBSUP, PSUBLSUP,
    PLSUBSUBSUP, PLSUBSUBLSUP, PLSUBSUPLSUP, PSUBSUPLSUP,
    PLSUBSUBSUPLSUP,
)

SSSCRIPT_OPS = (
    LOSUP, LOSUB, LOSUBSUP, LOLSUP, LOLSUB,
    LOLSUBSUB, LOLSUPSUP, LOLSUBLSUP, LOLSUBSUP, LOSUBLSUP,
    LOLSUBSUBSUP, LOLSUBSUBLSUP, LOLSUBLSUPSUP, LOSUBLSUPSUP,
    LOLSUBSUBLSUPSUP,
)

# Generic vscript operators
UNDER = Op(2, r'\underset{{{1}}}{{{0}}}', 'setscript')
OVER = Op(2, r'\overset{{{1}}}{{{0}}}', 'setscript')
UNDEROVER = Op(2, r'\overset{{{2}}}{{{\underset{{{1}}}{{{0}}}}}}', 'setscript')

# vscript operators with limits
LIMUNDER = Op(2, r'{0}\limits_{{{1}}}', 'limscript')
LIMOVER = Op(2, r'{0}\limits^{{{1}}}', 'limscript')
LIMUNDEROVER = Op(3, r'{0}\limits_{{{1}}}^{{{2}}}', 'limscript')

# vscript operators for fun_args and variable-size (vs)
# "SL" stands for script-like
SLUNDER = Op(2, r'{0}_{{{1}}}', 'script-like')
SLOVER = Op(2, r'{0}^{{{1}}}', 'script-like')
SLUNDEROVER = Op(3, r'{0}_{{{1}}}^{{{2}}}', 'script-like')

VSCRIPT_TYPES = ('setscript', 'limscript', 'script-like')

ALLSCRIPT_TYPES = SCRIPT_TYPES + VSCRIPT_TYPES
