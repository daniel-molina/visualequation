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

"""A module to manage the class and operations related to scripts.

Two types of scripts are considered:

    *   Corner scripts.
    *   Vertical scripts.

A subeq which self.pp.ccls is CCls.OP or attribute self._char_class is
CCls.OP can have any combination of them. Else, it can have only scripts of
the same type (or corner ones or vertical ones). Depending on that, we can
classify scripts operators in three subtypes.

    *   LO: Script operators for bases which are CCls.OP.
    *   VERT: Script operators which only manage vertical scripts.
    *   CORN: Script operators which only manage corner scripts.

.. note::
    Implementation note: This script currently combines two philosophies
    to manage scripts (probably centered around ScriptOp and ScriptPars each
    one), so lot of code is probably unneeded. In an new iteration it is
    encouraged to simplify the concept. One idea would be to use lists of 7
    elements for ScriptPars independently of the ScriptOpSubtype.
"""

from typing import Optional, Union
from copy import deepcopy
from enum import Enum
from collections import OrderedDict

from .subeqs import Subeq
from .idx import Idx, SelMode
from .ops import Op, RVOID, CCls, primitive


class ScriptOpSubtype(Enum):
    LO = 0
    VERT = 1
    CORN = 2


class ScriptPos(Enum):
    """ A enum for script positions.

    Reasoning:
            5 6 7 <--- Super-scripts (left, center, right)
              1   <--- Base
            2 3 4 <--- Sub-scripts (left, center, right)

    ..note::
        Specific values are being used to simplify the code below (do not
        change them without a very good reason and fixing the dependent code).
    """
    LSUB = 2
    CSUB = 3
    RSUB = 4
    LSUP = 5
    CSUP = 6
    RSUP = 7


VERT_SCR_POS_TUPLE = (ScriptPos.CSUB, ScriptPos.CSUP)
CORN_SCR_POS_TUPLE = (ScriptPos.LSUB, ScriptPos.RSUB,
                      ScriptPos.LSUP, ScriptPos.RSUP)

