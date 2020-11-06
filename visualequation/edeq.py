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

    EQ_CHANGED Equation modified (and maybe selection).
    SEL_CHANGED: Selection modified, but apparently not the equation.
    IDENTICAL: Nor equation nor selection has been modified.

    The rest are similar to IDENTICAL but can have specific meanings.


    "Selection" includes self.idx and self.selm.

    An eq has not been "apparently modified" if Subeq(self) is the same or:

        *   pjuxt-block <-> tjuxt-block
        *   tjuxt-block <-> integrated juxteds
    """
    EQ_MODIFIED = auto()
    SEL_MODIFIED = auto()
    IDENTICAL = auto()
    NO_SUBEQ_RIGHT = auto()
    NO_SUBEQ_LEFT = auto()
    NO_SUBEQ_UP = auto()
    NO_SUBEQ_DOWN = auto()
    NO_SUBEQ_TO_DELETE = auto()
    NO_VOID_BLOCK = auto()
    SUBEQ_IS_SYMBOL = auto()
    NO_SUPEQ = auto()
    EMPTY_EQ = auto()
    EMPTY_HIST = auto()

    def smth_happened(self):
        return self in (self.EQ_MODIFIED, self.SEL_MODIFIED)


def add2hist(func):
    """Update history according to function return value.

    Rules according to return value:
        *   If EQ_MODIFIED, current history entry is updated with initial
            state and final state is added afterwards.
        *   If SEL_MODIFIED, final state is added to history.
        *   Else, history is not modified.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # It is not know in advance whether eq will be modified by func
        init_eq = deepcopy(Subeq(self))
        init_idx = self.idx[:]
        init_rcursor = self.selm
        new_state = func(self, *args, **kwargs)

        if new_state not in (NewEqState.EQ_MODIFIED, NewEqState.SEL_MODIFIED):
            return new_state
        if new_state is NewEqState.EQ_MODIFIED:
            self.hist.ovrwrt_current(init_eq, init_idx, init_rcursor)

        self.hist.add(deepcopy(Subeq(self)), self.idx[:], self.selm)
        return new_state
    return wrapper


