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
import types


from . import eqqueries
from . import groups
from . import simpleeqcreator
from .errors import ShowError
from .symbols import utils


"""
An interface to safely edit and select subequations of an equation.
"""


def new_selection(func):
    @functools.wraps(func)
    def wrapper(eq, idx, *args, **kwargs):
        pass

    return wrapper


def _rinsert_nonjuxtsubeq(eq, idx, usubeq):
    """Insert an usubeq that is not a JUXT-ublock to the right of a subeq.

    :param idx: The index of a subeq behind which *subeq* will be inserted.
    :param usubeq: The subequation to insert. It cannot start with a JUXT.
    :param eq: The equation in which to insert *subeq*.
    :return: Index of first inserted element and *idx* updated.
    """
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0 or arg2_idx < idx:
        # idx points to an uarg or a last citizen
        end_idx = eqqueries.nextsubeq(eq, idx)
        eq[idx:end_idx] = [utils.JUXT] + eq[idx:end_idx] + usubeq
        return end_idx + 1, idx + 1
    else:
        # idx points to a citizen but not the last one
        eq[arg2_idx:arg2_idx] = [utils.JUXT] + usubeq
        return arg2_idx + 1, idx


def _linsert_nonjuxtsubeq(eq, idx, usubeq):
    """Insert an usubeq that is not a JUXT-ublock to the left of a subeq.

    :param idx: The index of a subeq in front of which *usubeq* will be
    inserted.
    :param usubeq: The subequation to insert. It cannot start with a JUXT.
    :param eq: The equation in which to insert_from_panel *subeq*.
    :return: Index of first inserted element and *idx* updated.
    """
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0 or arg2_idx < idx:
        # idx points to eq, an uarg or a last citizen
        eq[idx:idx] = [utils.JUXT] + usubeq
        return idx + 1, idx + 1 + len(usubeq)
    else:
        # idx points to a citizen but not the last one
        eq[idx:idx] = usubeq + [utils.JUXT]
        return idx, idx + len(usubeq) + 1


def _rinsert_juxtsubeq(eq, idx, usubeq):
    """Insert a JUXT-ublock to the right of a subeq.

    :param eq: The equation in which to insert *usubeq*.
    :param idx: The index of a subeq of reference to insert *usubeq*.
    :param usubeq: The subequation to insert. It must start with a JUXT.
    :return: Index of last citizen inserted and *idx* updated.
    """
    subeq_last_citizen = eqqueries.last_citizen(usubeq, 1)
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0 or arg2_idx < idx:
        # idx points to eq, an uarg or a last citizen
        end_idx = eqqueries.nextsubeq(eq, idx)
        eq[idx:end_idx] = [utils.JUXT] + eq[idx:end_idx] + usubeq
        # We are inserting a JUXT and subeq has another:
        # first citizen od subeq has an offset of 2 JUXTs
        return end_idx + 1 + subeq_last_citizen, idx + 1
    else:
        # idx points to a citizen but not the last one
        eq[arg2_idx:arg2_idx] = usubeq[:subeq_last_citizen] + [utils.JUXT] \
                                + usubeq[subeq_last_citizen:]
        return arg2_idx + subeq_last_citizen + 1, idx


def _linsert_juxtsubeq(eq, idx, usubeq):
    """Insert a JUXT-ublock to the left of a subeq.

    :param eq: The equation in which to insert *usubeq*.
    :param idx: The index of a subeq of reference to insert *usubeq*.
    :param usubeq: The subequation to insert. It must start with a JUXT.
    :return: Index of first citizen inserted and :idx: updated.
    """
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    subeq_last_citizen = eqqueries.last_citizen(usubeq, 1)
    if juxt_idx < 0 or arg2_idx < idx:
        # idx points to eq, an uarg or a last citizen
        eq[idx:idx] = usubeq[:subeq_last_citizen] + [utils.JUXT] \
                      + usubeq[subeq_last_citizen:]
        return idx + 1, idx + len(usubeq) + 1
    else:
        # idx points to a citizen but not the last one
        eq[idx:idx] = usubeq[1:subeq_last_citizen] + [utils.JUXT] \
                      + usubeq[subeq_last_citizen:] + [utils.JUXT]
        return idx, idx + len(usubeq) + 2