SCRIPTOPS_DICT = {
    # is_lo, lsub, csub, rsub, lsup, csup, rsup
    (True, False, True, False, False, False, False):
        r'{0}_{{{1}}}',
    (True, False, False, False, False, True, False):
        r'{0}^{{{1}}}',
    (True, False, True, False, False, True, False):
        r'{0}_{{{1}}}^{{{2}}}',
    (True, True, False, False, False, False, False):
        r'\sideset{{_{{{1}}}}}{{}}{{{0}}}',
    (True, False, False, True, False, False, False):
        r'\sideset{{}}{{_{{{1}}}}}{{{0}}}',
    (True, False, False, False, True, False, False):
        r'\sideset{{^{{{1}}}}}{{}}{{{0}}}',
    (True, False, False, False, False, False, True):
        r'\sideset{{}}{{^{{{1}}}}}{{{0}}}',
    (True, True, False, True, False, False, False):
        r'\sideset{{_{{{1}}}}}{{_{{{2}}}}}{{{0}}}',
    (True, True, False, False, True, False, False):
        r'\sideset{{_{{{1}}}^{{{2}}}}}{{}}{{{0}}}',
    (True, True, False, False, False, False, True):
        r'\sideset{{_{{{1}}}}}{{^{{{2}}}}}{{{0}}}',
    (True, False, False, True, True, False, False):
        r'\sideset{{^{{{2}}}}}{{_{{{1}}}}}{{{0}}}',
    (True, False, False, True, False, False, True):
        r'\sideset{{}}{{_{{{1}}}^{{{2}}}}}{{{0}}}',
    (True, False, False, False, True, False, True):
        r'\sideset{{^{{{1}}}}}{{^{{{2}}}}}{{{0}}}',
    (True, True, False, True, True, False, False):
        r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}}}{{{0}}}',
    (True, True, False, True, False, False, True):
        r'\sideset{{_{{{1}}}}}{{^{{{3}}}_{{{2}}}}}{{{0}}}',
    (True, True, False, False, True, False, True):
        r'\sideset{{^{{{2}}}_{{{1}}}}}{{^{{{3}}}}}{{{0}}}',
    (True, False, False, True, True, False, True):
        r'\sideset{{^{{{2}}}}}{{^{{{3}}}_{{{1}}}}}{{{0}}}',
    (True, True, False, True, True, False, True):
        r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}^{{{4}}}}}{{{0}}}',
    # +Under
    (True, True, True, False, False, False, False):
        r'\sideset{{_{{{1}}}}}{{}}{{{0}}}_{{{2}}}',
    (True, False, True, True, False, False, False):
        r'\sideset{{}}{{_{{{2}}}}}{{{0}}}_{{{1}}}',
    (True, False, True, False, True, False, False):
        r'\sideset{{^{{{2}}}}}{{}}{{{0}}}_{{{1}}}',
    (True, False, True, False, False, False, True):
        r'\sideset{{}}{{^{{{2}}}}}{{{0}}}_{{{1}}}',
    (True, True, True, True, False, False, False):
        r'\sideset{{_{{{1}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}',
    (True, True, True, False, True, False, False):
        r'\sideset{{_{{{1}}}^{{{3}}}}}{{}}{{{0}}}_{{{2}}}',
    (True, True, True, False, False, False, True):
        r'\sideset{{_{{{1}}}}}{{^{{{3}}}}}{{{0}}}_{{{2}}}',
    (True, False, True, True, True, False, False):
        r'\sideset{{^{{{3}}}}}{{_{{{2}}}}}{{{0}}}_{{{1}}}',
    (True, False, True, True, False, False, True):
        r'\sideset{{}}{{_{{{2}}}^{{{3}}}}}{{{0}}}_{{{1}}}',
    (True, False, True, False, True, False, True):
        r'\sideset{{^{{{2}}}}}{{^{{{3}}}}}{{{0}}}_{{{1}}}',
    (True, True, True, True, True, False, False):
        r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}',
    (True, True, True, True, False, False, True):
        r'\sideset{{_{{{1}}}}}{{^{{{4}}}_{{{3}}}}}{{{0}}}_{{{2}}}',
    (True, True, True, False, True, False, True):
        r'\sideset{{^{{{3}}}_{{{1}}}}}{{^{{{4}}}}}{{{0}}}_{{{2}}}',
    (True, False, True, True, True, False, True):
        r'\sideset{{^{{{3}}}}}{{^{{{4}}}_{{{2}}}}}{{{0}}}_{{{1}}}',
    (True, True, True, True, True, False, True):
        r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}^{{{5}}}}}{{{0}}}_{{{2}}}',
    # +Over
    (True, True, False, False, False, True, False):
        r'\sideset{{_{{{1}}}}}{{}}{{{0}}}^{{{2}}}',
    (True, False, False, True, False, True, False):
        r'\sideset{{}}{{_{{{1}}}}}{{{0}}}^{{{2}}}',
    (True, False, False, False, True, True, False):
        r'\sideset{{^{{{1}}}}}{{}}{{{0}}}^{{{2}}}',
    (True, False, False, False, False, True, True):
        r'\sideset{{}}{{^{{{2}}}}}{{{0}}}^{{{1}}}',
    (True, True, False, True, False, True, False):
        r'\sideset{{_{{{1}}}}}{{_{{{2}}}}}{{{0}}}^{{{3}}}',
    (True, True, False, False, True, True, False):
        r'\sideset{{_{{{1}}}^{{{2}}}}}{{}}{{{0}}}^{{{3}}}',
    (True, True, False, False, False, True, True):
        r'\sideset{{_{{{1}}}}}{{^{{{3}}}}}{{{0}}}^{{{2}}}',
    (True, False, False, True, True, True, False):
        r'\sideset{{^{{{2}}}}}{{_{{{1}}}}}{{{0}}}^{{{3}}}',
    (True, False, False, True, False, True, True):
        r'\sideset{{}}{{_{{{1}}}^{{{3}}}}}{{{0}}}^{{{2}}}',
    (True, False, False, False, True, True, True):
        r'\sideset{{^{{{1}}}}}{{^{{{3}}}}}{{{0}}}^{{{2}}}',
    (True, True, False, True, True, True, False):
        r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}}}{{{0}}}^{{{4}}}',
    (True, True, False, True, False, True, True):
        r'\sideset{{_{{{1}}}}}{{^{{{4}}}_{{{2}}}}}{{{0}}}^{{{3}}}',
    (True, True, False, False, True, True, True):
        r'\sideset{{^{{{2}}}_{{{1}}}}}{{^{{{4}}}}}{{{0}}}^{{{3}}}',
    (True, False, False, True, True, True, True):
        r'\sideset{{^{{{2}}}}}{{^{{{4}}}_{{{1}}}}}{{{0}}}^{{{3}}}',
    (True, True, False, True, True, True, True):
        r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}^{{{5}}}}}{{{0}}}^{{{4}}}',
    # +UnderOver
    (True, True, True, False, False, True, False):
        r'\sideset{{_{{{1}}}}}{{}}{{{0}}}_{{{2}}}^{{{3}}}',
    (True, False, True, True, False, True, False):
        r'\sideset{{}}{{_{{{2}}}}}{{{0}}}_{{{1}}}^{{{3}}}',
    (True, False, True, False, True, True, False):
        r'\sideset{{^{{{2}}}}}{{}}{{{0}}}_{{{1}}}^{{{3}}}',
    (True, False, True, False, False, True, True):
        r'\sideset{{}}{{^{{{3}}}}}{{{0}}}_{{{1}}}^{{{2}}}',
    (True, True, True, True, False, True, False):
        r'\sideset{{_{{{1}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}^{{{4}}}',
    (True, True, True, False, True, True, False):
        r'\sideset{{_{{{1}}}^{{{3}}}}}{{}}{{{0}}}_{{{2}}}^{{{4}}}',
    (True, True, True, False, False, True, True):
        r'\sideset{{_{{{1}}}}}{{^{{{4}}}}}{{{0}}}_{{{2}}}^{{{3}}}',
    (True, False, True, True, True, True, False):
        r'\sideset{{^{{{3}}}}}{{_{{{2}}}}}{{{0}}}_{{{1}}}^{{{4}}}',
    (True, False, True, True, False, True, True):
        r'\sideset{{}}{{_{{{2}}}^{{{4}}}}}{{{0}}}_{{{1}}}^{{{3}}}',
    (True, False, True, False, True, True, True):
        r'\sideset{{^{{{2}}}}}{{^{{{4}}}}}{{{0}}}_{{{1}}}^{{{3}}}',
    (True, True, True, True, True, True, False):
        r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}^{{{5}}}',
    (True, True, True, True, False, True, True):
        r'\sideset{{_{{{1}}}}}{{^{{{5}}}_{{{3}}}}}{{{0}}}_{{{2}}}^{{{4}}}',
    (True, True, True, False, True, True, True):
        r'\sideset{{^{{{3}}}_{{{1}}}}}{{^{{{5}}}}}{{{0}}}_{{{2}}}^{{{4}}}',
    (True, False, True, True, True, True, True):
        r'\sideset{{^{{{3}}}}}{{^{{{5}}}_{{{2}}}}}{{{0}}}_{{{1}}}^{{{4}}}',
    (True, True, True, True, True, True, True):
        r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}^{{{6}}}}}{{{0}}}'
        r'_{{{2}}}^{{{5}}}',
    # Non-lo corners
    (False, True, False, False, False, False, False):
        r'\tensor*[_{{{1}}}]{{{0}}}{{}}',
    (False, False, False, True, False, False, False):
        r'\tensor*{{{0}}}{{_{{{1}}}}}',
    (False, False, False, False, True, False, False):
        r'\tensor*[^{{{1}}}]{{{0}}}{{}}',
    (False, False, False, False, False, False, True):
        r'\tensor*{{{0}}}{{^{{{1}}}}}',
    (False, True, False, True, False, False, False):
        r'\tensor*[_{{{1}}}]{{{0}}}{{_{{{2}}}}}',
    (False, True, False, False, True, False, False):
        r'\tensor*[_{{{1}}}^{{{2}}}]{{{0}}}{{}}',
    (False, True, False, False, False, False, True):
        r'\tensor*[_{{{1}}}]{{{0}}}{{^{{{2}}}}}',
    (False, False, False, True, True, False, False):
        r'\tensor*[^{{{2}}}]{{{0}}}{{_{{{1}}}}}',
    (False, False, False, True, False, False, True):
        r'\tensor*{{{0}}}{{^{{{2}}}_{{{1}}}}}',
    (False, False, False, False, True, False, True):
        r'\tensor*[^{{{1}}}]{{{0}}}{{^{{{2}}}}}',
    (False, True, False, True, True, False, False):
        r'\tensor*[_{{{1}}}^{{{3}}}]{{{0}}}{{_{{{2}}}}}',
    (False, True, False, True, False, False, True):
        r'\tensor*[_{{{1}}}]{{{0}}}{{^{{{3}}}_{{{2}}}}}',
    (False, True, False, False, True, False, True):
        r'\tensor*[^{{{2}}}_{{{1}}}]{{{0}}}{{^{{{3}}}}}',
    (False, False, False, True, True, False, True):
        r'\tensor*[^{{{2}}}]{{{0}}}{{^{{{3}}}_{{{1}}}}}',
    (False, True, False, True, True, False, True):
        r'\tensor*[_{{{1}}}^{{{3}}}]{{{0}}}{{_{{{2}}}^{{{4}}}}}',
    # Non-lo vertical
    (False, False, True, False, False, False, False):
        r'\underset{{{1}}}{{{0}}}',
    (False, False, False, False, False, True, False):
        r'\overset{{{1}}}{{{0}}}',
    (False, False, True, False, False, True, False):
        r'\overset{{{2}}}{{\underset{{{1}}}{{{0}}}}}',
}


