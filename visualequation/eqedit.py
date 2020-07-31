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
            # Uarg subcase: idx points to the base of a script
            # Convert script operator if needed
            scriptops.update_scriptblock(eq, idx - 1, utils.JUXT)

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
            scriptops.update_scriptblock(eq, idx-1, utils.JUXT)

        eq[idx:idx] = [utils.JUXT] + subeq
        return idx + 1, idx + 1 + len(subeq)
    else:
        # idx points to a citizen but not the last one
        eq[idx:idx] = subeq + [utils.JUXT]
        return idx, idx + len(subeq) + 1


def _rinsert_juxtsubeq(eq, idx, subeq):
    """Insert a subeq which starts by JUXT to the right of a subeq.

    .. note::
        If *idx* points to a citizen and subeq is a JUXT-ublock, citizens of
        *subeq* are integrated as co-citizens of the citizen in *idx*.

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
        # We are inserting a JUXT and subeq has another JUXT:
        # that means that first citizen of subeq has an offset of 2
        return end_idx + 1 + subeq_last_citizen, idx + 1
    else:
        # idx points to a citizen but not the last one
        eq[arg2_idx:arg2_idx] = subeq[:subeq_last_citizen] + [utils.JUXT] \
                                + subeq[subeq_last_citizen:]
        return arg2_idx + subeq_last_citizen + 1, idx


def _linsert_juxtsubeq(eq, idx, subeq):
    """Insert a subeq which starts by JUXT to the left of a subeq.

    .. note::
        If *idx* points to a citizen and subeq is a JUXT-ublock, citizens of
        *subeq* are integrated as co-citizens of the citizen in *idx*.

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
    """Insert a subeq to the right of another subeq.

    .. note::
        If a JUXT-ublock is inserted to the right of a citizen, citizens are
        integrated as co-citizens.

    .. note::

        *   *idx* must not point to a NEWARG.
        *   *subeq* must not be [NEWARG].

    Returned index is:

        *   If *subeq* starts by JUXT, the index in *eq* of last citizen of
            *subeq*.
        *   Else, the first element of *subeq* in *eq*.

    :param eq: A valid equation.
    :param idx: The index of a subeq behind which *usubeq* will be inserted.
    :param subeq: The subequation to insert. It can be any valid subequation.
    :return: The index that should be selected if *idx* points to current sel.
    """
    if subeq[0] == utils.JUXT:
        lcitizen_idx, newidx = _rinsert_juxtsubeq(eq, idx, subeq)
        return lcitizen_idx
    else:
        felem_idx, newidx = _rinsert_nonjuxtsubeq(eq, idx, subeq)
        return felem_idx + 1 if groups.is_group(subeq[0]) else felem_idx


def _safely_dissolve_simplejuxtublock(eq, idx, is_1st_arg_kept,):
    """Disolve JUXT-ublock made up by two citizens.

    Apart from removing the JUXT and the non-kept citizen, it checks if the
    JUXT-ublock was the base of a script op or the arg of a group and correct
    the environment.

    .. note::
        If the JUXT-ublock is a base, scripts can be modified after
        modification of the base.

    :param eq: An equation.
    :param idx: The index of a JUXT ublock of two citizens.
    :param is_1st_arg_kept: True if the first arg of the JUXT-ublock is
    preserved. Else, The second one is preserved.
    :return: Index of kept JUXT arg in *eq* after the call.
    """
    idx1 = idx + 1
    end1 = eqqueries.nextsubeq(eq, idx1)
    idx2 = end1 + 1
    end2 = eqqueries.nextsubeq(eq, idx2)
    kept_arg = eq[idx1:end1] if is_1st_arg_kept else eq[idx2:end2]

    if not idx:
        eq[:] = kept_arg
        return 0

    if eq[idx-1] in (utils.GROUP, utils.TEMPGROUP) \
            or (eq[idx-1] == utils.SOLIDGROUP and len(kept_arg) == 1):
        # No need to use groups.ungroup in this simple case
        eq[idx-1:end2] = kept_arg
        return idx - 1

    eq[idx:end2] = kept_arg
    if scriptops.is_base(eq, idx):
        scriptops.update_scriptblock(eq, idx - 1, eq[idx])
    return idx


