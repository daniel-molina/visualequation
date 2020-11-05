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


"""Most important operations to edit an eq.

It is intended to be polished by a safer interface so the application does not
need to call these methods directly.
"""

from typing import Union
from .subeqs import Subeq
from .idx import Idx
from .ops import *
from .scriptops import insert_script, remove_script, update_scriptblock, \
    is_base, is_script
from . import simpleeqcreator


class EqCore(Subeq):
    """Class to edit an equation.

    .. note::
        Methods not starting by underscore will suppose that self.idx points
        to selected equation. As a consequence:

            *   self.idx must point to an usubeq before calling them.
            *   The only supeq of the usubeq pointed by self.idx which may be a
                GOP-block is its 1-level supeq (but strict subeqs may be also
                GOP-blocks).

    Responsibilities:

        *   Methods of this class change self.selm if appropriated.

    Implementation note:
        This is a large class and it is easy to get lost. Let's try to respect
        the following conventions.

            *   Methods starting with underscore (_), apart from being expected
                to be used in a controlled way, they should not modify other
                attributes than self.eq. To mitigate this limitation, they can
                return useful information as the expected self.idx and
                self.selm that should be set under a typical use of the method.

            *   Methods not starting with underscore are intended to be safe
                to call independently of the input. They should set those
                property of this class such that the method is autonomous.

            *   Argument names referring to indices will be based on the word
                'index'.
                Indices defined in the code will be based on the word 'idx'.
                When code does a trivial use of an index argument, it is OK
                to reuse the unmodified index parameter if it is safe to do
                so (remember that special values, such as -1, may be passed).

            *   An index parameter with value of -1 means 'use self.idx'.
                In any other case, it will be understood as a valid argument to
                initialize a Idx.

        Definitions:

            *   A method which assures that returned or set index points always
                to an usubeq with correct selm is known as a
                'final-sel-checker'.

            *   A method which assures that operation will not change a base
                without correcting the correspondent script op is known as a
                'base-checker'.
    """
    def __init__(self, eq: Optional[list] = None, idx: Optional[list] = None,
                 selm: SelMode = SelMode.LCUR,
                 ovrwrt: bool = False, debug: bool = True):
        super().__init__(deepcopy(eq))
        # The index of current subeq being selected.
        if idx is not None:
            self.idx = Idx(idx)
        elif self.is_perm_jb():
            self.idx = Idx(1)
        else:
            self.idx = Idx()
        self.selm = selm
        self.ovrwrt = ovrwrt
        self.debug = debug

    def _repr_aux(self):
        s_repr = self._repr_elem(self) + ", " + str(self.idx) \
                 + ", " + str(self.selm)
        if self.ovrwrt:
            s_repr += ", ovrwrt=True"
        if not self.debug:
            s_repr += ", debug=False"
        return s_repr

    def __repr__(self):
        return "EqCore(" + self._repr_aux(self) + ")"

    def _idx_arg(self, index=-1):
        """Return an Idx based on passed value.

        If *index* is -1, a copy of self.idx is returned.
        Else, Idx(*index*) is returned.
        """
        return self.idx[:] if index == -1 else Idx(index)

    def _refidx_arg(self, refindex=-2, index=-1):
        """Return an Idx bassed on passed value (suited for refindices).

        If *refindex* is -2, return _safe_idx_arg(*index*).
        Else, return _safe_idx_arg(*refindex*).

        .. note::
            *refindex in (-1, None) are valid values.
        """
        if refindex == -2:
            return self._idx_arg(index)
        return self._idx_arg(refindex)

    def _subeq_arg(self, subeq=0, index=-1):
        """Return a deepcopy of a subequation.

        If *subeq* is not 0, return a Subeq constructed with a deepcopy of
        *subeq*.

        Elif *index* is -1, return a deepcopy of self(self.idx).

        Else, return a deepcopy of self(index).
        """
        if subeq != 0:
            return deepcopy(Subeq(subeq))
        if index != -1:
            return deepcopy(self(index))
        return deepcopy(self(self.idx))

    def _set(self, elem, index=-1):
        """A 'hard' replacement.

        If replacement is a JUXT-block, it will be replaced as a whole.

            *   Not a final-sel-checker
            *   Not a base-checker

        Replacement is always done in pointed subeq.
        """
        self(index if index != -1 else self.idx)[:] = deepcopy(elem)

    def is_hl(self):
        """Return whether pointed subeq is highlighted."""
        return self.selm in (SelMode.RHL, SelMode.LHL)

    def is_cur(self):
        """Return whether pointed subeq displays a cursor."""
        return self.selm in (SelMode.RCUR, SelMode.LCUR)

    def is_rhl(self):
        return self.selm is SelMode.RHL

    def is_lhl(self):
        return self.selm is SelMode.LHL

    def is_rcur(self):
        return self.selm is SelMode.RCUR

    def is_lcur(self):
        return self.selm is SelMode.LCUR

    def is_r(self):
        return self.selm in (SelMode.RCUR, SelMode.RHL)

    def is_l(self):
        return self.selm in (SelMode.LCUR, SelMode.LHL)

    def _correctly_point(self, index=-1, right_pref=False):
        """Return a valid index and SelMode.

            *   Implements final-sel-checker
            *   base-checker.
        """
        idx = self._idx_arg(index)
        s = self(idx)
        if s.is_perm_jb():
            if right_pref:
                return idx + [s.last_par_ord()], SelMode.RCUR
            return idx + [1], SelMode.LCUR
        if not right_pref or s.is_void():
            return idx, SelMode.LCUR
        if self.is_nonlastjuxted(idx):
            return idx.nextpar(), SelMode.LCUR
        return idx, SelMode.RCUR

    def _dissolve_temp_jb(self, index: Union[list, int] = -1,
                          refindex: Union[list, int] = -2):
        """Dissolve a tjuxt-block.

        Return an updated *refindex*.

        .. note::
            Pointed subeq must be a tjuxt-block.

        .. note::
            *refindex* cannot be equal to pointing index if associated
            tjuxt-block is a juxted.
        """
        idx = self._idx_arg(index)
        refidx = self._refidx_arg(refindex, index)
        tjb = self(idx)
        if not self.is_juxted(idx):
            tjb[0] = tjb[0].equiv_pjuxt()
            return refidx

        if refidx == idx:
            raise ValueError("refindex cannot point to the tjuxt-block if it "
                             "is a juxted.")
        self._replace_integrating(tjb, idx)
        if refidx[:len(idx)] != idx:
            return refidx
        return refidx[:len(idx) - 1] \
            + [refidx[len(idx) - 1] + refidx[len(idx)] - 1] \
            + refidx[len(idx) + 1:]

    def _condtly_correct_scriptop(self, newbase, index=-1, refindex=-2):
        """Correct a script-block if index points to a base and it is needed.

            *   Not a final-sel-checker
            *   Implements base-checker

        This function should used by those methods with the tag: base-checker.

        Return an updated *refindex*.

        :param newbase: The new subeq which will be in pointed subeq.
        :param index: Index of the element which may be a base.
        :param refindex: Index to return after operation.
        """
        idx_base = self._idx_arg(index)
        refidx = self._refidx_arg(refindex, index)
        if is_base(self, idx_base):
            return update_scriptblock(Subeq(newbase), self,
                                      idx_base[:-1], refidx)
        return refidx

    def _rinsert(self, subeq, index=-1):
        """Insert a subeq to the right.

        *   Not a final-sel-checker
        *   base-checker

        Return index of _inserted subeq_. Index of originally _pointed subeq_
        after insertion is retval.prevpar().

        .. note::
            It does not care about the particular form of inserted subeq.
        .. note::
            Pointed subeq must not be a juxt-block.
        """
        idx = self._idx_arg(index)
        s_new = self._subeq_arg(subeq)
        s = self(idx)
        sup = self.supeq(idx)
        if sup != -2 and sup.is_perm_jb():
            # Case: pointed subeq is a juxted
            # Note: Checked in Python doc that insertions after len(L)-1 are
            # legitimate
            idx.nextpar(set=True)
            sup.insert(idx[-1], s_new)
            sup[0].current_n += 1
            return idx

        # Case: pointed subeq is not a juxted
        s[:] = [PJuxt()] + [s[:], s_new]
        return self._condtly_correct_scriptop(s, idx, idx + [2])

    def _rinsert_integrating(self, juxtblock, index=-1):
        """Integrate juxteds of a jb to the right of pointed subeq.

        *   Not a final-sel-checker
        *   base-checker

        Return the index of _last introduced juxted_ (integrated or not).

        Index of _pointed subeq_ after insertion is:
        retval[:-1] + [retval[ -1] - len(*juxtblock*) + 1].

        .. note::
            *juxtblock* must be a juxt-block.
        .. note::
            Pointed subeq must not be a juxt-block.
        """
        idx = self._idx_arg(index)
        jb = self._subeq_arg(juxtblock)

        sup = self.supeq(idx)
        s = self(idx)
        if sup == -2 or not sup.is_jb():
            s[:] = [PJuxt(len(jb))] + [s[:]] + jb[1:]
            return idx + [len(jb)]

        sup[:] = sup[:idx.nextord()] + jb[1:] + sup[idx.nextord():]
        sup[0].current_n += len(jb) - 1
        return idx[:-1] + [idx[-1] + len(jb) - 1]

    def _linsert(self, subeq, index=-1):
        """Insert a subeq to the left.

        *   Not a final-sel-checker
        *   base-checker

        It returns index of _pointed subeq_ after the insertion. Index of
        _inserted subeq_ is retval.prevpar().

        .. note::
            It does not care about the particular form of inserted subeq.
        .. note::
            Pointed subeq must not be a juxt-block.
        """
        idx = self._idx_arg(index)
        s_new = self._subeq_arg(subeq)

        s = self(idx)
        sup = self.supeq(idx)
        if sup != -2 and sup.is_perm_jb():
            # Case: pointed subeq is a juxted
            # Note: Checked in doc that insertions after len(L)-1 are allowed
            sup.insert(idx[-1], s_new)
            sup[0].current_n += 1
            return idx.nextpar()

        # Case: pointed subeq is not a juxted
        s[:] = [PJuxt()] + [s_new, s[:]]
        return self._condtly_correct_scriptop(s, idx, idx + [2])

    def _linsert_integrating(self, juxtblock, index=-1):
        """Integrate juxteds of a jb to the left of pointed subeq.

        *   Not a final-sel-checker
        *   base-checker

        It returns index of _pointed subeq_ after the insertion.
        Index of last integrated juxted is retval.prevpar().

        .. note::
            *juxtblock* must be a juxt-block.
        .. note::
            Pointed subeq must not be a juxt-block.
        """
        idx = self._idx_arg(index)
        jb = self._subeq_arg(juxtblock)

        sup = self.supeq(idx)
        s = self(idx)
        if sup == -2 or not sup.is_jb():
            s[:] = [PJuxt(len(jb))] + jb[1:] + [s[:]]
            return idx + [len(jb)]

        sup[:] = sup[:idx[-1]] + jb[1:] + sup[idx[-1]:]
        sup[0].current_n += len(jb) - 1
        return idx[:-1] + [idx[-1] + len(jb) - 1]

    def _replace_integrating(self, juxtblock, index=-1):
        """Replace a subequation with juxteds of a juxt-block.

        *   Not a final-sel-checker
        *   base-checker

        If pointed subeq is not a juxted, it is replaced by *juxtblock*.
        In particular, the type of the *juxtblock* is not modified (t/p-juxt).

        If pointed subeq is a juxted, it is replaced by every juxted included
        in *juxtblock*.

        Return an index and a bool:

            *   If juxteds of *juxtblock* are effectively integrated, the
                index of the last juxted of *juxtblock* in eq is returned.
                Bool will be True.
                Note: It is assured that index of first juxted coincides with
                pointing index since eq structure is not modified in this case.
            *   Else, index will point to *juxtblock* and bool will be False.
        """

        idx = self._idx_arg(index)
        r = self._subeq_arg(juxtblock)

        sup = self.supeq(idx)
        s = self(idx)

        if sup == -2 or not sup.is_jb():
            # Case: No juxteds are integrated
            s[:] = r
            return self._condtly_correct_scriptop(r, idx), False

        # Case: some juxteds will be integrated
        sup[:] = sup[:idx[-1]] + r[1:] + sup[idx[-1] + 1:]
        sup[0].current_n += len(r) - 2
        return idx[:-1] + [idx[-1] + len(r) - 2], True

    def _replace(self, repl, index=-1):
        """Replace pointed subeq.

        *   Not a final-sel-checker
        *   base-checker

        Return pointing index after the operation.
        """

        r = self._subeq_arg(repl)
        new_idx = self._condtly_correct_scriptop(r, index, index)
        self._set(r, new_idx)
        return new_idx

    def _replace_by_void(self, index=-1):
        """Replace pointed subeq by the correct void (PVOID or RVOID).

        *   Not a final-sel-checker
        *   base-checker

        Return the index of inserted void.
        """
        idx = self._idx_arg(index)
        if is_script(self, idx):
            return self._replace([RVOID], idx)
        return self._replace([PVOID], idx)

    def _vanish_juxted(self, reljuxted=0, index=-1):
        """Vanish pointed juxted or a cojuxted. It removes the juxt op if only
        two juxted are present before the operation.

        *   final-sel-checker
        *   base-checker

        If *reljuxted* == n != 0, it vanishes the |n|-th juxted to the right or
        left of pointed juxted depending whether n is positive or negative,
        respectively. Caller must check by itself that referred juxted exists.

        Return expected index and SelMode if pointed subeq was selected. In
        particular:

            *   If *reljuxted* != 0, return value is current selection
                unmodified except for structure corrections of eq.
            *   Elif pointed juxted is not a last juxted, the index of the
                juxted originally to the right of the vanished one and
                SelMode.LCURSOR.
            *   Else, the index of the juxted originally to the left of the
                vanished one and SelMode.RCURSOR (independently of self.selm).

        Return value is intended to have an intuitive behavior when several
        juxteds are vanished by pressing successive times DEL or BACKSPACE.

        .. note::
            It does not check supeqs. Pointed subeq MUST be a juxted.

        .. note::
            Even if no voids should appear to the user as juxteds, they can be
            there expecting this method to remove them, as in _flat_out. This
            method will vanish them as with any other subeq.

        .. note::
            Implementation notes:

                *   Pointed subeq cannot be a base because it must be a juxted
                    and juxted cannot be bases, but the juxt-block can.
        """
        # Pointed juxted
        pointed_idx = self._idx_arg(index)
        # Juxted to delete (may be pointed juxted)
        del_idx = pointed_idx[:-1] + [pointed_idx[-1] + reljuxted]
        jb = self.supeq(del_idx)

        if len(jb) == del_idx[-1] + 1:
            # Case: Vanish a last juxted
            if len(jb) > 3:
                del jb[-1]
                jb[0].current_n -= 1
                retidx = pointed_idx
                if reljuxted == 0:
                    retidx[-1] -= 1
            else:
                jb[:] = deepcopy(jb[1])
                retidx = self._condtly_correct_scriptop(jb, del_idx[:-1])

            return retidx, SelMode.RCUR

        if del_idx[-1] == 1:
            # Case: Vanish first juxted
            if len(jb) > 3:
                del jb[1]
                jb[0].current_n -= 1
                retidx = pointed_idx
                if reljuxted != 0:
                    retidx[-1] -= 1
            else:
                jb[:] = deepcopy(jb[2])
                retidx = self._condtly_correct_scriptop(jb, pointed_idx[:-1])

            return retidx, SelMode.LCUR
        # Case: Intermediate juxted
        del jb[del_idx[-1]]
        jb[0].current_n -= 1
        retidx = pointed_idx
        if reljuxted < 0:
            retidx[-1] -= 1

        return retidx, SelMode.LCUR

    # Not tested from here!

    def _flat(self, index=-1):
        """Remove lop of pointed block, joining its non-void pars in a jb.

        If pointed subeq is not a block or it is a juxt-block, nothing is done.

        If every param of pointed block B is a void:

            *   If B is is a juxted, B is vanished.
            *   Else, B is replaced by a void.

        *   final-sel-checker
        *   base-checker

        Return an updated *index* and selm or None (None means that no
        operation was applied).

        .. note::
            Probably the caller does not want to call this method on individual
            juxteds if they are not highlighted and instead, use this method
            on every juxted. However, that is up to the caller.

        .. note::
            A tjuxt-block is created when selection is highlighted and subeq to
            replace is a a pjuxt-block.
        """
        idx = self._idx_arg(index)
        s = self(idx)
        if len(s) == 1 or s.is_jb():
            return

        # From here, s is a block different than a juxt block
        repl_c = simpleeqcreator.SimpleEqCreator()
        repl_c.extend(s[1:], accept_voids=False)
        repl = repl_c.get_eq()
        n_insertions = repl_c.n_inserted_subeqs()

        if n_insertions == 0:
            if self.is_juxted(idx):
                # Case: Every param of lop-s was a void and s is a juxted
                return self._vanish_juxted(0, idx)
            else:
                return self._replace_by_void(idx), SelMode.LCUR

        # Note: repl cannot be a tjuxt-block
        if self.is_juxted(idx) and repl.is_perm_jb():  # s == self(idx)
            if self.is_hl():
                # Case: Selection is a juxted, highlighted and repl is a pjb.
                repl[0] = repl[0].equiv_tjuxt()
                return self._replace(repl, idx), self.selm
            # Case: Selection is a juxted, not highlighted and repl is a pjb.
            ret_idx = self._replace_integrating(repl, idx)[0]
            if self.is_rcur():
                return ret_idx, self.selm
            # Note: idx points to 1st juxted (_replace_integrating doc)
            return idx, self.selm

        if self.is_juxted(idx):
            # Case: Selection is a juxted and repl is not a jb.
            return self._replace(repl, idx), self.selm

        if self.is_hl() and repl.is_perm_jb():
            # Case: selection is not a juxted, is highlighted and repl is a pjb
            repl[0] = repl[0].equiv_tjuxt()
            return self._replace(repl, idx), self.selm

        if repl.is_perm_jb():
            # Case: selection is not a juxted, is not highlighted and repl is a
            # pjb
            ret_idx = self._replace(repl, idx)
            return self._correctly_point(ret_idx, self.is_r())

        # Case: selection is not a juxted, is not highlighted and repl is
        # not a pjb
        return self._replace(repl, idx), self.selm

    def _flat_supeq(self, index=-1):
        """Remove leading operator of supeq, joining its params in a jb.

        *   final-sel-checker
        *   base-checker

        It returns an updated *index* and SelMode supposing that it acts on
        current selection. If no operation is applied, None is returned
        instead.

        Behaviour: Consider pointed subeq S.

            *   If its supeq does not exist, nothing is done.
            *   Else, consider its supeq SUP:

                *   If every param of lop-SUP is a void:

                    *   If SUP is a juxted, SUP is vanished
                    *   Else, SUP is replaced by a void.

                *   Elif SUP is a juxted, vanish any cojuxted equal to void
                    (legacy behaviour).
                *   Else, replace SUP with any non-void param of lop-SUP,
                    being params joined together by a pjuxt-block if necessary.

        Implementation notes:

            *   There should not be voids in juxt-blocks, but it works by
                now.
            *   Code is complex. That should be fixed.
        """
        idx = self._idx_arg(index)
        if not idx:
            return

        # From here, supeq of idx exists
        sup_idx = idx[:-1]
        sup = self(sup_idx)
        n_void_pars = self.n_voids(sup_idx)
        n_non_void_pars = len(sup[1:]) - n_void_pars
        if n_void_pars == 0 and sup.is_perm_jb():
            # Case: A juxted is selected and no co-juxted is void
            return None

        if n_non_void_pars == 0:
            # Case: Every param of lop-sup is a void
            if self.is_juxted(sup_idx):
                # Subcase: sup is a juxted
                return self._vanish_juxted(0, sup_idx)

            # Subcase: sup is not a juxted
            return self._replace_by_void(sup_idx), SelMode.LCUR

        # - Build replacement -
        par_ord = idx[-1]
        repl_c = simpleeqcreator.SimpleEqCreator()
        repl_c.extend(sup[1:par_ord], accept_voids=False)
        par = deepcopy(sup[par_ord])
        if par.is_perm_jb():
            par[0] = par[0].equiv_tjuxt()
        par_pos_in_repl = repl_c.n_inserted_subeqs()
        # If *par* is a void, include it.
        # -> It will be deleted below and a good selection will be chosen
        repl_c.append(par)
        repl_c.extend(sup[par_ord + 1:], accept_voids=False)

        # - Replace -
        repl = repl_c.get_eq()
        if repl.is_jb():
            ret_idx, integrated = self._replace_integrating(repl, sup_idx)
        else:
            integrated = False
            ret_idx = self._replace(repl, sup_idx)

        # - Return useful selection -

        # Note: par was never inserted as a pjuxt-block in repl_c so calling
        # repl_c.get_idx with [] as argument is legitimate
        par_idx_in_repl = repl_c.get_idx([], par_pos_in_repl)

        if not self.is_juxted(ret_idx):
            # Case: A non-juxted was replaced by repl
            new_idx = ret_idx + par_idx_in_repl
            if par.is_void():
                return self._vanish_juxted(0, new_idx)
        elif integrated:
            # A juxted was replaced by repl and repl was a pjuxt-block, so some
            # juxteds were integrated
            # Note: sup_idx is a valid index for first integrated juxted as
            # documented in _replace_integrating.
            new_idx = sup_idx[:-1] \
                      + [sup_idx[-1] + par_idx_in_repl[0] - 1]
            if par.is_void():
                return self._vanish_juxted(0, new_idx)
        else:
            # A juxted was replaced by repl, and repl was not a PJUXT-block
            # Note: It is not possible for a pointed void to match this case
            new_idx = ret_idx

        if self.is_hl():
            return new_idx, self.selm
        return self._correctly_point(new_idx, self.is_rcur())