@primitive
class ScriptOp(Op):
    ABBREV = "SO"

    def __init__(self, lo_subtype, *args, **kwargs):
        """Define a ScriptOp by passing needed ScriptPos's as parameters."""

        if not isinstance(lo_subtype, bool):
            raise TypeError("Parameter full_subtype must be a bool.")

        if not args:
            raise ValueError("At least one ScriptPos parameter must be "
                             "provided.")

        if lo_subtype:
            self._subtype = ScriptOpSubtype.LO
        elif args[0] in VERT_SCR_POS_TUPLE:
            self._subtype = ScriptOpSubtype.VERT
        else:
            self._subtype = ScriptOpSubtype.CORN

        # dicts not ordered prior to Python 3.7
        self._scripts = OrderedDict.fromkeys(ScriptPos, False)
        for spos in args:
            if not isinstance(spos, ScriptPos):
                raise TypeError("Positional parameters must be ScriptPos's.")
            if self._scripts[spos]:
                raise ValueError("Positional parameter " + repr(spos)
                                 + " has been passed more than once.")
            self._scripts[spos] = True

        # Look for incompatibilities
        if self._subtype is not ScriptOpSubtype.LO:
            danger = False
            for n in (3, 6):
                if ScriptPos(n) in args:
                    danger = True
                    break
            if danger:
                for n in (2, 4, 5, 7):
                    if ScriptPos(n) in args:
                        raise ValueError("ScriptPos parameters are not "
                                         "compatible with non-LO ScriptOp.")
        key = (self._subtype is ScriptOpSubtype.LO,)
        key += tuple(val for val in self._scripts.values())
        super().__init__(SCRIPTOPS_DICT[key], len(args) + 1, 1, **kwargs)

    def is_lo(self):
        return self._subtype is ScriptOpSubtype.LO

    def is_vert(self):
        return self._subtype is ScriptOpSubtype.VERT

    def is_corn(self):
        return self._subtype is ScriptOpSubtype.CORN

    def _repr_priv(self):
        s_repr = "True" if self.is_lo() else "False"
        for spos, present in self._scripts.items():
            if present:
                s_repr += ", " + str(spos)
        return s_repr

    def __repr__(self):
        return "ScriptOp(" + self._repr_priv() + self._repr_pub() + ")"

    def __str__(self):
        s = "LO" if self.is_lo() else ""
        for spos, val in self._scripts.items():
            if val:
                s += spos.name
        return s + self._str_pub()

    def valid_scripts_values(self):
        """Return an iterator through valid _scripts values, in order.

        .. note::
            Valid script are not those which are present, but those allowed by
            the ScriptOpSubtype.
        """
        if self.is_lo():
            return self._scripts.values()
        if self.is_vert():
            return (self._scripts[ScriptPos(num)] for num in (3, 6))
        return (self._scripts[ScriptPos(num)] for num in (2, 4, 5, 7))

    def valid_scripts_keys(self, only_used=False):
        """Return an iterator through valid _scripts keys, in order.

        .. note::
            Valid script are not those which are present, but those allowed by
            the ScriptOpSubtype.
        """
        if only_used:
            return (k for k, v in self._scripts.items() if v)
        if self.is_lo():
            return self._scripts.keys()
        if self.is_vert():
            return (ScriptPos(num) for num in (3, 6))
        return (ScriptPos(num) for num in (2, 4, 5, 7))

    def valid_scripts_items(self):
        """Return an iterator through valid _scripts items, in order.

        .. note::
            Valid script are not those which are present, but those allowed by
            the ScriptOpSubtype.
        """
        if self.is_lo():
            return self._scripts.items()
        return ((k, self._scripts[k]) for k in self.valid_scripts_keys())

    def ord2spos(self, ord: int):
        """Given the ordinal of an argument, return associated ScriptPos.

        .. note::
            *ord* == 1 would always refer to the base, which is not a
            ScriptPos.
            In that case, an exception is raised.
        """
        if not isinstance(ord, int):
            raise TypeError("Parameter ord must be an int.")
        if ord < 2 or ord > self._n_args:
            raise ValueError("Parameter ordinal is not in (2, "
                             + str(self._n_args) + ").")
        ord_counter = 1
        for spos, present in self._scripts.items():
            if present:
                ord_counter += 1
            if ord_counter == ord:
                return spos
        raise ValueError("This should never have happened...")

    def spos2ord(self, pos: ScriptPos):
        """Given a ScriptPos, return the ordinal of associated argument."""
        if not isinstance(pos, ScriptPos):
            raise TypeError("Parameter pos must be a ScriptPos.")
        if not self._scripts[pos]:
            raise ValueError("Passed ScriptPos is not present in this op.")
        ord = 1
        for k, v in self._scripts.items():
            if v:
                ord += 1
            if k is pos:
                return ord
        raise ValueError("This should never have happened...")

    def _script2r(self, spos):
        """Return the ScriptPos to the right of spos.

        If instance does not have a script to the right of *spos*, None is
        returned.

        .. note::
            *spos* MUST be an existing ScriptPos for the instance.
        """
        # Golf code contest starts here :P
        # It would be sane to write this more clearly.
        if spos in (ScriptPos.RSUB, ScriptPos.RSUP):
            return None
        v = 2 if spos.value < 5 else 5
        if self._scripts[ScriptPos(v + 2)]:
            if not self._scripts[ScriptPos(v + 1)] or spos.value == v + 1:
                return ScriptPos(v + 2)
            return ScriptPos(v + 1)
        if self._scripts[ScriptPos(v + 1)] and spos.value == v:
            return ScriptPos(v + 1)

    def _script2l(self, spos):
        """Return the ScriptPos to the left of spos.

        If instance does not have a script to the left of *spos*, None is
        returned.

        .. note::
            *spos* MUST be an existing ScriptPos for the instance.
        """
        if spos in (ScriptPos.LSUB, ScriptPos.LSUP):
            return None
        v = 2 if spos.value < 5 else 5
        if self._scripts[ScriptPos(v)]:
            if not self._scripts[ScriptPos(v + 1)] or spos.value == v + 1:
                return ScriptPos(v)
            return ScriptPos(v + 1)
        if self._scripts[ScriptPos(v + 1)] and spos.value == v + 2:
            return ScriptPos(v + 1)

    def rstep(self, arg_ord: Optional[int] = None):
        self._assert_valid_args(arg_ord)
        if arg_ord is None:
            return 1
        if arg_ord != 1 and self._script2r(self.ord2spos(arg_ord)) is not None:
            return arg_ord + 1

    def lstep(self, arg_ord: Optional[int] = None):
        self._assert_valid_args(arg_ord)
        if arg_ord is None:
            return 1
        if arg_ord != 1 and self._script2l(self.ord2spos(arg_ord)) is not None:
            return arg_ord - 1

    def ustep(self, arg_ord: Optional[int], selmode: SelMode):
        self._assert_valid_args(arg_ord, selmode)
        if arg_ord != 1:
            spos = self.ord2spos(arg_ord)
            if spos.value > 4:
                return None
            return 1
        if selmode in (SelMode.RCUR, SelMode.RHL):
            for pos in (ScriptPos.CSUP, ScriptPos.RSUP, ScriptPos.LSUP):
                if self._scripts[pos]:
                    return self.spos2ord(pos)

        for pos in (ScriptPos.CSUP, ScriptPos.LSUP, ScriptPos.RSUP):
            if self._scripts[pos]:
                return self.spos2ord(pos)

    def dstep(self, arg_ord: Optional[int], selmode: SelMode):
        self._assert_valid_args(arg_ord, selmode)
        if arg_ord != 1:
            spos = self.ord2spos(arg_ord)
            if spos.value <= 4:
                return None
            return 1
        if selmode in (SelMode.RCUR, SelMode.RHL):
            for pos in (ScriptPos.CSUB, ScriptPos.RSUB, ScriptPos.LSUB):
                if self._scripts[pos]:
                    return self.spos2ord(pos)
        else:
            for pos in (ScriptPos.CSUB, ScriptPos.LSUB, ScriptPos.RSUB):
                if self._scripts[pos]:
                    return self.spos2ord(pos)

    def to_json(self):
        scripts_list = [k.value for k, v in self._scripts.items() if v]
        return dict(cls=self.ABBREV, typ=self._subtype.value, scr=scripts_list)

    @classmethod
    def from_json(cls, dct):
        spos_list = [ScriptPos(v) for v in dct["scr"]]
        return cls(ScriptOpSubtype(dct["typ"]), *spos_list)