def _linsert(eq, idx, subeq):
    """Insert an usubeq to the left of a subequation.

    .. note::
        If a JUXT-ublock is inserted to the left of a citizen, citizens are
        integrated as co-citizens.

    .. note::

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
        return felem_idx + 1 if groups.is_group(subeq[0]) else felem_idx


def _replace_integrating(eq, idx, subeq, subeq_idx=None):
    """Replace subeq starting at *idx* by integrating citizens, if needed.

    If *idx* does not point to a citizen or *subeq* does not start with JUXT,
    it is an ordinary replacement.
    Else, citizen C which start at *idx* is removed and citizens of *subeq*
    are added as co-citizens of the JUXT-ublock in *eq* to which C belonged.

    Return the index in *eq* of primitive with index *subeq_idx* in *subeq*
    after substitution.

    .. note::
        Avoid this function if *idx* points to current selection: Replacement
        should be probably selected in that case and if *subeq* starts by JUXT,
        _replace_tgrouped would be the appropriated function to use.

    .. note::
        To be consistent, prefer _replace_tgrouped if *subeq* is actually a
        group.

    .. note::
        *subeq* must not be [NEWARG]. Consider _remove_selection instead.

    .. note::
        If *idx* points to the argument of a group, the group op index is
        considered instead of *idx* to perform the substitution.

    :param eq: Equation in which the replacement is done.
    :param idx: The index of a subeq which will be replaced.
    :param subeq: Subeq with which subeq starting at :idx: will be replaced.
    :param subeq_idx: The index of a primitive of *subeq*.
    :return: The index in *eq* of primitive with index *subeq_idx* in *subeq*.
    """
    # If selection is the argument of a group, replace the full group
    if idx and groups.is_grouped(eq, idx):
        idx -= 1

    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if subeq[0] != utils.JUXT or juxt_idx < 0 or arg2_idx < idx:
        # subeq does not start with JUXT or idx points to:
        #   1. eq, or
        #   2. An uarg, or
        #   3. A last citizen
        if scriptops.is_base(eq, idx):
            # Subcase: Substitute (v)script base
            scriptops.update_scriptblock(eq, idx - 1, subeq[0])

        end = eqqueries.nextsubeq(eq, idx)
        eq[idx:end] = subeq
        return idx + subeq_idx
    else:
        # idx points to the first argument of a JUXT (terminal or not)
        subeq_last_citizen = eqqueries.last_citizen(subeq, 1)
        eq[idx:arg2_idx] = subeq[1:subeq_last_citizen] + [utils.JUXT] \
                           + subeq[subeq_last_citizen:]
        retval = idx + subeq_idx
        if subeq_idx >= subeq_last_citizen:
            retval += 1
        return retval


def _replace_tgrouped(eq, idx, subeq):
    """Replace subequation as a whole. Precede replacement by a TEMPGROUP
    if needed.

    .. note::
        *subeq* must not be [NEWARG]. Consider _remove_selection instead.

    .. note::
        If *idx* points to the argument of a group, result is equivalent to
        passing *idx*-1.

    Rules:

        *   If *idx* does not point to a citizen or *subeq* does not start
            with JUXT, it is an ordinary replacement.
        *   Else, the citizen in *idx* is replaced by *subeq* "protected"
            with a TEMPGROUP.

    .. note::
        If *subeq*[0] is a group operator, no TEMPGROUP addition is considered.
        Note that, returned value in that case is the index of the group op,
        which should not be selected.

    :param eq: Equation in which the replacement is done.
    :param idx: The index of a subeq which will be replaced.
    :param subeq: Subeq with which subeq starting at *idx* will be replaced.
    :return: The index of the first element of *subeq* in *eq*.
    """
    # If *idx* points to the argument of a group, replace the full group
    if groups.is_grouped(eq, idx):
        idx -= 1

    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0 or subeq[0] != utils.JUXT:
        # idx points to an uarg or eq; or subeq does not start with JUXT
        if scriptops.is_base(eq, idx):
            # Subcase: Substitute script base
            scriptops.update_scriptblock(eq, idx - 1, subeq[0])

        end = eqqueries.nextsubeq(eq, idx)
        eq[idx:end] = subeq
        return idx

    # From this point, subeq starts with JUXT and idx points to a citizen
    if idx < arg2_idx:
        # Subcase: idx points to a citizen which is not a last one
        eq[idx:arg2_idx] = [utils.TEMPGROUP] + subeq
    else:
        # Subcase: idx points to a last citizen
        end = eqqueries.nextsubeq(eq, idx)
        eq[idx:end] = [utils.TEMPGROUP] + subeq
    return idx + 1


def remove_eq(eq):
    eq[:] = [utils.NEWARG]
    return 0, 0


def _remove_selection(eq, idx, dir):
    """Remove selection and return what must be selected. Direction is only
    used to define next selection.

    This function does nothing if *idx* points to a NEWARG.

    .. note::
        It has sense to call this function if:

        *   Backward delete with dir == 1.
        *   Forward delete with dir in (-1, 0).


    .. note::

        *   *idx* must not point to a NEWARG.
        *   *dir* must be in (-1, 0, 1). 2 is not a valid value.

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

    :param eq: An equation.
    :param idx: Index of current selection.
    :param dir: Direction of selection. Only values (-1, 0, 1). Must not be 2.
    """
    # Correct index if the argument of a group is selected
    if groups.is_grouped(eq, idx):
        idx -= 1

    if not idx:
        # Case: remove whole eq
        return remove_eq(eq)

    juxt_idx, otherarg = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0:
        # Case: Remove uarg
        if scriptops.is_base(eq, idx):
            # Uarg subcase: idx points to the base of a script
            # Convert (v)script operator if needed
            scriptops.update_scriptblock(eq, idx - 1, utils.NEWARG)

        end = eqqueries.nextsubeq(eq, idx)
        eq[idx:end] = [utils.NEWARG]
        return idx, 0

    # From this point, we know idx points to citizen
    if otherarg < idx:
        # Case: Remove last citizen
        if eqqueries.is_parent_juxt(eq, juxt_idx):
            return _safely_dissolve_simplejuxtublock(eq, juxt_idx, True)

        end = eqqueries.nextsubeq(eq, juxt_idx)
        eq[juxt_idx:end] = eq[otherarg:idx]
        return juxt_idx, 1 if dir else 0

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


def flat_block(eq, idx, dir=1):
    """Flat selection by removing leading op and joining args in a JUXT-ublock.
    If selection is the arg of a SOLIDGROUP or GROUP, the group op is
    substituted by a TEMPGROUP or deleted.

    Return final selection and direction.


    .. note::
        It is expected that *idx* points to current selection. In particular,
        *idx* must not point to a group op.

    .. note::
        (To guarantee that a call to this function modifies the equation) it
        is required that *idx* must NOT point to:

            *   A symbol, or
            *   Op with no args, or
            *   A JUXT-ublock which is not the arg of a GROUP or SOLIDGROUP.
        You can use is_flat_block_allowed to check those conditions.


    Rules:

        *   If selected ublock is a JUXT-ublock (protected by a group), change
            the group to a TEMPGROUP.
        *   Elif selected ublock is a (non-JUXT-ublock) arg of a SOLIDGROUP,
            delete the SOLIDGROUP.
        *   Elif leading op of selected ublock only has NEWARG uargs, delete
            selection and select another subequation of *eq* according to the
            rules of _remove_selection.
        *   Elif selected ublock has one uarg (different than NEWARG), replace
            selection by that uarg and select it with the same direction as
            originally. If originally selected ublock was a citizen, do the
            replacement with a temporary group if uarg is a JUXT-ublock.
        *   Else, join every non-NEWARG uarg of selected ublock in a
            JUXT-ublock and replace selection by that JUXT-ublock. In the case
            that some uargs were JUXT-ublocks, integrate their citizens as
            co-citizens of the created JUXT-ublock, in the expected order.
            Select the JUXT-ublock without modifying original direction. If
            originally selected ublock was a citizen, do the replacement with
            a temporary group.
    """
    if eq[idx] == utils.JUXT:
        # It is required that if idx points to a JUXT it is preceded by a group
        eq[idx-1] = utils.TEMPGROUP
        return idx, dir

    if groups.is_sgrouped(eq, idx):
        return groups.ungroup(eq, idx), dir

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

    # It is OK if some of the vargs are groups or solid groups.
    subeq_c = simpleeqcreator.SimpleEqCreator()
    for varg in vargs:
        subeq_c.extend(varg)
    new_idx = _replace_tgrouped(eq, idx, subeq_c.get_eq())
    return new_idx + 1 if groups.is_group(eq[new_idx]) else new_idx, dir


def is_flat_block_allowed(eq, idx):
    return not isinstance(eq[idx], str) and eq[idx].n_args != 0 \
            and (eq[idx] != utils.JUXT or groups.is_pgrouped(eq, idx)
                 or groups.is_sgrouped(eq, idx))


def flat_external_block(eq, idx, dir=1, remove_mode=0):
    """Core function to flat the least external block of selection
    (essentially remove the leading operator and join uargs in JUXT-ublock).
    It also ungroups in some circunstances.

    Parameter *remove_mode* is expected to be:

        *   If the call to this function is the consequence of deleting, 1.
        *   If the call to this function is the consequence of suppression, -1.
        *   Otherwise (special key-combination), 0.

    .. note::
        Subequation pointed by *idx* cannot be:

            *   The whole equation, or
            *   A citizen if its JUXT-ublock is the whole equation, or
            *   A group argument if the group-block is a citizen of the
                whole equation.
        You can use is_flat_external_block_allowed to verify that those
        conditions are satisfied.
        Note that this operation has no sense in those cases and you should
        leave equation unmodified even if the user asked explicitly to perform
        the operation.

    .. note::
        If selection is the argument of a group, it is guaranteed that the
        group block will still be present and unmodified in the final equation
        and its argument still selected. Note that in that case, rules are
        applied as if the whole group block were virtually selected (which is
        not allowed by selection rules) instead of its argument.

    Rules:

        If selection is:

            *   A citizen of a grouped JUXT-ublock, or
            *   The argument of a group which block is the citizen of a
                grouped JUXT-ublock,
        then, the JUXT-ublock is ungrouped.

        Elif selection is:

            *   The argument of a group such that the group-block is an uarg of
                an operator O, or
            *   An uarg which op O is not a group,
        then, do the following (selection rules explained at the end):

            *   If every argument of O is a NEWARG, remove the block defined by
                O according to the rules of _remove_selection as if the whole
                block was selected with direction equal to *remove_mode*.
                (This case does not apply if selection is a group argument).
            *   Elif only one argument of O is not a NEWARG and it is also
                different than a JUXT-ublock, replace block defined by O with
                that argument.
            *   Elif only one argument of O is not a NEWARG and it is a
                JUXT-ublock, replace the block defined by O with the mentioned
                JUXT-ublock. Read section "final selection" to know more about
                the replacement.
            *   Else (more than one non-NEWARG args), create a JUXT-ublock
                whose citizens are:

                    *   Every non-NEWARG argument which is not a JUXT-ublock,
                        and
                    *   Every citizen of any argument which is a JUXT-ublock.

                Relative order of citizens will be the same in which they
                appear in the equation. Then:

                    *   If block defined by O is not a citizen, replace O by
                        the JUXT-ublock.
                    *   Else (O is a citizen), replace O with the citizens of
                        the created JUXT-ublock in such a way that its citizens
                        are co-citizens of the JUXT-ublock to which O belonged.
                        Read section "final selection" to know more about the
                        replacement.

            Final selection for this case:

                *   If every argument of O is a NEWARG, selection is decided by
                    _remove_selection's rules under conditions stated above.
                *   If selection is not a NEWARG, final selection will be the
                    original one and with the same direction. In the case that
                    selection is a non-groped JUXT-ublock, protect it with a
                    TEMPGROUP in the case that block defined by O is a citizen
                    or if O has more non-NEWARG arguments.
                *   Else (a NEWARG is selected and O has at least one
                    non-NEWARG arg), *remove_mode* decides the selection:

                        *   If remove_mode == 0 (NEUTRAL mode):

                            *   If there is at least one non-NEWARG argument to
                                the right, select the first one and set dir=-1
                                ("neither you nor I" strategy).
                            *   Else select the first non-NEWARG to the left
                                and set dir=1.

                        *   If remove_mode == 1 (FORWARD mode):

                            *   If there is at least one non-NEWARG argument to
                                the right, select the first one and set dir=1.
                            *   Else, select the first non-NEWARG to the left
                                and set dir=1.

                        *   If remove_mode == -1 (BACKWARD mode):

                            *   If there is at least one non-NEWARG argument to
                                the left, select the first one and set dir=1.
                            *   Else, select the first non-NEWARG to the right
                                and set dir=-1.

        Elif selection is:

            *   The argument of a group such that the group-block is a citizen
                of a (non-grouped) JUXT-ublock which is the uarg of an
                operator O, or
            *   A citizen of a (non-grouped) JUXT-ublock which is the uarg of
                an operator O,
        (note that O is guaranteed to exist by the conditions required to call
        this function) then, do the following (selection rules explained at the
        end):

            *   If O does not have other non-NEWARG arguments (a citizen is
                always a non-NEWARG argument):

                *   If block defined by O is not a citizen (an uarg or the
                    whole eq), replace block defined by O with the JUXT-ublock
                    to which selection belongs.
                *   Else, remove block defined by O and integrate selection and
                    its co-citizens as co-citizens of the JUXT-ublock to which
                    block defined by O belonged.

            *   Else (O has other non-NEWARG arguments), integrate selection
                and other args of O as citizens of a JUXT-ublock with the same
                rules than in the similar case explained above.

            Final selection for this case:

                Leave selected original selection and with te same direction.
                Note that *remove_mode* is never used in this case.
    """
    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, idx)

    if juxt_idx > 0 and groups.is_pgrouped(eq, juxt_idx):
        # Case: Selection is a citizen of a grouped JUXT-ublock
        return groups.ungroup(eq, juxt_idx, idx), dir

    if groups.is_grouped(eq, idx):
        parent_juxt_idx = eqqueries.parent_juxt(eq, idx-1)
        if parent_juxt_idx >= 0 and groups.is_pgrouped(eq, parent_juxt_idx):
            # Case: Selection is the arg of a group which block is the citizen
            # of a grouped JUXT-ublock
            return groups.ungroup(eq, parent_juxt_idx, idx), dir


    # Set variables that define rest of function's casuistic:
    #   The case in which a citizen is selected is managed by selecting its
    #   JUXT-ublock and setting and offset value.
    #   "Selected argument" below will refer to the JUXT-ublock if this
    #   case applies
    arg_idx = idx
    offset = 0
    if juxt_idx >= 0:
        # Current selection is a citizen
        # (and it is assumed that the JUXT-ublock is not the whole equation)
        parent_juxt = eqqueries.parent_juxt(eq, idx)
        arg_idx = parent_juxt
        offset = parent_juxt - idx

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
    # Note!: Returned value has been recoded without testing, there can be bugs
    return _replace_integrating(eq, op_idx, subeq_c.get_eq(),
                                subeq_c.get_idx(offset, sel_ridx)), dir


def is_flat_external_block_allowed(eq, idx):
    """Return whether flat_external_block is allowed to be called."""
    if not idx:
        return False

    if groups.is_group(eq[idx-1]):
        idx -= 1

    juxt_idx, ignored = eqqueries.other_juxt_arg(eq, idx)
    # Condition is: Not a citizen or citizen of JUXT-ublock != eq
    return juxt_idx != 0


def _remove_arg(eq, idx, dir, remove_mode=1):
    """Remove an argument by flatting the operator or downgrading/removing a
    script op.

    .. note::
        Usually you would want to use this function if the arg is a NEWARG,
        but that is not a requirement.

    Parameter *remove_mode* is expected to be:

        *   1 for forward remove.
        *   -1 for backward remove.

     Rules:

        *   If *idx* points to the argument of a script operator which is
            not the base, downgrade the script operator if there are more
            scripts or remove it if it was the only script.
        *   Else, apply rules of flat_external_block.
    """
    # Any group (including solid groups) should also be replaced completely
    if groups.is_grouped(eq, idx):
        idx -= 1

    op_idx, arg_pos = eqqueries.whosearg_filter_type(eq, idx)

    # Flat operator if not a script
    if op_idx < 0 \
            or eq[op_idx] not in scriptops.SCRIPT_OP_TYPES \
            or scriptops.is_base(eq, idx):
        return flat_external_block(eq, idx, dir, remove_mode)

    # Remove
    return scriptops.remove_script(eq, idx), 1


def _rremove(eq, idx):
    """Remove "to the right" of selection and return new valid index.

    .. note::
        Selection must NOT be the whole equation so it is provided that this
        function always modify the equation.

    Rules:

        *   If selection has a co-citizen to the right, remove it.
        *   Else, flat the least external operator.

    Selection and direction are not modified.
    """
    juxt_idx, otherarg = eqqueries.other_juxt_arg(eq, idx)
    if juxt_idx < 0 or otherarg < idx:
        # Cases: selection is an uarg or a last citizen
        return flat_external_block(eq, idx, 1, -1)[0]
    elif eq[otherarg] == utils.JUXT:
        # Case: selection is a citizen before the last but one
        end = eqqueries.nextsubeq(eq, otherarg + 1)
        eq[otherarg:end] = []
        return idx

    # From this point, selection is a last but one co-citizen
    is_juxtublock_dissolved = eqqueries.is_parent_juxt(eq, juxt_idx)
    if is_juxtublock_dissolved:
        # Case: JUXT-ublock only has two citizens
        return _safely_dissolve_simplejuxtublock(eq, juxt_idx, True)

    end = eqqueries.nextsubeq(eq, otherarg)
    eq[juxt_idx:end] = eq[idx:otherarg]
    return idx - 1


def _lremove(eq, idx):
    """Remove "to the left" of selection and return a valid index.

    .. note::
        Selection must NOT be the whole equation so it is provided that this
        function always modify the equation.

    Rules:

        *   If selection has a co-citizen to the left, remove it.
        *   Else, flat the least external operator.

    Selection and direction are not modified.
    """

    lcocitizen_idx = eqqueries.cocitizen(eq, idx, forward=False)
    if lcocitizen_idx < 0:
        # Case: selection is not a citizen or it is a first citizen
        return flat_external_block(eq, idx, -1, 1)
    elif eq[idx-1] == utils.JUXT:
        # Case: selection is a non-last, non-first citizen
        eq[lcocitizen_idx-1:idx-1] = []
        return lcocitizen_idx

    # From this point, selection is a last citizen
    if eqqueries.is_parent_juxt(eq, lcocitizen_idx-1):
        return _safely_dissolve_simplejuxtublock(eq, lcocitizen_idx-1, False)

    eq[lcocitizen_idx-1:idx] = []
    return lcocitizen_idx - 1


def insert(eq, idx, dir, pseudoelem):
    """Insert/replace a subequation from a primitive or part of a subequation.

    .. note::
        If *pseudoelem* is a tuple, first element must be a complete or
        incomplete block and the second element an integer specifying how many
        arguments are left free. If that integer is 0, it means that the block
        is already complete.

    .. note::
        *pseudoelem* must not be a single NEWARG, JUXT op or group op.
        *pseudoelem*[0][0] must not be a JUXT if *pseudoelem*[1] > 0.
        In case you are considering those cases, are you sure there is not a
        better function?

    :param eq: An equation.
    :param idx: Index of current selection.
    :param dir: Current direction of selection.
    :param pseudoelem: A symbol, operator or tuple as indicated in the first
    note.
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
                first arg set to selected subequation and the rest of args, if
                any, set to NEWARGs.

        *   If *pseudoelem* is a tuple:

            *   If *pseudoelem*[1] == 0, replace *pseudoelem*[0] grouped.
            *   Else, equivalent to consider *pseudoelem*[0] an Op with
                n_args == *pseudoelem*[1].

    Final selection and direction:

        *   If *psudoelem* is a symbol, op with 0 arguments or tuple with
            *psudoelem*[1] == 0, select it and set dir to 1.
        *   Elif dir is in (-1, 0, 1), select first NEWARG and set dir to 0.
        *   Elif there is at least a NEWARG, select it and set dir to 0.
        *   Else, select introduced subequation and set dir to 1.
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
        subeq = [pseudoelem] + [utils.NEWARG]*n_final_newargs
    elif pseudoelem[1] == 0:
        # pseudoelem[0] is a valid block
        subeq = pseudoelem[0]
    elif dir == 2:
        # pseudoelem[0] needs current selection in first unset argument
        n_final_newargs = pseudoelem[1] - 1
        sel_end = eqqueries.nextsubeq(eq, idx)
        subeq = pseudoelem[0] + eq[idx:sel_end] \
                 + [utils.NEWARG]*n_final_newargs
    else:
        # pseudoelem[0] needs only NEWARGs
        n_final_newargs = pseudoelem[1]
        subeq = pseudoelem[0] + [utils.NEWARG]*n_final_newargs

    # _replace_*, _rinsert and _linsert take care of groups and script ops
    # **only in eq**, not in the passed subeq.
    if dir in (0, 2):
        subeq_idx = _replace_tgrouped(eq, idx, subeq)
        # Select correctly the replacement
        if n_final_newargs:
            # subeq cannot be a JUXT-ublock if n_final_newargs > 0
            return subeq_idx + len(subeq) - n_final_newargs, 0
        elif groups.is_group(subeq[0]):
            # If subeq had a group leading op, select its argument
            return subeq_idx + 1, 1
        else:
            return subeq_idx, 1
    # _rinsert and _linsert return always a valid index to select
    elif dir == 1:
        return _rinsert(eq, idx, subeq), 1
    elif dir == -1:
        return _linsert(eq, idx, subeq), 1


