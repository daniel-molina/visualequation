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

from copy import deepcopy
import functools

from . import eqqueries
from . import scriptops
from . import simpleeqcreator
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
    """Class to edit an equation.

    Philosophy about JUXTs:
        By default, any operation will integrate juxteds of a juxt-block unless
        it is protected by a GOP. TJUXTs are only used to temporally select a
        several juxteds of a JUXT-block. A JUXT-block will only be used as a
        juxted under specific circumstances (mainly under user request).

    Implementation note:
        This is a large class and it is easy to get lost. Let's try to respect
        the following conventions.

            *   Methods starting with underscore (_), apart from being used
                only by other methods of this class, they should not modify
                other attributes than self.eq. Instead, they can return
                useful information or the self.idx and self.dir that should be
                set under a typical use of that method.

            *   Methods not starting with underscore are intended to be safe
                to call independently of the input. They should set any
                property of the class so the method performs an operation
                completely.

            *   A method which acts on the indicated index if:

                *   Index points to a non-usubeq, or
                *   Index points to a usubeq which 1-level supeq is a usubeq.
                and, on the contrary, acts over the biggest supeq having
                pointed index as urepr, is known as a 'supeq-checker'.

            *   A method which assures that returned or set index points always
                to an usubeq is known as a 'final-idx-checker'.

            *   A method which assures that operation will not change a base
                without correcting the correspondent script op is known as a
                'base-checker'.
    """
    @debuginit
    def __init__(self, eq0=None, sel_idx0=None, dir0=None, do_overwrite=False):
        # Equation. It must be assured that any reference to self.eq will be
        # always valid.
        self.eq = deepcopy(eq0) if eq0 is not None else utils.void()
        # The index of the *user subeq* (usubeq) where public methods will
        # act. It is typically the selected subeq.
        self.idx = sel_idx0[:] if sel_idx0 is not None else []
        # Typically the direction of the selection. It modifies methods
        # behavior.
        if dir0 is not None:
            self.dir = dir0
        elif eqqueries.get(self.idx, self.eq) == utils.void():
            self.dir = utils.VDIR
        else:
            self.dir = utils.RDIR
        # Another modifier for the methods: the overwrite mode.
        self.ovrwrt = do_overwrite if do_overwrite is not None else False

    def _set(self, elem, idx=None):
        """A 'hard' replacement. If replacement is a JUXT-block, it will be
        replaced as a whole.

            *   Not a supeq-checker
            *   Not a final-idx-checker
            *   Not a base-checker

        If *idx* is not specified, it is equivalent to pass self.idx.

        It does not return because replacement is always done in *idx*.
        """
        if idx is None:
            idx = self.idx

        # Replace whole eq
        if not idx:
            self.eq[:] = deepcopy(elem)
            return

        # Find strict subeq of eq to replace (not that easy in python)
        eqref = self.eq
        for lev, pos in enumerate(idx):
            if lev == len(idx) - 1:
                break
            eqref = eqref[pos]

        # Replace
        eqref[idx[-1]][:] = deepcopy(elem)

    def _get_safe_dir(self, dirflag=0, subeq=None, idx=None):
        """Set direction respecting overwrite mode and subeq being selected.

            *   Not a supeq-checker
            *   Not final-idx-checker
            *   base-checker not applicable.

        If *dirflag* is:

            *    1, right.
            *   -1, left.
            *    5, self.dir unless that is utils.VDIR; in that case, right.
            *   -5, self.dir unless that is utils.VDIR; in that case, left.
            *    0, you trust that self.ovrwrt is True or *subeq* is VOID-like.

        If *subeq* is:

            *   None, it uses subeq pointed by idx to check whether it is a
                VOID.
            *   0, it is equivalent to pass utils.void().
            *   ow., it uses passed subequation to consider returned direction.

        If *idx* is:

            *   None, self.idx is used instead.
            *   ow., subeq pointed by *idx is considered instead of *subeq*. To
                use this parameter, *subeq* must be None.
        """
        if self.ovrwrt:
            return utils.ODIR
        if subeq == 0:
            return utils.VDIR
        s_idx = self.idx if idx is None else idx
        s = eqqueries.get(s_idx, self.eq) if subeq is None else subeq
        if s == utils.void():
            return utils.VDIR
        if dirflag == 1:
            return utils.RDIR
        if dirflag == -1:
            return utils.LDIR
        if dirflag == 5:
            return self.dir if self.dir != utils.VDIR else utils.RDIR
        if dirflag == -5:
            return self.dir if self.dir != utils.VDIR else utils.LDIR

    def _get_biggest_subeq_same_urepr(self, idx=None):
        """If *idx* points to a usubeq U and it has supeq which urepr is US,
        return the index of the biggest supeq with that property. If *idx*
        points to non-usubeq subeq or mentioned supeq does not exist, *idx*
        is returned.

        This function is used by those methods with the tag: supeq-checker.

        Case *idx* being None is equivalent to pass self.idx.
        """
        usubeq_idx = self.idx[:] if idx is None else idx[:]
        new_idx = eqqueries.biggest_supeq_with_urepr(usubeq_idx, self.eq)
        if not isinstance(new_idx, list):
            return usubeq_idx
        return new_idx

    def _condtly_correct_scriptop(self, newbase, idx=None, supeq=None):
        """Correct a script operator if idx points to a base and it is needed.

        .. note::
            Calling this function never harms. It only acts if necessary.

        This function is used by those methods with the tag: base-checker.


        It does no return because replacement, if it is done, does not change
        eq structure.

        :param newbase: The new block which will be used in *idx*.
        :param idx: Index of the element which may be a base. None -> self.idx.
        :param supeq: (Optional) If you know the supeq of *idx*, you can pass
        it.
        """
        base_idx = self.idx if idx is None else idx
        sup = eqqueries.supeq(base_idx, self.eq, True) \
            if supeq is None else supeq
        if sup != -2 and base_idx[-1] == 1 and scriptops.is_scriptop(sup[0]):
            scriptops.update_scriptblock(newbase, sup)

    @debug
    def _rinsert(self, subeq):
        """Insert a subeq to the right. If subeq is a JUXT-block, a TJUXT-block
        is inserted instead.

        *   Not a supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        It has sense to call this function when inserting and:

            *   Non-overwrite mode is used, and
            *   Direction is RDIR.

        It returns the index of insert subeq.
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
            self._condtly_correct_scriptop(sel, None, sup)
            return self.idx + [2]

    @debug
    def _linsert(self, subeq):
        """Insert a subeq to the left. If subeq is a JUXT-block, a TJUXT-block
        is inserted instead.

        *   Not a supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        It has sense to call this function when inserting and:

            *   Non-overwrite mode is used, and
            *   Direction is LDIR.

        It returns the index of inserted subeq.
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
            if sup != -2 and self.idx[-1] == 1 \
                    and scriptops.is_scriptop(sup[0]):
                scriptops.update_scriptblock(sel, sup)
            return self.idx + [1]

    @debug
    def _replace_integrating(self, s_repl, idx=None):
        """Replace a subequation integrating juxteds if appropriated.

        *   supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        .. note::
            *   Do NOT use this method by pointing the urepr of the whole eq.
            *   To replace current selection you should use _replace.

        If *s_repl* is a juxt-block JB and actual subeq being replaced is a
        juxted of a juxt-block EJB, juxteds of JB are integrated as juxteds of
        EJB.

        If *idx* is None that is equivalent to pass self.idx. Note however that
        this method should not be used to replace actual selection.

        Return the index of subeq where replacement was finally done (*idx*
        or supeq's).
        """
        # Choose correct subeq to replace
        referred_idx = self.idx if idx is None else idx
        repl_idx = self._get_biggest_subeq_same_urepr(referred_idx)

        # This method assumes there is a supeq
        sup = eqqueries.supeq(repl_idx, self.eq, True)
        if not eqqueries.isb(s_repl) or not eqqueries.isjuxtblock(s_repl) \
                or sup[0] != utils.JUXT:
            # Case: No juxteds are integrated
            self._condtly_correct_scriptop(s_repl, repl_idx, sup)
            sup[repl_idx[-1]][:] = deepcopy(s_repl)
            return repl_idx

        # Case: some juxteds will be integrated
        sup[:] = sup[:repl_idx[-1]] + s_repl[1:] + sup[repl_idx[-1] + 1:]
        return repl_idx

    @debug
    def _replace(self, subeq, idx=None):
        """Replace pointed subeq or a supeq.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        If *idx* is None that is equivalent to pass self.idx.

        Return expected index to be selected.

        It should be called in overwrite mode or when inserting if selection
        is a VOID.
        """
        repl_idx = self._get_biggest_subeq_same_urepr(idx)

        # Correct script op if needed in the case that repl_idx points to a
        # base
        self._condtly_correct_scriptop(subeq, repl_idx)

        # Replace
        self._set(subeq, repl_idx)

        # Select the urepr of replacement
        return repl_idx + eqqueries.urepr([], subeq)

    def _empty(self, idx=None):
        """Replace pointed subeq or supeq by a VOID.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        It returns the index of inserted VOID.
        """
        return self._replace(utils.void(), idx)

    def remove_eq(self):
        """Replace the whole eq by a VOID."""
        self.idx[:] = []
        self._set(utils.void())
        self.dir = self._get_safe_dir(0, 0)

    @debug
    def _vanish_juxted(self, idx=None):
        """Vanish "selected" juxted. It removes the juxt op if only one juxted
        is left.

        *   Not a supeq-checker
        *   final-idx-checker
        *   base-checker

        .. note::
            It does not check supeqs. self.idx MUST point to a juxted.

            If the real juxted is a non-usubeq and its urepr is selected,
            change self.idx before calling this function so it points to the
            right juxted.

        Return index expected to be selected and its direction. That's done
        that way because final selection is tricky for this operation.

        It has sense to call this function if selection is a juxted and
        desired operation is:

            *   Backward delete with dir == RDIR.
            *   Forward delete with dir in (LDIR, VDIR, ODIR).

        .. note::
            Implementation notes:

                *   Do NOT use here any supeq-checker. Use _set when necessary.
                *   Pointed subeq cannot be a base because it must be a juxted,
                    but its juxt-block can.
        """
        j_idx = self.idx[:] if idx is None else idx[:]
        juxtblock = eqqueries.supeq(j_idx, self.eq, True)
        if len(juxtblock) == j_idx[-1] + 1:
            # Case: Vanish last juxted
            if self.ovrwrt:
                # Overwrite mode -> Replace by VOID or select next mate
                rmate = eqqueries.mate(j_idx, self.eq, True)[0]
                if rmate == -1:
                    self._set(utils.void(), j_idx)
                    return j_idx, self._get_safe_dir()
                # (!) The other overwrite case is not completed until later

            # Normal mode -> Select juxted to the left, prefer RDIR
            if len(juxtblock) > 3:
                del juxtblock[-1]
                j_idx[-1] -= 1
            else:
                juxtblock[:] = deepcopy(juxtblock[1])
                del j_idx[-1]
                print(repr(j_idx), repr(self.eq))
                self._condtly_correct_scriptop(juxtblock, j_idx)

            if self.ovrwrt:
                return rmate, self._get_safe_dir()
            else:
                return (eqqueries.urepr(j_idx, self.eq),
                        self._get_safe_dir(1, None, j_idx))

        if j_idx[-1] == 1:
            # Case: Vanish first juxted -> Juxted to the right, prefer LDIR
            if len(juxtblock) > 3:
                del juxtblock[1]
            else:
                juxtblock[:] = deepcopy(juxtblock[2])
                del j_idx[-1]
                self._condtly_correct_scriptop(juxtblock, j_idx)

            return (eqqueries.urepr(j_idx, self.eq),
                    self._get_safe_dir(-1, None, j_idx))

        # Case: Intermediate juxted
        del juxtblock[j_idx[-1]]
        # If dir is RDIR -> Juxted to the left, prefer same DIR.
        # Else -> Juxted to the right (done automatically), prefer same DIR.
        if self.dir == utils.RDIR:
            j_idx[-1] -= 1
        return (eqqueries.urepr(j_idx, self.eq),
                self._get_safe_dir(5, None, j_idx))

    @debug
    def _flat(self, idx=None):
        """Remove lop of block pointed by index while leaving its args
        (joined by a juxt-block if necessary).

        *   Not a supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        *idx* can point to any subeq, not necessarily an usubeq.

       It return True if equation was edited. Else, False.

        .. note::
            It does not edit eq if it is pointed:

                *   A symbol (or 0-args op), or
                *   A juxt-block.
        """
        flat_idx = self.idx if idx is None else idx
        s = eqqueries.get(flat_idx, self.eq)
        if len(s) == 1 or s[0] in (utils.JUXT, utils.TJUXT):
            return False

        validpars = [par for par in s[1:] if par != utils.void()]
        if not validpars:
            s[:] = utils.void()
        else:
            repl_subeq = simpleeqcreator.SimpleEqCreator()
            for validpar in validpars:
                repl_subeq.extend(validpar)
            s[:] = repl_subeq.get_eq()

        self._condtly_correct_scriptop(s, flat_idx)
        return True


def flat_external_block(eq, idx, dir=1, remove_mode=0):
    """Core function to flat the least external block of selection
    (essentially remove the leading operator and join uargs in JUXT-ublock).
    It also ungroups in some circumstances.

    Parameter *remove_mode* is expected to be:

        *   If the call to this function is the consequence of backward
            deleting, 1.
        *   If the call to this function is the consequence of forward
            deleting, -1.
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


def _clever_vanish(self):
    """Vanish biggest supeq having selection as urepr if that exists. Else,
    vanish selection. It removes juxts when only one juxted is left.

    It totally removes a script if that is the actual subeq to vanish.

    It does not remove

    It sets idx and dir.

    .. note::
        It must be called only to make disappear current selection.
        Expected use is:

            *   Backward delete with dir == 1.
            *   Forward delete with dir in (-1, 0).

    .. note:
        Final selection is intentionally not documented here. Read the
        source code which is intended to be clear.
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
        # Case: Vanish a non-juxted
        if scriptops.is_scriptop(sup[0]):
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
    script_idx = scriptops.insert_script(idx, eq, dir, is_superscript)
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