class ScriptPars(list):
    def __init__(self, base: Subeq, subtype: ScriptOpSubtype):
        """Create a ScriptOp pars list from a base and requested ScriptOpType.

        The number of pars is decided according to *subtype* and they all
        are set to None.
        """

        super().__init__()
        self.append(deepcopy(Subeq(base)))
        if subtype is ScriptOpSubtype.VERT:
            self.extend([None] * 2)
        elif subtype is ScriptOpSubtype.CORN:
            self.extend([None] * 4)
        else:
            self.extend([None] * 6)

    def find(self, script_pos: ScriptPos):
        """Return script position in a pars list. If script parameters are not
        compatible with pars, return -1.

        .. note::
            Only compatibility of referred script in provided *self* is
            checked. In particular, it is NOT checked whether the base
            (pars[0]) is valid for the op associated to *self*.

        :param script_pos: A script position.
        :return: script position in pars (from 1 to len(pars)-1 since base is
                 not a script) or -1.
        """
        if len(self) == 3:
            if script_pos not in VERT_SCR_POS_TUPLE:
                return -1
            return VERT_SCR_POS_TUPLE.index(script_pos) + 1
        if len(self) == 5:
            if script_pos not in CORN_SCR_POS_TUPLE:
                return -1
            return CORN_SCR_POS_TUPLE.index(script_pos) + 1

        return script_pos.value - 1

    def set_script(self, script_pos: ScriptPos, pspar: Subeq):
        self[self.find(script_pos)] = pspar

    def get_script(self, script_pos: ScriptPos):
        """Get current script in pars given its script position.

        If script is not compatible with passed pars, -1 is returned.
        """
        pos = self.find(script_pos)
        return self[pos] if pos > 0 else -1

    def transform2lo(self):
        """Transform, if needed, to match the best LO ScriptOp.

        .. note::
            This function only changes script positions being used, it does NOT
            check whether the base is valid for certain subtype. It does not
            care
            about valid bases.
        """
        if len(self) == 3:
            self[:] = [self[0], None, self[1], None, None, self[2], None]
        elif len(self) == 5:
            self[:] = [self[0], self[1], None, self[2], self[3], None, self[4]]

    def transform2corn(self):
        """Transform, if needed, pars to match the best CORN ScriptOp.

        .. note::
            This function only changes script positions being used, it does
            NOT check whether the base is valid for certain subtype. It does
            not care about valid bases.

        Consider transform2nonfull if you do not want to impose CORN on VERT.
        """
        if len(self) == 3:
            self[:] = [self[0], None, self[1], None, self[2]]
            return
        if len(self) == 5:
            return
        if self[2] is None and self[5] is None:
            self[:] = [self[0], self[1], self[3], self[4], self[6]]
            return
        self[:] = [self[0], None, self[2], None, self[5]]

    def transform2vert(self):
        """Transform, if needed, pars to match the best VERT ScriptOp.

        .. note::
            This function only changes script positions being used, it does NOT
            check whether the base is valid for certain type_. It does not care
            about valid bases.

        Consider scriptop_pars2nonfull_pars function if you do not want to
        impose VERT on CORN.
        """
        if len(self) == 3:
            return
        if len(self) == 5:
            self[:] = [self[0], self[2], self[4]]
            return
        if self[2] is None and self[5] is None:
            self[:] = [self[0], self[3], self[6]]
            return
        self[:] = [self[0], self[2], self[5]]

    def transform2nonfull(self):
        """Decide whether VERT or CORN fit better certain pars and return the
        correspondent new pars.

        .. note::
            This function only changes script positions being used, it does NOT
            check whether the base is valid at all.
        """
        if len(self) != 7:
            return
        if self[2] is None and self[5] is None:
            # No subeqs are lost in this case
            self[:] = [self[0], self[1], self[3], self[4], self[6]]
            return
        # Some subeqs may be lost in this case
        self[:] = [self[0], self[2], self[5]]

    @classmethod
    def from_scriptblock(cls, subeq: Subeq, index: Idx = None):
        """Return a ScriptPars of the passed script-block.

        If subeq is a symbol or lop-block is not a ScriptOp, -1 is returned.

        .. note::
            It is OK if the script-block does not have a valid base according
            to does_require_full (probably because you are modificating the
            eq). Decisions are taken based on lop-block.
        """

        s = subeq(index)
        op = s[0]
        # Check that it is effectively a script-block
        if not isinstance(op, ScriptOp):
            return -1

        pars = cls(deepcopy(s[1]), op._subtype)
        for i, (spos, present) in enumerate(op.valid_scripts_items()):
            pars[i + 1] = deepcopy(s[op.spos2ord(spos)]) if present else None
        return pars

    def argord2index(self, argord: int):
        """Return the position of the n-th non-None par in pars list.

        .. note::

            flat_pos == 0 would mean the base in the pars of a script-block.
        """

        valid_pars_found = 0
        for pars_pos, pars_arg in enumerate(self):
            if pars_arg is not None:
                if valid_pars_found == argord:
                    return pars_pos
                else:
                    valid_pars_found += 1
        raise ValueError("Invalid argord parameter: " + repr(argord) + ".")

    def index2scriptpos(self, index):
        """Return the ScriptPos associated to certain element of self
        specified by its index"""
        if index == 0:
            raise ValueError("Invalid 0 index parameter. That is the base.")
        if index < 0 or index > len(self) - 1:
            raise ValueError("Invalid index parameter: " + repr(index) + ".")
        if len(self) == 7:
            return ScriptPos(index + 1)
        if len(self) == 5:
            return ScriptPos((2, 4, 5, 7)[index - 1])
        return ScriptPos((3, 6)[index - 1])

    def spos2argord(self, spos: ScriptPos):
        """Return the ordinal of a parameter of a ScriptOp given the pars
        representation of its block and the ScriptPos of the param."""
        index = self.find(spos)
        if index == -1:
            raise ValueError("Instance not compatible with passed ScriptPos.")
        return self.index2argord(index)

    def used_scriptpos(self):
        """Return a generator of used ScriptPos's in order."""
        return (self.index2scriptpos(num + 1) for num, p in enumerate(self[1:])
                if p is not None)

    def index2argord(self, index: int):
        """Return the ordinal of a parameter of a ScriptOp given the pars
        representation of its block and the position in pars of the parameter.

        .. note::
            *par_pos* == 0 refers to the base of a script-block => 1 will be
            returned in every case.

        :param index: The position of the par in *self* (first par_pos is 0).
        :return: The parameter ordinal associated to *par_pos* in a ScriptOp.
        """
        # Take into account the leading op, which is not included in args
        ordinal = 1
        if self[index] is None:
            raise ValueError("Request is not valid. Referred element is "
                             "None.")
        for i in range(index):
            if self[i] is not None:
                ordinal += 1
        return ordinal

    def scriptop(self):
        """Return the operator associated to a pars list.

        .. note::
            If every argument (except possibly the base) is None, None is
            returned.
        """
        tpl = tuple(self.used_scriptpos())
        if not tpl:
            return None
        if len(self) == 7:
            return ScriptOp(True, *tpl)
        return ScriptOp(False, *tpl)

    def scriptblock(self):
        """Return associated script block.

        .. note::
            If every argument, except possibly the base, is None, -1 is
            returned.
        """
        op = self.scriptop()
        if op is None:
            return -1
        return Subeq([op] + [item for item in self if item is not None])