def _rinsert(eq, idx, usubeq):
    """Insert an usubeq to the right of a subequation.

    .. warning::

        *   *idx* must not point to a NEWARG.
        *   *usubeq* must not be [NEWARG].

    Returned index is:

        *   If :subeq: is a JUXT-ublock, the index in :eq: of last citizen
            of subequation :subeq:.
        *   Else, the first element of :subeq:.

    :eq: A valid equation.
    :idx: The index of a subeq behind which *usubeq* will be inserted.
    :subeq: The subequation to insert. It can be any valid subequation.
    :return: The index that must be selected.
    """
    if usubeq[0] == utils.JUXT:
        lcitizen_idx, newidx = _rinsert_juxtsubeq(eq, idx, usubeq)
        return lcitizen_idx
    else:
        felem_idx, newidx = _rinsert_nonjuxtsubeq(eq, idx, usubeq)
        return felem_idx


def _linsert(eq, idx, usubeq):
    """Insert an usubeq to the left of a subequation.

    .. warning::

        *   *idx* must not point to a NEWARG.
        *   *usubeq* must not be [NEWARG].


    Returned index is:

        *   If *usubeq* is a JUXT-ublock, the index in *eq* of first citizen
            of *usubeq*.
        *   Else, the first element of *usubeq*.

    :param idx: The index of a subeq in front of which *subeq* will be
    inserted.
    :param usubeq: The subequation to insert. It can be any valid subequation.
    :return: The index that must be selected.
    """
    if usubeq[0] == utils.JUXT:
        fcitizen_idx, newidx = _linsert_juxtsubeq(eq, idx, usubeq)
        return fcitizen_idx
    else:
        felem_idx, newidx = _linsert_nonjuxtsubeq(eq, idx, usubeq)
        return felem_idx


def _replace_script_base(eq, idx, usubeq):
    """Replace the base of a script operator."""



def _replace_integrating(eq, idx, usubeq):
    """Replace subeq starting at idx by integrating citizens, if needed.

    Requirement:

        *   subeq must not be [NEWARG]

    If :idx: does not point to a citizen or :subeq: is not a JUXT-ublock,
    it is an ordinary replacement.
    Else, citizen which start at :idx: is removed and citizens of :subeq:
    are added as co-citizens of the corresponding JUXT-ublock in :eq:.

    Returned value:

        *   If every element with index i in :subeq: has index :idx: + i in
            :eq: after replacement, 0 is returned
        *   Else, 1 is returned. It means that:

            *   Any citizen, except the last one, with index i in :subeq:, has
                index :idx: + i - 1 in :eq:.
            *   Last citizen in :subeq: has index :idx: + i in :eq:.

            Note:

                That happens when :subeq: is a JUXT-ublock and :idx: pointed to
                a citizen which was not the last one of some JUXT-ublock in
                :eq:.

    :param eq: Equation in which the replacement is done.
    :param idx: The index of a subeq which will be replaced.
    :param usubeq: Subeq with which subeq starting at :idx: will be replaced.
    :return: A flag value explained above.
    """
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if usubeq[0] != utils.JUXT or juxt_idx < 0 or arg2_idx < idx:
        # subeq does not start with JUXT or idx points to:
        #   1. eq, or
        #   2. An uarg, or
        #   3. A last citizen
        end_index = eqqueries.nextsubeq(eq, idx)
        eq[idx:end_index] = usubeq
        return 0
    else:
        # idx points to the first argument of a JUXT (terminal or not)
        subeq_last_citizen = eqqueries.last_citizen(usubeq, 1)
        eq[idx:arg2_idx] = usubeq[1:subeq_last_citizen] + [utils.JUXT] \
                           + usubeq[subeq_last_citizen:]
        return 1


