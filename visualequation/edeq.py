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

from functools import wraps

from . import eqdebug
from .eqcore import EqCore
from .scriptops import *
from .ops import *
from .eqhist import EqHist


class NewEqState(Enum):
    """Class of return values for main methods of EdEq.

    IDENTICAL: Nor equation nor selection has been modified.
    SEL_CHANGED: Selection modified, but apparently not the equation.
    EQ_CHANGED Equation modified (and maybe selection).

    "Selection" includes self.idx and self.selm.

    An eq has not been "apparently modified" if Subeq(self) is the same or:

        *   pjuxt-block <-> tjuxt-block
        *   tjuxt-block <-> integrated juxteds
    """
    IDENTICAL = auto()
    SEL_MODIFIED = auto()
    EQ_MODIFIED = auto()


UL = Op(r"\underline{{{0}}}")
LCARET = Op(r"\left\vert {0} \right.")
RCARET = Op(r"\left. {0} \right\vert")
OCARET = Op(r"\begingroup\color{{red}}\left\vert {0} \right.\endgroup")
LH = Op(r"\begingroup\color{{blue}}\left\vert {0} \right.\endgroup")
RH = Op(r"\begingroup\color{{blue}}\left. {0} \right\vert\endgroup")

def eq2display(func):
    """Display equation image after operation.

    .. note::
        Return values of function are being discarded. This fact must be
        considered to decide the decorator order (this one should be the most
        external).
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)

        eq2disp = deepcopy(Subeq(self))
        if self.is_lcur() and self.ovrwrt:
            eq2disp(self.idx)[:] = [OCARET, self(self.idx[:])]
        elif self.is_lcur():
            eq2disp(self.idx)[:] = [LCARET, self(self.idx[:])]
        elif self.is_rcur():
            eq2disp(self.idx)[:] = [RCARET, self(self.idx[:])]
        elif self.is_lhl():
            eq2disp(self.idx)[:] = [LH, self(self.idx[:])]
        else:
            eq2disp(self.idx)[:] = [RH, self(self.idx[:])]
        return eq2disp

    return wrapper


def add2hist(func):
    """Update history according to function return value.

    Rules according to return value:
        *   If IDENTICAL, history is not modified.
        *   If SEL_MODIFIED, final state is added to history.
        *   If EQ_MODIFIED, current history entry is updated with initial
            state and final state is added afterwards.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # It is not know in advance whether eq will be modified by func
        init_eq = deepcopy(Subeq(self))
        init_idx = self.idx[:]
        init_rcursor = self.selm
        new_state = func(self, *args, **kwargs)
        if new_state is NewEqState.IDENTICAL:
            return new_state
        if new_state is NewEqState.EQ_MODIFIED:
            self.hist.ovrwrt_current(init_eq, init_idx, init_rcursor)
        self.hist.add(deepcopy(Subeq(self)), self.idx[:], self.selm)
        return new_state
    return wrapper