# Dictionaries providing a map between positions of pars before a change of
# script-block and after it. VERT_CORN means that the VERT is more external.
CORN2VERT_DICT = {0: 0, 2: 1, 4: 2}
CORN2LO_DICT = {0: 0, 1: 1, 2: 3, 3: 4, 4: 6}
CORN2CORN_VERT_DICT = {0: (0, 0), 1: (1,), 2: (2,), 3: (3,), 4: (4,)}
CORN2VERT_CORN_DICT = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (0, 3), 4: (0, 4)}
CORN_VERT2VERT_CORN_DICT = {(0, 0): (0, 0),
                            (1,): (0, 1), (0, 1): (1,), (2,): (0, 2),
                            (3,): (0, 3), (0, 2): (2,), (4,): (0, 4)}
VERT2LO_DICT = {0: 0, 1: 2, 2: 5}
VERT2CORN_VERT_DICT = {0: (0, 0), 1: (0, 1), 2: (0, 2)}
VERT2VERT_CORN_DICT = {0: (0, 0), 1: (1,), 2: (2,)}
CORN_VERT2LO_DICT = {
    (0, 0): 0, (1,): 1, (0, 1): 2, (2,): 3, (3,): 4, (0, 2): 5, (4,): 6}
VERT_CORN2LO_DICT = {
    (0, 0): 0, (0, 1): 1, (1,): 2, (0, 2): 3, (0, 3): 4, (2,): 5, (0, 4): 6}