def _replace_grouped(eq, idx, usubeq, temp=False):
    """Replace subeq which starts at idx as a group, if needed.

    .. warning::
        *subeq* must not be [NEWARG]

    Rules:

        *   If *idx* does not point to a citizen or *subeq* is not a
            JUXT-ublock, it is an ordinary replacement.
        *   Else, the citizen in *idx* is replaced by *subeq* "protected"
            with a group operator.

    If you want a group operator in front of your subeq even if it is not
    a JUXT-ublock, add it by yourself and call this (or replace_integrating)
    function then.

    :param eq: Equation in which the replacement is done.
    :param idx: The index of a subeq which will be replaced.
    :param usubeq: Subeq with which subeq starting at *idx* will be replaced.
    :param temp: Indicates whether the group will be temporal, if it is
    included.
    :return: An index pointing to the subequation that must be selected.
    """
    if usubeq[0] != utils.JUXT:
        # subeq does not start with JUXT
        end_idx = eqqueries.nextsubeq(eq, idx)
        eq[idx:end_idx] = usubeq
        return idx

    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0:
        # idx points to an uarg or eq
        end_idx = eqqueries.nextsubeq(eq, idx)
        eq[idx:end_idx] = usubeq
        return idx

    gop = utils.TEMPGROUP if temp else utils.GROUP
    if idx < arg2_idx:
        # idx points to the first argument of a JUXT
        eq[idx:arg2_idx] = [gop] + usubeq
        return idx + 1
    else:
        # idx points to the a last citizen
        end_idx = eqqueries.nextsubeq(eq, idx)
        eq[idx:end_idx] = [gop] + usubeq
        return idx + 1


def remove_eq(eq):
    eq[:] = [utils.NEWARG]
    return 0, 0


def _remove_selection(eq, idx, dir):
    """Remove current selection. It does nothing with empty arguments.

    Requirement:

        *   :idx: must not point to a NEWARG.

    Rules depending on selection:

        *   If it is an uarg or eq, a NEWARG is put in its place, it is
            selected and direction is set to 0.
        *   Elif it is a last citizen, after its removal the co-citizen
            to the left is selected and direction is set to 1.
        *   Elif it is a first citizen, after its removal the co-citizen to
            the right is selected and direction is set to -1.
        *   Else (intermediate citizen), the citizen is removed and:

            *   If direction was 1, the co-citizen to the left is selected
                and direction is not changed.
            *   Else (direction was -1), the co-citizen to the right is
                selected and direction is not changed.
    """
    if not idx:
        return remove_eq(eq)

    juxt_idx, otherarg = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0:
        # Case: Remove uarg
        end_idx = eqqueries.nextsubeq(eq, idx)
        eq[idx:end_idx] = [utils.NEWARG]
        return idx, 0

    # From this point, we know idx points to citizen
    if otherarg < idx:
        # Case: Remove last citizen
        # It does not matter which kind of replace you use in this case
        _replace_grouped(juxt_idx, eq[otherarg:idx], eq)
        return juxt_idx, 1

    # From here, selection is a citizen which is not the last one
    # Low-level hardcore starts... :P
    juxt_juxt_idx, prev_cocitizen_idx \
        = eqqueries.other_juxt_arg(eq, juxt_idx)
    eq[juxt_idx:otherarg] = []
    if juxt_juxt_idx < 0:
        # Case: first citizen WAS just removed
        if eq[idx] != utils.JUXT:
            idx -= 1
        return idx, -1
    else:
        # Case: intermediate citizen WAS just removed and dir was 1
        if dir == 1:
            idx = prev_cocitizen_idx
        elif eq[juxt_idx] != utils.JUXT:
            # Subcase: Removed citizen WAS before last but one citizen
            idx -= 1
        return idx, dir


