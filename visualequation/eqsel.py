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


def get_valid_index(eq, idx, forward=True):
    """
    idx must be a value in the range [0, len(eq)-1], both ends included.
    If idx is a valid element to be selected, return it.
    Being a valid element means:
     * It is not an intermediate JUXT.
     * It is not the first argument of an operator which attribute type_ is
       equal to 'index' or 'opindex'.
     If it is not a valid element return the next (or previous, if forward is
       equal to False) element which is a valid element.
    This is just a function. In particular, local equation is NOT updated.

    Implementation note:

        Index 0 and len(eq) -1 are guaranteed to be valid according to the
        current definition of valid element, so it is not checked that
        output value is in the range [0, len(eq)-1].

    """
    # Avoid intermediate JUXTs
    if eqtools.is_intermediate_juxt(eq, idx):
        cond = True
        while cond:
            idx += 1 if forward else -1
            cond = eqtools.is_intermediate_juxt(eq, idx)
    # Avoid first argument of index operators: \sideset is picky
    if idx != 0 \
            and hasattr(eq[idx - 1], 'type_') \
            and eq[idx - 1].type_ in ('index', 'opindex'):
        idx += 1 if forward else -1
    return idx


def is_valid_index(eq, idx, forward=True):
    """
    Return whether idx is a valid index. If it is not, 2nd output value is a
    a valid index in direction specified by forward.
    """
    valididx = get_valid_index(eq, idx, forward)
    return (True, idx) if idx == valididx else (False, valididx)


class ForwardIndices:
    def __init__(self):
        # It indicates whether previous index returned by get_next_index
        # was done by applying steps 2 or 3 described in get_next_index
        # docstring.
        self.selecting_previous_blocks = False
        # Equation passed in the previous call
        # Only used if self.selecting_previous_blocks is True
        self.expected_eq = None
        # Returned index in the previous call
        # Only used if self.selecting_previous_blocks is True
        self.expected_idx = None
        # It is called I in get_next_index docstring
        self.last_element_of_block = None

    def get_next_index(self, eq, idx):
        """
        Return the index pointing to next forward selection of eq from idx.

        An index that is not valid according to the rules of function
        get_valid_index will be never returned. Instead, returned index will be
        the same that would be returned after calling this function the
        needed number of times such that a valid index was returned supposing
        that first sentence of this paragraph does not apply.

        Next forward selection is determined according to the following rules,
        which order of priority is the same in which they are listed:

            0. If len(eq) == 1, return 0 (independently of idx, which should
                be 0).
            1. If idx == 0 (the whole equation is selected), return 1 (it can
                be a single element or an operator).
            2. If idx points to the last element of the last argument of some
                block (intermediate JUXTs are not considered blocks), return
                the index of the first element (smaller than idx) of the
                smallest block satisfying the condition.
                Let us define I equal to idx if this rule apply.
            3. If previous call to this function returned according to rule
                number 2 or 3, and both times passed values eq were identical,
                and idx of this call is identical to the value returned by the
                previous call (satisfaction of last two conditions typically
                means that the user did not modify the equation nor selected
                another element of the equation), if there exist at least
                another block (which index is smaller than idx) which last
                element of last argument has index I, return the index of the
                first element of the smallest block satisfying the condition.
                If that block does not exists, this rule does not apply.
            4. If all conditions of rule 3 are satisfied except the block
                existence, return I+1.
                If len(eq) == I+1, this rule does not apply.
            5. Return idx+1. (It always applies since applying previous
               rules to the last element of the equation develops into
               returning 0)
        """
        # Case 0
        # If self.eq only has one element, it is not an operator so it is
        # assured that it is a valid element.
        if len(eq) == 1:
            return 0

        # Case 1
        # If the whole equation is selected, select first valid element.
        # According to current definition of valid element it is guaranteed
        # that at least the last element of eq is valid.
        if idx == 0:
            return get_valid_index(eq, 1)

        # Rest of cases (2, 3, 4, and 5)
        if self.selecting_previous_blocks \
                and self.expected_eq == eq and self.expected_idx == idx:
            block_idx = self.expected_idx - 1
        else:
            self.selecting_previous_blocks = False
            self.last_element_of_block = idx
            block_idx = None

        exists_block = True
        is_block_valid = False
        while exists_block and not is_block_valid:
            exists_block, block_idx = eqtools.is_last_element_of_block(
                eq, self.last_element_of_block, block_idx)
            if exists_block:
                is_block_valid, ignored = is_valid_index(eq, block_idx)
                if not is_block_valid:
                    block_idx -= 1

        # It is guaranteed that previous while loop must finish with one of
        # these two states:
        #  a. exist_block == True  and is_block_valid == True
        #  b. exist_block == False and is_block_valid == False
        if exists_block:
            # Case 2 and 3
            if not self.selecting_previous_blocks:
                self.selecting_previous_blocks = True
                self.expected_eq = list(eq)
            self.expected_idx = block_idx
            return block_idx
        else:
            # Case 4 and 5 (no-last-element-of-block variant)
            self.selecting_previous_blocks = False
            return get_valid_index(eq, self.last_element_of_block + 1)


class Selection:
    def __init__(self, init_eq, init_index, temp_dir, setpixmap):
        self.eq = init_eq
        self.index = init_index
        self.right = True
        self.forward_indices = ForwardIndices()
        self.game = game.Game()
        self.temp_dir = temp_dir
        self.setpixmap = setpixmap
        self.dpi = 300

    def display(self, eq=None, right=True):
        """
        Display image. If eq is not None self.eq is updated before displaying.
        Specifying no right implies it is True, independently of self.right
        (legacy behavior)
        """
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
        eqsel_png = conversions.eq2png(eqsel, self.dpi, None, self.temp_dir)
        self.setpixmap(QPixmap(eqsel_png))

    def set_valid_index(self, eq=None, forward=True):
        """
        If self.index points to a valid element do nothing.
        Else, change it to the next (or previous, according to forward value)
        element which is valid.
        Read docstring of set_valid_index to know the details about what a
        valid element is.
        If eq is passed, local equation is updated.
        """
        if eq is not None:
            self.eq = eq
        self.index = get_valid_index(self.eq, self.index, forward)

    def display_next(self):
        """
        If self.right = False, then just set self.right = True and
            display the formula.
        Else, set self.index to the next forward index according to the
            rules of function get_next_index and display the formula.
        """
        # If ghost is not looking to the right, just turn around the ghost.
        # Do not modify any other variables to leave the state OK for further
        # calls.
        if not self.right:
            self.right = True
        else:
            self.index = self.forward_indices.get_next_index(
                self.eq, self.index)
        self.display()

    def display_prev(self):
        """
        Set index to the previous selection and display image.
        """
        if self.right:
            self.right = False
        elif self.index == 0:
            self.index = len(self.eq) - 1
        else:
            self.index -= 1
        # Avoid places where selection is not desired
        self.set_valid_index(forward=False)
        self.display(right=False)

    def display_surrounding_block(self, level=1):
        """
        Set index to the beginning of the block containing index and display.
        """
        self.index = eqtools.surrounding_block_start(self.eq, self.index)
        # set_valid_index is known to place outputs of surrounding_block_start
        # in sites compatible with the next call to that function.
        self.set_valid_index(forward=False)
        self.display(right=True)