VERT2CORN_DICT = {v: k for k, v in CORN2VERT_DICT.items()}
LO2CORN_DICT = {v: k for k, v in CORN2LO_DICT.items()}
CORN_VERT2CORN_DICT = {v: k for k, v in CORN2CORN_VERT_DICT.items()}
VERT_CORN2CORN_DICT = {v: k for k, v in CORN2VERT_CORN_DICT.items()}
VERT_CORN2CORN_VERT_DICT = {v: k for k, v in CORN_VERT2VERT_CORN_DICT.items()}
LO2VERT_DICT = {v: k for k, v in VERT2LO_DICT.items()}
CORN_VERT2VERT_DICT = {v: k for k, v in VERT2CORN_VERT_DICT.items()}
VERT_CORN2VERT_DICT = {v: k for k, v in VERT2VERT_CORN_DICT.items()}
LO2CORN_VERT_DICT = {v: k for k, v in CORN_VERT2LO_DICT.items()}
LO2VERT_CORN_DICT = {v: k for k, v in VERT_CORN2LO_DICT.items()}


def does_require_lo(base: Subeq):
    return not isinstance(base[0], str) \
           and (base[0].pp["ccls"] is CCls.OP
                or (base[0].pp["ccls"] is None
                    and base[0]._ccls is CCls.OP))


def is_scriptop(elem: Union[Subeq, Op], index: Optional[Idx] = None):
    """Return whether an operator is an script op."""
    op = elem if index is None else elem(index)
    return isinstance(op, ScriptOp)


def is_base(eq: Subeq, index: Idx):
    """Returns whether pointed subeq is a base."""
    return index != [] and index[-1] == 1 and is_scriptop(eq, index.outlop())


def is_script(eq: Subeq, index: Idx):
    return index != [] and index[-1] != 1 and is_scriptop(eq, index.outlop())


def _map_refindex(sb_index, ref_index, ext_prev_pars, prev_pars, ext_next_pars,
                  next_pars):
    """Return the equivalent index of a subequation after a modification of a
    script-block or a external-internal script-block (modification is not
    managed by this function, only the correction of the index).

    Requirements:

        This function is very flexible. The only requirement is that
        *ref_index* must point to a real subeq before the operation.

    In case that *ref_index* points to a script involved in the operation and
    it does not exist after it, -1 is returned.

    *sb_index* must be the index of the script-block that was effectively
    updated. In the case of being two of them, the most external one.

    *ext_prev_pars* and/or *ext_next_pars* must be set to None if there is no
    previous/next external script block.
    """
    sbidx = Idx(sb_index)
    refidx = Idx(ref_index)
    start = refidx[:len(sbidx)]
    tail = refidx[len(sbidx):]
    if start != sbidx or not tail:
        # It always includes the case ref_index == []
        return refidx

    # Note: tail has at least one element at this point
    if ext_prev_pars is None:
        prev_pos_key = prev_pars.argord2index(tail.pop(0) - 1)
    elif tail == [1] and ext_next_pars is None:
        return start
    elif tail == [1]:
        return start + [1]
    elif tail[0] == 1:
        prev_pos_key = (0, prev_pars.argord2index(tail[1] - 1))
        del tail[0:2]
    else:
        prev_pos_key = (ext_prev_pars.argord2index(tail.pop(0) - 1),)

    def next_pos_value2l(next_pos_val):
        # It can raise ValueError, which will be handled by the caller below
        if ext_next_pars is None:
            # This case assures that value is not a tuple
            return [next_pars.index2argord(next_pos_val)]
        elif len(next_pos_val) == 1:
            return [ext_next_pars.index2argord(next_pos_val[0])]
        else:
            return [1, next_pars.index2argord(next_pos_val[1])]

    def prev_pos_key2idx(key_dict=None):
        """If argument is None it is understood that the mapping is the
        identity function: pos -> pos"""
        try:
            if key_dict is None:
                return start + next_pos_value2l(prev_pos_key) + tail
            else:
                return start + next_pos_value2l(key_dict[prev_pos_key]) + tail
        except ValueError:
            return -1

    if ext_prev_pars is None and ext_next_pars is None:
        if len(prev_pars) == len(next_pars):
            return prev_pos_key2idx()
        if len(prev_pars) == 3 and len(next_pars) == 5:
            return prev_pos_key2idx(VERT2CORN_DICT)
        if len(prev_pars) == 3 and len(next_pars) == 7:
            return prev_pos_key2idx(VERT2LO_DICT)
        if len(prev_pars) == 5 and len(next_pars) == 3:
            return prev_pos_key2idx(CORN2VERT_DICT)
        if len(prev_pars) == 5 and len(next_pars) == 7:
            return prev_pos_key2idx(CORN2LO_DICT)
        if len(prev_pars) == 7 and len(next_pars) == 3:
            return prev_pos_key2idx(LO2VERT_DICT)
        if len(prev_pars) == 7 and len(next_pars) == 5:
            return prev_pos_key2idx(LO2CORN_DICT)

    if ext_prev_pars and ext_next_pars is None:
        if len(ext_prev_pars) == 3 and len(next_pars) == 3:
            return prev_pos_key2idx(VERT_CORN2VERT_DICT)
        if len(ext_prev_pars) == 3 and len(next_pars) == 5:
            return prev_pos_key2idx(VERT_CORN2CORN_DICT)
        if len(ext_prev_pars) == 3 and len(next_pars) == 7:
            return prev_pos_key2idx(VERT_CORN2LO_DICT)
        if len(ext_prev_pars) == 5 and len(next_pars) == 3:
            return prev_pos_key2idx(CORN_VERT2CORN_DICT)
        if len(ext_prev_pars) == 5 and len(next_pars) == 5:
            return prev_pos_key2idx(CORN_VERT2CORN_DICT)
        if len(ext_prev_pars) == 5 and len(next_pars) == 7:
            return prev_pos_key2idx(CORN_VERT2LO_DICT)

    if ext_prev_pars is None and ext_next_pars:
        if len(prev_pars) == 3 and len(ext_next_pars) == 3:
            return prev_pos_key2idx(VERT2VERT_CORN_DICT)
        if len(prev_pars) == 3 and len(ext_next_pars) == 5:
            return prev_pos_key2idx(VERT2CORN_VERT_DICT)
        if len(prev_pars) == 5 and len(ext_next_pars) == 3:
            return prev_pos_key2idx(CORN2VERT_CORN_DICT)
        if len(prev_pars) == 5 and len(ext_next_pars) == 5:
            return prev_pos_key2idx(CORN2CORN_VERT_DICT)
        if len(prev_pars) == 7 and len(ext_next_pars) == 3:
            return prev_pos_key2idx(LO2VERT_CORN_DICT)
        if len(prev_pars) == 7 and len(ext_next_pars) == 5:
            return prev_pos_key2idx(LO2CORN_VERT_DICT)

    if len(ext_prev_pars) == len(ext_next_pars):
        return prev_pos_key2idx()
    if len(ext_prev_pars) == 3 and len(ext_next_pars) == 5:
        return prev_pos_key2idx(VERT_CORN2CORN_VERT_DICT)
    return prev_pos_key2idx(CORN_VERT2VERT_CORN_DICT)


