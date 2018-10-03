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

from PyQt5.QtGui import *

from . import eqtools
from . import conversions
from .symbols import utils
from . import game

class Selection:
    def __init__(self, init_eq, init_index, temp_dir, setPixmap):
        self.eq = init_eq
        self.index = init_index
        self.right = True
        self.game = game.Game()
        self.temp_dir = temp_dir
        self.setPixmap = setPixmap

    def display(self, eq=None,  right=True):
        # If equation is provided, substitute the current one
        if eq is not None:
            self.eq = eq
        if not 0 <= self.index < len(self.eq):
            raise ValueError('Provided index outside the equation.')
        eqsel = list(self.eq)
        if right:
            self.right = True
            eqsel.insert(self.index, utils.REDIT)
        else:
            self.right = False
            eqsel.insert(self.index, utils.LEDIT)

        self.game.update(eqsel)
        eqsel_png = conversions.eq2png(eqsel, None, None, self.temp_dir)
        self.setPixmap(QPixmap(eqsel_png))

    def display_next(self):
        """ Set image to the next selection"""
        if not self.right:
            self.right = True
        elif self.index == len(self.eq) - 1:
            self.index = 0
        else:
            self.index += 1
        # Avoid places where selection is not desired
        # Avoid intermediate JUXTs
        if eqtools.is_intermediate_JUXT(self.eq, self.index):
            cond = True
            while cond:
                self.index += 1
                cond = eqtools.is_intermediate_JUXT(self.eq, self.index)
        # Avoid first argument of index operators: \sideset is picky
        if self.index != 0\
           and hasattr(self.eq[self.index - 1], 'type_') \
           and self.eq[self.index - 1].type_ in ('index', 'opindex'):
            self.index += 1
            
        self.display(right=True)

    def display_prev(self):
        """ Set image to the next selection according to self.sel_index. """
        if self.right:
            self.right = False
        elif self.index == 0:
            self.index = len(self.eq) - 1
        else:
            self.index -= 1
        # Avoid places where selection is not desired
        # Avoid intermediate JUXTs
        if eqtools.is_intermediate_JUXT(self.eq, self.index):
            cond = True
            while cond:
                self.index -= 1
                cond = eqtools.is_intermediate_JUXT(self.eq, self.index)
        # Avoid first argument of index operators: \sideset is picky
        if self.index != 0 \
           and hasattr(self.eq[self.index - 1], 'type_') \
           and self.eq[self.index - 1].type_ in ('index', 'opindex'):
            self.index -= 1
        self.display(right=False)
