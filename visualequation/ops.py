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

# Class to manage properties. None is a default value for each field,
# associated to particular value that must be also explicitly chosen
PP_KEYS = ("color", "font", "style")


class PublicProperties(dict):
    def __init__(self, **kwargs):
        super().__init__(dict.fromkeys(PP_KEYS))
        for k, v in kwargs.items():
            if k not in self:
                raise KeyError(repr(k) + " is not a public property.")
            self[k] = v

    def __setitem__(self, k, v):
        if k not in PP_KEYS:
            raise KeyError(repr(k) + " is not a public property.")
        super().__setitem__(k, v)


PSEUDOSYMB_WRONG_PP_ARG_ERROR_MSG = "pp must be a PublicProperties"
PSEUDOSYMB_PP_MIXED_ERROR_MSG = "pp must be a PublicProperties"


class PseudoSymb:
    def __init__(self, name: str, latex_code: str,
                 pp: Optional[PublicProperties] = None, **kwargs):
        """Create a PseudoSymb.

        .. note::
            If pp parameter is used it is kept as a reference. You may want to
            pass a copy of an already used PublicProperties.
        """
        if not isinstance(name, str):
            raise TypeError("Parameter name must be a str.")
        if not isinstance(latex_code, str):
            raise TypeError("Parameter latex_code must be a str.")
        self._name = name
        self._latex_code = latex_code

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

    def _repr_private(self):
        return repr(self._name) + ", " + repr(self._latex_code)

    def _repr_pp(self):
        s_repr = ""
        for k, v in self.pp.items():
            if v is not None:
                s_repr += ", " + k + "=" + repr(v)

        return s_repr

    def __repr__(self):
        return "PseudoSymb(" + self._repr_private() + self._repr_pp() + ")"

    def __str__(self):
        return self._name.upper()

    def __hash__(self):
        # Names must be unique for different instances
        return hash(self._name)


class Op(PseudoSymb):
    """Class for primitive elements of an equation."""

    def __init__(self, name: str, latex_code: str,
                 n_args: int = 1, pref_arg: int = 1, lo_base: bool = False,
                 user_sel: bool = True,
                 pp: Optional[PublicProperties] = None,
                 **kwargs):
        super().__init__(name, latex_code, pp=pp, **kwargs)
        if not isinstance(n_args, int):
            raise TypeError("Parameter n_args must be an int.")
        if n_args == 0 or n_args < -1:
            raise ValueError("Parameter n_args must be positive or -1.")

        if not isinstance(pref_arg, int):
            raise TypeError("Parameter pref_arg must be an int.")
        if pref_arg < 1:
            raise ValueError("Parameter pref_arg must be positive.")

        if not isinstance(lo_base, bool):
            raise TypeError("Parameter lo_base must be a bool.")

        if not isinstance(user_sel, bool):
            raise TypeError("Parameter user_sel must be a bool.")

        self._n_args = n_args
        self._pref_arg = pref_arg
        self._lo_base = lo_base
        self._user_sel = user_sel

    def _repr_private_aux(self, no_n_args=False, no_pref_arg=False,
                          no_lo_base=False, no_user_sel=False):
        s_repr = ""
        if not no_n_args and self._n_args != 1:
            s_repr += ", n_args=" + repr(self._n_args)
        if not no_pref_arg and self._pref_arg != 1:
            s_repr += ", pref_arg=" + repr(self._pref_arg)
        if not no_lo_base and self._lo_base:
            s_repr += ", lo_base=True"
        if not no_user_sel and not self._user_sel:
            s_repr += ", user_sel=False"

        return s_repr

    def __repr__(self):
        return "Op(" + self._repr_private() + self._repr_pp() \
               + self._repr_private_aux() + ")"

    def rstep(self, arg_ord: Optional[int] = None):
        """Return ordinal of argument to select after pressing RIGHT.

        :param arg_ord: Ordinal of parameter already selected. None means that
                       no parameter is already selected.
        :return: Ordinal of parameter to select. None means "continue outside".
        """
        if arg_ord is None:
            return 1
        elif not isinstance(arg_ord, int) \
                or 1 > arg_ord or arg_ord > self._n_args:
            raise ValueError("Argument " + str(arg_ord) + " is not valid.")
        return arg_ord + 1 if arg_ord != self._n_args else None

    def lstep(self, arg_ord: Optional[int] = None):
        """Return ordinal of argument to select after pressing LEFT.

        :param arg_ord: Ordinal of parameter already selected. None means that
                       no parameter is already selected.
        :return: Ordinal of parameter to select. None means "continue outside".
        """
        if arg_ord is None:
            return self._n_args
        elif not isinstance(arg_ord, int) \
                or 1 > arg_ord or arg_ord > self._n_args:
            raise ValueError("Argument " + str(arg_ord) + " is not valid.")
        return arg_ord - 1 if arg_ord != 1 else None

    def ustep(self, arg_ord: Optional[int] = None):
        """Return ordinal of argument to select after pressing UP.

        :param arg_ord: Ordinal of parameter already selected. None means that
                       no parameter is already selected.
        :return: Ordinal of parameter to select. None means "continue outside".
        """
        if arg_ord is None:
            return None
        elif not isinstance(arg_ord, int) \
                or 1 > arg_ord or arg_ord > self._n_args:
            raise ValueError("Argument " + str(arg_ord) + " is not valid.")
        return None

    def dstep(self, arg_ord: Optional[int] = None):
        """Return ordinal of argument to select after pressing DOWN.

        :param arg_ord: Ordinal of parameter already selected. None means that
                       no parameter is already selected.
        :return: Ordinal of parameter to select. None means "continue outside".
        """
        if arg_ord is None:
            return None
        elif not isinstance(arg_ord, int) or 1 > arg_ord \
                or arg_ord > self._n_args:
            raise ValueError("Argument " + str(arg_ord) + " is not valid.")
        return None