def flat_internal_op(eq, idx, dir):
    """Flat the least internal operator.

    Rules:

        *   If selection is a symbol, operator with no arguments or
            JUXT-ublock, remove selection by the rules of
            _remove_selection.
        *   Else, apply rules of _flat_external_op_core considering that
            operator referred there is current selection and some of its
            arguments is selected.
            Final selection will be all the non-NEWARG arguments, without
            changing the direction, adding a temporal group if necessary.
    """
    if isinstance(eq[idx], str) \
            or eq[idx].n_args == 0 \
            or eq[idx] == utils.JUXT:
        return _remove_selection(eq, idx, dir)

    arg_idx = idx + 1
    vargs = []  # list of valid args
    for ignored in range(eq[idx].n_args):
        next_arg_idx = eqqueries.nextsubeq(eq, arg_idx)
        if eq[arg_idx] != utils.NEWARG:
            vargs.append(eq[arg_idx:next_arg_idx])
        arg_idx = next_arg_idx

    if not vargs:
        # Subcase: No argument is valid, delete the entire operator.
        return _remove_selection(eq, idx, dir)

    subeq_c = simpleeqcreator.SimpleEqCreator()
    for varg in vargs:
        subeq_c.extend(varg)
    return _replace_grouped(eq, idx, subeq_c.get_eq(), temp=True), dir


