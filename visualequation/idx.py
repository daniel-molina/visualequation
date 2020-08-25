#  visualequation is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  visualequation is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import List, Union, Iterable

SUPEQ_ERROR_MSG = "Pointed subeq does not have a supeq"
SupeqError = IndexError(SUPEQ_ERROR_MSG)
STRICT_SUBEQ_ERROR_MSG = "Pointed subeq does have a strict subeq"
StrictSubeqError = IndexError(STRICT_SUBEQ_ERROR_MSG)
LOP_ERROR_MSG = "Pointed elem is a lop, not a subeq"
LopError = IndexError(LOP_ERROR_MSG)
NO_CO_PAR_ERROR_MSG = "Pointed subeq does not have a co-par in specified dir"
NoCoParError = IndexError(NO_CO_PAR_ERROR_MSG)

IDX_TYPE_ERROR_MSG = "Building values for Idx must be integers, possibly " \
                     "in a list or tuple"
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

    def __init__(self, *args):
        if not len(args) or (len(args) == 1 and args[0] is None):
            list.__init__(self)
        elif len(args) > 1 or (len(args) == 1 and isinstance(args[0], int)) \
                or not len(args):
            self.check_iterable(args)
            list.__init__(self, args)
        elif isinstance(args[0], (list, tuple)):
            self.check_iterable(args[0])
            list.__init__(self, args[0])
        else:
            raise IdxTypeError

    def __str__(self):
        return list.__repr__(self)

    def __repr__(self):
        return "Idx(" + list.__repr__(self) + ")"

    def __add__(self, other: List[int]):
        return Idx(list.__add__(self, other))

    def __mul__(self, n: int):
        return Idx(list.__mul__(self, n))

    def __rmul__(self, n: int):
        return Idx(list.__rmul__(self, n))

    def __getitem__(self, key: Union[slice, int]):
        if isinstance(key, slice):
            return Idx(list.__getitem__(self, key))
        return list.__getitem__(self, key)

    def __setitem__(self, key: Union[slice, int], value: Union[List, int]):
        if isinstance(key, int):
            self.check_value(value)
            list.__setitem__(self, key, value)
        else:
            self.check_iterable(value)
            list.__setitem__(self, key, value)

    def __iadd__(self, collect):
        if not isinstance(collect, (list, tuple)):
            raise IdxTypeError
        self.check_iterable(collect)
        return list.__iadd__(self, collect)

    def __imul__(self, n):
        return Idx(list.__imul__(self, n))

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

        If *set* is True, an exception is raised in the previous case.
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