class PJuxt(Op):
    def __init__(self, initial_n: int = 2, **kwargs):
        super().__init__("pjuxt", "", n_args=-1, user_sel=False, **kwargs)
        if not isinstance(initial_n, int):
            raise TypeError("Parameter initial_n must be an int.")
        if initial_n < 2:
            raise ValueError("Parameter initial_n must be bigger than 1.")
        self.current_n = initial_n

    def __repr__(self):
        return "PJuxt(" + repr(self.current_n) + self._repr_pp() + ")"

    def equiv_tjuxt(self):
        return TJuxt(self.current_n, pp = deepcopy(self.pp))

    def rstep(self, arg_ord: Optional[int] = None):
        """Return ordinal of argument to select after pressing RIGHT.

        :param arg_ord: Ordinal of parameter already selected. None means that
                       no parameter is already selected.
        :return: Ordinal of parameter to select. None means "continue outside".
        """
        if arg_ord is None:
            return 1
        elif not isinstance(arg_ord, int) \
                or 1 > arg_ord or arg_ord > self.current_n:
            raise ValueError("Argument " + str(arg_ord) + " is not valid.")
        return arg_ord + 1 if arg_ord != self.current_n else None

    def lstep(self, arg_ord: Optional[int] = None):
        """Return ordinal of argument to select after pressing LEFT.

        :param arg_ord: Ordinal of parameter already selected. None means that
                       no parameter is already selected.
        :return: Ordinal of parameter to select. None means "continue outside".
        """
        if arg_ord is None:
            return self.current_n
        elif not isinstance(arg_ord, int) \
                or 1 > arg_ord or arg_ord > self.current_n:
            raise ValueError("Argument " + str(arg_ord) + " is not valid.")
        return arg_ord - 1 if arg_ord != 1 else None


class TJuxt(Op):
    def __init__(self, initial_n: int = 2, **kwargs):
        super().__init__("tjuxt", "", n_args=-1, **kwargs)
        self.current_n = initial_n

        if not isinstance(initial_n, int):
            raise TypeError("Parameter initial_n must be an int.")
        if initial_n < 2:
            raise ValueError("Parameter initial_n must be bigger than 1.")
        self.current_n = initial_n

    def equiv_pjuxt(self):
        return PJuxt(self.current_n, pp = deepcopy(self.pp))


# The following PseudoSymbs instances are defined to here because they are not
# supposed to be modified
SELARG = Op("selarg", r'\cdots')
#PVOID = Op("pvoid", r'\begingroup\color{purple}\oblong\endgroup')
PVOID = Op("pvoid", r'\oblong')
#TVOID = Op("tvoid", r'\begingroup\color{lightgray}\oblong\endgroup')
#TVOID = Op("tvoid", r'\oblong')
#IEDIT = Op("ledit", r'\left\lgroup {0} \right\rmoustache', 1)
IEDIT = Op("ledit", r'\begingroup\color{{blue}}{0}\endgroup', n_args=1)
OEDIT = Op("sedit", r'\left\rmoustache {0} \right\lmoustache', n_args=1)

