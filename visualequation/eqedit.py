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
from .subeqs import Subeq
from .dirsel import Dir
from .idx import Idx
from .ops import *
from . import scriptops
from . import simpleeqcreator
#from .symbols import utils


class EditableEq(Subeq):
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
                useful information as the self.idx and self.dir that should be
                set under a typical use of the method.

            *   Methods not starting with underscore are intended to be safe
                to call independently of the input. They should set any
                property of this class so the method performs an operation
                completely.

            *   Indices argument names will be similar to the string 'index'.
                Indices used in the code will be similar to the string 'idx',
                unless code does a trivial use of an index argument so it is
                considerer simpler to reuse the unmodified index parameter.
                An index parameter with value of -1 means 'use self.idx'.
                In any other case, it will be understood as a valid argument of
                Idx-ctor.

        Definitions:

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
    def __init__(self, eq0=None, sel_index0=None, dir0=None, debug=True):
        super().__init__(deepcopy(eq0))
        # The index of current subeq being selected.
        if sel_index0 is not None:
            self.idx = Idx(sel_index0)
        elif self.is_gopb():
            self.idx = Idx(1)
        else:
            self.idx = Idx()
        # The direction of the selection.
        if dir0 is not None:
            self.dir = dir0
        elif self(self.idx).is_pvoid():
            self.dir = Dir.V
        else:
            self.dir = Dir.R
        self.debug = debug

    def __repr__(self):
        return "EditableEq(" + self._repr_aux(self) + ", " + str(self.idx) \
                + ", " + str(self.dir) + ", " + repr(self.debug) + ")"

    def _safe_idx_arg(self, index):
        """Return a copy of self.idx if index is -1. Else, a new index build
         as Idx(index)."""
        return self.idx[:] if index == -1 else Idx(index)

    def _safe_refidx_arg(self, refindex, index=-1):
        """Return _safe_idx_arg(index) if refindex is -2.

        Else, _safe_idx_arg(refindex), so value -1 or None have meanings for
        both parameters.
        """
        if refindex == -2:
            return self._safe_idx_arg(index)
        else:
            return self._safe_idx_arg(refindex)

    def _safe_subeq_arg(self, subeq=0, index=-1):
        """Return a deepcopy of a subequation.

        If *subeq* is not 0, return a Subeq constructed with a deepcopy of
        *subeq*.

        Elif *index* is not -1, return a deepcopy of self(index).

        Else, return a deepcopy of self(self.idx).
        """
        if subeq != 0:
            return Subeq(deepcopy(subeq))
        if index != -1:
            return deepcopy(self(index))
        return deepcopy(self(self.idx))

    def _set(self, elem, index=-1):
        """A 'hard' replacement. If replacement is a JUXT-block, it will be
        replaced as a whole.

            *   Not a supeq-checker
            *   Not a final-idx-checker
            *   Not a base-checker

        Replacement is always done in pointed subeq.
        """
        idx = self._safe_idx_arg(index)
        self(idx)[:] = deepcopy(elem)

    def is_odir(self):
        return self.dir is Dir.O

    def is_rdir(self):
        return self.dir is Dir.R

    def is_ldir(self):
        return self.dir is Dir.L

    def is_vdir(self):
        return self.dir is Dir.V

    def _safe_dir(self, dirflag=0, subeq: Union[int, None] = 0, index=-1):
        """Set direction respecting overwrite mode and a subeq that is
        supposed to be selected before or after the call to this method.

            *   Not a supeq-checker
            *   Not final-idx-checker
            *   base-checker not applicable.

        wp ~ "when possible" ~ self.dir is not O and referred subeq is not
        PVOID.

        If *dirflag* is:

            *    1, use R wp.
            *   -1, use L wp.
            *    5, use self.dir unless it was V; in that case, R wp.
            *   -5, use self.dir unless it was V; in that case, L wp.
            *    0, do not do anything wp (use it with responsibility).

        WARNING: If subeq is not a PVOID, self.dir == Dir.V and *dirflag* is
        set to 0, Dir.V is returned. Use of *dirflag* == 0 is not recommended
        and it may be unsupported in the future.

        If *subeq* is:

            *   0, it uses subeq referred by *index*.
            *   None, it is equivalent to pass [ops.PVOID].
            *   ow., it uses passed subequation.

        If *index* is:

            *   -1, equivalent to pass self.idx.
            *   ow., self(*index*) is considered. For this parameter to take
                effect, *subeq* must be 0. Else, it is ignored.

        .. note::

            It is OK to refer to a GOP-block instead of its par even if that
            is the one that is going to be selected (a GOP-par cannot be a
            PVOID).

        """
        if self.is_odir():
            return Dir.O
        if subeq is None:
            return Dir.V
        if subeq != 0:
            s = Subeq(subeq)
        else:
            s = self(self.idx) if index == -1 else self(index)
        if s.is_pvoid():
            return Dir.V
        # From here, subeq to be selected is not PVOID and self.dir != Dir.O
        if dirflag == 0:
            return self.dir
        if dirflag in (1, Dir.R):
            return Dir.R
        if dirflag in (-1, Dir.L):
            return Dir.L
        if dirflag == 5:
            return self.dir if self.dir != Dir.V else Dir.R
        if dirflag == -5:
            return self.dir if self.dir != Dir.V else Dir.L
        raise ValueError("Incorrect input parameters")

    def _condtly_correct_scriptop(self, newbase, index=-1, refindex=-2):
        """Correct a script-block if index points to a base and it is needed.

        WARNING: Read this note:

        .. note::
            This function may invalidate any reference to any element of
            the script block after the call.
            If the index of some inner element is required, this function
            would need to be updated (and changes would go deeper in
            scriptops.py).

        This function is used by those methods with the tag: base-checker.

        :param newbase: The new block which will be used in pointed subeq.
        :param index: Index of the element which may be a base. -1 -> self.idx.
        :param refindex: Index to return after operation. -2 -> index.
        """
        idx_base = self._safe_idx_arg(index)
        refidx = self._safe_refidx_arg(refindex, index)
        if scriptops.is_base(self, idx_base):
            return scriptops.update_scriptblock(Subeq(newbase), self,
                                                idx_base[:-1], refidx)
        return Idx(refidx)

    def _biggest_subeq_same_urepr(self, index=-1, retidx=False):
        """If pointed subeq is a GOP-par, return the GOP-block.
        Else, return pointing subeq.

        This function is used by methods with the tag: supeq-checker.
        """
        idx = self._safe_idx_arg(index)
        retval = self.biggest_supeq_with_urepr(idx, retidx)
        if retval == -1:
            return idx if retidx else self(idx)
        return retval

    #@debug
    def _rinsert(self, subeq, index=-1):
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
        idx = self._safe_idx_arg(index)
        s_new = self._safe_subeq_arg(subeq)
        if s_new.is_perm_jb():
            s_new[0] = TJUXT
        sel = self(idx)
        sup = self.supeq(idx)
        if sup != -2 and sup.is_perm_jb():
            # Case: pointed subeq is a juxted (included being also juxt-block)
            # Note: Checked in Python doc that insertions after len(L)-1 are
            # allowed
            sup.insert(idx[-1] + 1, s_new)
            return idx[:-1] + [idx[-1] + 1]

        if sel.is_perm_jb():
            # Case: pointed subeq is a juxt-block JB and is not a juxted
            # => Equivalent to have last juxted of JB pointed
            sel.append(s_new)
            return idx + [len(sel) - 1]

        # Case: pointed subeq is a non-juxt-block and is not a juxted
        sel[:] = [PJUXT] + [sel[:]] + [s_new]
        return self._condtly_correct_scriptop(sel, idx, idx + [2])

    #@debug
    def _linsert(self, subeq, index=-1):
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
        idx = self._safe_idx_arg(index)
        s_new = self._safe_subeq_arg(subeq)
        if s_new.is_perm_jb():
            s_new[0] = TJUXT

        sel = self(idx)
        sup = self.supeq(idx)
        if sup != -2 and sup.is_perm_jb():
            # Case: pointed subeq is a juxted (included being also juxt-block)
            # Note: Checked in doc that insertions after len(L)-1 are allowed
            sup.insert(idx[-1], s_new)
            return idx

        if sel.is_perm_jb():
            # Case: pointed subeq is a juxt-block and also not a juxted
            sel.insert(1, s_new)
            return idx + [1]

        # Case: pointed subeq is a non-juxt-block and is not a juxted
        sel[:] = [PJUXT] + [s_new] + [sel[:]]
        return self._condtly_correct_scriptop(sel, idx, idx + [1])

    #@debug
    def _replace_integrating(self, repl, index=-1):
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
        because it always integrates if appropriated, never PJUXT -> TJUXT.

        Return the index of subeq which was finally replaced (*index* or the
        index of the supeq if it was a GOP-par) in the final equation.
        """
        # Choose correct subeq to replace
        idx = self._biggest_subeq_same_urepr(index, True)
        s_repl = self._safe_subeq_arg(repl)

        sup = self.supeq(idx)
        s = sup[idx[-1]] if sup != -2 else self(idx)

        if not s_repl.is_perm_jb() or sup == -2 or not sup.is_perm_jb():
            # Case: No juxteds are integrated
            s[:] = s_repl
            return self._condtly_correct_scriptop(s_repl, idx, idx)

        # Case: some juxteds will be integrated
        sup[:] = sup[:idx[-1]] + s_repl[1:] + sup[idx[-1] + 1:]
        return idx

    #@debug
    def _replace(self, subeq, index=-1):
        """Replace pointed subeq, or supeq if pointed one is a GOP-param.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        It does not care about juxts stuff, only GOP-pars.

        Return expected index to be selected in the case that pointed subeq
        represents current selection.

        .. note::
            It is expected to be called in overwrite mode or when inserting if
            selection is a [PVOID].
        """
        idx = self._biggest_subeq_same_urepr(index, True)

        # Correct script op if needed in the case that idx points to a base
        new_idx = self._condtly_correct_scriptop(subeq, idx, idx)

        # Replace
        self._set(subeq, new_idx)

        # Select the urepr of replacement
        return self.urepr(new_idx, True)

    def _empty(self, idx=-1):
        """Replace pointed subeq or supeq if pointed subeq is a GOP-par.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        It returns the index of inserted PVOID.
        """
        return self._replace([PVOID], idx)

    def remove_eq(self):
        """Replace the whole eq with a [PVOID]."""
        self.idx[:] = []
        self._set([PVOID])
        self.dir = self._safe_dir()

    def _vanish_juxted(self, reljuxted=0, index=-1):
        """Vanish pointed juxted or a cojuxted. It removes the juxt op if only
        one juxted is left in the juxt-block.

        *   Not a supeq-checker
        *   final-idx-checker
        *   base-checker

        Return index expected to be selected and its direction. That's done
        that way because final selection is tricky for this operation.

        .. note::

            *   It is intended to work also if pointed subeq is not an usubeq.
            *   It does not check supeqs. Pointed subeq MUST be a juxted.
            *   It vanishes the juxted independently of self.dir, but returned
                direction will depend on self.dir before the call.

        If *reljuxted* == n != 0, it vanishes the n-th juxted to the right or
        left of pointed juxted depending whether n is positive or negative,
        respectively. Caller must check by itself that referenced juxted
        exists.

        If *reljuxted* != 0, returned values are the index and dir of
        originally pointed juxted, index possibly corrected due to internal
        changes.

        .. note::
            Even if no PVOIDs should appear to the user as juxteds, they can be
            there expecting this method to remove there, as in _flat_lopblock.

        .. note::
            Implementation notes:

                *   Do NOT use here any supeq-checker method -> Prefer _set.
                *   Pointed subeq cannot be a base because it must be a juxted,
                    but its juxt-block can.
                *   It has no sense to vanish juxteds inside GOP-blocks since
                    they cannot be selected.
        """
        # Pointed juxted
        pointed_idx = self._safe_idx_arg(index)
        # Juxted to delete (may be pointed juxted)
        del_idx = pointed_idx[:-1] + [pointed_idx[-1] + reljuxted]
        juxtblock = self.supeq(del_idx)

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
                retidx = self._condtly_correct_scriptop(juxtblock, retidx,
                                                        retidx)

            # prefer RDIR
            return (self.urepr(retidx, True),
                    self._safe_dir(0 if reljuxted else 1, 0, retidx))

        if del_idx[-1] == 1:
            # Case: Vanish first juxted
            if len(juxtblock) > 3:
                del juxtblock[1]
                # Select juxted to the right
                retidx = pointed_idx
                if reljuxted:
                    retidx[-1] -= 1
            else:
                juxtblock[:] = deepcopy(juxtblock[2])
                retidx = pointed_idx[:-1]
                retidx = self._condtly_correct_scriptop(juxtblock, retidx,
                                                        retidx)
            # Prefer LDIR
            return (self.urepr(retidx, True),
                    self._safe_dir(0 if reljuxted else -1, 0, retidx))

        # Case: Intermediate juxted
        #
        # Rules when reljuxted == 0:
        # ODIR -> Juxted to the right, ODIR.
        # LDIR -> Juxted to the right, prefer LDIR.
        # RDIR -> Juxted to the left, prefer RDIR.
        # VDIR -> Juxted to the left, prefer RDIR
        #
        # Using successive times the same deleting keystroke will have
        # consistent results.
        # There is another valid option for VDIR. The chosen one is less
        # surprising so it is preferred. In addition, chosen option does not
        # require to know the deleting direction.
        del juxtblock[del_idx[-1]]
        retidx = pointed_idx
        if reljuxted < 0 \
                or (not reljuxted and (self.is_rdir() or self.is_vdir())):
            retidx[-1] -= 1

        return self.urepr(retidx, True), self._safe_dir(0, 0, retidx)

    def _flat(self, index=-1):
        """Dissolve pointed block while leaving its non-VOID pars joined by a
        juxt-block if necessary. If every param is non-VOID pointed block is
        a juxted, block is vanished.

        *   Not a supeq-checker
        *   final-idx-checker
        *   base-checker

        *index* can point to any subeq, not necessarily an usubeq.

       It returns an updated *index*, the adequate direction supposing
       that it acts on current selection and a boolean indicating whether
       some operation was applied to the equation.

        .. note::
            No operation is applied if what is pointed is:

                *   A symbol (or 0-args op), or
                *   A juxt-block.
        """
        idx = self._safe_idx_arg(index)
        s = self(idx)
        if len(s) == 1 or s.is_jb():
            return self.urepr(idx, True), self._safe_dir(5, 0, idx), False

        repl_c = simpleeqcreator.SimpleEqCreator()
        repl_c.extend(s[1:], accept_voids=False)
        repl = repl_c.get_eq()
        n_insertions = repl_c.n_inserted_subeqs()

        if n_insertions == 0 and self.is_juxted(idx):
            return (*self._vanish_juxted(0, idx), True)

        s[:] = repl[:]
        if self.is_juxted(idx) and s.is_perm_jb():  # s == self(idx)
            s[0] = TJUXT
        new_idx = self._condtly_correct_scriptop(s, idx, idx)
        return new_idx, self._safe_dir(5, 0, new_idx), True

    def _flat_lopblock(self, index=-1):
        """Remove leading operator and leave params (joined in a juxt-block if
        necessary).

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        .. note::
            It is expected that no supeq is a TJUXT-block.

        .. note::
            It works fine with TVOIDs (which should be always selected and be
            juxteds).

        Consider eff_s be pointed subeq or its supeq if pointed subeq is a
        GOP-par. Let eff_idx be the index of eff_s.

        Return an updated *index* and whether some operation was applied to the
        equation.

        Note: There should not be PVOIDs in JUXT-blocks, but supported by now.
        It is possible that some methods currently relay on that behavior.

        In any other case, return expected selection and direction supposing
        that current selection is pointed subeq.

        Rules:

            *   If every param of lop-eff_s is a PVOID:

                *   If eff_is a juxted, eff_s is vanished
                *   Else, eff_s is replaced by a PVOID.

            *   Elif eff_s is a juxted, vanish any juxted equal to PVOID.
            *   Else, replace the eff_s with any non-PVOID param, joined
                together by a juxt-block if necessary.
        """
        idx = self._biggest_subeq_same_urepr(index, True)
        if not idx:
            return -2

        # It is guaranteed by previous code that:
        #   1. Supeq exists, and
        #   2. Supeq is an usubeq
        sup_idx = idx[:-1]
        sup = self(sup_idx)
        n_void_pars = sup[1:].count([PVOID])
        n_non_void_pars = len(sup) - n_void_pars - 1
        if not n_void_pars and sup.is_perm_jb():
            return -5

        if not n_non_void_pars:
            # Case: Every param is a PVOID
            if self.is_juxted(sup_idx):
                # Subcase: supeq is a juxted
                return self._vanish_juxted(0, sup_idx)

            sup[:] = [PVOID]
            self._condtly_correct_scriptop(sup, sup_idx)
            return sup_idx, self._safe_dir(0, None)

        # - Build replacement -
        par_ord = idx[-1]
        repl_c = simpleeqcreator.SimpleEqCreator()
        repl_c.extend(sup[1:par_ord], accept_voids=False)
        par = deepcopy(sup[par_ord])
        if par.is_perm_jb():
            par[0] = TJUXT
        par_pos_in_repl = repl_c.n_inserted_subeqs()
        # If par is a void, include it.
        # -> It will be deleted below and a good selection will be chosen
        repl_c.append(par, accept_voids=True)
        repl_c.extend(sup[par_ord + 1:], accept_voids=False)

        # - Replace -

        # It is assumed that pointed subeq was selected, so no supeq of what is
        # is defined as idx (eff_idx in docstring) can be a GOP-block
        self._replace_integrating(repl_c.get_eq(), sup_idx)

        # - Return useful selection -

        # Note: par was never inserted as a JUXT-block in repl_c so calling
        # repl_c.get_idx with [] as argument is legitimate
        par_idx_in_repl = repl_c.get_idx([], par_pos_in_repl)
        if not self.is_juxted(sup_idx):
            # A non-juxted was replaced by repl
            new_idx = sup_idx + par_idx_in_repl
            if par.is_pvoid():
                return self._vanish_juxted(0, new_idx)
        elif par_idx_in_repl:
            # A juxted was replaced by repl and repl was a juxt-block
            new_idx = sup_idx[:-1] + [sup_idx[-1] + par_idx_in_repl[0] - 1]
            if par.is_pvoid():
                return self._vanish_juxted(0, new_idx)
        else:
            # A juxted was replaced by repl, which was not a juxt-block
            # Note: It is not possible for a pointed VOID to match this case
            new_idx = sup_idx

        new_idx = self.urepr(new_idx, True)
        return new_idx, self._safe_dir(5, 0, new_idx)

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
            del_idx = self._biggest_subeq_same_urepr()
            sup = eqqueries.supeq(del_idx, self.eq, True)
            # Whole eq is pointed
            if sup == -2:
                if self.is_vdir() or (self.is_rdir() and forward) \
                        or ((self.is_ldir() or self.is_odir()) and not forward):
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
                if (self.is_rdir() and not forward) or (
                        self.is_ldir() and forward) \
                        or (self.is_odir() and sup[par_ord] and forward):
                    # Subcase: Delete a non-VOID non-juxted subeq
                    self.idx = self._empty()
                    self.dir = self._safe_dir(0, 0)
                    continue

                # Subacase: Flat non-juxt lop (includes VOID and non-VOID par)
                self.idx, self.dir = self._flat_lopblock(None, sup)
                continue

            # From here, a juxted is pointed
            if self.is_vdir():
                # Subcase: A VOID is selected
                # (This subcase should not happen)
                self.idx, self.dir = self._vanish_juxted()
                continue

            if (not forward and self.is_rdir()) or (forward and self.is_ldir()) \
                    or (self.is_odir() and par_ord != len(sup) - 1):
                # Subcase: Vanish pointed juxted
                self.idx, self.dir = self._vanish_juxted()
                continue

            if self.is_odir() and forward and par_ord == len(sup) - 1 \
                    and sup[par_ord] != utils.void(temp=True):
                # Subcase: Replace non-TVOID last juxted with a TVOID
                self._replace(utils.void(temp=True), del_idx)
                continue

            if forward and len(sup[1:]) > par_ord:
                # Subcase: Delete juxted to the right
                self.idx = self._vanish_juxted(1)[0]
                continue
            if self.is_odir() and not forward and par_ord == 2 == len(sup) - 1 \
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
        eff_pointed_s = self._biggest_subeq_same_urepr(None, True)
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
            eff_pointed_idx = self._biggest_subeq_same_urepr()
            if self.is_odir() or self.is_vdir() or substitute_1st_free_arg:
                # A replacement regardless of whether replacement contains
                # current selection
                self._replace(subeq, eff_pointed_idx)
            elif self.is_rdir():
                ret_idx = self._rinsert(subeq, eff_pointed_idx)
                self.idx = eqqueries.urepr(ret_idx, self.eq)
            else:
                ret_idx = self._linsert(subeq, eff_pointed_idx)
                self.idx = eqqueries.urepr(ret_idx, self.eq)

            if free_args:
                # Select first free arg if it exists in any case
                sel = eqqueries.get(self.idx, self.eq)
                self.idx.append(len(sel) - free_args)
            elif self.is_odir():
                # Select next juxted or create a TVOID if ODIR
                npars_sup = eqqueries.npars(self.eq, self.idx[:-1])
                if eqqueries.isjuxted(self.idx, self.eq) \
                        and npars_sup != self.idx[-1]:
                    self.idx[-1] += 1
                else:
                    self.idx = self._rinsert(utils.void(temp=True))
            self.dir = self._safe_dir(5)

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
        base_idx = self._biggest_subeq_same_urepr()
        # scriptops.insert_script manages correctly a TVOID
        script_idx = scriptops.insert_script(base_idx, self.eq, scriptdir,
                                             is_superscript, script)
        retval = True
        if script_idx[-1] >= 0:
            script_idx[-1] *= -1
            retval = False

        self.idx = eqqueries.urepr(script_idx, self.eq)
        self.dir = self._safe_dir(1)
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

