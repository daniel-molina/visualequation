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
Functions to debug an equation.
"""

import functools

from .idx import Idx
from .ops import *
from .subeqs import Subeq

PASSED_MSG = "OK!"


def checkeqstructure(bare_eq: list):
    """Check validity of an eq according strictly to the current formalism.

    .. note::
        *bare_eq* can be a list, not necessarily a Subeq.

    .. note::
        Type and values of attributes starting with underscore is not checked.
        They are responsibility of constructors since they are not supposed to
        be modified later.

    .. note::
        Structure of indices is not checked, that is managed directly by Idx.
    """

    def helper(s, index=None):
        idx = [] if index is None else index[:]

        if not isinstance(s, list):
            return "Element in " + str(idx) \
                   + " should be a subeq but is not a list."

        if len(s) == 0:
            return "Subeq in " + str(idx) + " has no length."

        if isinstance(s[0], PseudoSymb):
            if not isinstance(s[0].pp, PublicProperties):
                return "Attribute pp of element in " + str(idx + [0]) \
                       + " is not of type PublicProperties."

        if len(s) == 1:
            if not (isinstance(s[0], str) or isinstance(s[0], PseudoSymb)):
                return "Subeq in " + str(idx) + " has length 1 and content " \
                        + " is not a str or PseudoSymb."

            if isinstance((s[0]), Op):
                return "Subeq in " + str(idx) + " has length 1 and content " \
                        + "is a Op."

        if len(s) > 1:
            if not isinstance(s[0], Op):
                return "Element in " + str(idx) + " has len " + str(len(s)) \
                       + " > 1 and first element is not an Op."

            if s[0]._n_args > 0 and s[0]._n_args != len(s) - 1:
                return "Subeq in " + str(idx) + " has a lop which expects " \
                       + str(s[0]._n_args) + " != " + str(len(s) - 1) \
                       + " parameters."

            # Juxts
            if isinstance(s[0], (PJuxt, TJuxt)) \
                    and not isinstance(s[0].current_n, int):
                return "Juxt in " + str(idx + [0]) + " has an attribute " \
                       + "current_n which is not of type int."

            if isinstance(s[0], (PJuxt, TJuxt)) and s[0].current_n < 2:
                return "Juxt in " + str(idx) + " has an attribute " \
                       + "current_n which is smaller than 2."

            if isinstance(s[0], (PJuxt, TJuxt)) \
                    and s[0].current_n != len(s) - 1:
                return "Juxt-block in " + str(idx) + " has " \
                       + str(len(s) - 1) + " juxted(s) but attribute "\
                       + "current_n of its lop is " + str(s[0].current_n) + "."

            if isinstance(s[0], (PJuxt, TJuxt)) and len(s) < 3:
                return "Subeq in " + str(idx) + " is a juxt-block which " \
                       + "has only 1 juxted."

            # Recursive check.
            for ord in range(1, len(s)):
                msg = helper(s[ord], idx + [ord])
                if PASSED_MSG != msg:
                    return msg

        return PASSED_MSG

    return helper(bare_eq)


def checkrules(eq: Subeq, index: Idx, selm: SelMode):
    """Check that an equation satisfy the conditions of current implementation
    of an equation in Visual Equation.

    *sel_idx* must point to selected subeq.

    *dir* must be the current direction.

    It checks:

        *   Building rules.
        *   Selectivity rules.
        *   Direction rules.
        *   Other assumptions of Visual Equation.

    .. note::
        This function intentionally does not check *sel_idx* nor *eq*
        structures: checkstructure function should be called before calling
        this function.
    """
    # ---- Check types of passed elements ---
    if not isinstance(eq, Subeq):
        return "Equation is not a Subeq."

    if not isinstance(index, Idx):
        return "Equation index is not an Idx."

    if not isinstance(selm, SelMode):
        return "Equation selm is not a SelMode."

    # Check that pointed element exists
    eqref = eq
    for lev, pos in enumerate(index):
        if len(eqref) == 1:
            return "Subeq in " + str(index[:lev]) \
                   + " is a symbol. It cannot be indexed."
        if pos > len(eqref) - 1:
            return "Subeq in " + str(index[:lev]) \
                   + " has no position " + str(pos) + "."

        eqref = eqref[pos]

    # Check that pointed element is not the first one (the place for a lop)
    if index and index[-1] == 0:
        return "The leading element of a Subeq is pointed."

    # ----- Check conditions on pointed subeq -----

    # PVOIDs require LCUR
    if eq.is_pvoid(index) and selm is not SelMode.LCUR:
        return "A pvoid is selected and selm is not LCUR."

    # Tjuxt-blocks require highlighting
    if eq.is_temp_jb(index) and selm in (SelMode.RCUR, SelMode.LCUR):
        return "A tjuxt-block is selected and selm is " + selm.name + "."

    # Pjuxt-blocks cannot be pointed
    if eq.is_perm_jb(index):
        return "Subequation supposed to be selected is a pjuxt-block."

    # Non-last juxteds are not compatible with RCUR
    if eq.is_nonlastjuxted(index) and selm is SelMode.RCUR:
        return "Value of selm is RCUR and selected subeq " \
               "is a non-last juxted."

    # ----- End check conditions of pointed subeq -----

    # ----- Check conditions on every subeq ----
    def helper(i=None):
        idx = Idx(i)

        if len(idx) == 0:
            sup = -2
            s = eq
        else:
            sup = eq(idx[:-1])
            s = sup[idx[-1]]

        # Tjuxt-blocks must be selected
        if s.is_temp_jb():
            if index != idx:
                return "Subeq in " + str(idx) + " is a tjuxt-block and it " \
                       + "is not selected."

        # pjuxt-blocks cannot be juxteds
        if s.is_perm_jb() and sup != -2 and sup.is_perm_jb():
            return "Pjuxt-block in " + str(idx) + " is a juxted."

        # PVOIDs cannot be juxteds
        if s.is_pvoid() and sup != -2 and sup.is_jb():
            return "PVOID in " + str(idx) + " is a juxted."

        # End part of helper which recursively checks parameters
        if len(s) > 1:
            for ord in range(1, len(s)):
                msg = helper(idx + [ord])
                if PASSED_MSG != msg:
                    return msg

        return PASSED_MSG

    return helper()


def check_edeq(edeq):
    if type(edeq.uld) != int:
        return "Attribute uld must be of type int (current type: " \
            + type(edeq.uld).__name__ + ")."

    if edeq.uld < 0:
        return "Attribute uld must be positive (current value: " \
            + repr(edeq.uld) + ")."

    msg = checkeqstructure(edeq)
    if msg != PASSED_MSG:
        return msg

    msg = checkrules(edeq, edeq.idx, edeq.selm)
    if msg != PASSED_MSG:
        return msg

    return PASSED_MSG


HEADER = '\033[95m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def debuginit(fun):
    """Decorator to debug a __init__ method."""

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        fun(self, *args, **kwargs)
        if not self.debug:
            return

        print(">>>>> Debugging started <<<<<")
        print(BLUE + "\neq: " + ENDC + BOLD + str(self) + ENDC)
        print(
            BLUE + "\nidx: " + ENDC + BOLD + str(self.idx) + ENDC
            + BLUE + "\tselm: " + ENDC + BOLD + str(self.selm.name) + ENDC
            + BLUE + "\tovrwrt: " + ENDC + BOLD + repr(self.ovrwrt) + ENDC
            + BLUE + "\tuld: " + ENDC + BOLD + repr(self.uld) + ENDC
        )

        msg = check_edeq(self)
        if msg != PASSED_MSG:
            print(FAIL + "ERROR " + ENDC + "=======> " + BOLD + msg + ENDC)
            # A __init__ must not return something that is not None
        else:
            print("\nNo errors found in initial equation. OK")

    return wrapper


def debug(fun):
    """Decorator to debug a regular method."""

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        if not self.debug:
            return fun(self, *args, **kwargs)

        # Debugging eq and idx
        msg = check_edeq(self)
        if msg != PASSED_MSG:
            print(FAIL + "ERROR " + ENDC + "=======> " + BOLD + msg + ENDC)
            return -99
        else:
            print("Tests passed before call to "
                  + BOLD + fun.__name__ + ENDC + ". Executing now...")

        retval = fun(self, *args, **kwargs)

        s_args = ""
        for arg in args:
            if isinstance(arg, list) and arg and isinstance(arg[0],
                                                            PseudoSymb):
                # Do the output more readable
                s_args += str(Subeq(arg)) + ", "
            else:
                s_args += str(arg) + ", "
        for k, v in kwargs.items():
            s_args += k + "=" + str(v) + ", "
        if s_args:
            s_args = s_args[:-2]

        print(BLUE + "\neq: " + ENDC + BOLD + str(self) + ENDC)
        print(
            BLUE + "\nidx: " + ENDC + BOLD + str(self.idx) + ENDC
            + BLUE + "\tselm: " + ENDC + BOLD + str(self.selm.name) + ENDC
            + BLUE + "\tovrwrt: " + ENDC + BOLD + repr(self.ovrwrt) + ENDC
            + BLUE + "\tuld: " + ENDC + BOLD + repr(self.uld) + ENDC + "\n"
            + WARNING + fun.__name__ + ENDC + "(" + s_args + ") -> "
            + BOLD + (retval.name if hasattr(retval, "name") else "-") + ENDC
        )

        msg = check_edeq(self)
        if msg != PASSED_MSG:
            print(FAIL + "ERROR " + ENDC + "=======> " + BOLD + msg + ENDC)
            print("Forcing quit now because of an error.")
            quit()
        else:
            print("\nTests passed after call. OK")

        return retval

    return wrapper
