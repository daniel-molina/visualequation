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

from typing import Optional
from copy import deepcopy
from enum import Enum, auto

from .idx import SelMode


class ColorProp(Enum):
    BLACK = auto()
    BLUE = auto()
    BROWN = auto()
    CYAN = auto()
    DARKGRAY = auto()
    GRAY = auto()
    GREEN = auto()
    LIGHTGRAY = auto()
    LIME = auto()
    MAGENTA = auto()
    OLIVE = auto()
    ORANGE = auto()
    PINK = auto()
    PURPLE = auto()
    RED = auto()
    TEAL = auto()
    VIOLET = auto()
    WHITE = auto()
    YELLOW = auto()

class FontProp(Enum):
    MATHIT = auto()
    MATHRM = auto()
    MATHBF = auto()
    MATHSF = auto()
    MATHTT = auto()


class StyleProp(Enum):
    DISPLAY = 1
    CDISPLAY = -1
    TEXT = 2
    CTEXT = -2
    SCRIPT = 3
    CSCRIPT = -3
    SCRIPTSCRIPT = 4
    CSCRIPTSCRIPT = -4


class PublicProperties(dict):
    # Properties can be None, the default value for each type,
    # associated to particular value that may be also explicitly chosen.
    TYPES = dict(
        color=ColorProp,
        font=FontProp,
        style=StyleProp,
    )

    def __init__(self, **kwargs):
        super().__init__(dict.fromkeys(self.TYPES.keys()))
        for k, v in kwargs.items():
            if k not in self:
                raise KeyError(repr(k) + " is not a public property.")
            self[k] = v

    def __setitem__(self, k, v):
        if k not in self.TYPES.keys():
            raise KeyError(repr(k) + " is not a public property.")
        super().__setitem__(k, v)

    def to_json(self):
        d = {k: v.value for k, v in self.items() if v is not None}
        if d:
            d["cls"] = "PP"
            return d

    @classmethod
    def from_json(cls, dct):
        pp = cls()
        for k, v in dct.items():
            if k != "cls":
                pp[k] = cls.TYPES[k](v)
        return pp


PSEUDOSYMB_WRONG_PP_ARG_ERROR_MSG = "pp must be a PublicProperties"
PSEUDOSYMB_PP_MIXED_ERROR_MSG = "pp must be a PublicProperties"


class PseudoSymb:
    def __init__(self, latex_code: str, lo_base: bool = False,
                 pp: Optional[PublicProperties] = None,
                 **kwargs):
        """Create a PseudoSymb.

        .. note::
            If pp parameter is used it is kept as a reference. You may want to
            pass a copy of an already used PublicProperties.
        """
        if not isinstance(latex_code, str):
            raise TypeError("Parameter latex_code must be a str.")
        self._latex_code = latex_code

        if not isinstance(lo_base, bool):
            raise TypeError("Parameter lo_base must be a bool.")
        self._lo_base = lo_base

        if pp is not None:
            if not isinstance(pp, PublicProperties):
                raise TypeError(PSEUDOSYMB_WRONG_PP_ARG_ERROR_MSG)
            if kwargs:
                raise TypeError(PSEUDOSYMB_PP_MIXED_ERROR_MSG)
            self.pp = pp
        else:
            self.pp = PublicProperties(**kwargs)

    def __eq__(self, other):
        if type(self) is type(other):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def _repr_priv(self):
        """Return a string containing the args of private attributes."""
        s_repr = repr(self._latex_code)
        if self._lo_base:
            s_repr += ", True"
        return s_repr

    def _repr_pub(self):
        """Helper."""
        s = ""
        for k, v in self.pp.items():
            if v is not None:
                s += ", " + k + "=" + str(v)
        return s

    def __repr__(self):
        """Return a valid string to generate the object.

        .. note::
            Python reminder: Output displayed by Python interpreter uses repr
            implicitly.
        """
        return "PseudoSymb(" + self._repr_priv() + self._repr_pub() + ")"

    def _str_pub(self):
        s_pp = ""
        for v in self.pp.values():
            if v is not None:
                s_pp += ", " + v.name
        return "{" + s_pp[2:] + "}" if s_pp else ""

    def __str__(self):
        return type(self).__name__ + self._str_pub()

    def __hash__(self):
        return hash(self.__dict__)