def _change2full(eq: Subeq, index, refindex=None):
    """Helper function.

    eq(index) must be a script-block.

    If pointed subeq is a VERT/CORN script-block, it checks whether the
    1-level supeq is a CORN/VERT script-block so their scripts can be included
    in the new LO script-block.
    """
    idx = Idx(index)
    refidx = Idx(refindex)
    sb = eq(idx)
    op_subtype = sb[0]._subtype
    if op_subtype is ScriptOpSubtype.LO:
        return refidx

    inner_pars = ScriptPars.from_scriptblock(sb)
    sup = eq.supeq(idx)
    ext_pars = None
    if sup != -2 and isinstance(sup[0], ScriptOp) \
            and sup[0]._subtype is not op_subtype:
        # It cannot be the case of sup being a LO ScriptOp-block because of
        # Subeqs building rules: they cannot have ScriptOp-blocks as bases.
        ext_pars = ScriptPars.from_scriptblock(sup)
        del idx[-1]

    if op_subtype is ScriptOpSubtype.CORN:
        # Sub-cases:
        #   [CORN, ...] -> [LO, ...]
        #   [VERT, [CORN, ...], ...] -> [LO, ...]
        new_pars = ScriptPars(inner_pars[0], ScriptOpSubtype.LO)
        new_pars[1:] = [inner_pars[1], None, inner_pars[2],
                        inner_pars[3], None, inner_pars[4]]
        if ext_pars:
            new_pars[2] = ext_pars[1]
            new_pars[5] = ext_pars[2]
    elif not ext_pars:
        # Subcase: [VERT, ...] -> [LO, ...]
        new_pars = ScriptPars(inner_pars[0], ScriptOpSubtype.LO)
        new_pars[1:] = [None, inner_pars[1], None, None, inner_pars[2], None]
    else:
        # Subcase: [CORN, [VERT, ...], ...] -> [LO, ...]
        new_pars = ScriptPars(inner_pars[0], ScriptOpSubtype.LO)
        new_pars[1:] = [ext_pars[1], inner_pars[1], ext_pars[2],
                        ext_pars[3], inner_pars[2], ext_pars[4]]

    # Note: idx has previously been corrected if needed
    eq(idx)[:] = new_pars.scriptblock()
    return _map_refindex(idx, refidx, ext_pars, inner_pars, None, new_pars)


def _change2nonfull(eq: Subeq, index, refindex=None):
    """Helper function.

    eq(index) must be a script-block.

    It does not check any supeq, so they are never combined with the new
    scriptop. However, to avoid loosing scripts a LO script-block will be
    converted in a CORN script-block which base is a VERT script-block if
    necessary.

    Implementation note:

        [LO, ...] -> [CORN, [VERT, ...], ....]
    """
    idx = Idx(index)
    refidx = Idx(refindex)
    sb = eq(idx)
    op = sb[0]
    op_subtype = op._subtype
    if op_subtype is not ScriptOpSubtype.LO:
        return refidx

    pars = ScriptPars.from_scriptblock(sb)
    new_ext_pars = None
    if pars[2] is None and pars[5] is None:
        new_inner_pars = ScriptPars(pars[0], ScriptOpSubtype.CORN)
        new_inner_pars[1:] = [pars[1], pars[3], pars[4], pars[6]]
        new_pars = new_inner_pars
    elif [pars[1], pars[3], pars[4], pars[6]].count(None) == 4:
        new_inner_pars = ScriptPars(pars[0], ScriptOpSubtype.VERT)
        new_inner_pars[1:] = [pars[2], pars[5]]
        new_pars = new_inner_pars
    else:
        # Two script ops are needed to avoid missing any script
        # -> Use VERT op externally and CORN internally
        new_inner_pars = ScriptPars(pars[0], ScriptOpSubtype.VERT)
        new_inner_pars[1:] = [pars[2], pars[5]]
        inner_sb = new_inner_pars.scriptblock()

        new_ext_pars = ScriptPars(inner_sb, ScriptOpSubtype.CORN)
        new_ext_pars[1:] = [pars[1], pars[3], pars[4], pars[6]]
        new_pars = new_ext_pars

    sb[:] = new_pars.scriptblock()
    return _map_refindex(idx, refidx, None, pars, new_ext_pars, new_inner_pars)


