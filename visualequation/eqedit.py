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

import copy
import functools

from . import eqqueries
#from . import groups
#from . import scriptops
#from . import simpleeqcreator
from .symbols import utils


"""
An interface to safely edit an equation.
"""


def debuginit(fun):
    """Test a method."""

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        print("**** START DEBUGGING (Initial object) ****")

        fun(self, *args, **kwargs)
        print("\nself.eq: " + repr(self.eq))
        print("\nself.idx: " + repr(self.idx) + "\tdir: " + repr(self.dir))
        print("**** END DEBUGGING ****")

    return wrapper


def debug(fun):
    """Test a method."""

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        print("**** START DEBUGGING ****")
        print("Method: " + repr(fun))
        # Debugging eq and idx
        msg = eqqueries.check(self.idx, self.eq, False)
        if msg != "OK!":
            print("------>", msg)
            return
        else:
            print("Note: self.eq and self.idx were valid before function "
                  "call. Calling now...")

        retval = fun(self, *args, **kwargs)
        print("\nself.eq: " + repr(self.eq))
        print("\nself.idx: " + repr(self.idx) + "\tdir: " + repr(self.dir))
        print("\nReturn: " + repr(retval))
        print("**** END DEBUGGING ****")

    return wrapper


class EditableEq:
    @debuginit
    def __init__(self, eq0=None, sel_idx0=None, dir0=None, do_overwrite=False):
        self.eq = copy.deepcopy(eq0) if eq0 is not None else utils.void()
        self.idx = sel_idx0[:] if sel_idx0 is not None else []
        if dir0 is not None:
            self.dir = dir0
        elif eqqueries.get(self.idx, self.eq) == utils.void():
            self.dir = utils.VDIR
        else:
            self.dir = utils.RDIR
        self.ovrwrt = do_overwrite if do_overwrite is not None else False

    def _set(self, elem, idx=None):
        """Replace selection. If replacement is a JUXT-block, it will be
        replaced as a whole (TJUXTs are used only to build selections).

        If *idx* is not specified, it means current selection.

        .. note::
            It is a "hard" replacement, meaning that it does not check for
            supeqs which are non-usubeqs.
        """
        if idx is None:
            idx = self.idx

        if not idx:
            self.eq[:] = copy.deepcopy(elem)
            return

        eqref = self.eq
        for lev, pos in enumerate(idx):
            if lev == len(idx) - 1:
                break
            eqref = eqref[pos]

        eqref[idx[-1]][:] = copy.deepcopy(elem)

    @debug
    def _rinsert(self, subeq):
        """Insert a subeq to the right. If subeq is a JUXT-block, a TJUXT-block
        is inserted instead.

        Return the index of inserted subeq.
        """
        sel = eqqueries.get(self.idx, self.eq)
        sup = eqqueries.supeq(self.idx, self.eq, True)
        s_new = subeq if subeq[0] != utils.JUXT else [utils.TJUXT] + subeq[1:]
        if sup != -2 and sup[0] == utils.JUXT:
            # Case: selection is a juxted
            # Note: Checked in doc that insertions after len(L)-1 are allowed
            sup.insert(self.idx[-1] + 1, s_new)
            return self.idx[:-1] + [self.idx[-1] + 1]
        elif sel[0] == utils.JUXT:
            # Case: selection is a juxt-block and is not a juxted
            sel.append(s_new)
            return self.idx + [len(sel) - 1]
        else:
            # Case: selection is a non-juxt-block and is not a juxted
            sel[:] = [utils.JUXT] + [sel[:]] + [s_new]
            return self.idx + [2]

    @debug
    def _linsert(self, subeq):
        """Insert a subeq to the left. If subeq is a JUXT-block, a TJUXT-block
        is inserted instead.

        Return the index of inserted subeq
        """
        sel = eqqueries.get(self.idx, self.eq)
        sup = eqqueries.supeq(self.idx, self.eq, True)
        s_new = subeq if subeq[0] != utils.JUXT else [utils.TJUXT] + subeq[1:]
        if sup != -2 and sup[0] == utils.JUXT:
            # Case: selection is a juxted
            # Note: Checked in doc that insertions after len(L)-1 are allowed
            sup.insert(self.idx[-1], s_new)
            return self.idx[:]
        elif sel[0] == utils.JUXT:
            # Case: selection is a juxt-block and is not a juxted
            sel[1:] = s_new + sel[1:]
            return self.idx + [1]
        else:
            # Case: selection is a non-juxt-block and is not a juxted
            sel[:] = [utils.JUXT] + [s_new] + [sel[:]]
            return self.idx + [1]

    @debug
    def _replace_integrating(self, idx, subeq):
        """Replace selection or biggest supeq having selection as urepr if
        that exists (in any other case, replace pointed subeq).

        .. note::
            Do NOT use this method by pointing the urepr of the whole eq.
            To replace current selection you should use _replace.

        .. note::
            Passed index will be the index of whole replacement or first
            integrated juxted.
        """
        repl_idx = eqqueries.biggest_supeq_with_urepr(idx, self.eq)
        if not isinstance(repl_idx, list):
            repl_idx = idx[:]
        sup = eqqueries.supeq(repl_idx, self.eq, True)
        if not eqqueries.isb(subeq) or not eqqueries.isjuxtblock(subeq) \
                or sup[0] != utils.JUXT:
            sup[repl_idx[-1]][:] = copy.deepcopy(subeq)
            return repl_idx

        # From this point it is assured that some juxteds will be integrated
        sup[:] = sup[:repl_idx[-1]] + subeq[1:] + sup[repl_idx[-1]+1:]
        return repl_idx

    @debug
    def replace(self, subeq):
        """Replace selection or biggest supeq having selection as urepr if
        that exists (in any other case, replace pointed subeq).

        It sets index to the urepr of replacement.

        .. note::
            It expects current selection to be an usubeq.
        """
        repl_idx = eqqueries.biggest_supeq_with_urepr(self.idx, self.eq)
        if not isinstance(repl_idx, list):
            repl_idx = self.idx[:]
        self._set(subeq, repl_idx)
        self.idx[:] = repl_idx + eqqueries.urepr([], subeq)
        if subeq == utils.void() and not self.ovrwrt:
            self.dir = utils.VDIR

    def remove_eq(self):
        self._set(utils.void(), [])
        self.idx[:] = []
        if not self.ovrwrt:
            self.dir = utils.VDIR

    def _clever_vanish(self):
        """Remove selection or biggest supeq having selection as urepr if
        that exists (in any other case, replace pointed subeq). It does not
        remove any visible outlop structure, but yes filters and juxts when
        only one juxted is left.

        It sets idx and dir.

        .. note::
            It must be called only to make disappear current selection.
            Expected use is:

                *   Backward delete with dir == 1.
                *   Forward delete with dir in (-1, 0).

        .. note:
            Final selection is intentionally not documented here. Read the
            source code, that is intended to be clear.
        """
        # Adjust the replacement index
        repl_idx = eqqueries.biggest_supeq_with_urepr(self.idx, self.eq)
        if not isinstance(repl_idx, list):
            repl_idx = self.idx[:]

        if not repl_idx:
            # Case: remove whole eq
            self.remove_eq()

        sup = eqqueries.supeq(repl_idx, self.eq, True)
        if not eqqueries.isjuxtblock(sup):
            # Case: Remove non-juxted subeq

        juxt_idx, otherarg = eqqueries.other_juxt_arg(eq, idx)
        if juxt_idx < 0:

            if scriptops.is_base(eq, idx):
                # Uarg subcase: idx points to the base of a script
                # Convert (v)script operator if needed
                scriptops.update_scriptblock(eq, idx - 1, utils.VOID)

            end = eqqueries.nextsubeq(eq, idx)
            eq[idx:end] = [utils.VOID]
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
            scriptops.update_scriptblock(eq, idx - 1, utils.VOID)

        end = eqqueries.nextsubeq(eq, idx)
        eq[idx:end] = [utils.VOID]
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
        if eq[arg_idx] != utils.VOID:
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
        if eq[arg_idx] != utils.VOID:
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
                + [utils.VOID] * n_final_newargs
    elif isinstance(pseudoelem, utils.Op):
        # pseudoelem is an op and every argument will be set to a NEWARG
        n_final_newargs = pseudoelem.n_args
        subeq = [pseudoelem] + [utils.VOID] * n_final_newargs
    elif pseudoelem[1] == 0:
        # pseudoelem[0] is a valid block
        subeq = pseudoelem[0]
    elif dir == 2:
        # pseudoelem[0] needs current selection in first unset argument
        n_final_newargs = pseudoelem[1] - 1
        sel_end = eqqueries.nextsubeq(eq, idx)
        subeq = pseudoelem[0] + eq[idx:sel_end] \
                + [utils.VOID] * n_final_newargs
    else:
        # pseudoelem[0] needs only NEWARGs
        n_final_newargs = pseudoelem[1]
        subeq = pseudoelem[0] + [utils.VOID] * n_final_newargs

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

    if eq[idx] == utils.VOID:
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
    if eq[idx1]:
        pass
    return idx2 + (end2 - idx2) - (end1 - idx1)


def transpose_neighbours(eq, idx, dir):
    w2_idx = idx


    w1_idx = eqqueries.prev_neighbour(eq, idx)
    if w1_idx > 0:
        transpose_helper(self, w1_idx)