def _flat_external_op_core(eq, idx, dir, remove_mode=0):
    """Flat the least external operator.

    Parameter :remove_mode: is expected to be:

        *   If this function is the consequence of deleting, 1.
        *   If this function is the consequence of suppression, -1.
        *   Otherwise, 0.

    Main behavior:

        Consider the least external operator of selected usubeq (read below
        about the behaviour if selection is a citizen):

        *   If every argument of operator is a NEWARG, remove the subeq
            defined by the operator by the rules of _remove_selection
            supposing that it is selected with the same direction than
            :remove_mode:.
        *   If only one argument of the operator is not a NEWARG and it is
            not a JUXT-ublock, replace the subequation defined by the
            operator with that argument.
        *   If only one argument of the operator is not a NEWARG and it is
            a JUXT-ublock, replace the subequation defined by the
            operator with the JUXT-ublock preceded by a temporal group.
        *   Else (more than one non-NEWARG arguments), create a JUXT-ublock
            were citizens will be:

            *   Every non-NEWARG argument which is not a JUXT-ublock, and
            *   Every citizen of any argument which is a JUXT-ublock.

            Relative order of citizens will be the same in which they
            appear in the equation.

            The operator considered can be itself an usubeq or a citizen:

            *   If operator is an usubeq, replace it by the JUXT-ublock.
            *   Else (operator is a citizen) replace operator with the
                citizens of the created JUXT-ublock in such a way that
                its citizens are co-citizens of the JUXT-ublock to which
                operator belonged.

    Finally selected subequation will be:

        *   If every argument of the operator is a NEWARG, selection
            is decided by self._remove_selection's rules.
        *   If selection is not a NEWARG, selection will be the same than
            originally selected and with the same direction.
        *   Else (NEWARG selected and there is at least one non-NEWARG),
            remove_mode parameter decides the selection:

            *   If remove_mode == 0 (NEUTRAL node):

                *   If there is at least one non-NEWARG argument to the
                    right, select the first one and set dir = -1 (neither you
                    nor I).
                *   Else select the first non-NEWARG to the left and set
                    dir = 1.

            *   If remove_mode == 1 (SUPR mode):

                *   If there is at least one non-NEWARG argument to the
                    right, select the first one and set dir = 1.
                *   Else, select the first non-NEWARG to the left and set
                    dir = 1.

            *   If remove_mode == -1 (DEL mode):

               *    If there is at least one non-NEWARG argument to the
                    left, select the first one and set self.eqsel.dir = 1.
                *   Else, select the first non-NEWARG to the right and set
                    dir = -1.

    Special cases:

    If selection is a citizen:

        *   If the JUXT-ublock to which selection belongs is the whole
            equation, remove the whole equation.
        *   Elif there are not other non-NEWARG arguments:

            *   If operator is an usubeq, replace the operator with the
                JUXT-ublock to which selection belongs.
            *   Else, remove operator and integrate selection and its
                co-citizens as co-citizens of the JUXT-ublock to which
                operator belonged.

        *   Else (there are other non-NEWARG arguments), apply the
            equivalent rule in the "Main behavior" section.

        In the last 2 cases leave selected the originally selected citizen
        and with the same direction.
        Note that remove_mode parameter is never used in this case.
    """
    # Set variables that define function's casuistic:
    #   The case in which a citizen is selected is managed by selecting its
    #   JUXT-ublock and setting and offset value.
    #   "Selected argument" below will refer to the JUXT-ublock if this
    #   case applies
    arg_idx = idx
    offset = 0
    old_sel_was_last_citizen = False
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx >= 0:
        # Current selection is a citizen
        parent_juxt = eqqueries.parent_juxt(eq, idx)
        if parent_juxt == 0:
            # Case: Selection is a citizen of the whole equation
            return remove_eq()

        arg_idx = parent_juxt
        offset = parent_juxt - idx
        if arg2_idx < idx:
            old_sel_was_last_citizen = True

    # Index of operator and ordinal of selected argument (starting from 1)
    op_idx, arg_ord = eqqueries.whosearg(eq, arg_idx)
    # Get information about arguments of the operator
    arg_idx = op_idx + 1
    vargs = []  # list of valid args
    # ridx stands for "reduced index", an index of vargs
    arg_ridx = -1
    larg_ridx = -1
    rarg_ridx = -1
    for current_arg_ord in range(1, eq[op_idx].n_args + 1):
        next_arg_idx = eqqueries.nextsubeq(eq, arg_idx)
        # Consider only args != NEWARG
        if eq[arg_idx] != utils.NEWARG:
            if current_arg_ord == arg_ord:
                arg_ridx = len(vargs)
            elif current_arg_ord < arg_ord:
                larg_ridx = len(vargs)
            elif rarg_ridx < 0 and current_arg_ord > arg_ord:
                rarg_ridx = len(vargs)
            vargs.append(eq[arg_idx:next_arg_idx])
        arg_idx = next_arg_idx

    if not vargs:
        # Case: No argument is valid, delete the entire operator.
        return _remove_selection(eq, op_idx, remove_mode)

    # Decide selected argument and its direction
    if arg_ridx >= 0:
        sel_ridx = arg_ridx  # offset != 0 managed later
    elif remove_mode == 0:
        if rarg_ridx >= 0:
            sel_ridx = rarg_ridx
            dir = -1
        else:
            sel_ridx = larg_ridx
            dir = 1
    elif remove_mode == 1:
        if rarg_ridx >= 0:
            sel_ridx = rarg_ridx
        else:
            sel_ridx = larg_ridx
        dir = 1
    else:
        if larg_ridx >= 0:
            sel_ridx = larg_ridx
            dir = 1
        else:
            sel_ridx = rarg_ridx
            dir = -1

    # Create a JUXT-ublock with the arguments
    subeq_c = simpleeqcreator.SimpleEqCreator()
    for varg in vargs[:sel_ridx]:
        subeq_c.extend(varg)
    if vargs[sel_ridx][0] == utils.JUXT and not offset:
        subeq_c.extend([utils.TEMPGROUP] + vargs[sel_ridx])
    else:
        subeq_c.extend(vargs[sel_ridx])
    for varg in vargs[sel_ridx + 1:]:
        subeq_c.extend(varg)

    # Replace the equation and select correctly
    takecare = _replace_integrating(eq, op_idx, subeq_c.get_eq())
    if takecare and (sel_ridx != len(vargs)
                     or (offset and not old_sel_was_last_citizen)):
        return op_idx + subeq_c.get_idx(offset, sel_ridx) - 1, dir
    else:
        return op_idx + subeq_c.get_idx(offset, sel_ridx), dir


