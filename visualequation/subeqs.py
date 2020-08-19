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

Symbols: [str|Op0]
Blocks:  [OpN, par1, par2, ..., parN] where parX can be a symbol or a block.

Example: [PJUXT, ["2"], ["x"], [FRAC, ["c"], ["d"]]]

.. note::
    Current implementation: A non-usubeq is necessarily a GOP-block and its
    parameter cannot be a GOP-block.

.. note::
    Policy:

        *   Idxs can return a Idx or mutate itself.
        *   Subeqs can return a reference to part of itself or return a Idx.
        *   Whenever a Idx is returned, it must be not a reference to
            another Idx.
"""
from copy import deepcopy
from typing import List, Tuple, Union, Iterable, Optional

from . import ops
SUPEQ_ERROR_MSG = "Pointed subeq does not have a supeq"
SupeqError = IndexError(SUPEQ_ERROR_MSG)
STRICT_SUBEQ_ERROR_MSG = "Pointed subeq does have a strict subeq"
StrictSubeqError = IndexError(STRICT_SUBEQ_ERROR_MSG)
LOP_ERROR_MSG = "Pointed elem is a lop, not a subeq"
LopError = IndexError(LOP_ERROR_MSG)
NO_CO_PAR_ERROR_MSG = "Pointed subeq does not have a co-par in specified dir"
NoCoParError = IndexError(NO_CO_PAR_ERROR_MSG)
IDX_TYPE_ERROR_MSG = "Idx values must be integers"
IdxTypeError = TypeError(IDX_TYPE_ERROR_MSG)
IDX_VALUE_ERROR_MSG = "Idx values must be non-negative"
IdxValueError = ValueError(IDX_VALUE_ERROR_MSG)

class Idx(list):
    """A class to manage indices referring a subeq of another subeq.

    .. note::
        To simplify operations, 0's are allowed to be used in middle positions.
        Use the debug module to verify that they are not finally there.

    When using the provided methods, results will be strictly correct only if
    self is used to refer a subeq of an equation.
    """
    @classmethod
    def check_value(cls, value):
        if not isinstance(value, int):
            raise IdxTypeError
        if value < 0:
            raise IdxValueError

    @classmethod
    def check_iterable(cls, value):
        for c in value:
            cls.check_value(c)

    def __init__(self, *args: Iterable):
        # If the number of arguments is correct, check values.
        # Else, let list.__init__ blame.
        if len(args) == 1:
            self.check_iterable(*args)
        list.__init__(self, *args)

    def __str__(self):
        return list.__repr__(self)

    def __repr__(self):
        return "Idx(" + list.__repr__(self) + ")"

    def __add__(self, other: List[int]):
        return Idx(list.__add__(self, other))

    def __getitem__(self, key: Union[slice, int]):
        if isinstance(key, slice):
            return Idx(list.__getitem__(self, key))
        return list.__getitem__(self, key)

    def __setitem__(self, key: Union[slice, int], value: Union[List, int]):
        if isinstance(key, int):
            self.check_value(value)
            list.__setitem__(self, key, value)
        else:
            list.__setitem__(self, key, Idx(value))

    def append(self, value: int):
        self.check_value(value)
        list.append(self, value)

    def extend(self, iterable: Iterable):
        self.check_iterable(iterable)
        list.extend(self, iterable)

    def insert(self, pos: int, value: int):
        self.check_value(value)
        list.insert(self, pos, value)

    def parord(self):
        """Return the ordinal of pointed parameter or -2 if it points to the
        whole eq.

        Index must not point to a lop.
        """
        return self[-1] if self else -2

    def supeq(self, set=False):
        """Return the index of the 1-lev supeq of pointed subeq or -2 if that
        does not exist.
        """
        if not set:
            return self[:-1] if self else -2
        if not self:
            raise SupeqError
        del self[-1]

    def outlop(self, set=False):
        """Return index of lop of pointed subeq.

        If pointed subeq is the whole eq (block or symbol), -2 is returned.

        If *set* is True, a exception is be raised in the mentioned case.
        """
        if not set:
            return self[:-1] + [0] if self else -2
        if not self:
            raise SupeqError
        self[-1] = 0

    def prevpar(self, set=False):
        """Return index of left par of a subeq, -2 if pointed subeq is not a
        par or -1 if pointed subeq is a 1st par or lop."""
        if not set:
            if not self:
                return -2
            return self[:-1] + [self[-1] - 1] if self[-1] > 1 else -1
        if not self:
            raise SupeqError
        if self[-1] == 1:
            raise NoCoParError
        self[-1] -= 1

    def level(self):
        """Return the nesting level of pointed subeq."""
        return len(self)


NOIDX = Idx([])

SUBEQ_CONTAINER_TYPE_ERROR_MSG = "Allowed iterables to provide Subeq " \
                                 "elements are lists and tuples"
SubeqContainerTypeError = TypeError(SUBEQ_CONTAINER_TYPE_ERROR_MSG)
SUBEQ_ELEM_TYPE_ERROR_MSG = "Elements used to build a Subeq must be lists, " \
                            "tuples, str and/or Ops"
SubeqElemTypeError = TypeError(SUBEQ_ELEM_TYPE_ERROR_MSG)
SUBEQ_VALUE_ERROR_MSG = "Strings and 0-args ops must always be the single " \
                        "element of a list or tuple."
SubeqValueError = ValueError(SUBEQ_VALUE_ERROR_MSG)
SUBEQ_ORDINARY_INDEXING_ERROR_MSG = "Accessing Subeq elements with a key ([" \
                                    "]) requires key being an integer or slice"
SubeqOrdinaryIndexingError = TypeError(SUBEQ_ORDINARY_INDEXING_ERROR_MSG)


class Subeq(list):
    """A class to manage subequations.

    .. note::
        To simplify slicing and concatenation, Subeqs are allowed to have
        Ops with n_args != 0 in random positions or just one subeq ([["d"]]).

    Some methods will provide only correct results for every input if self is
    a whole equation and not a strict subeq.
    """
    @classmethod
    def check_value(cls, value, container_len):
        if not isinstance(value, str) and not isinstance(value, ops.Op):
            raise SubeqElemTypeError
        if container_len > 1 \
                and (isinstance(value, str) or not value.n_args):
            raise SubeqValueError

    def __init__(self, *args: Iterable):
        # Better allow [] to be a Subeq even if that is not a valid subeq than
        # reject it or transform it into [VOID].
        # This way, we keep compatibility with list slicing, etc.
        # Equivalently, do not force a correct structure or geometry of
        # elements here, better use the debug module for that task.
        if len(args) == 1 and \
                not (isinstance(args[0], list) or isinstance(args[0], tuple)):
            # Subeqs are derived from lists, so they pass the check
            raise SubeqContainerTypeError
        list.__init__(self, *args)
        for pos, e in enumerate(self):
            if isinstance(e, Subeq):
                # Trust in any Subeq previously built
                pass
            elif isinstance(e, list) or isinstance(e, tuple):
                self[pos] = Subeq(e)
            else:
                self.check_value(e, len(self))

    def __add__(self, other: List):
        return Subeq(list.__add__(self, other))

    def __getitem__(self, key: Union[slice, int]):
        if isinstance(key, slice):
            return Subeq(list.__getitem__(self, key))
        elif isinstance(key, int):
            return list.__getitem__(self, key)
        else:
            raise SubeqOrdinaryIndexingError

    def __setitem__(self, key: Union[slice, int],
                    value: Union[List, Tuple, str, ops.Op]):
        if isinstance(key, int):
            # Incorrect subeqs formed by this method should be equivalent to
            # those allowed by __init__.
            if not isinstance(value, (str, ops.Op, list, tuple)):
                raise SubeqElemTypeError
            if len(self) > 1 \
                    and (isinstance(value, str)
                         or (isinstance(value, ops.Op) and not value.n_args)):
                raise SubeqValueError
        elif isinstance(key, slice):
            if not isinstance(value, (list, tuple)):
                raise SubeqContainerTypeError
        else:
            raise SubeqOrdinaryIndexingError

        if isinstance(value, (str, ops.Op)):
            list.__setitem__(self, key, value)
        else:
            list.__setitem__(self, key, Subeq(value))

    def __str__(self):
        if len(self) == 0:
            return "[]"
        s_str = "[" + str(self[0])
        for e in self[1:]:
            s_str += ", " + str(e)
        return s_str + "]"

    @classmethod
    def _repr_aux(cls, elem):
        if not isinstance(elem, Subeq):
            return repr(elem)
        elif not len(elem):
            return "[]"
        else:
            s_str = "[" + cls._repr_aux(elem[0])
            for e in elem[1:]:
                s_str += ", " + cls._repr_aux(e)
            return s_str + "]"

    def __repr__(self):
        if len(self) == 0:
            return "Subeq()"
        return "Subeq(" + self._repr_aux(self) + ")"

    def __bool__(self):
        return self != [ops.PVOID]

    @classmethod
    def subeq2latex(cls, s):
        """Return latex code of a subeq."""
        if len(s) == 1:
            return s[0] if isinstance(s[0], str) else s[0].latex_code
        elif s[0].n_args == -1:
            return " ".join(map(cls.subeq2latex, s[1:]))
        else:
            return s[0].latex_code.format(*map(cls.subeq2latex, s[1:]))

    def latex(self):
        return self.subeq2latex(self)

    def __call__(self, idx: Idx):
        """Get a reference to eq element given its index.

        (If you modify the return value, subeq is modified.)
        """
        s = self
        for pos in idx:
            s = s[pos]
        return s

    def is_pvoid(self, idx: Optional[Idx] = None):
        idx = NOIDX if idx is None else idx
        return not self(idx)

    def is_tvoid(self, idx: Optional[Idx] = None):
        idx = NOIDX if idx is None else idx
        return self(idx) == [ops.TVOID]

    def is_void(self, idx: Optional[Idx] = None):
        idx = NOIDX if idx is None else idx
        return not self(idx) or self(idx) == [ops.TVOID]

    def isb(self, idx: Optional[Idx] = None):
        idx = NOIDX if idx is None else idx
        return len(self(idx)) > 1

    def isusubeq(self, idx: Optional[Idx] = None):
        """Return if a subeq element is an usubeq, including lops."""
        idx = NOIDX if idx is None else idx
        # A lop is not an usubeq
        if idx and not idx[-1]:
            return False
        return self(idx)[0] != ops.GOP

    def is_perm_jb(self, idx: Optional[Idx] = None):
        idx = NOIDX if idx is None else idx
        return self(idx)[0] == ops.PJUXT

    def is_temp_jb(self, idx: Optional[Idx] = None):
        idx = NOIDX if idx is None else idx
        return self(idx)[0] == ops.TJUXT

    def is_jb(self, idx: Optional[Idx] = None):
        idx = NOIDX if idx is None else idx
        return self(idx)[0] == ops.PJUXT or self(idx)[0] == ops.TJUXT

    def is_juxted(self, idx):
        return idx != NOIDX and self.supeq(idx).is_jb()

    def is_gopb(self, idx: Optional[Idx] = None):
        idx = NOIDX if idx is None else idx
        return self(idx)[0] == ops.GOP

    def is_goppar(self, idx: Idx):
        if not idx:
            return False
        return self.supeq(idx)[0] == ops.GOP

    def supeq(self, idx: Idx):
        """Get the supeq of subeq of self pointed by idx or -2."""
        return self(idx[:-1]) if idx else -2

    def outlop(self, idx: Idx):
        """Get the lop of parameter pointed by idx.

        self must be a whole equation to have reliable results for every *idx*.

        If the whole subeq is pointed, -2 is returned.
        """
        return self(idx[:-1] + [0]) if idx else -2

    def inlop(self, idx: Optional[Idx] = None, retidx=False):
        """Get lop of subeq S of self pointed by idx or -3 if S is a symbol."""
        idx = NOIDX if idx is None else idx
        s = self(idx)
        if len(s) == 1:
            return -3
        else:
            return idx + [0] if retidx else s[0]

    def nthpar(self, idx: Optional[Idx] = None, n = -1, retidx = False):
        """Return the n-th parameter of an op given the index of its op-block.

        If you want the last parameter, pass n == -1.

        If *idx* points to a symbol, -3 is returned.
        Elif the operator does not have enough args, -1 is returned.
        Elif *n* is 0, -5 is returned.
        """
        idx = NOIDX if idx is None else id
        if not n:
            return -5

        block = self(idx)
        last_ord = len(block) - 1
        if not last_ord:
            return -3
        elif n > last_ord:
            return -1

        if n == -1:
            n = last_ord
        return idx + [n] if retidx else block[n]

    def relpar(self, idx: Idx, n=1, retidx=False):
        """Get a co-parameter ref or its index.

        Return -1 if requested parameter does not exist or -2 if idx is [].
        """
        if not idx:
            return -2
        sup = self.supeq(idx)
        ord = idx[-1] + n
        if 0 < ord < len(sup):
            return idx[:-1] + [ord] if retidx else sup[ord]
        return -1

    def prevpar(self, idx: Idx, retidx=False):
        """Return prev co-parameter.

        If idx is [], return -2.
        Elif idx points to first param or lop, return -1.
        """
        return self.relpar(idx, -1, retidx)

    def nextpar(self, idx: Idx, retidx=False):
        """Return parameter to the right.

        If idx is [], return -2.
        Elif it is a last param or lop, return -1.
        """
        return self.relpar(idx, 1, retidx)

    def urepr(self, idx: Optional[Idx] = None, retidx=False):
        """Return the urepr of a subeq.

        A more general approach based on "VE ops are faithful" was previously
        coded and can be recovered from the DVCS.
        """
        idx = NOIDX if idx is None else idx
        s = self(idx)
        if s.is_gopb():
            return idx + [1] if retidx else s[1]
        return idx[:] if retidx else s

    def biggest_supeq_with_urepr(self, idx: Optional[Idx], retidx=False):
        """Get biggest subeq which has pointed usubeq as urepr.

        self is recommended to be an equation (see note below).

        If pointed subeq is a non-usubeq, -1 is returned.

        A more general approach based on "VE ops are faithful" was previously
        coded and can be recovered from the DVCS.

        .. note::
            If idx is [] and self is a usubeq, result is only guaranteed to be
            valid if self is the whole equation.
        """
        idx = NOIDX if idx is None else idx
        if not idx:
            if self[0] == ops.GOP:
                return -1
            return idx[:] if retidx else self

        sup = self(idx[:-1])
        if sup[0] == ops.GOP:
            return idx[:-1] if retidx else sup
        if sup[idx[-1]][0] == ops.GOP:
            return -1
        return idx[:] if retidx else sup[idx[-1]]

    def ulevel(self, idx):
        """Return the nesting ulevel of pointed usubeq.

        If *idx* does not point to a usubeq, minus the ulevel of its urepr is
        returned.
        """
        s = self
        ulev = 0
        for pos in idx:
            if not s.is_gopb():
                ulev += 1
            s = s[pos]
        if s.is_gopb():
            return -ulev
        return ulev

    def selectivity(self, idx: Idx):
        """Give information on selectivity of a subequation.

        self must be an equation.

        Return  2 if subequation is SELECTABLE and is not a GOP-par.
        Return  1 if subequation is SELECTABLE and is a GOP-par.
        Return  0 if subequation is a GOP-block which par is selectable.
        Return -1 if subequation is a GOP-par strict subeq.

        .. note::
            A subequation is selectable if, and only if, return value is
            positive.

        .. note::
            To know that return value is -1 is not enough to know if subeq is a
            usubeq. Since this function informs about selectivity, it is not
            considered important to inform about the user property itself.
        """
        s = self
        gopb_reached = False
        for parord in idx:
            if gopb_reached:
                return -1
            if s.is_gopb():
                gopb_reached = True
            s = s[parord]

        if gopb_reached:
            return 1
        if s.is_gopb():
            return 0
        return 2

    def mate(self, idx: Idx, right: bool, ulevel_diff = 0, retidx = False):
        """Return the mate to the left and a ulevel difference.

        self must be an equation.

        If it is a last mate and right is True or it is a first mate and right
        is, False, -1 is returned.

        Parameter *ulevel_diff* indicate the ulevel of the mates as an offset:
        Supposing that subeq pointed by *idx* is a N-ulevel peer and the
        intention is to find its M-ulevel mate to the right or left for M > N,
        *ulevel_diff* must be M - N.

        .. note::
            If first call to this function is done with *ulevel_diff* equal to
            0, then a next call using the correspondent second output value is
            a valid call to look for mates of usubeq pointed in the former
            call.

        .. note::
            The algorithm described in HACKING.md.
        """
        sidx = idx[:]
        uld = ulevel_diff

        # Find common usupeq
        while True:
            pord = sidx.parord()
            if pord == -2:
                return -1, None
            sidx = sidx[:-1]
            s = self(sidx)
            uld += 0 if s.is_gopb() else 1
            if (right and pord != len(s) - 1) or (not right and pord != 1):
                break

        # Find mate
        pord += 1 if right else -1
        while True:
            uld -= 0 if self(sidx).is_gopb() else 1
            sidx = self.nthpar(sidx, pord, True)
            lop_s = self.inlop(sidx)
            if not uld or lop_s == -3 or lop_s == ops.GOP:
                return self.urepr(sidx, retidx), uld
            # -1 is a flag value accepted by nthpar
            pord = 1 if right else -1

    def boundary_mate(self, ulevel: int, last = False, retidx = False):
        """Return the first or last *N*-ulevel mate of eq.

        self must be an equation.
        """
        s = self
        bmate_idx = NOIDX
        ul = -1
        while True:
            if len(s) == 1:
                return bmate_idx if retidx else s
            if s.is_gopb():
                return bmate_idx + [1] if retidx else s[1]
            ul += 1
            if ul == ulevel:
                return bmate_idx if retidx else s
            bmate_idx.append(len(s) - 1 if last else 1)
            s = s[bmate_idx[-1]]

    def boundary_symbol(self, idx: Optional[Idx] = None, last = False,
                        strict = True, retidx = False):
        """Return the first or last symbol of a subeq.

        self must be an equation if *strict* is False.

        If *strict* is False and the boundary symbol is not selectable, it will
        return the GOP-par with biggest usupeq nesting level.

        If *strict* is False, and pointed subeq has not a selectable urepr, -1
        is returned.
        """
        new_idx = NOIDX[:] if idx is None else idx[:]
        s = self(new_idx)
        flag = self.selectivity(new_idx)
        if not strict:
            if flag == -1:
                return -1
            if flag == 1:
                return new_idx if retidx else s

        # From this point we know that s is not a subeq of a GOP-par
        while True:
            if len(s) == 1:
                return new_idx if retidx else s
            if not strict and s.is_gopb():
                return new_idx + [1] if retidx else s[1]
            new_idx.append(len(s) - 1 if last else 1)
            s = s[new_idx[-1]]
