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
from .errors import ShowError

class Selection:
    def __init__(self, init_eq, init_index, temp_dir, setPixmap):
        self.eq = init_eq
        self.index = init_index
        self.right = True
        self.is_op_rsel = False
        self.eq_copy_op_rsel = None
        self.index_copy_op_rsel = None
        self.end_op_rsel = None
        self.game = game.Game()
        self.temp_dir = temp_dir
        self.setPixmap = setPixmap

    def display(self, eq=None, right=True):
        # If equation is provided, substitute the current one
        if eq is not None:
            self.eq = eq
        if not 0 <= self.index < len(self.eq):
            ShowError('Provided index outside the equation in display.', True)
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

    def set_valid_index(self, eq=None, forward=True):
        """ Change index, if needed, where selection is valid. """
        if eq is not None:
            self.eq = eq
        # Avoid intermediate JUXTs
        if eqtools.is_intermediate_JUXT(self.eq, self.index):
            cond = True
            while cond:
                self.index += 1 if forward else -1
                cond = eqtools.is_intermediate_JUXT(self.eq, self.index)
        # Avoid first argument of index operators: \sideset is picky
        if self.index != 0\
           and hasattr(self.eq[self.index - 1], 'type_') \
           and self.eq[self.index - 1].type_ in ('index', 'opindex'):
            self.index += 1 if forward else -1            

    def display_next(self):
        """ 
        Set image to the next selection
        """
        # We had a previous op_rsel but now eq was modified: restart
        if self.is_op_rsel and (self.eq_copy_op_rsel != self.eq or
                                self.index_copy_op_rsel != self.index):
            self.is_op_rsel = False
            self.eq_copy_op_rsel = None
            self.index_copy_op_rsel = None
            self.end_op_rsel = None
        if self.is_op_rsel:
            op_rsel_cond, op_rsel_index = eqtools.is_next_element_after_op(
                self.eq, self.end_op_rsel, self.index)
            # We had a previous op_rsel but not anymore:
            #  Set index, initially, in the original position and let this
            #  function to do something with it
            if not op_rsel_cond:
                # Avoid double stop when covering the whole equation
                if self.index != 0:
                    self.index = self.end_op_rsel
                self.is_op_rsel = False
                self.eq_copy_op_rsel = None
                self.index_copy_op_rsel = None
                self.end_op_rsel = None
        else:
            op_rsel_cond, op_rsel_index = eqtools.is_next_element_after_op(
                self.eq, self.index, None)
            
        if not self.right:
            self.right = True
        # End of operator detected
        elif op_rsel_cond:
            if not self.is_op_rsel:
                self.end_op_rsel = self.index
                self.is_op_rsel = True
                self.eq_copy_op_rsel = list(self.eq)
            self.index = op_rsel_index
            self.index_copy_op_rsel = self.index
        else:
            if self.index == len(self.eq) - 1:
                self.index = 0
            else:
                self.index += 1
            self.set_valid_index(forward=True)

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
        self.set_valid_index(forward=False)
        self.display(right=False)