def _remove_arg(eq, idx, remove_mode=0):
    """Remove an argument.

    Requirement:

        *   It is expected that :idx: points to a NEWARG, so dir is supposed
            to be 0.

    Parameter :remove_mode: is expected to be:

        *   If this function is the consequence of deleting, 1.
        *   If this function is the consequence of suppression, -1.

     Rules:
        *   If :idx: points to a script operator, downgrade the script
            operator.
        *   Else, apply rules of _flat_external_op_core.
    """
    isscript, script_op_idx, arg_pos = eqqueries.is_script(eq, idx)

    if not isscript:
        return _flat_external_op_core(eq, idx, 0, remove_mode)

    args = eqqueries.indexop2arglist(eq, script_op_idx)
    # Find which element of the list has to be removed
    # Note that arg_pos only applies non-None arguments
    valid_pos = 0
    for pos, arg in enumerate(args):
        if arg is not None:
            if valid_pos == arg_pos:
                args[pos] = None
                break
            else:
                valid_pos += 1
    new_op = eqqueries.arglist2indexop(args)
    end_block = eqqueries.nextsubeq(eq, script_op_idx)
    if new_op is None:
        eq[script_op_idx:end_block] = args[0]
    else:
        new_args = eqqueries.flat_arglist(args)
        eq[script_op_idx:end_block] = [new_op] + new_args
    return script_op_idx, 1


def _rremove(eq, idx):
    """Remove "to the right" of selection and return new valid index.

    Rules:

        *   If selection is the whole equation, do nothing.
        *   Elif it has a co-citizen to the right, remove it.
        *   Else, flat the least external operator.

    Selection and direction are not modified.
    """
    juxt_idx, otherarg = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx >= 0:
        # Case: selection is a citizen
        if idx < otherarg:
            if eq[otherarg] == utils.JUXT:
                # Subcase: selection is a citizen before the last but one
                end_idx = eqqueries.nextsubeq(eq, otherarg + 1)
                eq[otherarg:end_idx] = []
            else:
                # Subcase: selection is a last but one co-citizen
                end_idx = eqqueries.nextsubeq(eq, otherarg)
                eq[juxt_idx:end_idx] \
                    = eq[idx:otherarg]
                idx -= 1
        else:
            # Subcase: selection is a last citizen
            _flat_external_op_core(eq, idx)
    elif idx:
        # Case: selection is an uarg
        _flat_external_op_core(eq, idx)
    return idx


def _lremove(eq, idx):
    """Remove "to the left" of selection.and return a valid index.

    Rules:

        *   If selection is the whole equation, do nothing.
        *   Elif it has a co-citizen to the left, remove it.
        *   Else, flat the least external operator.

    Selection and direction are not modified.
    """
    # Check if it is the arg of a JUXT and leave it clean
    lcocitizen_idx = eqqueries.cocitizen(eq, idx, forward=False)
    if lcocitizen_idx < 0:
        # Case: selection is not a citizen or it is a first citizen
        _flat_external_op_core()
    elif eq[idx - 1] == utils.JUXT:
        # Case: selection is not the last citizen
        eq[lcocitizen_idx - 1:idx - 1] = []
        idx = lcocitizen_idx
    else:
        # Case: selection is the last citizen
        eq[lcocitizen_idx - 1:idx] = []
        idx = lcocitizen_idx - 1
    return idx