def update_scriptblock(nextbase: list, eq: Subeq, index=None, refindex=None):
    """Update a script op if needed by providing the next base it will have.
    Pointed subeq must be the supeq of the subeq being modified. That is,
    the script block if modified subeq is really a base, but it is OK if it
    is not really a script block (nothing is done in that case and refindex
    is returned unmodified).

    A 1-level supeq which is a script-block will be collapsed if reasonable
    when updating from nonlo to lo script-block. Similarly, a lo script-block
    may be extended into a combination of script-block and setscript-block,
    being the first one the most external.

    .. note::
        The script operator is updated independently of which is its current
        base, only value *nextbase* is considered.

    Implementation note:

        The main reasoning for the previous behaviour is to facilitate not
        loose any information in simple operations, like navigating through
        the equation. If that behavior results disturbing, it may be considered
        to force the loss of scripts for this general function. Maybe writing
        two versions is the best idea if both are useful.
    """
    scriptblock = eq(index)
    refidx = Idx(refindex)
    nb = Subeq(nextbase)

    if not isinstance(scriptblock[0], ScriptOp):
        return refidx
    if scriptblock[0].is_lo():
        if does_require_lo(nb):
            return refidx
        # VERT/CORN (or a combination of both) -> LO
        return _change2nonfull(eq, index, refindex)

    if not does_require_lo(nb):
        return refidx
    return _change2full(eq, index, refindex)


def _insert_initial_script(baseref: Subeq, script_pos: ScriptPos,
                           newscript: Subeq):
    """Insert a script to a block which is (currently) not a base or requested
    script is not compatible with operator script of base pointed.

    Index of the script will be index of *baseref* plus [2]
    """
    if does_require_lo(baseref):
        subtype = ScriptOpSubtype.LO
    elif script_pos in VERT_SCR_POS_TUPLE:
        subtype = ScriptOpSubtype.VERT
    else:
        subtype = ScriptOpSubtype.CORN
    pars = ScriptPars(baseref, subtype)
    # referred script is guaranteed to be valid in pars list because we
    # constructed pars with the correct subtype
    pars.set_script(script_pos, newscript)
    baseref[:] = pars.scriptblock()


def insert_script(index, eq: Subeq, script_pos: ScriptPos,
                  newscript: Optional[list] = None):
    """Insert a script and return its index.

    Return the index of the inserted script, or its ordinal in the current
    script block if the index already existed.

    If *newscript* is None, a [RVOID] will be used as script, if it did not
    exist.

    .. note::
        Pointing to a script-block is almost equivalent to point to its base,
        except:

            *   Selection is preferred to be a base than a script-block,
                as expected intuitively. This matters in complex setups.
            *   Return value will be negative if a script-block is considered.

    Rules:

        Notation: The term 'minimal' script op refers to the script op which
        has only one script. That script will be the requested one.

        *   If *index* does not point to a current base, a minimal script
            operator will be added, being its base the subeq pointed by
            *index*.
            The index of the created script will be returned.
        *   Elif *index* points to a current base, requested script does not
            exist and the script is compatible with the script operator, script
            operator is upgraded and the index of the new script is returned.
        *   Elif *idx* points to a current base which script op is not
            compatible with requested script, a new minimal script block
            containing the requested script will replace that base.
            The index of the new script in *eq* is returned.
        *   Else (*idx* points to a current base and requested script exists),
            *eq* is not modified and the ordinal of the script par matching
            requested script is returned.

    :param index: The index of the subeq which will be the base of the script.
    :param eq: An equation.
    :param scrip_pos: Position to insert the script.
    :param newscript: A subeq with which to initialize script. None means void.
    :return: The index of inserted script. If it already existed, a flag.
    """
    scr = deepcopy(Subeq([RVOID] if newscript is None else newscript))
    idx = Idx(index)
    script_op_pointed = False
    if not is_base(eq, idx) and is_scriptop(eq(idx)[0]):
        # Case: idx does point to a scriptop which is not a base
        idx += [1]
        script_op_pointed = True

    if not is_base(eq, idx):
        # Case: idx does not point to a base
        baseref = eq if not idx else eq(idx)
        _insert_initial_script(baseref, script_pos, scr)
        return idx[:] + [2]

    supeq = eq.supeq(idx)
    pars = ScriptPars.from_scriptblock(supeq)
    script = pars.get_script(script_pos)
    if script == -1:
        # Case: Requested script is not compatible with current operator
        if script_op_pointed:
            _insert_initial_script(supeq, script_pos, scr)
            return idx[:-1] + [2]
        else:
            _insert_initial_script(supeq[idx[-1]], script_pos, scr)
            return idx[:] + [2]

    if script is not None:
        # Case: Requested script already exists
        return pars.spos2argord(script_pos) * (-1 if script_op_pointed else 1)

    # Case: Requested script is compatible with current ScriptOpSubtype and
    # script is not present
    pars.set_script(script_pos, scr)
    supeq[:] = pars.scriptblock()
    return idx[:-1] + [pars.spos2argord(script_pos)]


def remove_script(index, eq: Subeq, refindex):
    """Remove pointed script from equation. Intentionally not accepting
    strict subeqs of an equation because its subeq may need to be modified.

     The script op will be downgraded or removed, depending on
     whether other scripts remain. It may modify a script-subeq of the
     script-block.

    Return an updated *refindex*, or -1 if it points to the script being
    removed.

    .. note::
        *index* MUST point to an argument of a script operator DIFFERENT than
        the base.

    .. note::
        If script op is removed, the base is placed in the same position in
        which the script op-block was except in the case detailed below:
    """
    refidx = Idx(refindex)
    idx = Idx(index)
    sb = eq.supeq(idx)  # This function assumes a script => supeq exists
    prev_pars = ScriptPars.from_scriptblock(sb)
    # -- Remove script from pars list --
    # Note: Subtracting 1 since indexing starts from 0 and real pars from 1
    pars = deepcopy(prev_pars)
    pars[pars.argord2index(idx[-1] - 1)] = None
    new_block = pars.scriptblock()

    if new_block != -1:
        # Case: Downgrade script op
        sb[:] = new_block
        return _map_refindex(idx[:-1], refidx, None, prev_pars, None, pars)

    # Case: Substitute script-block using its base as replacement
    sb[:] = pars[0]
    retval = update_scriptblock(pars[0], eq, idx[:-2], refidx)
    if idx[:-1] != refidx[:len(idx) - 1]:
        return retval

    refidx_tail = refidx[len(idx) - 1:]
    if refidx_tail and refidx_tail[0] != 1:
        return -1
    return idx[:-1] + refidx_tail[1:]