class EdEq(EqCore):
    """A class that allows a user to edit and navigate an equation by using a
    safe interface.

    Most of methods return a NewEqState, used in particular by add2hist:

        *   If eq is modified, EQ_MODIFIED.
        *   If selection is modified but, at least apparently, not eq,
            SEL_MODIFIED.
        *   Else, a specific value giving information about the no action.


    "Selection" includes self.idx and self.selm.

    "An eq has not been apparently modified" if Subeq(self) is the same or:

        *   pjuxt-block <-> tjuxt-block
        *   tjuxt-block <-> integrated juxteds

    Implementation notes:

        *   self.idx must always point to a subeq which is not a pjuxt-block
            before any after any method call.
        *   It is very easy to forget that current selection can be a
            highlighted tjuxt-block. Except in the following methods:

                *   self.__init__
                *   self._change_sel
                *   self._vanish_sel
                *   self._void_sel
                *   self._remove_eq
                *   self.flat
                *   self.flat_supeq
                *   self._insert_strict

            it is forbidden to set self.idx and self.selm manually unless it is
            explicitly reasoned and commented.
        *   Remember to pass the updated value of current index to _change_sel
            if it may have been previously modified!!
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

    def _repr_aux(self):
        s_repr = super()._repr_aux()
        if self.uld != 0:
            s_repr += ", uld=" + repr(self.uld)
        if self.hist != EqHist(Subeq(self), self.idx[:], self.selm):
            s_repr += ", hist=" + repr(self.hist)
        return s_repr

    def __repr__(self):
        return "EdEq(" + self._repr_aux() + ")"

    def _reset_method_attrs(self, uld=0):
        """Reset all or part of variables managing the preferences of
        movements, and other method-specific attributes.

        Parameters holding value -1 means will use current value of attribute.
        """
        if uld != -1:
            self.uld = uld

    def _vanish_sel(self):
        """Vanish current selection and set a new selection."""
        self.idx, self.selm = self._vanish_juxted(0)

    def _void_sel(self):
        """Replace selection by a void."""
        self.idx = self._replace_by_void(self.idx)
        self.selm = SelMode.LCUR

    def _remove_sel(self):
        """Vanish/replace by void depending whether selection is a juxted."""
        if self.is_juxted(self.idx):
            self._vanish_sel()
        else:
            self._void_sel()

    def _remove_eq(self):
        """Helper to remove the whole eq.

        If eq is a pvoid, just return EMPTY_EQ.
        Else:

            *   Set it to [PVOID].
            *   Set self.idx and self.selm properly.
            *   Return EQ_MODIFIED.
        """
        if self.is_void():
            return NewEqState.EMPTY_EQ
        self.idx[:] = []
        self.selm = SelMode.LCUR
        self._set([PVOID])
        return NewEqState.EQ_MODIFIED

    @eqdebug.debug
    @add2hist
    def flat(self):
        if self.is_hl() or not self.is_juxted(self.idx):
            retval = self._flat()
            if retval is None:
                return NewEqState.SUBEQ_IS_SYMBOL
            self.idx[:], self.selm = retval
            return NewEqState.EQ_MODIFIED

        # TODO?: Flat every juxted??
        return NewEqState.IDENTICAL

    @eqdebug.debug
    @add2hist
    def flat_supeq(self):
        if self.idx and not self.is_juxted(self.idx):
            retval = self._flat_supeq()
            if retval is None:
                return NewEqState.NO_SUPEQ
            self.idx[:], self.selm = retval
            return NewEqState.EQ_MODIFIED

        # TODO?: Flat supeq of pjuxt-block??
        return NewEqState.IDENTICAL

    def _change_sel(self, new_index: Union[list, int], right_pref: bool,
                    hl = False, ignore_sel = False):
        """Modify current selection safely.

        If current selection is a tjuxt-block, it is dissolved or transformed
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

        *ignore_sel* should be always False, but if you are sure of what you
        are doing a True value will skip modifications of selected subeq
        before updating selection.
        """

        new_idx = self._idx_arg(new_index)
        if not ignore_sel and self.is_temp_jb(self.idx):

            if hl and new_idx == self.idx:
                self.selm = SelMode.RHL if right_pref else SelMode.LHL
                return
            new_idx = self._dissolve_temp_jb(self.idx, new_idx)

        if not hl:
            self.idx[:], self.selm = self._correctly_point(new_idx, right_pref)
            return

        new_s = self(new_idx)
        if new_s.is_perm_jb():
            new_s[0] = new_s[0].equiv_tjuxt()
        self.idx[:] = new_idx
        self.selm = SelMode.RHL if right_pref else SelMode.LHL

    @eqdebug.debug
    def switch_ovrwrt(self):
        self.ovrwrt = not self.ovrwrt
        return NewEqState.SEL_MODIFIED

    @eqdebug.debug
    @add2hist
    def select_all(self):
        self._reset_method_attrs()
        self._change_sel([], False, hl=True)
        return NewEqState.SEL_MODIFIED

    @eqdebug.debug
    @add2hist
    def move2mate(self, right, pbc):
        """Select mate to the left/right with LCUR.

        If RDIR and going to the left, just set LDIR.
        """
        self._reset_method_attrs(uld=-1)

        if not right and self.is_rcur():
            # Case: RCUR and left
            self._change_sel(-1, False)
            return NewEqState.SEL_MODIFIED

        # From here, another subeq must be selected
        retval = self.mate(self.idx, right, self.uld, True)
        if retval == -1:
            # Case: No mate in specified direction
            if not pbc:
                if right:
                    return NewEqState.NO_SUBEQ_RIGHT
                return NewEqState.NO_SUBEQ_LEFT

            ul = self.uld + self.ulevel(self.idx)
            new_idx = self.boundary_mate(ul, not right, True)
            self.uld += self.ulevel(self.idx) - self.ulevel(new_idx)
            self._change_sel(new_idx, False)
            return NewEqState.SEL_MODIFIED

        # Typical case
        self._change_sel(retval[0], False)
        self.uld = retval[1]
        return NewEqState.SEL_MODIFIED

    @eqdebug.debug
    @add2hist
    def move2symb(self, right, pbc):
        """Select the closest symbol. Not so interesting."""
        pass
        # self._reset_method_attrs()
        #
        # if self.is_lcur() and right and not self.is_nonlastjuxted(self.idx):
        #     self.selm = SelMode.RCUR
        #     return NewEqState.SEL_MODIFIED
        #
        # if self.is_rcur() and not right:
        #     self.selm = SelMode.LCUR
        #     return NewEqState.SEL_MODIFIED
        #
        # ret_mate = self.mate(self.idx, right, 0, True)
        # if ret_mate != -1:
        #     idx = ret_mate[0]
        # elif pbc:
        #     return NewEqState.IDENTICAL
        # else:
        #     idx = Idx()
        #
        # new_idx = self.boundary_symbol(last=not right, retindex=True)
        # self._change_sel(new_idx, not right)
        # return NewEqState.SEL_MODIFIED

    @eqdebug.debug
    @add2hist
    def rmove(self):
        """Move to a subequation to the right."""

        self._reset_method_attrs()

        if not self.idx and self.is_void():
            # Case: Whole eq is empty
            return NewEqState.NO_SUBEQ_RIGHT

        if self.is_hl():
            # Case: Selection is highlighted
            self._change_sel(-1, True)
        elif self.isb(self.idx) and self.is_lcur():
            # Case: Selection is a block with LCUR
            arg_ord = self(self.idx)[0].rstep()
            self._change_sel(self.idx + [arg_ord], False)
        elif self.is_juxted(self.idx):
            if not self.isb(self.idx) and self.is_lcur():
                # Case: Selection is a juxted and symbol with LCUR.
                self._change_sel(-1, True)
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
        elif not self.isb(self.idx) and not self.is_void(self.idx) \
                and self.is_lcur():
            # Case: Selection is a non-juxted non-void symbol with LCUR
            self._change_sel(-1, True)
        elif not self.idx:
            # Case: Selection is a (non-void) eq with RCUR
            self._change_sel(-1, False)
        else:
            # Case: Selection is not eq and (non-juxted with RCUR or void)
            arg_ord = self(self.idx[:-1])[0].rstep(self.idx[-1])
            if arg_ord is None:
                self._change_sel(self.idx[:-1], True)
            else:
                self._change_sel(self.idx[:-1] + [arg_ord], False)

        return NewEqState.SEL_MODIFIED

    @eqdebug.debug
    @add2hist
    def lmove(self):
        """Move to a subequation to the left."""
        self._reset_method_attrs()

        if not self.idx and self.is_void():
            # Case: Whole eq is empty
            return NewEqState.NO_SUBEQ_LEFT

        if self.is_hl():
            # Case: Selection is highlighted
            self._change_sel(-1, False)
        elif self.isb(self.idx) and self.is_rcur():
            # Case: Selection is a block with RCUR
            arg_ord = self(self.idx)[0].lstep()
            self._change_sel(self.idx + [arg_ord], True)
        elif self.is_rcur():
            # Case: Selection is a symbol with RCUR
            self._change_sel(-1, False)
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
            return NewEqState.NO_SUBEQ_UP if up else NewEqState.NO_SUBEQ_DOWN
        if up:
            retval = self(index[:-1])[0].ustep(index[-1], self.selm)
        else:
            retval = self(index[:-1])[0].dstep(index[-1], self.selm)

        if retval is not None:
            self._change_sel(index[:-1] + [retval], False)
            return NewEqState.SEL_MODIFIED

        return self._vmove(index[:-1], up)

    @eqdebug.debug
    @add2hist
    def umove(self):
        return self._vmove(self.idx, True)

    @eqdebug.debug
    @add2hist
    def dmove(self):
        return self._vmove(self.idx, False)

    @eqdebug.debug
    @add2hist
    def remove_eq(self):
        """Replace the whole eq with a [PVOID]."""
        self._reset_method_attrs()
        return self._remove_eq()

    @eqdebug.debug
    def reset_eq(self):
        """Start a new equation, discarding history.

        It manually modify self.hist, add2hist decorator not used.

        .. note::
            eq and index may remain identical if the first one is equal to []
            and the second one equal to Subeq(new_subeq).
        """

        self._reset_method_attrs()

        if self.hist == EqHist(Subeq(), Idx(), SelMode.LCUR):
            assert self.is_pvoid()
            return NewEqState.EMPTY_HIST
        self.hist.reset(deepcopy(Subeq()), self.idx, self.selm)
        return self._remove_eq()

    @eqdebug.debug
    def undo(self):
        """Undo last edition."""
        retval = self.hist.get_prev()
        if retval is None:
            return NewEqState.EMPTY_HIST
        self[:], self.idx[:], self.selm = retval
        return NewEqState.EQ_MODIFIED

    @eqdebug.debug
    def redo(self):
        """Undo last edition."""
        retval = self.hist.get_next()
        if retval is None:
            return NewEqState.EMPTY_HIST
        self[:], self.idx[:], self.selm = retval
        return NewEqState.EQ_MODIFIED

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
            self._remove_sel()
            return NewEqState.EQ_MODIFIED

        # From here, selection is not highlighted
        if not self.idx:
            # Case: Act on whole eq
            if (not forward and self.is_lcur()) \
                    or (forward and self.is_rcur()):
                return NewEqState.NO_SUBEQ_TO_DELETE
            return self._remove_eq()

        # From here, supeq exists
        sup = self.supeq(self.idx)
        par_ord = self.idx[-1]
        sup_idx = self.idx[:-1]
        s = sup[par_ord]

        if not sup.is_perm_jb():
            # Case: s is a non-juxted
            if sup.all_void():
                # Subcase: Every par of lop-sup is a void

                # Advice note:
                # Supeq of sel is going to be deleted: no need to worry about
                # changing current selection before removal
                self.idx[:] = sup_idx
                self._remove_sel()
                return NewEqState.EQ_MODIFIED

            if (forward and self.is_lcur()) or \
                    (not forward and self.is_rcur()):
                if not s.is_void():
                    # Subcase: Delete non-void non-juxted
                    self._void_sel()
                    return NewEqState.EQ_MODIFIED

                if is_script(self, self.idx):
                    # Subcase: Remove an empty script

                    # Advice note:
                    # Selected script is selected and it is going to be
                    # removed. No need to worry about selection before
                    # operation
                    base_idx = remove_script(self.idx, self,
                                             self.idx[:-1] + [1])
                    self._change_sel(base_idx, True, ignore_sel=True)
                    return NewEqState.EQ_MODIFIED

            # Subcase: Void cannot be removed and supeq is not allowed to
            # be flatted.
            return NewEqState.NO_VOID_BLOCK

        # From here, s is a juxted
        if not forward and self.is_lcur() and self.idx[-1] != 1:
            # Subcase: s is a juxted and its lcojuxted must be vanished
            self._change_sel(self.idx.prevpar(), False)
            self._vanish_sel()
            return NewEqState.EQ_MODIFIED
        if (not forward and self.is_rcur()) or (forward and self.is_lcur()):
            # Case: s is juxted and must be vanished
            self._vanish_sel()
            return NewEqState.EQ_MODIFIED

        # Case: s is a juxted a nothing is deleted.
        return NewEqState.NO_SUBEQ_TO_DELETE

    def _choose_void_par(self, s: Subeq):
        """Return the argument ordinal of the lop which should be selected or
        substituted.

        Return None if no argument is useful for that purpose.
        """
        if s.isb():
            if s[s[0]._pref_arg].is_void():
                return s[0]._pref_arg
            else:
                for par_pos, par in enumerate(s[1:]):
                    if par.is_void():
                        return par_pos + 1

    def _overwrite_sel(self, s: Subeq, substituting=False):
        if s.is_perm_jb():
            ret_idx = self._replace_integrating(s, self.idx)[0]
            self._change_sel(ret_idx, True, ignore_sel=True)
            return NewEqState.EQ_MODIFIED

        void_ord = self._choose_void_par(s)
        if void_ord is not None and substituting:
            s[void_ord][:] = self(self.idx)
        ret_idx = self._replace(s, self.idx)

        if void_ord is None:
            self._change_sel(ret_idx, True, ignore_sel=True)
        elif substituting:
            # Advise note: Index must be corrected. Done without _change_sel.
            # It manages any usubeqs, tjuxt-blocks in particular, not altering
            # the highlight.
            self.idx[:] = ret_idx + [void_ord]
        else:
            self._change_sel(ret_idx + [void_ord], False, ignore_sel=True)

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

        void_ord = self._choose_void_par(s)
        if void_ord is not None:
            if self.is_lcur():
                self.idx.prevpar(set=True)
            self.selm = SelMode.LCUR
            self.idx += [void_ord]

        return NewEqState.EQ_MODIFIED

    @eqdebug.debug
    @add2hist
    def insert_subeq(self, subeq: list):
        """Standard insert.

        .. note::
            *subeq* must be any valid subequation different than:

                *   A void, and
                *   A tjuxt-block.

         .. note::
            To avoid redundant copies, no deep copies of *subeq* are made.
        """

        assert not isinstance(subeq[0], (TJuxt, Void))
        self._reset_method_attrs()

        s = self._subeq_arg(subeq)

        if self.is_hl():
            # Case: Overwrite substituting (even if self.ovrwrt)
            return self._overwrite_sel(s, True)

        if (self.ovrwrt and not self.is_rcur()) or self.is_void(self.idx):
            # Case: Overwrite
            return self._overwrite_sel(s)

        # Case: Insert
        return self._insert_strict(s)

    def insert_from_callable(self, callable_: type, *args, **kwargs):
        """Insert a subeq given a callable and the arguments it needs to
        generate a:

            *   Subeq, or
            *   PseudoSubeq, or
            *   Op.

        This method will take care of inserting any required void in each case.
        """
        elem = callable_(*args, **kwargs)
        if isinstance(elem, Subeq):
            return self.insert_subeq(elem)
        if isinstance(elem, ScriptOp):
            return self.insert_subeq([elem, [PVOID]]
                                     + [[RVOID]] * (elem._n_args - 1))
        if isinstance(elem, Op):
            return self.insert_subeq([elem] + [[PVOID]] * elem._n_args)
        if isinstance(elem, (PseudoSymb, str)):
            return self.insert_subeq([elem])
        raise TypeError("Element generated by callable is invalid.")


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
        base_or_scrblock_idx = self.idx
        # All scripts but last
        for pos in args[:-1]:
            retval = insert_script(base_or_scrblock_idx, self, pos)
            if not isinstance(retval, int):
                base_or_scrblock_idx = retval[:-1] + [1]
                is_eq_mod = True

        # Last script
        ret_val = insert_script(base_or_scrblock_idx, self, args[-1])
        if isinstance(ret_val, Idx):
            self._change_sel(ret_val, False)
            is_eq_mod = True
        elif ret_val > 0:
            self._change_sel(base_or_scrblock_idx[:-1] + [ret_val], False)
        else:
            self._change_sel(base_or_scrblock_idx + [-ret_val], False)

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