def insert_primitive(eq, idx, dir, pelem):
    """Insert/replace a subequation from a primitive element.

    .. warning::
        *pelem* must not be a NEWARG nor a JUXT.

    :param eq: An equation.
    :param idx: Index of current selection.
    :param dir: Current direction of selection.
    :param pelem: The primitive parameter to insert.
    :return: New selection index and direction.

    Depending on *pelem* and *dir*, behavior is different:

        *   If *pelem* is a symbol or operator with 0 arguments:

            *   If *dir* is 1, insert it to the right of selection.
            *   Elif *dir* is -1, insert it to the left of selection.
            *   Else, substitute selection with the symbol.

        *   If *pelem* is an operator with more than one argument:

            *   If *dir* is 1, insert it to the right of selection with every
                argument set to a NEWARG.
            *   Elif *dir* is -1, insert it to the left of selection with every
                argument set to a NEWARG.
            *   Elif *dir* is 0, substitute selection with the operator with
                every argument set to a NEWARG.
            *   Elif *dir* is 2, substitute selection with the operator with
                every argument set to a NEWARG except the first one, which
                is set to the subequation that was selected.

    Final selection and direction:

        *   If *pelem* is a symbol, select it and set direction to 1.
        *   Elif *pelem* is an operator and dir in [-1, 0, 1], select first
            argument and set dir to 1.
        *   Elif *pelem* is an operator and dir is 2, select the second
            argument and set dir to 0.
    """

    if isinstance(pelem, str) \
            or (isinstance(pelem, utils.Op) and not pelem.n_args):
        usubeq = [pelem]
    elif dir == 2:
        sel_end = eqqueries.nextsubeq(eq, idx)
        usubeq = [pelem] + eq[idx:sel_end] + [utils.NEWARG]*(pelem.n_args - 1)
    else:
        usubeq = [pelem] + [utils.NEWARG] * pelem.n_args

    if not dir:
        usubeq_idx = _replace_integrating(eq, idx, usubeq)
        return usubeq_idx, 1 if len(usubeq) == 1 else usubeq_idx + 1, 0
    elif dir == 2:
        usubeq_idx = _replace_integrating(eq, idx, usubeq)
        arg1_end = eqqueries.nextsubeq(eq, usubeq_idx + 1)
        return arg1_end, 0
    elif dir == 1:
        return _rinsert(eq, idx, usubeq), 1
    elif dir == -1:
        return _linsert(eq, idx, usubeq), 1


def insert_substituting(eq, idx, dir, pelem):
    """Substitute current selection with a new subeq depending on primitive
    element.

    New subequation will be:

        *   If :pelem: is a symbol, the symbol.
        *   If :pelem: is an operator:

            *   If it is a 0-argument operator, the operator.
            *   Elif it is a 1-argument operator, selection preceded by the
                operator.
            *   Else, operator + selection + "as many NEWARGS as needed"


    Return:
        *   If introduced subequation is a symbol or operator with
            zero or one arguments, select subequation and set
            dir = 1.
        *   If it is an operator with more than one argument, select
            the second argument and set dir = 0.
    """
    if isinstance(pelem, str) or \
            (isinstance(pelem, utils.Op) and pelem.n_args == 0):
        _replace_integrating(eq, idx, pelem)
        dir = 1
    elif isinstance(pelem, utils.Op) and pelem.n_args == 1:
        # This insert is a list method
        eq.insert(idx, pelem)
        dir = 1
    elif isinstance(pelem, utils.Op) and pelem.n_args > 1:
        sel_end = eqqueries.nextsubeq(self.eq, self.eqsel.idx)
        self.eq[self.eqsel.idx:sel_end] \
            = [pelem] + self.eq[self.eqsel.idx:sel_end] \
              + [utils.NEWARG] * (pelem.n_args - 1)
        self.eqsel.idx = sel_end + 1
        self.eqsel.dir = 0
    else:
        ShowError('Unknown type of operator in insert_subst: '
                  + repr(pelem), True)

