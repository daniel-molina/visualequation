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
            return -99
        else:
            print("Note: self.eq and self.idx were valid before function "
                  "call. Calling now...")

        retval = fun(self, *args, **kwargs)
        print("\nself.eq: " + repr(self.eq))
        print("\nself.idx: " + repr(self.idx) + "\tdir: " + repr(self.dir))
        print("\nReturn: " + repr(retval))
        print("**** END DEBUGGING ****")
        return retval

    return wrapper


class EditableEq:
    """Class to edit an equation.

    .. note::
        Methods not starting by underscore will suppose that self.idx points
        to selected equation. As a consequence:

            *   self.idx must point to an usubeq before calling them.
            *   The only supeq of the usubeq pointed by self.idx which may be a
                GOP-block is its 1-level supeq (but strict subeqs may be also
                GOP-blocks).

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

    def set_idx(self, newidx=[]):
        self.idx[:] = newidx[:]

    def set_ovrwrt(self, val=True):
        if val:
            self.dir = utils.ODIR
        elif eqqueries.get(self.idx, self.eq) == utils.VOID:
            self.dir = utils.VDIR
        else:
            self.dir = utils.RDIR

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

    #@debug
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

    #@debug
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

    def _dissolve_subjb(self, idx=None, supref=None):
        """Integrate juxteds of a juxt-block JB in the juxt-block in which
        JB is juxted.

        *   Not a supeq-checker
        *   Not a final idx-checker
        *   base-checker (never checked because no base can be involved)

        If you have a reference to the external juxt-block, you can pass it.

        .. note::
            It is assumed that the requirement has foundation!
        """
        juxted_jb_idx = self.idx if idx is None else idx
        ext_jb = eqqueries.supeq(juxted_jb_idx, self.eq, True) \
            if supref is None else supref
        juxted_ord = juxted_jb_idx[-1]
        juxted_jb = ext_jb[juxted_ord]
        ext_jb[juxted_ord:juxted_ord+1] = juxted_jb[1:]

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

    #@debug
    def remove_eq(self):
        """Replace the whole eq by a VOID."""
        self.idx[:] = []
        self._set(utils.void())
        self.dir = self._get_safe_dir(0, 0)

    #@debug
    def _vanish_juxted(self, reljuxted=0, idx=None):
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

        If *reljuxted* == n != 0, it vanishes the n-th juxted to the right or
        left of pointed juxted (caller must check by itself that it exists),
        depending whether n is positive or negative, respectively.

        If *reljuxted* != 0, returned values are the index and dir of pointed
        juxted, likely corrected due to the removal of its co-juxted.

        .. note::
            Implementation notes:

                *   Do NOT use here any supeq-checker. Use _set when necessary.
                *   Pointed subeq cannot be a base because it must be a juxted,
                    but its juxt-block can.
        """
        pointed_idx = self.idx[:] if idx is None else idx[:]
        del_idx = pointed_idx[:-1] + [pointed_idx[-1] + reljuxted]
        juxtblock = eqqueries.supeq(del_idx, self.eq, True)
        # Point juxted to remove (responsibility of the caller that it exists)

        if len(juxtblock) == del_idx[-1] + 1:
            # Case: Vanish last juxted
            if self.odir():
                # Overwrite mode -> Replace by VOID (marginal case) or select
                # next mate
                rmate = eqqueries.mate(del_idx, self.eq, True)[0]
                if rmate == -1:
                    self._set(utils.void(), del_idx)
                    if reljuxted:
                        return (eqqueries.urepr(pointed_idx, self.eq),
                                utils.ODIR)
                    return del_idx, utils.ODIR
                # (!) The typical overwrite case is not completed until later

            # Normal mode -> Select juxted to the left, prefer RDIR
            if len(juxtblock) > 3:
                del juxtblock[-1]
                del_idx[-1] -= 1
            else:
                juxtblock[:] = deepcopy(juxtblock[1])
                del del_idx[-1]
                pointed_idx = del_idx
                self._condtly_correct_scriptop(juxtblock, del_idx)

            if self.odir():
                return rmate, utils.ODIR
            elif reljuxted:
                return eqqueries.urepr(pointed_idx, self.eq), self.dir
            else:
                return (eqqueries.urepr(del_idx, self.eq),
                        self._get_safe_dir(1, None, del_idx))

        if del_idx[-1] == 1:
            # Case: Vanish first juxted -> Juxted to the right, prefer LDIR
            if len(juxtblock) > 3:
                del juxtblock[1]
                pointed_idx[-1] -= 1
            else:
                juxtblock[:] = deepcopy(juxtblock[2])
                del del_idx[-1]
                pointed_idx = del_idx
                self._condtly_correct_scriptop(juxtblock, del_idx)

            if reljuxted:
                return eqqueries.urepr(pointed_idx, self.eq), self.dir
            else:
                return (eqqueries.urepr(del_idx, self.eq),
                        self._get_safe_dir(-1, None, del_idx))

        # Case: Intermediate juxted
        del juxtblock[del_idx[-1]]
        # If dir is RDIR -> Juxted to the left, prefer same DIR.
        # Else -> Juxted to the right (done automatically), prefer same DIR.
        if self.dir == utils.RDIR:
            del_idx[-1] -= 1

        if reljuxted > 0:
            return eqqueries.urepr(pointed_idx, self.eq), self.dir
        elif reljuxted < 0:
            pointed_idx[-1] -= 1
            return eqqueries.urepr(pointed_idx, self.eq), self.dir
        else:
            return (eqqueries.urepr(del_idx, self.eq),
                    self._get_safe_dir(5, None, del_idx))

    #@debug
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

    #@debug
    def _flat_lopblock(self, idx=None, supref=None):
        """Remove leading operator and leave params, joined in a juxt-block
        if necessary.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        If *idx* points to a non-usubeq, consider "par_idx" equal to *idx*.
        Else, consider "par_idx" the index of the biggest subeq of eq having
        the subeq with index *idx* as urepr.

        .. note::
            It is expected that no supeq of subeq pointed by par_idx is a
            TJUXT-block.

        Return -2 if par_idx is []. Equation is not edited in that case
        Return -5 if par_idx is not [] and equation is not edited. That happens
        if par_idx points to a juxted and no juxted of its juxt-block is VOID.
        Return expected selection and direction supposing that current
        selection is *idx* in any other case.

        Rules:

            *   If every param of the lop of param pointed by *par_idx* is
                VOID, the the lop-block is replaced by a VOID.
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
            sup[:] = utils.void()
            self._condtly_correct_scriptop(sup, sup_idx)
            return sup_idx, self._get_safe_dir(0, 0)

        # Build replacement
        par_ord = par_idx[-1]
        repl_c = simpleeqcreator.SimpleEqCreator()
        repl_c.extend(sup[1:par_ord], include_voids=False)
        par = deepcopy(sup[par_ord])
        if par[0] == utils.JUXT:
            # Being here implies that par is not a VOID
            par[0] = utils.TJUXT
        par_pos_in_repl = repl_c.n_inserted_subeqs()
        repl_c.append(par, include_voids=False)
        repl_c.extend(sup[par_ord + 1:], include_voids=False)

        # Polish replacement
        repl = repl_c.get_eq()
        is_sup_a_juxted = eqqueries.isjuxted(sup_idx, self.eq)
        is_par_a_void = par == utils.void()
        if is_sup_a_juxted and is_par_a_void and repl[0] == utils.JUXT:
            repl[0] = utils.TJUXT

        # Replace
        # Note: We know that sup is an usubeq, no need to check returned idx
        if is_sup_a_juxted:
            # _replace_integrating checks any base issue
            self._replace_integrating(repl, sup_idx)
        else:
            # _replace_integrating will consider non-usubeq supeqs of sup_id in
            # some cases and that is not what is desired.
            sup[:] = repl
            self._condtly_correct_scriptop(sup, sup_idx)

        if is_par_a_void:
            # Case: Select whole replacement
            new_idx = eqqueries.urepr(sup_idx, self.eq)
            return new_idx, self._get_safe_dir(5, None, new_idx)

        # Case: Select urepr of par
        # Note: par was never inserted as a JUXT-block in repl_c so
        # repl_c.get_idx with [] is allowed
        par_idx_in_repl = repl_c.get_idx([], par_pos_in_repl)
        if not is_sup_a_juxted:
            new_idx = sup_idx + par_idx_in_repl
        elif not par_idx_in_repl:
            new_idx = sup_idx
        else:
            new_idx = sup_idx[:-1] + [sup_idx[-1] + par_idx_in_repl[0] - 1]
        new_idx = eqqueries.urepr(new_idx, self.eq)
        return new_idx, self._get_safe_dir(5, None, new_idx)

    @debug
    def clever_delete(self, forward, num_arg=1):
        """Forward/Backward clever delete accepting a numeric argument.

        *   supeq-checker
        *   final-idx-checker
        *   base-checker

        .. note::
            Since it is a "clever" function, deletion in overwrite mode is
            more gedit-like than readline-like.

        Return the (positive) number of arguments not applied.
        """
        if not num_arg:
            return 0
        # Consider always a positive num_arg
        if num_arg < 0:
            forward = not forward
            num_arg *= -1

        del_idx = self._get_biggest_subeq_same_urepr()
        sup = eqqueries.supeq(del_idx, self.eq, True)

        # Whole eq is pointed
        if sup == -2:
            if self.vdir():
                return num_arg
            if (forward and self.rdir()) \
                    or (not forward and not self.rdir()):
                return num_arg

            self.remove_eq()
            return num_arg - 1

        par_ord = del_idx[-1]
        sup_idx = del_idx[:-1]
        # Let us set pointed subeq to del_idx to simplify the code.
        # Those cases which do not edit the equation will restore
        # self.idx to the original value.
        # (note: rest of defined variables are still valid)
        self.idx[:] = del_idx[:]
        # Note: This class do not allow VOID be the arg of a GOP
        # => No need to update self.dir.

        if sup[0] != utils.JUXT:
            if (not forward and self.rdir()) \
                    or (forward and (self.ldir() or self.odir())):
                # Subcase: Delete a non-juxted subeq
                self.idx = self._empty()
                self.dir = self._get_safe_dir(0, 0)
                return self.clever_delete(forward, num_arg - 1)

            # Subacase: Flat non-juxt lop (includes VOID and non-VOID param)
            self.idx, self.dir = self._flat_lopblock(None, sup)
            return self.clever_delete(forward, num_arg - 1)

        # From this here, a juxted is pointed
        if self.vdir():
            # Subcase: Delete VOID
            self.idx[:], self.dir = self._vanish_juxted()
            return self.clever_delete(forward, num_arg - 1)

        if (not forward and self.rdir()) \
                or (forward and (self.ldir() or self.odir())):
            # Subcase: Delete pointed juxted
            self.idx, self.dir = self._vanish_juxted()
            return self.clever_delete(forward, num_arg - 1)

        if forward and len(sup[1:]) > par_ord:
            # Subcase: Delete juxted to the right
            self.idx = self._vanish_juxted(1)[0]
            return self.clever_delete(forward, num_arg - 1)
        if not forward and par_ord != 1:
            # Subcase: Delete juxted to the left
            self.idx = self._vanish_juxted(-1)[0]
            return self.clever_delete(forward, num_arg - 1)

        supsup = eqqueries.supeq(sup_idx)

        if supsup == -2:
            # Subcase: First or last juxted of the whole eq (no edit)
            self.idx[:] += eqqueries.urepr([], sup[par_ord])
            return num_arg

        if supsup[0] != utils.JUXT:
            # Subcase: juxt-block of juxted JU is an argument of an op OP
            # which is not a juxt => flat OP-block
            # It is assured that there are no supeqs of JU being GOP-blocks
            self.idx, self.dir = self._flat_lopblock(sup_idx, supsup)
            self.idx.append(par_ord)
            return num_arg - 1

        # Subcase: juxt-block of juxted is another juxted JU
        # => behave as if JU was selected with the same dir
        del self.idx[-1]
        retval = self.clever_delete(forward, num_arg)
        if retval == num_arg:
            return num_arg
        self.idx.append(par_ord)
        return retval







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

