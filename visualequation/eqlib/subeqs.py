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

"""
Module to manage subequations, the basic building block.

Subequation format:

Symbols: [str|PseudoSymb]
Blocks:  [OpN, Subeq1, Subeq2, ..., SubeqN] where Subeqx is a symbol or block.

Example: [PJUXT, ["2"], ["x"], [FRAC, ["c"], ["d"]]]

.. note::
    *   No non-user args are considered.
    *   Pjuxt is the only non-user op so pjuxt-blocks are the only subeqs
        which are not usubeqs.
    *   A pjuxt cannot have as parameter a pjuxt-block (but a pjuxt can have
        tjuxt-block as parameter).

.. note::
    Policy:

        *   Subeqs can return a reference to part of itself or return a Idx.
        *   If a Idx is returned, it must not be a reference to a Idx being
            used.
"""

from typing import List, Tuple, Union, Iterable

from .idx import Idx
from .ops import *

SUBEQ_CONTAINER_TYPE_ERROR_MSG = "Allowed iterables to provide Subeq " \
                                 "elements are lists and tuples"
SubeqContainerTypeError = TypeError(SUBEQ_CONTAINER_TYPE_ERROR_MSG)
SUBEQ_ELEM_TYPE_ERROR_MSG = "Elements allowed to build a Subeq must be " \
                            "lists, tuples, strings and/or Ops"
SubeqElemTypeError = TypeError(SUBEQ_ELEM_TYPE_ERROR_MSG)
SUBEQ_IADD_TYPE_ERROR_MSG = "Elements allowed to iadd (+=) to a Subeq are " \
                              "Subeqs and Ops with n_args != 0"
SubeqIaddTypeError = TypeError(SUBEQ_IADD_TYPE_ERROR_MSG)
SUBEQ_APPEND_TYPE_ERROR_MSG = "Elements allowed to be appended to a Subeq " \
                              "are Subeqs, strings and Ops"
SubeqAppendTypeError = TypeError(SUBEQ_APPEND_TYPE_ERROR_MSG)
SUBEQ_EXTEND_TYPE_ERROR_MSG = "Elements allowed to extend a Subeq are " \
                              "Subeqs and Ops with n_args != 0"
SubeqExtendTypeError = TypeError(SUBEQ_EXTEND_TYPE_ERROR_MSG)
SUBEQ_INSERT_TYPE_ERROR_MSG = "Elements allowed to be inserted in a Subeq " \
                              "are Subeqs and Ops with n_args != 0"
SubeqInsertTypeError = TypeError(SUBEQ_INSERT_TYPE_ERROR_MSG)
SUBEQ_VALUE_ERROR_MSG = "Strings and 0-args ops must always be the single " \
                        "element of a list or tuple."
SubeqValueError = ValueError(SUBEQ_VALUE_ERROR_MSG)
SUBEQ_ORDINARY_INDEXING_ERROR_MSG = "Accessing Subeq elements with a key ([" \
                                    "]) requires key being an integer or slice"
SubeqOrdinaryIndexingError = TypeError(SUBEQ_ORDINARY_INDEXING_ERROR_MSG)
NOT_SUBEQ_ERROR_MSG = "Pointed element is not a Subeq"
NotSubeqError = TypeError(NOT_SUBEQ_ERROR_MSG)
NON_EXISTENT_SUBEQ_ERROR_MSG = "Requested subeq does not exist"
NonExistentSubeqError = IndexError(NON_EXISTENT_SUBEQ_ERROR_MSG)
EMPTY_SUBEQ_ERROR_MSG = "Pointed subeq is empty"
EmptySubeqError = ValueError(EMPTY_SUBEQ_ERROR_MSG)
NOT_USUBEQ_ERROR_MSG = "Pointed element is not an usubeq"
NotUsubeqError = ValueError(NOT_USUBEQ_ERROR_MSG)
NEGATIVE_ULD_ERROR_MSG = "Ulevel diff cannot be negative"
NegativeUldError = ValueError(NEGATIVE_ULD_ERROR_MSG)
NOT_AIDE_ERROR_MSG = "Pointed subeq is not an aide"
NotAideError = ValueError(NOT_AIDE_ERROR_MSG)
NEGATIVE_UL_ERROR_MSG = "An Ulevel cannot be negative"
NegativeUlError = ValueError(NEGATIVE_UL_ERROR_MSG)


