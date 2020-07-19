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

from . import eqqueries
from . import groups
from . import scriptops
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


def _rinsert_nonjuxtsubeq(eq, idx, subeq):
    """Insert a subeq not starting by JUXT to the right of a subeq.

    :param idx: The index of a subeq behind which *subeq* will be inserted.
    :param subeq: The subequation to insert. It cannot start with a JUXT.
    :param eq: The equation in which to insert *subeq*.
    :return: Index of first inserted element and *idx* "updated".
    """
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0 or arg2_idx < idx:
        # idx points to an uarg or a last citizen
        end_idx = eqqueries.nextsubeq(eq, idx)
        if scriptops.is_base(eq, idx):
            # Uarg subcase: idx points to the base of a (v)script
            # Convert (v)script operator if needed
            scriptops.update_scriptblock(eq, idx, utils.JUXT)

        eq[idx:end_idx] = [utils.JUXT] + eq[idx:end_idx] + subeq
        return end_idx + 1, idx + 1
    else:
        # idx points to a citizen but not the last one
        eq[arg2_idx:arg2_idx] = [utils.JUXT] + subeq
        return arg2_idx + 1, idx


def _linsert_nonjuxtsubeq(eq, idx, subeq):
    """Insert an subeq which does not start to the left of a subeq.

    :param idx: The index of a subeq in front of which *subeq* will be
    inserted.
    :param subeq: The subequation to insert. It cannot start with a JUXT.
    :param eq: The equation in which to insert_from_panel *subeq*.
    :return: Index of first inserted element and *idx* updated.
    """
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0 or arg2_idx < idx:
        # idx points to eq, an uarg or a last citizen
        if scriptops.is_base(eq, idx):
            # Uarg subcase: idx points to the base of a (v)script
            # Convert (v)script operator if needed
            scriptops.update_scriptblock(eq, idx, utils.JUXT)

        eq[idx:idx] = [utils.JUXT] + subeq
        return idx + 1, idx + 1 + len(subeq)
    else:
        # idx points to a citizen but not the last one
        eq[idx:idx] = subeq + [utils.JUXT]
        return idx, idx + len(subeq) + 1


def _rinsert_juxtsubeq(eq, idx, subeq):
    """Insert a subeq which starts by JUXT to the right of a subeq.

    :param eq: The equation in which to insert *subeq*.
    :param idx: The index of a subeq of reference to insert *subeq*.
    :param subeq: The subequation to insert. It must start with a JUXT.
    :return: Index of last citizen inserted and *idx* updated.
    """
    subeq_last_citizen = eqqueries.last_citizen(subeq, 1)
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0 or arg2_idx < idx:
        # idx points to eq, an uarg or a last citizen
        end_idx = eqqueries.nextsubeq(eq, idx)
        eq[idx:end_idx] = [utils.JUXT] + eq[idx:end_idx] + subeq
        # We are inserting a JUXT and subeq has another:
        # first citizen od subeq has an offset of 2 JUXTs
        return end_idx + 1 + subeq_last_citizen, idx + 1
    else:
        # idx points to a citizen but not the last one
        eq[arg2_idx:arg2_idx] = subeq[:subeq_last_citizen] + [utils.JUXT] \
                                + subeq[subeq_last_citizen:]
        return arg2_idx + subeq_last_citizen + 1, idx


def _linsert_juxtsubeq(eq, idx, subeq):
    """Insert a subeq which starts by JUXT to the left of a subeq.

    :param eq: The equation in which to insert *usubeq*.
    :param idx: The index of a subeq of reference to insert *usubeq*.
    :param subeq: The subequation to insert. It must start with a JUXT.
    :return: Index of first citizen inserted and :idx: updated.
    """
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    subeq_last_citizen = eqqueries.last_citizen(subeq, 1)
    if juxt_idx < 0 or arg2_idx < idx:
        # idx points to eq, an uarg or a last citizen
        eq[idx:idx] = subeq[:subeq_last_citizen] + [utils.JUXT] \
                      + subeq[subeq_last_citizen:]
        return idx + 1, idx + len(subeq) + 1
    else:
        # idx points to a citizen but not the last one
        eq[idx:idx] = subeq[1:subeq_last_citizen] + [utils.JUXT] \
                      + subeq[subeq_last_citizen:] + [utils.JUXT]
        return idx, idx + len(subeq) + 2


