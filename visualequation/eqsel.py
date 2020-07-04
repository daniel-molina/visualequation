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

import functools

from PyQt5.QtGui import *

from . import eqqueries
from . import conversions
from . import game
from . import groups
from .errors import ShowError
from .symbols import utils


def display_eq(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        retval = func()
        self.display()
        return retval

    return wrapper


def correct_selsubeq(eq, idx):
    """Define what is not a selsubeq and provide default selsubeq indices.

    This is the function which determines what selsubeq is not. As the code
    evolves and new ideas appear, definition can change.

    By now, a selsubeq satisfies:

        *   It is not a descendant JUXT.
        *   It is not the first argument of an operator which attribute type_
            is equal to 'script' or 'opindex'.
        *   It is not a group or temporal group.

    :eq: A valid equation.
    :idx: An index of a subequation in equation :eq:.
    :return: -1 if subequation IS a selsubeq, the index of default selsubeq.
    """
    # Descendant JUXTs
    if eqqueries.is_descendant_juxt(eq, idx):
        return idx+1
    # First argument of idx operators: \sideset is picky
    if idx != 0 \
            and isinstance(eq[idx-1], utils.Op) \
            and eq[idx-1].type_ in ('script', 'opindex'):
        return idx-1
    # Avoid groups and tempgroups
    if eq[idx] in [utils.GROUP, utils.TEMPGROUP]:
        return idx+1

    return -1


def is_selsubeq(eq, idx):
    return correct_selsubeq(eq, idx) < 0


class ForwardIndices:
    def __init__(self):
        # It indicates whether previous idx returned by next
        # was done by applying steps 2 or 3 described in next
        # docstring.
        self.selecting_previous_blocks = False
        # Equation passed in the previous call
        # Only used if self.selecting_previous_blocks is True
        self.expected_eq = None
        # Returned idx in the previous call
        # Only used if self.selecting_previous_blocks is True
        self.expected_idx = None
        # It is called I in next docstring
        self.last_element_of_block = None

    def next(self, eq, idx):
        """Return the index of the next selsubeq.

        Next selsubeq is returned. Calculation is done according to previous
        previous calls to this method and the index :idx: passed.

        This function defines the policy to determine what is the next
        selsubeq when navigating forward step-by-step (selsubeq-by-selsubeq).
        selsubeq's defintion used by this function relies on function
        get_selsubeq_index.

        It is perfectly OK to pass a modified version of the equation
        previously passed and any arbitrary valid index independently of a
        previous output, but this function is not coded to manage more than
        one equation simultaneously. Create different instances of
        ForwardIndices if you need that.

        Next rules define the output of this method, independently of the
        definition of a selsubeq. In the case that after the application of the
        rules a non-usubueq is determined, apply rules again (starting from
        rule 0) supposing that this function is called again using the same eq
        and with a value of :idx: identical to the "hypothetically returned"
        value by the previous call. Repeat that procedure until a valid
        selsubeq is determined.

        Rules must be read sequentially until one of them applies. Then, next
        rules must not be considered at all. To simplify the writing, returned
        value is named nextidx and arguments :idx: and :eq: are used.
        Commentaries inside parenthesis are intended to be helpful to the
        reader to understand the rules, but not part of the definition of the
        rules.

        Rules:

            0.  If len(eq) == 1, nextidx=0 (independently of idx, which should
                be 0).
            1.  If idx == 0 (the whole equation is selected), nextidx=1.
            2.  If

                    (*) there exists at least one ublock which last element
                    has index idx,

                then next selection is the smallest ublock which validates
                condition (*). If this rule apply, let us define (or
                redefine) i as the value of idx in this call (i will be
                possibly referred in next calls to this function if they
                arrive to rule 3).
            3.  If

                (a) previous selection determined by this function was
                    decided by rules 2 or 3 (this rule), and
                (b) eq value of this call is identical to value of eq of
                    previous call, and
                (c) idx of this call is identical to the value returned
                    by the previous call (nextidx), and
                (d) there exists at least one ublock which last element
                    has index i and is bigger than current selection (its
                    index is smaller than idx),

                then, next selection is the smallest ublock which validates (d)
                (satisfaction of (a) and (b) means that the user did not modify
                the equation nor selected another element of the equation
                after the previous call to this function)
            4.  If

                    (**)    (a) and (b) and (c),
                then, nextidx=i+1.
                (Explanatory note: an additional condition len(eq) != i+1 is
                not needed to avoid returning invalid index len(eq). That is
                because, at this point, len(eq) == i+1 and (a) implies that the
                whole equation was selected in a previous call. Then, rule 1
                would have been applied before arriving to rule 4.)
            5. nextidx=idx+1.
        """
        def apply_rules(idx):
            """
            It implements the rules without considering selsubeqs.
            """
            # Case 0
            if len(eq) == 1:
                return 0

            # Case 1
            if idx == 0:
                return 1

            # Rest of cases (2, 3, 4, and 5)
            # Prepare environment to check (*) and (d) with the same code
            if self.selecting_previous_blocks \
                    and self.expected_eq == eq and self.expected_idx == idx:
                block_idx = self.expected_idx
            else:
                self.selecting_previous_blocks = False
                self.last_element_of_block = idx
                block_idx = None

            # Check (*) and (d)
            block_idx = eqqueries.supeq_finishing_at(
                eq, self.last_element_of_block, block_idx)
            if block_idx >= 0:
                # Case 2 and 3
                if not self.selecting_previous_blocks:
                    self.selecting_previous_blocks = True
                    self.expected_eq = list(eq)
                self.expected_idx = block_idx
                return block_idx
            else:
                # Case 4 and 5
                self.selecting_previous_blocks = False
                return self.last_element_of_block + 1

        doreturn = False
        while not doreturn:
            idx = apply_rules(idx)
            doreturn = is_selsubeq(eq, idx)
        return idx


def sanitizeeq(func):
    """Sanitize equation.

    It must not be used by methods which modify the equation.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        ungroup = False
        if self.idx > 0 and self.eq[self.idx-1] != utils.TEMPGROUP:
            ungroup = True
            tempgroup_idx = self.idx

        retval = func(self, *args, **kwargs)

        # Temporal groups are ungrouped by this decorator
        if ungroup:
            groups.ungroup(self.eq, tempgroup_idx)
        # Set direction to 0 if a NEWARG is selected
        if self.eq[self.idx] == utils.NEWARG:
            self.dir = 0

        return retval

    return wrapper


class Selection:
    def __init__(self, init_eq, init_index, temp_dir, setpixmap):
        self.eq = init_eq
        self.idx = init_index
        self.dir = 0
        self.forward_indices = ForwardIndices()
        self.game = game.Game()
        self.temp_dir = temp_dir
        self.setpixmap = setpixmap
        self.dpi = 300

    def display(self):
        """
        Display equation image.
        """
        # Assert consistency of selection. Do it after updating so no need to
        # distinguish whether passed eq values was None.
        if not 0 <= self.idx < len(self.eq):
            ShowError('Invalid equation index found in eqsel.display.', True)

        eqselected = list(self.eq)

        if self.dir == 0:
            eqselected.insert(self.idx, utils.NEDIT)
        elif self.dir == 1:
            eqselected.insert(self.idx, utils.REDIT)
        else:
            eqselected.insert(self.idx, utils.LEDIT)

        self.game.update(eqselected)
        eqsel_png = conversions.eq2png(eqselected, self.dpi, None,
                                       self.temp_dir)
        self.setpixmap(QPixmap(eqsel_png))

    def set_selsubeq(self):
        """
        Correct self.index if it points to an invalid selection.

        Return True if a correction has been done. Else, False.

        Read docstring of correct_selsubeq to know the exact definition about
        what a valid selection is.
        """
        val = correct_selsubeq(self.eq, self.idx)
        if val >= 0:
            self.idx = val
            return True
        return False

    @sanitizeeq
    def navigate_forward(self):
        """
        If self.dir == -1, set self.dir = 1 and display the formula. Doing
            that does not change the internal state of ForwardIndices.
        Else (self.dir == 0 or 1), set self.index to the next selsubeq
            according to function next, set self.dir = 1 and
            display the formula.

        In any case, if at the end self.eq[self.index] == NEWARG, set self.dir
            to 0.
        """
        # Do not modify any other variables if just turning the ghost around
        # to leave the state OK for further calls.
        if self.dir != -1:
            self.idx = self.forward_indices.next(self.eq, self.idx)

        self.dir = 1 if self.eq[self.idx] != utils.NEWARG else 0
        self.display()

    def _prev_selsubeq(self, n=1):
        """
        Return the next selsubeq index when navigating backward.

        The following rules choose a candidate index to be returned. Read them
        sequentially until the index is chosen. If index define a
        selsubeq, return that index. Else, apply the procedure any times
        that is needed until a chosen index is a selsubeq. Then, return its
        index.

        Supposing that current index is idx, the rules are:

            *   If idx is 0, candidate index is len(eq) - 1.
            *   Else, check element with index idx-1:

                a.  If it is 0, candidate is 0.
                b.  Elif it is a symbol, operator with no arguments or has
                    attribute type_ equal to 'script' or 'opindex', candidate
                    index is this one.
                c.  Else, apply the rules again but considering the index
                    idx-1.
        """
        def apply_rules(idx):
            idx = idx - 1 if idx != 0 else len(self.eq) - 1
            while isinstance(self.eq[idx], utils.Op) \
                    and self.eq[idx].n_args \
                    and self.eq[idx].type_ not in ['script', 'opindex']:
                idx = idx - 1 if idx != 0 else len(self.eq) - 1
            return idx

        previdx = self.idx
        for var in range(n):
            previdx = apply_rules(previdx)
            while not is_selsubeq(self.eq, previdx):
                previdx = apply_rules(previdx)
        return previdx

    @sanitizeeq
    def navigate_backward(self):
        """Navigate backward and display the equation.

        If self.dir == 1, set self.dir = -1 and display the formula.
        Else navigate backward according to self._prev_selsubeq.
        In any case, if at the end self.eq[self.index] == NEWARG, set self.dir
        to 0.

        Rule: Move one index to the left. Repeat if necessary until reaching an
        selsubeq.
        """
        if self.dir != 1:
            self.idx = self._prev_selsubeq()

        if self.eq[self.idx] == utils.NEWARG:
            self.dir = 0
        else:
            self.dir = -1

        self.display()

    def stretch_selection(self, forward):
        """Stretch selection, using temporary groups if needed.

        Rules:
            *   If len(eq) == 1, do nothing.
            *   Elif selection is the whole equation, change
                self.dir according to :forward:.
            *   Elif selection is an usubeq but not the argument of a
                TEMPGROUP:

                *   If
                *   Select smallest usubeq that contains selection and is
                    bigger than selection.
                *   Change self.dir according :forward:.

            *   Elif selection is not the argument of a TEMPGROUP:

                *   If it has a co-citizen towards direction indicated by
                    :forward:, select both citizens and set self.dir according
                    to :forward:.
                *   Else, set self.dir according to :forward:.

            *   Elif self.dir and :forward: indicate the same direction:

                *   If the temporal group containing selection has a citizen
                    towards that direction, include that citizen.
                *   Else, do nothing

            *   Else, shrink selection by leaving outside the last citizen
                if :forward: is False or the first citizen otherwise. Flip
                direction.
        """
        if len(self.eq) == 1:
            return

        # Final direction is common in every case
        finaldir = 1 if forward else -1
        if not self.idx:
            self.dir = finaldir
            return

        gop = utils.TEMPGROUP
        if eqqueries.is_uarg(self.eq, self.idx) \
                and self.eq[self.idx-1] != gop:
            self.idx = eqqueries.usupeq(self.eq, self.idx)
            self.dir = finaldir
            return

        if self.eq[self.idx] != gop or not forward:
            # Create or extend backward
            cocitizen_idx = eqqueries.cocitizen(eq, idx, forward)
            if cocitizen_idx > 0:
                lidx = idx if forward else cocitizen_idx
                ridx = idx if not forward else cocitizen_idx
                if eqqueries.is_last_citizen(eq, ridx):
                    # Case: lidx points to last but one co-citizen
                    if eq[idx] == gop:
                        eq.pop(idx)
                    eq.insert_primitive(lidx - 1, 0, 0, gop)
                    return lidx - 1
                else:
                    # Case: lidx points somewhere before last but one
                    if eq[idx] == gop:
                        eq.pop(idx)
                    eq.pop(ridx - 1)
                    eq[lidx:lidx] = [gop, utils.JUXT]
                    return lidx
            return -1
        if forward:
            # Extend forward
            cocitizen_idx = eqqueries.cocitizen(eq, idx, forward=True)
            if cocitizen_idx > 0:
                old_last_member = eqqueries.last_citizen(eq, idx + 1)
                # Implementation note: Better not to take out of this if-else
                #   the common code modifying eq by know since if-else
                #   condition depends on eq.
                if eqqueries.is_last_citizen(eq, cocitizen_idx):
                    # Case: group is a last but one co-citizen
                    eq.insert_primitive(old_last_member, 0, 0, utils.JUXT)
                    eq.pop(idx - 1)
                    return idx - 1
                else:
                    # Case: group is a co-citizen before last but one
                    eq.insert_primitive(old_last_member, 0, 0, utils.JUXT)
                    eq.pop(cocitizen_idx - 1)
                    return idx
            return -1

        return idx

    def _select(self, idx):
        """Select subeq starting at idx. If dir was 0, change to 1."""
        self.idx = idx
        if not self.dir and self.eq[idx] != utils.NEWARG:
            self.dir = 1
        self.display()

    def _try_selection(self, func):
        """Do selection according to function if possible"""
        while True:
            idx = func(self.eq, self.idx)
            if idx < 0:
                return
            if is_selsubeq(self.eq, idx):
                self._select(idx)
                return

    def select_bigger_usubeq(self):
        """Select bigger usubeq containing selection."""
        self._try_selection(eqqueries.usupeq)

    def select_first_valid_arg(self):
        self.idx += 1
        # selsubeqs!!

    def select_prev_neighbour(self):
        """Select previous argument if usubeq or previous co-citizen if
        citizen.
        """
        self._try_selection(eqqueries.prev_neighbour)

    def select_next_neighbour(self):
        """Select next argument if usubeq or next co-citizen if citizen."""
        self._try_selection(eqqueries.next_neighbour)