class Subeq(list):
    """A class to manage subequations.

    .. note::
        To simplify slicing and concatenation, Subeqs are allowed to have
        Ops with n_args != 0 in random positions or just one subeq ([["d"]]).

    Some methods may produce incorrect results if self is a whole equation and
    not a strict subeq, but that should be stated in their docstring.

    Implementation note:

        *   It will be supposed that a referred subequation is correctly built.
        *   It will not be supposed (in most of cases) that the user requests
            something legitimate.
    """
    @classmethod
    def check_noncontainer_value(cls, value, container_len):
        if not (isinstance(value, str) or isinstance(value, PseudoSymb)):
            raise SubeqElemTypeError
        if container_len > 1 and not isinstance(value, Op):
            raise SubeqElemTypeError

    def __init__(self, *args):
        """Constructor.

        .. note::
            Better allow [] to be a Subeq (which is not a valid subeq) than
            reject it or transform it into [PVOID]:
            This way, we keep compatibility with list slicing, __add__, etc.
            Equivalently, do not force complex correct structure or geometry of
            elements here, better use the debug module for that task.
        """
        if len(args) == 1 and args[0] is None:
            list.__init__(self, [PVOID])
        elif len(args) == 1 and not (isinstance(args[0], (list, tuple))):
            # Subeqs are derived from lists, so they pass the check
            raise SubeqContainerTypeError
        else:
            # Let list.__init__ manage any len(args) > 1 issue
            list.__init__(self, *args)

        for pos, e in enumerate(self):
            if isinstance(e, Subeq):
                # Trust in any Subeq previously built
                continue
            elif isinstance(e, (list, tuple)):
                self[pos] = Subeq(e)
            else:
                self.check_noncontainer_value(e, len(self))

    def __add__(self, other):
        return Subeq(list.__add__(self, other))

    def __mul__(self, n: int):
        return Subeq(list.__mul__(self, n))

    def __rmul__(self, n: int):
        return Subeq(list.__rmul__(self, n))

    def __getitem__(self, key: Union[slice, int]):
        if isinstance(key, slice):
            return Subeq(list.__getitem__(self, key))
        elif isinstance(key, int):
            return list.__getitem__(self, key)
        else:
            raise SubeqOrdinaryIndexingError

    def __setitem__(self, key: Union[slice, int],
                    value: Union[List, Tuple, str, PseudoSymb]):
        if isinstance(key, int):
            # Incorrect subeqs formed by this method should be equivalent to
            # those allowed by __init__.
            if not isinstance(value, (str, PseudoSymb, list, tuple)):
                raise SubeqElemTypeError
            if len(self) > 1 and not isinstance(value, (Op, list, tuple)):
                raise SubeqValueError
        elif isinstance(key, slice):
            if not isinstance(value, (list, tuple)):
                raise SubeqContainerTypeError
        else:
            raise SubeqOrdinaryIndexingError

        if isinstance(value, (str, PseudoSymb)):
            list.__setitem__(self, key, value)
        else:
            list.__setitem__(self, key, Subeq(value))

    def __iadd__(self, collect):
        if not (isinstance(collect, (list, tuple))):
            # Subeqs are derived from lists, so they pass the check
            raise SubeqContainerTypeError
        for s in collect:
            if not (isinstance(s, (Subeq, Op))):
                raise SubeqIaddTypeError
        return list.__iadd__(self, collect)

    def __imul__(self, n):
        return Subeq(list.__imul__(self, n))

    def __str__(self):
        if not self:
            return "[]"
        if isinstance(self[0], str):
            # Emphasize that strings are really strings
            s_str = "[" + repr(self[0])
        else:
            s_str = "[" + str(self[0])
        for e in self[1:]:
            s_str += ", " + str(e)
        return s_str + "]"

    @classmethod
    def _repr_elem(cls, elem):
        if not isinstance(elem, Subeq):
            return repr(elem)
        if not len(elem):
            return "[]"
        # Do not assume that first element is a Op even if len > 1.
        s_str = "[" + cls._repr_elem(elem[0])
        for e in elem[1:]:
            s_str += ", " + cls._repr_elem(e)
        return s_str + "]"

    def __repr__(self):
        """Return a valid string to generate the object.

        .. note::
            Python reminder: Output displayed by Python interpreter uses repr
            implicitly.
        """
        if not self:
            return "Subeq()"
        return "Subeq(" + self._repr_elem(self) + ")"

    def append(self, value: Union['Subeq', str, PseudoSymb]):
        if not isinstance(value, (Subeq, PseudoSymb, str)):
            raise SubeqAppendTypeError
        if len(self) != 0 and not isinstance(value, (Subeq, Op)):
            # Note: Allowing a str/PseudoSymb to be appended to empty Subeqs is
            # crucial to copy.deepcopy
            raise SubeqAppendTypeError
        list.append(self, value)

    def extend(self, collect: Iterable[Union['Subeq', PseudoSymb]]):
        # Because extend is used to support insertion of several elements
        # there are no reasons to allow its use to an append use of single
        # strings and 0-args ops in empty Subeqs.
        if not (isinstance(collect, (list, tuple))):
            # Subeqs are derived from lists, so they pass the check
            raise SubeqContainerTypeError
        for s in collect:
            if not (isinstance(s, (Subeq, Op))):
                raise SubeqExtendTypeError
        list.extend(self, collect)

    def insert(self, pos: int, value: Union['Subeq', Op]):
        # Not supporting insertion of strings or 0-args Ops in empty subeqs.
        if not (isinstance(value, (Subeq, Op))):
            raise SubeqInsertTypeError
        list.insert(self, pos, value)

    def __call__(self, *args):
        """Get a reference to eq element given its index or specifying the
        indices as separated arguments.

        If you modify the return value, subeq is modified.
        """
        # Transforming into Idx has the advantage of checking for some errors
        # automatically
        s = self
        # Using an Idx has the advantage of checking for most of errors
        # automatically
        for pos in Idx(*args):
            s = s[pos]
        return s

    def latex(self):
        """Return LaTeX code of Subeq."""
        if len(self) == 1:
            return self[0] if isinstance(self[0], str) else self[0]._latex_code
        elif self[0]._n_args == -1:
            return " ".join(map(Subeq.latex, self[1:]))
        else:
            return self[0]._latex_code.format(*map(Subeq.latex, self[1:]))

    def isb(self, idx=None):
        s = self(idx)
        return isinstance(s, Subeq) and len(s) > 1

    def supeq(self, index):
        """Return the supeq of subeq pointed by idx or -2."""
        idx = Idx(index)
        if not idx:
            return -2
        sup = self(idx[:-1])
        if not isinstance(sup[idx[-1]], Subeq):
            raise NotSubeqError
        return sup

    def is_void(self, index=None, cls=None):
        s = self(index)
        if cls is None:
            cls = Void
        return len(s) == 1 and isinstance(s[0], cls)

    def is_rvoid(self, index=None):
        return self(index) == [RVOID]

    def is_pvoid(self, index=None):
        return self(index) == [PVOID]

    def n_voids(self, index=None, cls=None):
        """Return the number of voids which are parameters of a lop.

        Pointed subeq must be a block B so the number of voids of lop-B is
        returned.

        *cls* can be used to specify a particular class of Void.

        If pointed subeq is a symbol, -1 is returned.
        """
        s = self(index)
        if not isinstance(s, Subeq):
            raise NotSubeqError
        if not s.isb():
            return -1

        n = 0
        for par in s[1:]:
            if par.is_void(cls=cls):
                n += 1
        return n

    def all_void(self, index=None, cls=None):
        """Return whether every param of block pointed by index is a Void.

        If pointed subeq is a symbol, -1 is returned.
        """
        s = self(index)
        if not isinstance(s, Subeq):
            raise NotSubeqError
        if not s.isb():
            return -1
        return s.n_voids(cls=cls) == len(s) - 1

    def isusubeq(self, index=None):
        """Return if a subeq element is an usubeq, including lops."""
        s = self(index)
        return isinstance(s, Subeq) and not isinstance(s[0], PJuxt)

    def is_perm_jb(self, index=None):
        s = self(index)
        return isinstance(s, Subeq) and isinstance(s[0], PJuxt)

    def is_temp_jb(self, index=None):
        s = self(index)
        return isinstance(s, Subeq) and isinstance(s[0], TJuxt)

    def is_jb(self, index=None):
        s = self(index)
        return isinstance(s, Subeq) and isinstance(s[0], (PJuxt, TJuxt))

    def is_juxted(self, index):
        idx = Idx(index)
        # Do not assume that pointed elem is a subeq
        if not idx:
            return False
        sup = self(idx[:-1])
        return isinstance(sup[idx[-1]], Subeq) and sup.is_jb()

    def last_par_ord(self, index=None):
        """Return the ordinal of last par of pointed block.

        If pointed element is a symbol, -3 is returned.
        """
        s = self(index)
        if not isinstance(s, Subeq):
            raise NotSubeqError
        if not s.isb():
            return -3
        return len(s) - 1

    def is_lastpar(self, index):
        """Return whether a subequation is a last parameter.

        .. note::
            Whole equation is not a parameter, so False is returned.
        """
        idx = Idx(index)
        if not isinstance(self(idx), Subeq):
            raise NotSubeqError
        if not idx:
            return False
        return idx[-1] == len(self(idx[:-1])) - 1

    def is_lastjuxted(self, index):
        """Return whether a subequation is a last juxted."""
        return self.is_lastpar(index) and self.is_juxted(index)

    def is_nonlastjuxted(self, index):
        """Return whether pointed subeq is a juxted which is not a last one.

        .. note:
            Different than not self.is_lastjuxted(idx), which would return True
            even if pointed subeq is not a juxted.
        """
        # Note:
        return not self.is_lastpar(index) and self.is_juxted(index)

    def lopsup(self, index, retindex=False):
        """Get the lop of parameter pointed by idx.

        self must be a whole equation to get reliable results in every case.

        If *self* is pointed, -2 is returned.
        """
        index = Idx(index)
        if not isinstance(self(index), Subeq):
            raise NotSubeqError
        if not index:
            return -2
        return index.outlop() if retindex else self(index.outlop())

    def lop(self, index=None, retindex=False):
        """Get lop of subeq S of self pointed by idx or -3 if S is a symbol."""
        idx = Idx(index)
        s = self(idx)
        if not isinstance(s, Subeq):
            raise NotSubeqError
        if not s:
            raise EmptySubeqError
        if len(s) == 1:
            return -3
        return idx + [0] if retindex else s[0]

    def nthpar(self, index=None, n=-1, retindex=False):
        """Return the n-th parameter of an op given the index of the block of
        which it is the lop.

        If you want the last parameter, pass n == -1.

        If *idx* points to a symbol, -3 is returned.
        If the operator does not have enough args, -1 is returned.
        Because *n* == -1 is being used as a flag, any other negative *n*
        raises an error.
        """
        block = self(index)
        if not isinstance(block, Subeq):
            raise NotSubeqError
        last_ord = len(block) - 1
        if last_ord == 0:
            return -3
        if n == -1:
            n = last_ord
        if n > last_ord:
            return -1
        if n < 1:
            raise NonExistentSubeqError

        return Idx(index) + [n] if retindex else block[n]

    def relpar(self, index, n=1, retindex=False):
        """Get the nth co-parameter to the left/right, depending on n's sign.

        Return -1 if requested parameter does not exist or -2 if idx is [].

        Since this method is intended to be used with relative position, it
        can be useful to call this method without actually knowing the passed
        value of *idx* and/or *n*. => No error is raised if requested parameter
        does not exist.
        """
        new_idx = Idx(index)
        if not new_idx:
            return -2
        # Do not suppose that pointed elem is a subeq
        sup = self(new_idx[:-1])
        if not isinstance(sup[new_idx[-1]], Subeq):
            raise NotSubeqError
        ord = new_idx[-1] + n
        if 0 < ord < len(sup):
            return new_idx[:-1] + [ord] if retindex else sup[ord]
        return -1

    def prevpar(self, index, retindex=False):
        """Return prev co-parameter.

        If idx is [], return -2.
        Elif idx points to first param or lop, return -1.
        """
        return self.relpar(index, -1, retindex)

    def nextpar(self, index, retindex=False):
        """Return parameter to the right.

        If idx is [], return -2.
        Elif it is a last param or lop, return -1.
        """
        return self.relpar(index, 1, retindex)

    def ulevel(self, index):
        """Return the plus or minus the nesting ulevel of pointed usubeq.

        If *idx* does not point to a pjuxt-block, minus the ulevel of its
        juxteds is returned.

        .. note::
            "-0" is not an issue:

            Since *index* == [] returns always 0, a default value has not been
            set for it.
            If idx points to a 1-level subeq S and 0 is returned, it means that
            S is a juxted.
            In any other case, a non-zero value is returned so it can be
            deduced if pointed subeq is usubeq or not according to the sign.

            Concluding:

                *   If *index* is not [] and return value is non-negative,
                    pointed subeq is an usubeq (not a pjuxt-block).
                *   If *index* is not [] and return value is negative, pointed
                    subeq is a pjuxt-block.
                *   If *index* is [], return value is always 0 and no
                    information about self is provided.
        """
        idx = Idx(index)
        s = self
        ulev = 0
        for pos in idx:
            if not s.is_perm_jb():
                ulev += 1
            s = s[pos]
        if not isinstance(s, Subeq):
            raise NotSubeqError
        if s.is_perm_jb():
            return -ulev
        return ulev

    def selectivity(self, index=None):
        """Give information on selectivity of a subequation.

        self must be a whole equation.

        Return  1 if subequation is SELECTABLE and not a juxted.

        Return  0 if subequation is SELECTABLE and a juxted.

        Return  -1 if subequation is NOT SELECTABLE (it is a pjuxt-block).

        .. note::
            A subequation is selectable if, and only if, return value is
            non-negative.
        """
        idx = Idx(index)
        s = self(idx)
        if not isinstance(s, Subeq):
            raise NotSubeqError

        if s.is_perm_jb():
            return -1
        if self.is_juxted(idx):
            return 0
        return 1

    def mate(self, index, right: bool, ulevel_diff=0, retindex=False):
        """If index points to a N-level mate, return a (N+ulevel_diff)-mate
        and the ulevel difference of returned mate and a (N+ulevel_diff)-peer.

        *self* must be a whole equation.

        It is required for pointed mate to be an N-level aide if *ulevel_diff**
        is positive (it has no sense to use this method the other way).

        If pointed mate is a last mate and right is True or it is a first mate
        and right is False, -1 is returned. It includes eqs with only one mate.

        Parameter *ulevel_diff* must be a non-negative integer.

        .. note::
            If first call to this function is done with *ulevel_diff* equal to
            0, then a next call using the correspondent second output value is
            a valid call to look for mates of usubeqs pointed in the former
            call.

        .. note::
            The algorithm is described in doc/FORMALISM.md.
        """
        s = self(index)
        if ulevel_diff < 0:
            raise NegativeUldError
        # Note: Selectivity already checks if pointed elem is a subeq
        ret_sel = self.selectivity(index)
        if ret_sel == -1:
            raise NotUsubeqError
        if ulevel_diff != 0 and len(s) > 1:
            raise NotAideError

        # Find common usupeq
        sidx = Idx(index)
        uld = ulevel_diff
        while True:
            pord = sidx.parord()
            if pord == -2:
                return -1
            sidx.supeq(set=True)
            s = self(sidx)
            if not s.is_perm_jb():
                uld += 1
            if (right and pord != len(s) - 1) or (not right and pord != 1):
                break

        # Find mate
        pord += 1 if right else -1
        while True:
            if not self.is_perm_jb(sidx):
                uld -= 1
            sidx = self.nthpar(sidx, pord, True)
            lop_s = self.lop(sidx)
            if lop_s == -3 or (uld == 0 and not self.is_perm_jb(sidx)):
                return (sidx if retindex else self(sidx)), uld
            # -1 is a flag value accepted by nthpar
            pord = 1 if right else -1

    def boundary_mate(self, ulevel: int, last: bool, retindex=False):
        """Return the first or last N-ulevel mate of eq.

        *self* must be a whole equation.
        """
        if ulevel < 0:
            raise NegativeUlError
        s = self
        bmate_idx = Idx()
        ul = 0
        while True:
            if s.is_perm_jb():
                ord = len(s) - 1 if last else 1
                bmate_idx.append(ord)
                s = s[ord]
            if len(s) == 1:
                return bmate_idx if retindex else s
            if ul == ulevel:
                return bmate_idx if retindex else s
            ord = len(s) - 1 if last else 1
            bmate_idx.append(ord)
            s = s[ord]
            ul += 1

    def boundary_symbol(self, last: bool, retindex=False):
        """Return the first or last symbol of a subeq."""
        s = self
        idx = Idx()
        while True:
            if len(s) == 1:
                return idx if retindex else s
            ord = len(s) - 1 if last else 1
            idx.append(ord)
            s = s[ord]