@updatestate
def _insert_script_core(self, is_superscript):
    """
    Read self.insert_script docstring.
    """
    # Select the subequation of interest in the case that selection is a
    # JUXT.
    if self.eq[self.eqsel.idx] == utils.JUXT:
        if self.eqsel.dir == 1:
            self.eqsel.idx = eqqueries.last_citizen(
                self.eq, self.eqsel.idx)
        else:
            self.eqsel.idx += 1
    # Create an arglist with the current indices
    args = eqqueries.indexop2arglist(self.eq, self.eqsel.idx)
    # Include a NEWARG if the the index is not available
    if self.eqsel.dir != -1:
        script_id = 3 if is_superscript else 2
    else:
        script_id = 4 if is_superscript else 1
    if args[script_id] is None:
        args[script_id] = [utils.NEWARG]
        self.eqsel.dir = 0
    else:
        self.eqsel.dir = 1

    argselems_frombasetocurrent = 0
    for i in range(script_id):
        if args[i] is not None:
            argselems_frombasetocurrent += len(args[i])

    new_op = eqqueries.arglist2indexop(args)
    # Flat the list of args
    new_args = eqqueries.flat_arglist(args)
    new_ublock = [new_op] + new_args
    end_prev_ublock = eqqueries.nextsubeq(self.eq, self.eqsel.idx)
    self.eq[self.eqsel.idx:end_prev_ublock] = new_ublock

    self.eqsel.idx += 1 + argselems_frombasetocurrent

def insert_script(self, is_superscript):
    """Insert a sub or superscript and select it.

    If it already exists, just select it.

    If a JUXT-ublock is selected, put the script to the right of last
    citizen if eqsel.dir == 1. Else, put the script to the left of the
    first citizen.

    Some elements are blacklisted. Nothing is done in that case.
    """
    # Blacklist some operators
    if not (hasattr(self.eq[self.eqsel.idx], 'type_')
            and self.eq[self.eqsel.idx].type_ in utils.INDEX_BLACKLIST):
        self._insert_script_core(is_superscript)

@updatestate
def delete(self, supr=False):
    """
    Interface to remove subequations.

    self.eqsel.dir works as the position of a cursor:

        * If +1, it is to the right of selection.
        * If -1, it is to the left of selection.

    By default, it removes what is to the left of the cursor (current
    selection or "something to the left").

    If :supr: is True, this function works like a suppression, removing
    what is to the right of the cursor ("something to the right" or current
    selection).

    :supr: If True, use suppression rules instead of deletion ones.
    """
    if self.eqsel.idx == 0:
        # Remove whole equation
        self.remove_eq()
    elif self.eq[self.eqsel.idx] == utils.NEWARG:
        # Downgrade script or flat least external operator
        self._remove_arg()
    elif (self.eqsel.dir == 1 and not supr) \
            or (self.eqsel.dir == -1 and supr):
        # Remove current selection and set a nice selection
        self._remove_selection()
    elif self.eqsel.dir == 1:
        # Remove to the right
        self._rremove()
    else:
        # Remove to the left
        self._lremove()

def transpose_neighbours(self):
    w2_idx = self.eqsel.idx

    @updatestate
    def transpose_helper(self, w1_idx):
        endw2_idx = eqqueries.nextsubeq(self.eq, w2_idx)
        endw1_idx = eqqueries.nextsubeq(self.eq, w1_idx)

        temp = self.eq[w2_idx:endw2_idx]
        self.eq[w2_idx:endw2_idx] = self.eq[w1_idx:endw1_idx]
        self.eq[w1_idx:endw1_idx] = temp
        self.eqsel.idx += (endw2_idx - w2_idx) - (endw1_idx - w1_idx)
        self.eqsel.dir = 1

    w1_idx = eqqueries.prev_neighbour(self.eq, self.eqsel.idx)
    if w1_idx > 0:
        transpose_helper(self, w1_idx)