def insert_script(eq, idx, dir, is_superscript):
    """Insert a script and select it.

    If it already exists, just select it.

    :param eq: An equation.
    :param idx: Index in *eq* of the base of the script.
    """
    script_idx = scriptops.insert_script(eq, idx, dir, is_superscript)
    return script_idx, 0 if script_idx >= 0 else -script_idx, 1


def delete(eq, idx, dir, forward=False):
    """Remove a subequation according to selection and removal mode and return
    next selection.

    .. note::
        In some cases this function does not modify the equation.

    :param eq: An equation.
    :param idx: The index of currently selected subeq.
    :param dir: Current direction (-1, 0, 1, or 2).
    :param forward: A boolean indicating the remove direction.
    """
    if not idx:
        if (not dir and forward) or (dir == 1 and not forward) \
                or (dir == -1 and forward):
            return remove_eq(eq)
        return idx, dir

    if eq[idx] == utils.NEWARG:
        # Downgrade script op or flat least external operator
        return _remove_arg(eq, idx, dir, -1 if forward else 1)

    if (dir == 1 and not forward) or (dir == -1 and forward):
        # Remove current selection and set a nice selection
        return _remove_selection(eq, idx, dir)

    if dir == 1:
        # Remove to the right
        return _rremove(eq, idx), dir

    if dir == -1:
        # Remove to the left
        return _lremove(eq, idx), dir


def swap_subeqs(eq, idx1, idx2):
    """Exchange two non-overlapping subequations.

    The index of the first subequation after the function call, occupying the
    position of the second subeq before the call, is returned.

    .. note::
        No direction is considered nor returned.

    .. note::
        If subequation pointed by idx2 is the argument of a TEMPGROUP, that
        TEMPGROUP is removed.
    """
    end2 = eqqueries.nextsubeq(eq, idx2)
    end1 = eqqueries.nextsubeq(eq, idx1)

    temp = eq[idx2:end2]
    eq[idx2:end2] = eq[idx1:end1]
    eq[idx1:end1] = temp
    if eq[idx1]
    return idx2 + (end2 - idx2) - (end1 - idx1)


def transpose_neighbours(eq, idx, dir):
    w2_idx = idx


    w1_idx = eqqueries.prev_neighbour(eq, idx)
    if w1_idx > 0:
        transpose_helper(self, w1_idx)

