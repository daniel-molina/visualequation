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
    def __init__(self, eq0=None, sel_index0=None, ovrwrt=False, debug=True):
        super().__init__(deepcopy(eq0))
        # The index of current subeq being selected.
        if sel_index0 is not None:
            self.idx = Idx(sel_index0)
        elif self.is_gopb():
            self.idx = Idx(1)
        else:
            self.idx = Idx()
        # Flag for overwrite mode
        self.ovrwrt = ovrwrt
        self.debug = debug

    def __repr__(self):
        return "EditableEq(" + self._repr_aux(self) + ", " + str(self.idx) \
                + ", " + repr(self.ovrwrt) + ", " + repr(self.debug) + ")"

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

    def _condtly_correct_scriptop(self, newbase, index=-1, refindex=-2):
        """Correct a script-block if index points to a base and it is needed.

            *   Not a supeq-checker
            *   Not a final-idx-checker

        This function is used by those methods with the tag: base-checker.

        :param newbase: The new subeq which will be in pointed subeq.
        :param index: Index of the element which may be a base. -1 -> self.idx.
        :param refindex: Index to return after operation. -2 -> *index*.
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

            *   Not a final-idx-checker
            *   Not a base-checker

        This function is used by methods with the tag: supeq-checker.
        """
        idx = self._safe_idx_arg(index)
        retval = self.biggest_supeq_with_urepr(idx, retidx)
        if retval == -1:
            return idx if retidx else self(idx)
        return retval

    def _rinsert(self, subeq, index=-1):
        """Insert a subeq to the right.

        *   Not a supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        It returns index of _pointed subeq_ after the insertion. Index of
        _inserted subeq_ is retval[:-1] + [retval[-1] + 1].

        .. note::

            It does not care about the particular form of inserted subeq.
        """
        idx = self._safe_idx_arg(index)
        s_new = self._safe_subeq_arg(subeq)
        sel = self(idx)
        sup = self.supeq(idx)
        if sup != -2 and sup.is_perm_jb():
            # Case: pointed subeq is a juxted (included being also juxt-block)
            # Note: Checked in Python doc that insertions after len(L)-1 are
            # allowed
            sup.insert(idx[-1] + 1, s_new)
            return idx

        if sel.is_perm_jb():
            # Case: pointed subeq is a juxt-block JB and is not a juxted
            # => Equivalent to have last juxted of JB pointed
            sel.append(s_new)
            return idx

        # Case: pointed subeq is a non-juxt-block and is not a juxted
        sel[:] = [PJUXT] + [sel[:]] + [s_new]
        return self._condtly_correct_scriptop(sel, idx, idx + [1])

    def _rinsert_integrating(self, juxtblock, index=-1):
        """Integrate juxteds of a jb to the right of pointed subeq.

        *   Not a supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        It returns the pointing index updated after the insertion.

        .. note::

            *juxtblock* must be a juxt-block.
        """
        idx = self._safe_idx_arg(index)
        jb = self._safe_subeq_arg(juxtblock)

        sup = self.supeq(idx)
        s = self(idx)
        if sup.is_jb():
            sup[:] = sup[:idx[-1] + 1] + jb[1:] + sup[idx[-1] + 1:]
            return idx
        else:
            s[:] = [PJUXT] + s[:] + jb[1:]
            return idx + [1]

    def _linsert(self, subeq, index=-1):
        """Insert a subeq to the left.

        *   Not a supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        It returns index of _pointed subeq_ after the insertion. Index of
        _inserted subeq_ is retval[:-1] + [retval[-1] - 1].

        .. note::

            It does not care about the particular form of inserted subeq.
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
            # Case: pointed subeq is a juxt-block but not a juxted
            sel.insert(1, s_new)
            return idx + [1]

        # Case: pointed subeq is a non-juxt-block and is not a juxted
        sel[:] = [PJUXT] + [s_new] + [sel[:]]
        return self._condtly_correct_scriptop(sel, idx, idx + [1])

    def _linsert_integrating(self, juxtblock, index=-1):
        """Integrate juxteds of a jb to the left of pointed subeq.

        *   Not a supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        It returns index of _pointed subeq_ after the insertion.

        .. note::

            *juxtblock* must be a juxt-block.
        """
        idx = self._safe_idx_arg(index)
        jb = self._safe_subeq_arg(juxtblock)

        sup = self.supeq(idx)
        s = self(idx)
        if sup.is_jb():
            sup[:] = sup[:idx[-1]] + jb[1:] + sup[idx[-1]:]
            return idx
        else:
            s[:] = [PJUXT] + jb[1:] + s[:]
            return idx + [len(jb)]

    def _replace_integrating(self, repl, index=-1):
        """Replace a subequation integrating juxteds if appropriated.

        *   supeq-checker
        *   Not a final-idx-checker
        *   base-checker

        .. note::
            *   To replace current selection you should use _replace.

        If *repl* is a PJUXT-block JB and actual subeq being replaced is a
        juxted of a juxt-block EJB, juxteds of JB are integrated as juxteds of
        EJB. Else, it is a normal replacement (which includes the case *repl*
        being a TJUXT-block)

        This method should not be used just to replace actual selection
        because it always integrates if appropriated, never does PJUXT-block ->
        TJUXT-block.

        Return an index and a boolean:
            *   If *repl* is a PJUXT-block and its juxteds are integrated,
                returned index is the one of the last juxted and boolean is
                True. It is assured that index of first juxted coincides with
                pointing index since eq structure is not modified in this case.
            *   Else, index will point to *repl* and boolean will be False.
        """
        # Choose correct subeq to replace
        idx = self._biggest_subeq_same_urepr(index, True)
        s_repl = self._safe_subeq_arg(repl)

        sup = self.supeq(idx)
        s = sup[idx[-1]] if sup != -2 else self(idx)

        if not s_repl.is_perm_jb() or sup == -2 or not sup.is_perm_jb():
            # Case: No juxteds are integrated
            s[:] = s_repl
            return self._condtly_correct_scriptop(s_repl, idx), False

        # Case: some juxteds will be integrated
        sup[:] = sup[:idx[-1]] + s_repl[1:] + sup[idx[-1] + 1:]
        return idx[:-1] + [len(s_repl) - 2], True

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

    def _replace_by_pvoid(self, idx=-1):
        """Replace pointed subeq, or supeq if pointed subeq is a GOP-par, by
        a PVOID.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        It returns the index of inserted PVOID.
        """
        return self._replace([PVOID], idx)

    def _vanish_juxted(self, reljuxted=0, index=-1):
        """Vanish pointed juxted or a cojuxted. It removes the juxt op if only
        one juxted is left in the juxt-block.

        *   Not a supeq-checker
        *   final-idx-checker
        *   base-checker

        If *reljuxted* == n != 0, it vanishes the |n|-th juxted to the right or
        left of pointed juxted depending whether n is positive or negative,
        respectively. Caller must check by itself that referred juxted
        exists.

        Return:

            *   If *reljuxted* != 0, returned value is the final index of
                the pointed (and non-vanished) juxted.
            *   Elif pointed juxted is not a last juxted, the index expected to
                be selected (that is, the final index of the juxted to the
                right of the vanished one before the vanishing, which results
                in its position).
            *   Else, the final index of the juxted to the left before the
                vanishing. Note that in typical cases this method should not be
                used to remove last juxteds, being a replacement by TVOID or
                just doing nothing the appropriated action.

        Return value will have a consistent behavior when several juxteds are
        vanished by pressing successive times DEL or BACKSPACE.

        .. note::

            *   It works also if pointed juxted is not a usubeq.
            *   It does not check supeqs. Pointed subeq MUST be a juxted.
            *   It does NOT implement TVOID management.

        .. note::
            Even if no PVOIDs should appear to the user as juxteds, they can be
            there expecting this method to remove them, as in _flat_out. This
            method will vanish them as with any other subeq.

        .. note::
            Implementation notes:

                *   Do NOT use here any supeq-checker method => Use _set, e.g..
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
            # Note: Usually inappropriate when reljuxted == 0 (read docstring)
            if len(juxtblock) > 3:
                del juxtblock[-1]
                retidx = pointed_idx
                if reljuxted == 0:
                    # Select juxted to the left
                    retidx[-1] -= 1
            else:
                juxtblock[:] = deepcopy(juxtblock[1])
                retidx = self._condtly_correct_scriptop(juxtblock,
                                                        del_idx[:-1])

            return self.urepr(retidx, True)

        if del_idx[-1] == 1:
            # Case: Vanish first juxted
            if len(juxtblock) > 3:
                del juxtblock[1]
                # Select juxted to the right
                retidx = pointed_idx
                if reljuxted != 0:
                    retidx[-1] -= 1
            else:
                juxtblock[:] = deepcopy(juxtblock[2])
                retidx = self._condtly_correct_scriptop(juxtblock,
                                                     pointed_idx[:-1])

            return self.urepr(retidx, True)
        # Case: Intermediate juxted
        del juxtblock[del_idx[-1]]
        retidx = pointed_idx
        if reljuxted < 0:
            retidx[-1] -= 1

        return self.urepr(retidx, True)

    def _dissolve_subjb(self, refindex=None, index=-1):
        """Integrate nested juxteds of pointed juxt-block JB as juxteds of its
        supeq.

        *   Not a supeq-checker
        *   Not a final idx-checker
        *   base-checker (never checked because no base can be involved)

        Return index *refindex* after the operation. It MUST NOT be equal to
        index of JB, but it can be the index of a juxted of JB or their
        subequations.

        .. note::
            It is assumed that the requirements are satisfied.
        """
        refidx = self._safe_idx_arg(refindex)
        idx = self._safe_idx_arg(index)
        ext_jb = self.supeq(idx)
        jb_ord = idx[-1]
        jb = ext_jb[jb_ord]
        jb_level = len(idx)
        jb_n_pars = len(jb) - 1

        ext_jb[jb_ord:jb_ord + 1] = jb[1:]

        if not refidx:
            return []
        elif refidx[:jb_level - 1] != idx[:jb_level - 1] \
                or refidx[jb_level - 1] < idx[jb_level - 1]:
            return refidx
        elif refidx[jb_level - 1] == idx[jb_level - 1]:
            return idx[:-1] \
                   + [jb_ord + refidx[jb_level] - 1] \
                   + refidx[jb_level + 1:]
        else:
            return idx[:-1] \
                   + [refidx[jb_level - 1] + jb_n_pars - 1] \
                   + refidx[jb_level:]

    def _dissolve_tvoid(self, refindex, index=-1):
        """Remove a TVOID and return updated refindex.

        *refindex* must not be the index of pointed TVOID. If *refindex* points
        to the juxt-block of TVOID and it has only two juxteds, return value is
        equivalent to pass the index of the only cojuxted of TVOID.
        """
        refidx = self._safe_idx_arg(refindex)
        idx = self._safe_idx_arg(index)
        closest_juxted_idx_old = idx[:-1] + [idx[-1] - 1]
        closest_juxted_idx = self._vanish_juxted(1, closest_juxted_idx_old)
        if closest_juxted_idx == closest_juxted_idx_old \
                or refidx[:len(idx)] != closest_juxted_idx_old:
            return refidx
        del refidx[len(idx) - 1]
        return refidx

    def _flat(self, index=-1):
        """Dissolve pointed block B while leaving its non-PVOID pars joined
        by a juxt-block if necessary. If every param is PVOID, block B is
        vanished if it was a juxted or replaced by PVOID if it was a
        non-juxted.

        *   Not a supeq-checker, quite the opposite.
        *   final-idx-checker
        *   base-checker

        .. note::
            When a final juxted is vanished, no TVOID is included and return
            value (provided by _vanish_juxted) is probably unuseful.

        *index* can point to any subeq, not necessarily a usubeq. If pointed
        subeq is a GOP-block, it acts on its parameter.

       It returns an updated *index* and a boolean indicating whether some
       operation was applied to the equation.

        .. note::
            No operation is applied if what is pointed is:

                *   A symbol (or 0-args op), or
                *   A juxt-block.
        """
        idx = self.urepr(self._safe_idx_arg(index), True)
        s = self(idx)
        if len(s) == 1 or s.is_jb():
            return self.urepr(idx, True), False

        # From here, s is a block different than a juxt block
        repl_c = simpleeqcreator.SimpleEqCreator()
        repl_c.extend(s[1:], accept_pvoids=False)
        repl = repl_c.get_eq()
        n_insertions = repl_c.n_inserted_subeqs()

        if n_insertions == 0 and self.is_juxted(idx):
            # Case: Every param of lop-s was a PVOID and s is a juxted
            return self._vanish_juxted(0, idx), True

        s[:] = repl[:]
        if self.is_juxted(idx) and s.is_perm_jb():  # s == self(idx)
            s[0] = TJUXT
        new_idx = self._condtly_correct_scriptop(s, idx)
        return self.urepr(new_idx, True), True

    def _flat_out(self, index=-1):
        """Remove leading operator and leave params (joined in a juxt-block if
        necessary).

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        .. note::
            When a final juxted is vanished, no TVOID is included and return
            value (provided by _vanish_juxted) is probably unuseful.

        It returns an updated *index* and a boolean indicating whether some
        operation was applied to the equation.

        Rules:

        Consider eff_s be pointed subeq or its supeq if pointed subeq is a
        GOP-par. Let eff_idx be the index of eff_s.

            *   If every param of lop-eff_s is a PVOID:

                *   If eff_s is a juxted, eff_s is vanished
                *   Else, eff_s is replaced by a PVOID.

            *   Elif eff_s is a juxted, vanish any juxted equal to PVOID.
            *   Else, replace the eff_s with any non-PVOID param, joined
                together by a juxt-block if necessary.

        .. note::

            *   It is expected that no supeq is a TJUXT-block.
            *   It does not matter if pointed subeq is a GOP-par or GOP-block,
                the result is equivalent.
            *   It works fine with TVOIDs (which should be always selected and
                be juxteds).

        Implementation notes:

            *   There should not be PVOIDs in juxt-blocks, but supported by
                now.
            *   It is possible that some methods currently relay on that
                behavior.
            *   Code is still complex, that should be fixed.
        """
        idx = self._biggest_subeq_same_urepr(index, True)
        if not idx:
            return self.urepr(idx, True), False

        # From here:
        #   1. Supeq of idx exists, and
        #   2. Supeq of idx is a usubeq
        sup_idx = idx[:-1]
        sup = self(sup_idx)
        n_void_pars = sup[1:].count([PVOID])
        n_non_void_pars = len(sup) - n_void_pars - 1
        if not n_void_pars and sup.is_perm_jb():
            return self.urepr(idx, True), False

        if not n_non_void_pars:
            # Case: Every param of lop-sup is a PVOID
            if self.is_juxted(sup_idx):
                # Subcase: sup is a juxted
                return self._vanish_juxted(0, sup_idx), True

            # Subcase: sup is not a juxted
            sup[:] = [PVOID]
            ret_idx = self._condtly_correct_scriptop(sup, sup_idx, sup_idx)
            return self.urepr(ret_idx, True), True

        # - Build replacement -
        par_ord = idx[-1]
        repl_c = simpleeqcreator.SimpleEqCreator()
        repl_c.extend(sup[1:par_ord], accept_pvoids=False)
        par = deepcopy(sup[par_ord])
        if par.is_perm_jb():
            par[0] = TJUXT
        par_pos_in_repl = repl_c.n_inserted_subeqs()
        # If *par* is a PVOID, include it.
        # -> It will be deleted below and a good selection will be chosen
        repl_c.append(par)
        repl_c.extend(sup[par_ord + 1:], accept_pvoids=False)

        # - Replace -

        # It is assured that _replace_integrating below will act on sup_idx
        ret_idx, integrated = self._replace_integrating(repl_c.get_eq(),
                                                        sup_idx)

        # - Return useful selection -

        # Note: par was never inserted as a PJUXT-block in repl_c so calling
        # repl_c.get_idx with [] as argument is legitimate
        par_idx_in_repl = repl_c.get_idx([], par_pos_in_repl)

        if not self.is_juxted(ret_idx):
            # Case: A non-juxted was replaced by repl
            new_idx = ret_idx + par_idx_in_repl
            if par.is_pvoid():
                return self._vanish_juxted(0, new_idx), True
        elif integrated:
            # A juxted was replaced by repl and repl was a PJUXT-block, so some
            # juxteds were integrated
            # Note: sup_idx is a valid index for first integrated juxted as
            # documented in _replace_integrating.
            new_idx = sup_idx[:-1] \
                      + [sup_idx[-1] + par_idx_in_repl[0] - 1]
            if par.is_pvoid():
                return self._vanish_juxted(0, new_idx), True
        else:
            # A juxted was replaced by repl, and repl was not a PJUXT-block
            # Note: It is not possible for a pointed PVOID to match this case
            new_idx = ret_idx

        ret_idx = self.urepr(new_idx, True)
        return ret_idx, True

    def _group(self, index=-1):
        """Group a usubeq if necessary.

        *   supeq-checker
        *   final-idx-checker (guaranteed since passed idx must be an usubeq)
        *   base-checker (guaranteed because GOP is transparent for script ops)

        Return a boolean indicating whether a GOP was inserted. If True,
        pointed usubeq is now in pointing index + [1].
        """
        idx = self._safe_idx_arg(index)
        block = self(idx)
        if not block.isb():
            # Case: Pointed subeq is a symbol => No GOP must be set
            return False

        sup = self.supeq(idx)
        if sup != -2 and sup.is_gopb():
            # Case: Pointed block is already a GOP-par
            return False

        block[:] = [GOP, deepcopy(block)]
        return True

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