class EdEq(EqCore):
    """A class that allows a user to edit and navigate an equation by using a
    safe interface.

    Most of methods return a NewEqState for decorator add2hist:

        *   If eq and and selection are not modified at all, IDENTICAL.
        *   If selection is modified but, at least apparently, not eq,
            SEL_MODIFIED.
        *   If eq is modified, EQ_MODIFIED.

    "Selection" includes self.idx and self.selm.

    "An eq has not been apparently modified" if Subeq(self) is the same or:

        *   pjuxt-block <-> tjuxt-block
        *   tjuxt-block <-> integrated juxteds

    Implementation notes:

        *   self.idx must always point to a subeq which is not a pjuxt-block.
    """
    @eqdebug.debuginit
    def __init__(self, eq: list = None, idx: Optional[Idx] = None,
                 selm: SelMode = SelMode.LCUR,
                 ovrwrt: bool = False, debug: bool = True,
                 uld: int = 0, hist: Optional[EqHist] = None):
        super().__init__(eq, idx, selm, ovrwrt, debug)
        # ulevel diff
        self.uld = uld
        if hist is None:
            self.hist = EqHist(deepcopy(Subeq(eq)), self.idx[:], self.selm)
        else:
            self.hist = deepcopy(hist)

    def get_subeq(self, index=-1):
        """Return a deep copy of eq.

        If *index* is:

            *   -1, return current selection.
            *   None or [], return whole eq.
        """
        return Subeq(self._subeq_arg(0, index))

    @eq2display
    def get_eq2display(self):
        """Dummy function to get the equation to display.

        .. note::
            This should only be used in particular cases in which current
            eq to be displayed is not returned (for example, just after
            construction).
        """
        pass

    def _repr_aux(self):
        s_repr = super()._repr_aux()
        if self.uld != 0:
            s_repr += ", uld=" + repr(self.uld)
        if self.hist != EqHist(Subeq(self), self.idx[:], self.selm):
            s_repr += ", hist=" + repr(self.hist)
        return s_repr

    def __repr__(self):
        return "EdEq(" + self._repr_aux(self) + ")"

    def _reset_method_attrs(self, uld=0):
        """Reset all or part of variables managing the preferences of
        movements, and other method-specific attributes.

        Parameters holding value -1 means will use current value of attribute.
        """
        if uld != -1:
            self.uld = uld

    def _change_sel(self, new_index, right_pref: bool, hl = False,
                    current_index: Union[list, int] = -1):
        """Modify current selection safely.

        If current selection is a tjuxt-block, it is dissolved or tranformed
        into a pjuxt-block if reasonable. If final selection is a pjuxt-block,
        it is transformed to a tjuxt-block if *hl* is True or first or last
        juxted is pointed instead according to *right_pref*.

        .. note::
            If a tjuxt-block which is a juxted is selected and *hl* is False,
            *new_index* must not point to current index.

        *new_index* is the subeq to which move the cursor. If that is a
        pjuxt-block, its first or last juxted is considered.

        *right_pref* specifies to which side of pointed subeq the cursor must
        be placed.

        *hl* indicates if final selection will be highlighted.

        *current_index* should be always -1, but it is left as a parameter
        for strange situations.
        """
        current_idx = self._idx_arg(current_index)
        current_s = self(current_idx)
        new_idx = self._idx_arg(new_index)
        new_s = self(new_idx)

        if current_s.is_temp_jb():
            if hl and new_idx == current_idx:
                self.selm = SelMode.RHL if right_pref else SelMode.LHL
                return
            new_idx = self._dissolve_temp_jb(current_idx, new_idx)

        if not hl:
            self.idx[:], self.selm = self._correctly_point(new_idx, right_pref)
            return

        if new_s.is_perm_jb():
            new_s[0] = new_s[0].equiv_tjuxt()
        self.idx[:] = new_idx
        self.selm = SelMode.RHL if right_pref else SelMode.LHL

    @eq2display
    @eqdebug.debug
    def set_ovrwrt(self, value=True):
        if value == self.ovrwrt:
            return NewEqState.IDENTICAL
        self.ovrwrt = value
        return NewEqState.SEL_MODIFIED

    @eq2display
    @eqdebug.debug
    @add2hist
    def select_all(self):
        self._reset_method_attrs()
        self._change_sel([], False, True)
        return NewEqState.SEL_MODIFIED

    @eq2display
    @eqdebug.debug
    @add2hist
    def move2mate(self, right, pbc):
        """Select mate to the left/right.

        If a change of direction has sense, do that instead of selecting a new
        mate.
        """
        self._reset_method_attrs(uld=-1)

        if self.is_lcur() and right and not self.is_nonlastjuxted(self.idx):
            self.selm = SelMode.RCUR
            return NewEqState.SEL_MODIFIED

        if self.is_rcur() and not right:
            self.selm = SelMode.LCUR
            return NewEqState.SEL_MODIFIED

        retval = self.mate(self.idx, right, self.uld, True)
        if retval != -1:
            self._change_sel(retval[0], not right)
            self.uld = retval[1]
            return NewEqState.SEL_MODIFIED

        if not pbc:
            return NewEqState.IDENTICAL

        ul = self.uld + self.ulevel(self.idx)
        self._change_sel(self.boundary_mate(ul, not right, True), not right)
        return NewEqState.SEL_MODIFIED

    @eq2display
    @eqdebug.debug
    @add2hist
    def move2symb(self, right, pbc):
        """Select the closest symbol.

        If pbc is True, periodic boundary conditions apply.

        .. note::
            Implementation has been delayed!!!
            For sure it does not work.
        """
        self._reset_method_attrs()

        if self.is_lcur() and right and not self.is_nonlastjuxted(self.idx):
            self.selm = SelMode.RCUR
            return NewEqState.SEL_MODIFIED

        if self.is_rcur() and not right:
            self.selm = SelMode.LCUR
            return NewEqState.SEL_MODIFIED

        ret_mate = self.mate(self.idx, right, 0, True)
        if ret_mate != -1:
            idx = ret_mate[0]
        elif pbc:
            return NewEqState.IDENTICAL
        else:
            idx = Idx()

        new_idx = self.boundary_symbol(last=not right, retindex=True)
        self._change_sel(new_idx, not right)
        return NewEqState.SEL_MODIFIED

    @eq2display
    @eqdebug.debug
    @add2hist
    def rmove(self):
        """Move to a subequation to the right."""
        self._reset_method_attrs()

        if not self.idx and self.is_pvoid():
            # Case: Whole eq is empty
            return NewEqState.IDENTICAL

        if self.is_hl():
            # Case: Selection is highlighted
            self._change_sel(self.idx, True)
        elif self.isb(self.idx) and self.is_lcur():
            # Case: Selection is a block with LCUR
            arg_ord = self(self.idx)[0].rstep()
            self._change_sel(self.idx + [arg_ord], False)
        elif self.is_juxted(self.idx):
            if not self.isb(self.idx) and self.is_lcur():
                # Case: Selection is a juxted and symbol with LCUR.
                self._change_sel(self.idx, True)
            elif len(self.idx) == 1:
                # Case: Selection is a juxted of whole eq with RCUR
                self._change_sel([1], False)
            else:
                # Case: Selection is a juxted which pjb is not eq with RCUR
                arg_ord = self(self.idx[:-2])[0].rstep(self.idx[-2])
                if arg_ord is None:
                    self._change_sel(self.idx[:-2], True)
                else:
                    self._change_sel(self.idx[:-2] + [arg_ord], False)
        elif not self.isb(self.idx) and not self.is_pvoid(self.idx) \
                and self.is_lcur():
            # Case: Selection is a non-juxted non-PVOID symbol with LCUR
            self._change_sel(self.idx, True)
        elif not self.idx:
            # Case: Selection is a non-PVOID eq with RCUR
            self._change_sel(self.idx, False)
        else:
            # Case: Selection is not eq and (non-juxted with RCUR or PVOID)
            arg_ord = self(self.idx[:-1])[0].rstep(self.idx[-1])
            if arg_ord is None:
                self._change_sel(self.idx[:-1], True)
            else:
                self._change_sel(self.idx[:-1] + [arg_ord], False)

        return NewEqState.SEL_MODIFIED

    @eq2display
    @eqdebug.debug
    @add2hist
    def lmove(self):
        """Move to a subequation to the left."""
        self._reset_method_attrs()

        if not self.idx and self.is_pvoid():
            # Case: Whole eq is empty
            return NewEqState.IDENTICAL

        if self.is_hl():
            # Case: Selection is highlighted
            self._change_sel(self.idx, False)
        elif self.isb(self.idx) and self.is_rcur():
            # Case: Selection is a block with RCUR
            arg_ord = self(self.idx)[0].lstep()
            self._change_sel(self.idx + [arg_ord], True)
        elif self.is_rcur():
            # Case: Selection is a symbol with RCUR
            self._change_sel(self.idx, False)
        elif self.is_juxted(self.idx) and self.idx[-1] == 1:
            if len(self.idx) == 1:
                # Case: Selection is a first juxted of whole eq
                self._change_sel(len(self) - 1, True)
            else:
                # Case: Selection is a first juxted which pjb is not eq
                arg_ord = self(self.idx[:-2])[0].lstep(self.idx[-2])
                if arg_ord is None:
                    self._change_sel(self.idx[:-2], False)
                else:
                    self._change_sel(self.idx[:-2] + [arg_ord], True)
        elif self.is_juxted(self.idx):
            lidx = self.idx.prevpar()
            if self.isb(lidx):
                # Case: Selection is a non-first juxted and juxted to the left
                # is a block
                arg_ord = self(lidx)[0].lstep()
                self._change_sel(lidx + [arg_ord], True)
            else:
                # Case: Selection is a non-first juxted and juxted to the left
                # is a symbol
                self._change_sel(lidx, False)
        elif not self.idx:
            # Case: Selection is (non-juxted) whole eq with LCUR
            self._change_sel([], True)
        else:
            # Case: Selection is not eq and non-juxted with LCUR
            arg_ord = self(self.idx[:-1])[0].lstep(self.idx[-1])
            if arg_ord is None:
                self._change_sel(self.idx[:-1], False)
            else:
                self._change_sel(self.idx[:-1] + [arg_ord], True)

        return NewEqState.SEL_MODIFIED

    def _vmove(self, index, up):
        if not index:
            # Maybe it could send some signal to UI to select eq above??
            return NewEqState.IDENTICAL
        if up:
            retval = self(index[:-1])[0].ustep(index[-1], self.selm)
        else:
            retval = self(index[:-1])[0].dstep(index[-1], self.selm)

        if retval is not None:
            self.idx[:] = index[:-1] + [retval]
            self.selm = SelMode.LCUR
            return NewEqState.SEL_MODIFIED
        return self._vmove(index[:-1], up)

    @eq2display
    @eqdebug.debug
    @add2hist
    def umove(self):
        return self._vmove(self.idx, True)

    @eq2display
    @eqdebug.debug
    @add2hist
    def dmove(self):
        return self._vmove(self.idx, False)

    def _remove_eq_core(self):
        """Helper to remove the whole eq.

        If eq is PVOID, just return IDENTICAL.
        Else:

            *   Set it to [PVOID].
            *   Set self.idx and self.selm properly.
            *   Return EQ_MODIFIED.
        """
        if self.is_pvoid():
            return NewEqState.IDENTICAL
        self.idx[:] = []
        self.selm = SelMode.LCUR
        self._set([PVOID])
        return NewEqState.EQ_MODIFIED

    @eq2display
    @eqdebug.debug
    @add2hist
    def remove_eq(self):
        """Replace the whole eq with a [PVOID]."""
        self._reset_method_attrs()
        return self._remove_eq_core()

    @eq2display
    @eqdebug.debug
    def reset_eq(self, new_subeq=None):
        """Start a new equation, discarding history.

        It does not return meaningful values because it is not managed by
        add2hist.

        .. note::
            eq and index may remain identical if the first one is equal to []
            and the second one equal to Subeq(new_subeq).
        """
        self._reset_method_attrs()
        if new_subeq is None:
            self._remove_eq_core()
        else:
            self.idx[:] = []
            self.selm = SelMode.LCUR
            self[:] = deepcopy(new_subeq)
        self.hist.reset(deepcopy(Subeq(self)), self.idx, self.selm)

    @eq2display
    @eqdebug.debug
    def undo(self):
        retval = self.hist.get_prev()
        if retval is not None:
            self[:], self.idx[:], self.selm = retval

    @eq2display
    @eqdebug.debug
    def redo(self):
        retval = self.hist.get_next()
        if retval is not None:
            self[:], self.idx[:], self.selm = retval

    @eq2display
    @eqdebug.debug
    @add2hist
    def delete_subeq(self, forward):
        """Standard forward/Backward clever delete.

        *   final-idx-checker
        *   base-checker
        """
        self._reset_method_attrs()

        if self.is_hl():
            # Case: Selection is highlighted
            if self.is_juxted(self.idx):
                self.idx, self.selm = self._vanish_juxted(0)
            else:
                self.idx = self._replace_by_pvoid(self.idx)
                self.selm = SelMode.LCUR
            return NewEqState.EQ_MODIFIED

        # From here, selection is not highlighted
        sup = self.supeq(self.idx)
        if sup == -2:
            # Case: Act on whole eq
            if self.is_pvoid() or (not forward and self.is_lcur()) \
                    or (forward and self.is_rcur()):
                return NewEqState.IDENTICAL

            self._remove_eq_core()
            return NewEqState.EQ_MODIFIED

        # From here, supeq exists (sup != -2)
        par_ord = self.idx[-1]
        sup_idx = self.idx[:-1]
        s = sup[par_ord]

        if not sup.is_perm_jb():
            # Case: s is a non-juxted
            if sup.all_pvoid():
                # Subcase: Every par of lop-sup is PVOID
                if not self.is_juxted(sup_idx):
                    self.idx = self._replace_by_pvoid(sup_idx)
                    self.selm = SelMode.LCUR
                else:
                    self.idx, self.selm = self._vanish_juxted(0, sup_idx)
                return NewEqState.EQ_MODIFIED

            if (forward and self.is_lcur()) or \
                    (not forward and self.is_rcur()):
                if not s.is_pvoid():
                    # Subcase: Delete non-PVOID non-juxted
                    self.idx = self._replace_by_pvoid()
                    self.selm = SelMode.LCUR
                    return NewEqState.EQ_MODIFIED

                if is_script(self, self.idx):
                    # Subcase: Remove an empty script
                    ret_idx = remove_script(self.idx, self,
                                             self.idx[:-1] + [1])
                    self._change_sel(ret_idx, True)
                    return NewEqState.EQ_MODIFIED

            # Subcase: Non-juxted cannot be removed and supeq is not allowed to
            # be flatted.
            return NewEqState.IDENTICAL

        # From here, s is a juxted
        if not forward and self.is_lcur() and self.idx[-1] != 1:
            # Subcase: s is a juxted the lcojuxted must be vanished
            self.idx, self.selm = self._vanish_juxted(-1)
            return NewEqState.EQ_MODIFIED
        if (not forward and self.is_rcur()) or (forward and self.is_lcur()):
            # Case: s is juxted and must be vanished
            self.idx, self.selm = self._vanish_juxted()
            return NewEqState.EQ_MODIFIED

        # Case: s is a juxted a nothing is deleted.
        return NewEqState.IDENTICAL

    @eq2display
    @eqdebug.debug
    @add2hist
    def flat(self):
        if self.is_hl() or not self.is_juxted(self.idx):
            retval = self._flat()
            if retval is None:
                return NewEqState.IDENTICAL
            self.idx[:], self.selm = retval
            return NewEqState.EQ_MODIFIED

        # TODO?: Flat every juxted??
        return NewEqState.IDENTICAL

    @eq2display
    @eqdebug.debug
    @add2hist
    def flat_supeq(self):
        if self.idx and not self.is_juxted(self.idx):
            retval = self._flat_supeq()
            if retval is None:
                return NewEqState.IDENTICAL
            self.idx[:], self.selm = retval
            return NewEqState.EQ_MODIFIED

        # TODO?: Flat supeq of pjuxt-block??
        return NewEqState.IDENTICAL

    def _choose_pvoid(self, s: Subeq):
        """Return the argument ordinal of the lop which should be selected or
        substituted."""
        if s.isb():
            if s[s[0]._pref_arg].is_pvoid():
                return s[0]._pref_arg
            else:
                for par_pos, par in enumerate(s[1:]):
                    if par == [PVOID]:
                        return par_pos + 1

    def _overwrite(self, s: Subeq, substituting=False):
        if s.is_perm_jb():
            ret_idx = self._replace_integrating(s, self.idx)[0]
            self._change_sel(ret_idx, True)
            return NewEqState.EQ_MODIFIED

        pvoid_ord = self._choose_pvoid(s)
        if pvoid_ord is not None and substituting:
            s[pvoid_ord][:] = self(self.idx)
        ret_idx = self._replace(s, self.idx)

        if pvoid_ord is not None:
            self.selm = SelMode.LCUR
            self.idx += [pvoid_ord]
        else:
            self._change_sel(ret_idx, True)
        return NewEqState.EQ_MODIFIED

    def _insert_strict(self, s: Subeq):
        if s.is_perm_jb():
            # Subcase: Insert a juxt-block subeq
            if self.is_lcur():
                self.idx[:] = self._linsert_integrating(s)
            else:
                self.idx[:] = self._rinsert_integrating(s)
            return NewEqState.EQ_MODIFIED

        # Subcase: Insert a non-juxt-block subeq.
        if self.is_lcur():
            self.idx[:] = self._linsert(s)
        else:
            self.idx[:] = self._rinsert(s)

        pvoid_ord = self._choose_pvoid(s)
        if pvoid_ord is not None:
            self.selm = SelMode.LCUR
            if self.is_lcur():
                self.idx.prevpar(set=True)
            self.idx += [pvoid_ord]

        return NewEqState.EQ_MODIFIED

    @eq2display
    @eqdebug.debug
    @add2hist
    def insert_subeq(self, subeq: list):
        """Standard insert.

        .. note::
            *subeq* must be any valid subequation different than:

                *   A pvoid, and
                *   A tjuxt-block.

         .. note::
            To avoid redundant copies, no deep copies of *subeq* are made.
        """
        assert not isinstance(subeq[0], (TJuxt, Pvoid))
        self._reset_method_attrs()

        s = self._subeq_arg(subeq)

        if self.is_hl():
            # Case: Overwrite substituting (even if self.ovrwrt)
            return self._overwrite(s, True)

        if (self.ovrwrt and not self.is_rcur()) or self.is_pvoid(self.idx):
            # Case: Overwrite
            return self._overwrite(s)

        # Case: Insert
        return self._insert_strict(s)

    def insert_empty_block(self, op_class: type, *args, **kwargs):
        op = op_class(*args, **kwargs)
        return self.insert_subeq([op] + [[PVOID]] * op._n_args)

    @eq2display
    @eqdebug.debug
    @add2hist
    def add_scripts(self, *args):
        """Insert a script and select it.

        *   final-idx-checker
        *   base-checker

        *\*args* must be ScriptPos's.

        Last ScriptPos passed will be selected.

        Equation is not modified if every requested script exists.

        Last passed ScriptOp is selected.
        """

        if not args:
            raise ValueError("At least one argument must be passed.")
        self._reset_method_attrs()

        is_eq_mod = False
        base_idx = self.idx
        for pos in args[:-1]:
            retval = insert_script(base_idx, self, pos)
            if not isinstance(retval, int):
                base_idx = retval[:-1]
                is_eq_mod = True

        ret_val = insert_script(base_idx, self, args[-1])
        if isinstance(ret_val, int):
            self._change_sel(base_idx + [ret_val], False)
        else:
            self._change_sel(ret_val, False)
            is_eq_mod = True

        return NewEqState.EQ_MODIFIED if is_eq_mod else NewEqState.SEL_MODIFIED

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
                    eq.insert(lidx - 1, 0, 0, gop)
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
                    eq.insert(old_last_member, 0, 0, utils.JUXT)
                    eq.pop(idx - 1)
                    return idx - 1
                else:
                    # Case: group is a co-citizen before last but one
                    eq.insert(old_last_member, 0, 0, utils.JUXT)
                    eq.pop(cocitizen_idx - 1)
                    return idx
            return -1

        return idx


