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


"""An interface to safely edit an equation."""

from copy import deepcopy

from . import eqdebug
from . import eqqueries
from . import scriptops
from . import simpleeqcreator
from .symbols import utils


class EditableEq:
    """Class to edit an equation.

    .. note::
        Methods not starting by underscore will suppose that self.idx points
        to selected equation. As a consequence:

            *   self.idx must point to an usubeq before calling them.
            *   The only supeq of the usubeq pointed by self.idx which may be a
                GOP-block is its 1-level supeq (but strict subeqs may be also
                GOP-blocks).

    Responsibilities:

        *   Methods of this class introduce TVOIDs and delete/transform them
            if appropriated.

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
    @eqdebug.debuginit
    def __init__(self, eq0=None, sel_idx0=None, dir0=None):
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

    @eqdebug.debug
    def set_ovrwrt(self, new_ovrwrt_val=True):
        if (new_ovrwrt_val and self.odir()) \
                or (not new_ovrwrt_val and not self.odir()):
            return

        if new_ovrwrt_val:
            if not self.rdir():
                self.dir = utils.ODIR
                return

            self.dir = utils.ODIR
            eff_idx = self._get_biggest_subeq_same_urepr()
            sup = eqqueries.supeq(eff_idx, self.eq, True)
            if sup == -2 or sup[0] != utils.JUXT \
                    or eff_idx[-1] == len(sup) - 1:
                self.idx = self._rinsert(utils.void(temp=True), eff_idx)
            else:
                eff_idx[-1] += 1
                self.idx = eqqueries.urepr(eff_idx, self.eq)
            return

        # From here, new_ovrwrt_val is False and current dir is ODIR
        eff_idx = self._get_biggest_subeq_same_urepr()
        sup = eqqueries.supeq(eff_idx, self.eq, True)
        if sup == -2:
            s = eqqueries.get(eff_idx, self.eq)
        else:
            s = sup[eff_idx[-1]]

        # Set a dummy non-ODIR value to dir
        self.dir = utils.VDIR

        if s == utils.void(temp=True):
            # Final TVOID juxted -> previous juxted with RDIR
            self.idx = self._vanish_juxted(0, eff_idx)[0]
            self.dir = self._get_safe_dir(1)
            return

        if sup == -2 or sup[0] != utils.JUXT or eff_idx[-1] == 1:
            # Non-juxteds and first juxteds -> LDIR
            self.dir = self._get_safe_dir(-1)
        else:
            # Other cases -> Select juxted to the left with RDIR
            self.idx = eqqueries.urepr(eff_idx[:-1] - [eff_idx[-1] - 1],
                                       self.eq)
            self.dir = self._get_safe_dir(-1)
        return

    def odir(self):
        return self.dir == utils.ODIR

    def rdir(self):
        return self.dir == utils.RDIR

    def ldir(self):
        return self.dir == utils.LDIR

    def vdir(self):
        return self.dir == utils.VDIR

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
            *    0, you trust that dir is utils.ODIR or *subeq* is VOID-like.

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
        if self.odir():
            return self.dir
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

    def _get_biggest_subeq_same_urepr(self, idx=None, retsub=False):
        """If *idx* points to a usubeq U and it has supeq which urepr is US,
        return the index of the biggest supeq with that property. If *idx*
        points to non-usubeq subeq or mentioned supeq does not exist, *idx*
        is returned.

        This function is used by those methods with the tag: supeq-checker.

        Case *idx* being None is equivalent to pass self.idx.
        """
        usubeq_idx = self.idx[:] if idx is None else idx[:]
        retval = eqqueries.biggest_supeq_with_urepr(usubeq_idx, self.eq,
                                                    retsub)
        if not isinstance(retval, list):
            return eqqueries.get(usubeq_idx, self.eq) if retsub else usubeq_idx
        return retval

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

    #@debug
    def _rinsert(self, subeq, idx=None):
        """Insert a subeq to the right. If subeq is a JUXT-block, a TJUXT-block
        is inserted instead.

        *   Not a supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        It has sense to call this function when inserting and:

            *   Non-overwrite mode is used, and
            *   Direction is RDIR.

        It returns the index of inserted subeq.
        """
        pointed_idx = self.idx[:] if idx is None else idx[:]
        sel = eqqueries.get(pointed_idx, self.eq)
        sup = eqqueries.supeq(pointed_idx, self.eq, True)
        s_new = subeq if subeq[0] != utils.JUXT else [utils.TJUXT] + subeq[1:]
        if sup != -2 and sup[0] == utils.JUXT:
            # Case: selection is a juxted
            # Note: Checked in doc that insertions after len(L)-1 are allowed
            sup.insert(pointed_idx[-1] + 1, s_new)
            return pointed_idx[:-1] + [pointed_idx[-1] + 1]

        elif sel[0] == utils.JUXT:
            # Case: selection is a juxt-block and is not a juxted
            sel.append(s_new)
            return pointed_idx + [len(sel) - 1]
        else:
            # Case: selection is a non-juxt-block and is not a juxted
            sel[:] = [utils.JUXT] + [sel[:]] + [s_new]
            self._condtly_correct_scriptop(sel, None, sup)
            return pointed_idx + [2]

    #@debug
    def _linsert(self, subeq, idx=None):
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
        pointed_idx = self.idx[:] if idx is None else idx[:]
        sel = eqqueries.get(pointed_idx, self.eq)
        sup = eqqueries.supeq(pointed_idx, self.eq, True)
        s_new = subeq if subeq[0] != utils.JUXT else [utils.TJUXT] + subeq[1:]
        if sup != -2 and sup[0] == utils.JUXT:
            # Case: selection is a juxted
            # Note: Checked in doc that insertions after len(L)-1 are allowed
            sup.insert(pointed_idx[-1], s_new)
            return pointed_idx
        elif sel[0] == utils.JUXT:
            # Case: selection is a juxt-block and is not a juxted
            sel[1:] = s_new + sel[1:]
            return pointed_idx + [1]
        else:
            # Case: selection is a non-juxt-block and is not a juxted
            sel[:] = [utils.JUXT] + [s_new] + [sel[:]]
            if sup != -2 and pointed_idx[-1] == 1 \
                    and scriptops.is_scriptop(sup[0]):
                scriptops.update_scriptblock(sel, sup)
            return pointed_idx + [1]

    #@debug
    def _replace_integrating(self, s_repl, idx=None):
        """Replace a subequation integrating juxteds if appropriated.

        *   supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        .. note::
            *   To replace current selection you should use _replace.

        If *s_repl* is a JUXT-block JB and actual subeq being replaced is a
        juxted of a juxt-block EJB, juxteds of JB are integrated as juxteds of
        EJB. Else, it is a normal replacement (which includes the case *s_repl*
        being a TJUXT-block)

        If *idx* is None that is equivalent to pass self.idx. Note however that
        this method should not be used just to replace actual selection
        because it always integrates if appropriated.

        Return the index of subeq which was finally replaced (*idx* or the
        index of a non-usubeq supeq).
        """
        # Choose correct subeq to replace
        repl_idx = self.idx if idx is None else idx
        repl_idx = self._get_biggest_subeq_same_urepr(repl_idx)

        sup = eqqueries.supeq(repl_idx, self.eq, True)
        if sup != -2:
            s = sup[repl_idx[-1]]
        else:
            s = eqqueries.get(repl_idx, self.eq)

        if s_repl[0] != utils.JUXT or sup == -2 \
                or not eqqueries.isjuxtblock(sup):
            # Case: No juxteds are integrated
            self._condtly_correct_scriptop(s_repl, repl_idx)
            s[:] = deepcopy(s_repl)
            return repl_idx

        # Case: some juxteds will be integrated
        sup[:] = sup[:repl_idx[-1]] + s_repl[1:] + sup[repl_idx[-1] + 1:]
        return repl_idx

    #@debug
    def _replace(self, subeq, idx=None):
        """Replace pointed subeq or supeq if *idx* points to a GOP-param.

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
        """Replace pointed subeq or supeq if pointed subeq is a GOP-param.

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

    def _vanish_juxted(self, reljuxted=0, idx=None):
        """Vanish pointed juxted or a cojuxted. It removes the juxt op if only
        one juxted is left in the juxt-block.

        *   Not a supeq-checker
        *   final-idx-checker
        *   base-checker

        .. note::

            *   It IS perfectly fine if pointed subeq is not an usubeq.
            *   It does not check supeqs. Pointed subeq MUST be a juxted.
            *   It vanish a juxted independently of self.dir, but returned
                direction will depend on self.dir

        Return index expected to be selected and its direction. That's done
        that way because final selection is tricky for this operation.

        If *reljuxted* == n != 0, it vanishes the n-th juxted to the right or
        left of pointed juxted depending whether n is positive or negative,
        respectively. Caller must check by itself that referenced juxted
        exists.

        If *reljuxted* != 0, returned values are the index and dir of
        originally pointed juxted, likely corrected due to internal changes.

        .. note::
            Implementation notes:

                *   Do NOT use here any supeq-checker method.
                *   Use _set when necessary.
                *   Pointed subeq cannot be a base because it must be a juxted,
                    but its juxt-block can.
        """
        # Pointed juxted
        pointed_idx = self.idx[:] if idx is None else idx[:]
        # Juxted to delete (may be pointed juxted)
        del_idx = pointed_idx[:-1] + [pointed_idx[-1] + reljuxted]
        juxtblock = eqqueries.supeq(del_idx, self.eq, True)

        if len(juxtblock) == del_idx[-1] + 1:
            # Case: Vanish last juxted
            if len(juxtblock) > 3:
                del juxtblock[-1]
                retidx = pointed_idx
                if not reljuxted:
                    # Select juxted to the left
                    retidx[-1] -= 1
            else:
                juxtblock[:] = deepcopy(juxtblock[1])
                retidx = del_idx[:-1]
                self._condtly_correct_scriptop(juxtblock, retidx)

            # prefer RDIR
            return (eqqueries.urepr(retidx, self.eq),
                    self._get_safe_dir(1, None, retidx))

        if del_idx[-1] == 1:
            # Case: Vanish first juxted
            if len(juxtblock) > 3:
                del juxtblock[1]
                #  Select juxted to the right
                retidx = pointed_idx
                if reljuxted:
                    retidx[-1] -= 1
            else:
                juxtblock[:] = deepcopy(juxtblock[2])
                retidx = pointed_idx[:-1]
                self._condtly_correct_scriptop(juxtblock, retidx)
            # Prefer LDIR
            return (eqqueries.urepr(retidx, self.eq),
                    self._get_safe_dir(-1, None, retidx))

        # Case: Intermediate juxted
        #
        # Rules when reljuxted == 0:
        # ODIR -> Juxted to the right, ODIR.
        # LDIR -> Juxted to the right, prefer LDIR.
        # RDIR -> Juxted to the left, prefer RDIR.
        # VDIR -> Juxted to the left, prefer RDIR
        #
        # In every case, using successive times the same deleting keystroke
        # will have consistent results.
        # There are another valid option for last case. The chosen one is less
        # surprising so it is preferred. In addition, the chosen one does not
        # require to know the deleting direction.
        del juxtblock[del_idx[-1]]
        retidx = pointed_idx
        if reljuxted < 0 or (not reljuxted and (self.rdir() or self.vdir())):
            retidx[-1] -= 1

        return (eqqueries.urepr(retidx, self.eq),
                self._get_safe_dir(5, None, retidx))

    def _flat(self, idx=None):
        """Remove lop of block pointed by index while leaving its non-VOID args
        (joined by a juxt-block if necessary).

        *   Not a supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        *idx* can point to any subeq, not necessarily an usubeq.

       It return True if equation was edited. Else, False.

        .. note::
            It does not edit eq if it is pointed:

                *   A symbol (or 0-args op), or
                *   A juxt-block with no juxted equal to VOID.
        """
        flat_idx = self.idx if idx is None else idx
        s = eqqueries.get(flat_idx, self.eq)
        if len(s) == 1:
            return False

        repl_c = simpleeqcreator.SimpleEqCreator()
        repl_c.extend(s[1:], include_voids=False)
        repl = repl_c.get_eq()
        n_insertions = repl_c.n_inserted_subeqs()

        if s[0] in (utils.JUXT, utils.TJUXT):
            if n_insertions == len(s[1:]):
                return False

            if n_insertions > 1:
                s[1:] = repl[1:]
                return True
            # Other juxt cases are equivalent to non-juxt cases

        s[:] = repl[:]
        self._condtly_correct_scriptop(s, flat_idx)
        return True

    def _flat_lopblock(self, idx=None, supref=None):
        """Remove leading operator and leave params, joined in a juxt-block
        if necessary.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        If *idx* points to a non-usubeq, let "par_idx" be equal to the
        pointing index.
        Else, let "par_idx" be the index of the biggest subeq of eq having
        as urepr the pointed subeq.

        .. note::
            It is expected that no supeq of subeq pointed by par_idx is a
            TJUXT-block.

        .. note::
            It works fine with TVOIDs (which are always selected and are
            juxteds).

        Return -2 if par_idx is []. Equation is not edited in that case
        Return -5 if par_idx is not [] and equation is not edited. That happens
        if par_idx points to a juxted and no juxted of its juxt-block is VOID.

        Note: There should not be VOIDs in JUXT-blocks.

        In any other case, return expected selection and direction supposing
        that current selection is *idx*.

        Rules:

            *   If every param of the lop of param pointed by *par_idx* is
                VOID, then the lop-block is vanished if it is a juxted.
                Else, it is replaced by a VOID.
            *   Elif param pointed by *par_idx* is a juxted, vanish any juxted
                equal to VOID.
            *   Else, replace the lop-block of param pointed by *par_idx* with
                any non-VOID param joined together by a juxt-block if
                necessary.
        """
        par_idx = self.idx if idx is None else idx
        par_idx = self._get_biggest_subeq_same_urepr(par_idx)
        if not par_idx:
            return -2

        # It is guaranteed by previous code that supeq exists and is an usubeq
        sup_idx = par_idx[:-1]
        sup = eqqueries.get(sup_idx, self.eq) if supref is None else supref
        n_void_pars = sup[1:].count(utils.void())
        n_non_void_pars = len(sup) - n_void_pars - 1
        if not n_void_pars and sup[0] == utils.JUXT:
            return -5

        if not n_non_void_pars:
            # Case: Every param is a VOID
            eff_sup_idx = self._get_biggest_subeq_same_urepr(sup_idx)
            if eqqueries.isjuxted(eff_sup_idx, self.eq):
                # Subcase: supeq is the urepr of a juxted
                return self._vanish_juxted(0, eff_sup_idx)

            sup[:] = utils.void()
            self._condtly_correct_scriptop(sup, sup_idx)
            return sup_idx, self._get_safe_dir(0, 0)

        # Build replacement
        par_ord = par_idx[-1]
        repl_c = simpleeqcreator.SimpleEqCreator()
        repl_c.extend(sup[1:par_ord], include_voids=False)
        par = deepcopy(sup[par_ord])
        if par[0] == utils.JUXT:
            # Being here implies that par is not a void
            par[0] = utils.TJUXT
        par_pos_in_repl = repl_c.n_inserted_subeqs()
        # If par is a void, include it.
        # -> It will be deleted below and a good selection will be chosen
        repl_c.append(par, include_voids=True)
        repl_c.extend(sup[par_ord + 1:], include_voids=False)

        # Replace

        # It is assumed that pointed subeq was selected, so no supeq par can
        # be a GOP-block (nor usubeq)
        # -> _replace_integrating will replace faithfully in any case
        self._replace_integrating(repl_c.get_eq(), sup_idx)

        # Return useful selection

        # Note: par was never inserted as a JUXT-block in repl_c so
        # repl_c.get_idx with [] is allowed
        par_idx_in_repl = repl_c.get_idx([], par_pos_in_repl)
        if not eqqueries.isjuxted(sup_idx, self.eq):
            # A non-juxted was replaced by repl
            new_idx = sup_idx + par_idx_in_repl
            if par == utils.void():
                return self._vanish_juxted(0, new_idx)
        elif par_idx_in_repl:
            # A juxted was replaced by repl, which was a juxt-block
            new_idx = sup_idx[:-1] + [sup_idx[-1] + par_idx_in_repl[0] - 1]
            if par == utils.void():
                return self._vanish_juxted(0, new_idx)
        else:
            # A juxted was replaced by repl, which was not a juxt-block
            # Note: It is not possible for a pointed VOID to match this case
            new_idx = sup_idx

        new_idx = eqqueries.urepr(new_idx, self.eq)
        return new_idx, self._get_safe_dir(5, None, new_idx)

    @eqdebug.debug
    def delete_clever(self, forward, n=1):
        """Forward/Backward clever delete accepting a numeric argument.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        .. note::
            Deletion in overwrite mode is more gedit-like than readline-like.

        Return the (positive) number of arguments not applied.
        """
        # Consider always a positive num_arg
        if n < 0:
            forward = not forward
            n = -n

        for n in range(n, 0, -1):
            del_idx = self._get_biggest_subeq_same_urepr()
            sup = eqqueries.supeq(del_idx, self.eq, True)
            # Whole eq is pointed
            if sup == -2:
                if self.vdir() or (forward and self.rdir()) \
                        or (not forward and (self.ldir() or self.odir())):
                    return n

                self.remove_eq()
                return n - 1

            # From here, sup is a subequation
            par_ord = del_idx[-1]
            sup_idx = del_idx[:-1]
            # Let us set pointed subeq to del_idx to simplify the code.
            # Those cases which do not edit the equation will restore
            # self.idx to the original value.
            # (note: rest of defined variables are still valid)
            self.idx[:] = del_idx[:]
            # Note: VOID cannot be the arg of a GOP
            # => No need to update self.dir.

            if sup[0] != utils.JUXT:
                if (not forward and self.rdir()) \
                        or (forward and (self.ldir() or self.odir())):
                    # Subcase: Delete a non-juxted subeq
                    self.idx = self._empty()
                    self.dir = self._get_safe_dir(0, 0)
                    continue

                # Subacase: Flat non-juxt lop (includes VOID and non-VOID par)
                self.idx, self.dir = self._flat_lopblock(None, sup)
                continue

            # From here, a juxted is pointed
            if self.vdir():
                # Subcase: A VOID is selected
                # (This subcase should not happen)
                self.idx, self.dir = self._vanish_juxted()
                continue

            if (not forward and self.rdir()) or (forward and self.ldir()) \
                    or par_ord != len(sup) - 1:
                # Subcase: Vanish pointed juxted
                self.idx, self.dir = self._vanish_juxted()
                continue

            if self.odir() and forward and par_ord == len(sup) - 1 \
                    and sup[par_ord] != utils.void(temp=True):
                # Subcase: Replace non-TVOID last juxted with a TVOID
                self._replace(utils.void(temp=True), del_idx)
                continue

            if forward and len(sup[1:]) > par_ord:
                # Subcase: Delete juxted to the right
                self.idx = self._vanish_juxted(1)[0]
                continue
            if self.odir() and not forward and par_ord == 2 == len(sup) - 1 \
                    and sup[par_ord] == utils.void(temp=True):
                # Subcase: Delete the only juxted to the left of a TVOID
                self._set(utils.void(), sup_idx)
                self.idx = sup_idx[:]
                continue
            if not forward and par_ord != 1:
                # Subcase: Delete juxted to the left (excluding prev. subcase)
                self.idx = self._vanish_juxted(-1)[0]
                continue

            supsup = eqqueries.supeq(sup_idx, self.eq, True)

            if supsup == -2:
                # Subcase: First or last juxted of the whole eq (no edit)
                # Be sure that original index is restored
                self.idx[:] += eqqueries.urepr([], sup[par_ord])
                return n

            if supsup[0] != utils.JUXT:
                # Subcase: selection is a juxted JU of a juxt-block, which is
                # an argument of an op OP which is not a juxt => flat OP-block
                # It is assured that there are no supeqs of JU being GOP-blocks
                self.idx, self.dir = self._flat_lopblock(sup_idx, supsup)
                self.idx.append(par_ord)
                if eqqueries.get(self.idx, self.eq) == utils.void(temp=True):
                    self.idx, self.dir = self._vanish_juxted()
                return n - 1

            # Subcase: selection is a juxted of a juxt-block which is itself a
            # juxted JU => behave as if JU was selected with the same dir
            del self.idx[-1]
            retval = self.delete_clever(forward, n)
            self.idx.append(par_ord)
            return retval

        return 0

    def _group(self, idx=None):
        """Group a user subeq if necessary.

        *   supeq-checker
        *   final-idx-checker (guaranteed since passed idx must be an usubeq)
        *   base-checker (guaranteed because GOP is transparent for script ops)

        Return index of pointed subeq after operation.
        """
        block_idx = self.idx[:] if idx is None else idx[:]
        block = eqqueries.get(block_idx, self.eq)
        if len(block) == 1:
            return block_idx

        sup = eqqueries.supeq(block_idx, self.eq, True)
        if sup == -2 or sup[0] != utils.GOP:
            block[:] = [utils.GOP, deepcopy(block)]
            return block_idx + [1]

        return block_idx

    @eqdebug.debug
    def group(self):
        """Group pointed subeq, if needed.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker
        """
        self.idx[:] = self._group()

    @eqdebug.debug
    def insert_clever(self, pseudoe, substitute_1st_free_arg=False, n=1):
        """Insert/replace a subequation from a primitive or part of a
        subequation.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        *psudoe* can be:

            *   A string.
            *   An operator.
            *   A subequation.
            *   An incomplete subequation.

            An example of last case would be [OP, par1, par2] provided that
            OP.n_args > 2.

        .. note::
            If *pseudoe* is an operator OP, or incomplete subeq with lop OP,
            OP must not be a juxt nor a GOP.
        .. note::
            Definition of subeq to insert is done only once even if *n* > 2.
        """
        if n <= 0:
            return

        def void_list(n):
            """Create a list of voids which are not the same element.
            ( [utils.void()]*n creates references to the same VOID)
            """
            return [utils.void() for i in range(n)]

        # Create subeq to insert
        eff_pointed_s = self._get_biggest_subeq_same_urepr(None, True)
        if eff_pointed_s == utils.void(temp=True):
            eff_pointed_s = utils.void()
        pe_cp = deepcopy(pseudoe)
        free_args = 0
        if isinstance(pe_cp, str) \
                or (isinstance(pe_cp, utils.Op) and not pe_cp.n_args):
            subeq = [pe_cp]
        elif isinstance(pe_cp, utils.Op) and substitute_1st_free_arg:
            # pseudoelem is an op and first arg will be current selection
            assert pe_cp not in (utils.GOP, utils.JUXT, utils.TJUXT)
            free_args = pe_cp.n_args - 1
            subeq = [pe_cp] + [deepcopy(eff_pointed_s)] + void_list(free_args)
        elif isinstance(pe_cp, utils.Op):
            # pseudoelem is an op and every argument will be set to a VOID
            assert pe_cp not in (utils.GOP, utils.JUXT, utils.TJUXT)
            free_args = pe_cp.n_args
            subeq = [pe_cp] + void_list(free_args)
        elif eqqueries.isjuxtblock(pe_cp):
            assert len(pe_cp) > 2
            subeq = pe_cp
        elif isinstance(pe_cp[0], str) or pe_cp[0].n_args == len(pe_cp) - 1:
            # pseudoelem is a complete subeq
            # (substitute_1st_free_arg does not matter in this case)
            subeq = pe_cp
        elif substitute_1st_free_arg:
            # pseudoelem will use current selection in first unset argument
            assert pe_cp[0] != utils.GOP
            free_args = pe_cp[0].n_args - 1
            subeq = [pe_cp] + [deepcopy(eff_pointed_s)] + void_list(free_args)
        else:
            # pseudoelem needs only VOIDs
            assert pe_cp[0] != utils.GOP
            free_args = pe_cp[0].n_args
            subeq = [pe_cp] + void_list(free_args)

        # Insert subeq
        for n in range(n, 0, -1):
            eff_pointed_idx = self._get_biggest_subeq_same_urepr()
            if self.odir() or self.vdir() or substitute_1st_free_arg:
                # A replacement regardless of whether replacement contains
                # current selection
                self._replace(subeq, eff_pointed_idx)
            elif self.rdir():
                ret_idx = self._rinsert(subeq, eff_pointed_idx)
                self.idx = eqqueries.urepr(ret_idx, self.eq)
            else:
                ret_idx = self._linsert(subeq, eff_pointed_idx)
                self.idx = eqqueries.urepr(ret_idx, self.eq)

            if free_args:
                # Select first free arg if it exists in any case
                sel = eqqueries.get(self.idx, self.eq)
                self.idx.append(len(sel) - free_args)
            elif self.odir():
                # Select next juxted or create a TVOID if ODIR
                npars_sup = eqqueries.npars(self.eq, self.idx[:-1])
                if eqqueries.isjuxted(self.idx, self.eq) \
                        and npars_sup != self.idx[-1]:
                    self.idx[-1] += 1
                else:
                    self.idx = self._rinsert(utils.void(temp=True))
            self.dir = self._get_safe_dir(5)

    @eqdebug.debug
    def insert_script(self, scriptdir, is_superscript, script=None):
        """Insert a script and select it.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        If script already exists, just select it.

        Return True or False depending on whether the script was already
        present.
        """
        base_idx = self._get_biggest_subeq_same_urepr()
        # scriptops.insert_script manages correctly a TVOID
        script_idx = scriptops.insert_script(base_idx, self.eq, scriptdir,
                                             is_superscript, script)
        retval = True
        if script_idx[-1] >= 0:
            script_idx[-1] *= -1
            retval = False

        self.idx = eqqueries.urepr(script_idx, self.eq)
        self.dir = self._get_safe_dir(1)
        return retval



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