class Op(PseudoSymb):
    """Class for primitive elements of an equation."""

    def __init__(self, latex_code: str,
                 n_args: int = 1, pref_arg: int = 1, lo_base: bool = False,
                 pp: Optional[PublicProperties] = None,
                 **kwargs):
        super().__init__(latex_code, lo_base, pp=pp, **kwargs)
        if not isinstance(n_args, int):
            raise TypeError("Parameter n_args must be an int.")
        if n_args == 0 or n_args < -1:
            raise ValueError("Parameter n_args must be positive or -1.")

        if not isinstance(pref_arg, int):
            raise TypeError("Parameter pref_arg must be an int.")
        if pref_arg < 1:
            raise ValueError("Parameter pref_arg must be positive.")

        self._n_args = n_args
        self._pref_arg = pref_arg

    def _repr_priv(self):
        """Helper.

        .. note::
            It returns a string, not a repr of string.
        """
        s_repr = repr(self._latex_code)
        if self._n_args != 1:
            s_repr += ", " + repr(self._n_args)
        if self._pref_arg != 1:
            s_repr += ", pref_arg=" + repr(self._pref_arg)
        if self._lo_base:
            s_repr += ", lo_base=True"

        return s_repr

    def __repr__(self):
        """Return a valid string to generate the object.

        .. note::
            Python reminder: Output displayed by Python interpreter uses repr
            implicitly.
        """
        return "Op(" + self._repr_priv() + self._repr_pub() + ")"

    def _assert_valid_args(self, selmode: SelMode, arg_ord: Optional[int]):
        if not isinstance(selmode, SelMode):
            raise ValueError("Parameter selmode must be a SelMode.")
        if arg_ord is None:
            return
        if not isinstance(arg_ord, int):
            raise TypeError("Parameter arg_ord must be an int or None.")
        if arg_ord < 1 or arg_ord > self._n_args:
            raise ValueError("Parameter " + str(arg_ord) + " is not valid.")

    def rstep(self, selmode: SelMode, arg_ord: Optional[int] = None):
        """Return selmode and ordinal of par to select after pressing RIGHT.

        :param selmode: Current selection mode.
        :param arg_ord: Ordinal of parameter already selected. None means that
                        no parameter is already selected.
        :return: A pair similar to input or None, which means "continue
                 outside".
        """
        self._assert_valid_args(selmode, arg_ord)
        if arg_ord is None:
            return SelMode.LCURSOR, 1
        if arg_ord == self._n_args:
            return None
        return SelMode.LCURSOR, arg_ord + 1

    def lstep(self, selmode: SelMode, arg_ord: Optional[int] = None):
        """Return selmode and ordinal of par to select after pressing LEFT.

        :param selmode: Current selection mode.
        :param arg_ord: Ordinal of parameter already selected. None means that
                        no parameter is already selected.
        :return: A pair similar to input or None, which means "continue
                 outside".
        """
        self._assert_valid_args(selmode, arg_ord)
        if arg_ord is None:
            return SelMode.RCURSOR, self._n_args
        if arg_ord == 1:
            return None
        return SelMode.RCURSOR, arg_ord - 1

    def ustep(self, selmode: SelMode, arg_ord: Optional[int] = None):
        """Return selmode and ordinal of par to select after pressing UP.

        :param selmode: Current selection mode.
        :param arg_ord: Ordinal of parameter already selected. None means that
                        no parameter is already selected.
        :return: A pair similar to input or None, which means "not available".
        """
        self._assert_valid_args(selmode, arg_ord)
        return None

    def dstep(self, selmode: SelMode, arg_ord: Optional[int] = None):
        """Return selmode and ordinal of par to select after pressing DOWN.

        :param selmode: Current selection mode.
        :param arg_ord: Ordinal of parameter already selected. None means that
                        no parameter is already selected.
        :return: A pair similar to input or None, which means "not available".
        """
        self._assert_valid_args(selmode, arg_ord)
        return None