def _rinsert(eq, idx, subeq):
    """Insert an subeq to the right of a subequation.

    .. warning::

        *   *idx* must not point to a NEWARG.
        *   *usubeq* must not be [NEWARG].

    Returned index is:

        *   If *subeq* starts by JUXT, the index in *eq* of last citizen
            of subequation *subeq*.
        *   Else, the first element of *subeq* in *eq*.

    :param eq: A valid equation.
    :param idx: The index of a subeq behind which *usubeq* will be inserted.
    :param subeq: The subequation to insert. It can be any valid subequation.
    :return: The index that must be selected.
    """
    if subeq[0] == utils.JUXT:
        lcitizen_idx, newidx = _rinsert_juxtsubeq(eq, idx, subeq)
        return lcitizen_idx
    else:
        felem_idx, newidx = _rinsert_nonjuxtsubeq(eq, idx, subeq)
        return felem_idx + 1 if groups.is_some_group(subeq[0]) else felem_idx


def _linsert(eq, idx, subeq):
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
    :param subeq: The subequation to insert. It can be any valid subequation.
    :return: The index that must be selected.
    """
    if subeq[0] == utils.JUXT:
        fcitizen_idx, newidx = _linsert_juxtsubeq(eq, idx, subeq)
        return fcitizen_idx
    else:
        felem_idx, newidx = _linsert_nonjuxtsubeq(eq, idx, subeq)
        return felem_idx + 1 if groups.is_some_group(subeq[0]) else felem_idx


def _replace_integrating(eq, idx, subeq):
    """Replace subeq starting at idx by integrating citizens, if needed.

    .. note::
        Do not use this function if selection starts at *idx*: Replacement
        should be selected in that case. You can use _replace_grouped with a
        temporal group instead.

    .. note::
        subeq must not be [NEWARG]. Consider _remove_selection instead.

    If *idx* does not point to a citizen or *subeq* does not start with JUXT,
    it is an ordinary replacement.
    Else, citizen which start at *idx* is removed and citizens of *subeq*
    are added as co-citizens of the corresponding JUXT-ublock in *eq*.

    Meaning of returned value:

        *   If every element with index i in :subeq: has index *idx* + i in
            *eq* after replacement, 0 is returned
        *   Else, 1 is returned. It means that:

            *   Any citizen, except the last one, with index i in :subeq:, has
                index *idx* + i - 1 in *eq*.
            *   Last citizen in :subeq: has index *idx* + i in *eq*.

            .. note::
                That happens when *subeq* is a JUXT-ublock and *idx* pointed to
                a citizen which was not the last one of some JUXT-ublock in
                *eq*.

    :param eq: Equation in which the replacement is done.
    :param idx: The index of a subeq which will be replaced.
    :param subeq: Subeq with which subeq starting at :idx: will be replaced.
    :return: A flag explained above.
    """
    # If selection is the argument of a group, replace the full group
    # Note that solid groups should also be replaced totally
    if idx and groups.is_grouped_someway(eq, idx):
        idx -= 1

    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if subeq[0] != utils.JUXT or juxt_idx < 0 or arg2_idx < idx:
        # subeq does not start with JUXT or idx points to:
        #   1. eq, or
        #   2. An uarg, or
        #   3. A last citizen
        if scriptops.is_base(eq, idx):
            # Subcase: Substitute (v)script base
            scriptops.update_scriptblock(eq, idx, subeq[0])

        end = eqqueries.nextsubeq(eq, idx)
        eq[idx:end] = subeq
        return 0
    else:
        # idx points to the first argument of a JUXT (terminal or not)
        subeq_last_citizen = eqqueries.last_citizen(subeq, 1)
        eq[idx:arg2_idx] = subeq[1:subeq_last_citizen] + [utils.JUXT] \
                           + subeq[subeq_last_citizen:]
        return 1


def _replace_grouped(eq, idx, subeq, temp=False):
    """Replace subeq which starts at idx as a group, if needed.

    .. note::
        *subeq* must not be [NEWARG]. Consider _remove_selection instead.

    Rules:

        *   If *idx* does not point to a citizen or *subeq* does not start
            with JUXT, it is an ordinary replacement.
        *   Else, the citizen in *idx* is replaced by *subeq* "protected"
            with a group operator.

    If you want a group operator in front of *subeq* even if it does not
    start with JUXT, add it by yourself before calling this function (or
    _replace_integrating, which would be equivalent).

    :param eq: Equation in which the replacement is done.
    :param idx: The index of a subeq which will be replaced.
    :param subeq: Subeq with which subeq starting at *idx* will be replaced.
    :param temp: Indicates whether the group will be temporal, if it is
    included.
    :return: An index pointing to the subequation that must be selected.
    """
    # If selection is the argument of a group, replace the full group
    # Note that solid groups should also be replaced totally
    if groups.is_grouped_someway(eq, idx):
        idx -= 1

    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0 or subeq[0] != utils.JUXT:
        # idx points to an uarg or eq; or subeq does not start with JUXT
        if scriptops.is_base(eq, idx):
            # Subcase: Substitute (v)script base
            scriptops.update_scriptblock(eq, idx, subeq[0])

        end_idx = eqqueries.nextsubeq(eq, idx)
        eq[idx:end_idx] = subeq
        return idx

    gop = utils.TEMPGROUP if temp else utils.GROUP
    if idx < arg2_idx:
        # idx points to the first argument of a JUXT
        eq[idx:arg2_idx] = [gop] + subeq
        return idx + 1
    else:
        # idx points to a last citizen
        end_idx = eqqueries.nextsubeq(eq, idx)
        eq[idx:end_idx] = [gop] + subeq
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
    # Correct index if the argument of a group is selected
    # Note that solid groups also should be removed totally
    if groups.is_grouped_someway(eq, idx):
        idx -= 1

    if not idx:
        # Case: remove whole eq
        return remove_eq(eq)

    juxt_idx, otherarg = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0:
        # Case: Remove uarg
        if scriptops.is_base(eq, idx):
            # Uarg subcase: idx points to the base of a (v)script
            # Convert (v)script operator if needed
            scriptops.update_scriptblock(eq, idx, utils.NEWARG)

        end = eqqueries.nextsubeq(eq, idx)
        eq[idx:end] = [utils.NEWARG]
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


def _remove_arg(eq, idx, dir, remove_mode=1):
    """Remove an argument by flatting or downgrading its operator.

    .. note::
        Usually you would want to use this function if the arg is a NEWARG.

    Parameter +remove_mode+ is expected to be:

        *   If this function is the consequence of deleting, 1.
        *   If this function is the consequence of suppression, -1.

     Rules:

        *   If *idx* points to the argument of a (v)script operator which is
            not the base, downgrade the (v)script operator.
        *   Else, apply rules of _flat_external_op_core.
    """
    # Note that any group (including solid groups) should also be replaced
    # totally
    if groups.is_grouped_someway(eq, idx):
        idx -= 1

    op_idx, arg_pos = eqqueries.whosearg_filter_type(eq, idx)

    # Flat operator if not a script
    if op_idx < 0 \
            or eq[op_idx] not in utils.ALLSCRIPT_TYPES \
            or scriptops.is_base(eq, idx):
        return _flat_external_op_core(eq, idx, dir, remove_mode)

    # From this point it is assumed that we are dealing with the argument
    # of a script or vscript which is not the base
    return scriptops.remove_script(eq, idx), 1


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
                end = eqqueries.nextsubeq(eq, otherarg + 1)
                eq[otherarg:end] = []
            else:
                # Subcase: selection is a last but one co-citizen
                if scriptops.is_base(eq, juxt_idx):
                    # Sub-subcase: Dissolve JUXT in (v)script base
                    scriptops.update_scriptblock(eq, juxt_idx, eq[idx])

                end = eqqueries.nextsubeq(eq, otherarg)
                eq[juxt_idx:end] = eq[idx:otherarg]
                idx -= 1

                if idx and eq[idx-1] == utils.GROUP:
                    # Sub-subcase: Group has no sense any more
                    # Note that solid groups should not be removed
                    eq.pop(idx-1)
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
    elif eq[idx-1] == utils.JUXT:
        # Case: selection is not the last citizen
        eq[lcocitizen_idx-1:idx-1] = []
        idx = lcocitizen_idx
    else:
        # Case: selection is the last citizen
        if scriptops.is_base(eq, lcocitizen_idx-1):
            # Subcase: Dissolve JUXT-ublock in (v)script base
            scriptops.update_scriptblock(eq, lcocitizen_idx - 1, eq[idx])

        eq[lcocitizen_idx-1:idx] = []
        idx = lcocitizen_idx - 1

        if idx and eq[idx-1] == utils.GROUP:
            # Subcase: Group has no sense any more
            # Note that solid groups should not be removed
            eq.pop(idx-1)
            idx -= 1

    return idx


def insert(eq, idx, dir, pseudoelem):
    """Insert/replace a subequation from a primitive or part of a subequation.

    .. note::
        *pseudoelem* must not be a single NEWARG, JUXT, GROUP or TEMPGROUP.
        *pseudoelem*[0][0] must not be a JUXT if *pseudoelem*[0][1] > 0.
        In case you are considering those cases, are you sure there is not a
        better function.

    .. note::
        If *pseudoelem* is a tuple, first element must be the an incomplete
        block and second element an integer specifying how many arguments
        are left free. If integer is 0, it means that the block is already
        valid.

    :param eq: An equation.
    :param idx: Index of current selection.
    :param dir: Current direction of selection.
    :param pseudoelem: A symbol, operator or tuple.
    :return: New selection index and direction.

    Depending on *pseudoelem* and *dir*, behavior is different:

        *   If *pseudoelem* is a symbol or operator with 0 arguments:

            *   If *dir* is 1, insert it to the right of selection.
            *   Elif *dir* is -1, insert it to the left of selection.
            *   Else, substitute selection with the symbol.

        *   If *pseudoelem* is an operator with more than one argument:

            *   If *dir* is 1, insert it to the right of selection with every
                argument set to a NEWARG.
            *   Elif *dir* is -1, insert it to the left of selection with every
                argument set to a NEWARG.
            *   Elif *dir* is 0, substitute selection with the operator with
                every argument set to a NEWARG.
            *   Elif *dir* is 2, substitute selection with the operator with
                every argument set to a NEWARG except the first one, which
                is set to the subequation that was selected.

        *   If *pseudoelem* is a tuple:

            *   Too lazy to document now...
            *   If second element of the tuple is 0, insert....
            *   If *dir* is not 2, append as many NEWARGS as needed to the
                partial black to obtain a valid block and insert it as in the


    Final selection and direction:

        *   If *pelem* is a symbol or op with 0 arguments, select it and set
            dir to 1.
        *   Elif *pelem* is an operator (with some arguments) and dir is in
            (-1, 0, 1), select first argument and set dir to 1.
        *   Else, select the first included NEWARG and set dir to 0.
    """
    # Create subeq to insert
    n_final_newargs = 0
    if isinstance(pseudoelem, str) \
            or (isinstance(pseudoelem, utils.Op) and not pseudoelem.n_args):
        # pseudoelem is symbol or 0-arg op
        subeq = [pseudoelem]
    elif isinstance(pseudoelem, utils.Op) and dir == 2:
        # pseudoelem is an op and first arg will be current selection
        n_final_newargs = pseudoelem.n_args - 1
        sel_end = eqqueries.nextsubeq(eq, idx)
        subeq = [pseudoelem] + eq[idx:sel_end] \
                 + [utils.NEWARG]*n_final_newargs
    elif isinstance(pseudoelem, utils.Op):
        # pseudoelem is an op and every argument will be set to a NEWARG
        n_final_newargs = pseudoelem.n_args
        subeq = [pseudoelem] + [utils.NEWARG] * n_final_newargs
    elif pseudoelem[1] == 0:
        # pseudoelem[0] is a valid block
        subeq = pseudoelem[0]
    elif dir == 2:
        # pseudoelem[0] needs current selection in first unset argument
        n_final_newargs = pseudoelem[1] - 1
        sel_end = eqqueries.nextsubeq(eq, idx)
        subeq = pseudoelem[0] + eq[idx:sel_end] \
                 + [utils.NEWARG] * n_final_newargs
    else:
        # pseudoelem[0] needs only NEWARGs
        n_final_newargs = pseudoelem[1]
        subeq = pseudoelem[0] + [utils.NEWARG]*n_final_newargs

    # _replace_*, _rinsert and _linsert take care of groups and bases **in eq**
    if dir in (0, 2):
        # _replace_integrating does not provide a selection as output, but a
        # flag
        flag = _replace_integrating(eq, idx, subeq)
        # Select correctly the replacement
        if n_final_newargs:
            # Do not consider flag if there are NEWARGs, subeq is not allowed
            # to start with JUXT in that case
            return idx + len(subeq) - n_final_newargs, 0
        # Correct selection depending on flag and presence of group in subeq
        elif not flag or groups.is_some_group(subeq[0]):
            return idx, 1
        else:
            return idx - 1, 1
    # _rinsert and _linsert return always a valid index to select
    elif dir == 1:
        return _rinsert(eq, idx, subeq), 1
    elif dir == -1:
        return _linsert(eq, idx, subeq), 1


def insert_script(eq, idx, dir, is_superscript):
    """Insert a sub or superscript and select it.

    If it already exists, just select it.
    """
    script_idx = scriptops.insert_script(eq, idx, dir, is_superscript)
    if script_idx < 0:
        return -script_idx, 1
    else:
        return script_idx, 0


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