class Juxt(Op):
    def __init__(self, initial_n: int = 2, **kwargs):
        super().__init__(r"", n_args=-1, **kwargs)
        if not isinstance(initial_n, int):
            raise TypeError("Parameter initial_n must be an int.")
        if initial_n < 2:
            raise ValueError("Parameter initial_n must be bigger than 1.")
        self.current_n = initial_n

    def _assert_valid_args(self, selmode: SelMode, arg_ord: Optional[int]):
        if not isinstance(selmode, SelMode):
            raise ValueError("Parameter selmode must be a SelMode.")
        if arg_ord is None:
            return
        if not isinstance(arg_ord, int):
            raise TypeError("Parameter arg_ord must be an int or None.")
        if arg_ord < 1 or arg_ord > self.current_n:
            raise ValueError("Parameter " + str(arg_ord) + " is not valid.")

    def __repr__(self):
        """Return a valid string to generate the object.

        .. note::
            Python reminder: Output displayed by Python interpreter uses repr
            implicitly.
        """
        s = ""
        if self.current_n != 2:
            s += repr(self.current_n)
        extra = self._repr_pub()
        if extra and not s:
            extra = extra[2:]
        return "Juxt(" + s + extra + ")"

    def rstep(self, selmode: SelMode, arg_ord: Optional[int] = None):
        """Return selmode and ordinal of par to select after pressing RIGHT."""
        self._assert_valid_args(selmode, arg_ord)
        if arg_ord is None:
            return SelMode.LCURSOR, 1
        if arg_ord == self.current_n:
            return None
        return SelMode.LCURSOR, arg_ord + 1

    def lstep(self, selmode: SelMode, arg_ord: Optional[int] = None):
        """Return selmode and ordinal of par to select after pressing LEFT."""
        self._assert_valid_args(selmode, arg_ord)
        if arg_ord is None:
            return SelMode.RCURSOR, self.current_n
        if arg_ord == 1:
            return None
        return SelMode.RCURSOR, arg_ord - 1


class PJuxt(Juxt):
    def __init__(self, initial_n: int = 2, **kwargs):
        super().__init__(initial_n, **kwargs)

    def __repr__(self):
        return "P" + super().__repr__()

    def __str__(self):
        return "PJuxt" + str(self.current_n) + self._str_pub()

    def equiv_tjuxt(self):
        return TJuxt(self.current_n, pp=deepcopy(self.pp))

    def to_json(self):
        return dict(cls="PJ", n=self.current_n, pp=self.pp.to_json())

    @classmethod
    def from_json(cls, dct):
        return cls(dct["n"], pp=dct["pp"])


class TJuxt(Juxt):
    def __init__(self, initial_n: int = 2, **kwargs):
        super().__init__(initial_n, **kwargs)

    def __str__(self):
        return "TJuxt" + str(self.current_n) + self._str_pub()

    def __repr__(self):
        return "T" + super().__repr__()

    def to_json(self):
        return dict(cls="TJ", n=self.current_n, pp=self.pp.to_json())

    @classmethod
    def from_json(cls, dct):
        return cls(dct["n"], pp=dct["pp"])

    def equiv_pjuxt(self):
        return PJuxt(self.current_n, pp=deepcopy(self.pp))


class Pvoid(PseudoSymb):
    def __init__(self):
        super().__init__(r'\oblong')

    def __str__(self):
        return "PVOID"


PVOID = Pvoid()

# The following PseudoSymbs instances are defined here because they are not
# supposed to be modified
SELARG = PseudoSymb(r'\cdots')
#PVOID = Op("pvoid", r'\begingroup\color{purple}\oblong\endgroup')
#TVOID = Op("tvoid", r'\begingroup\color{lightgray}\oblong\endgroup')
#TVOID = Op("tvoid", r'\oblong')
#IEDIT = Op("ledit", r'\left\lgroup {0} \right\rmoustache', 1)
IEDIT = Op(r'\begingroup\color{{blue}}{0}\endgroup', n_args=1)
OEDIT = Op(r'\left\rmoustache {0} \right\lmoustache', n_args=1)

