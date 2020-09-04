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
import re

from .dirsel import Dir
from .idx import Idx
from .ops import *
from.subeqs import Subeq


PASSED_MSG = "OK!"


def checkeqstructure(bare_eq):
    """Check validity of an eq according strictly to the formalism of an
    equation."""

    def helper(s, index=None):
        idx = [] if index is None else index[:]

        if not isinstance(s, list):
            return "Subeq in " + str(idx) + " is not a list."

        if len(s) == 0:
            return "Subeq in " + str(idx) + " has no length."

        if len(s) == 1:
            if not (isinstance(s[0], str) or isinstance(s[0], Op)):
                return "Subeq in " + str(idx) \
                        + " has length 1 and content is not a str or Op."

            if isinstance(s[0], Op) and s[0].n_args:
                return "Subeq in " + str(idx) + " has length 1 and content " \
                    + "is a Op with n_args == " + str(s[0].n_args) + " != 0."

        if len(s) > 1:
            if not isinstance(s[0], Op):
                return "Subeq in " + str(idx) + " has len " + str(len(s)) \
                       + " > 1 and first element is not an Op."

            if s[0].n_args == 0 or s[0].n_args < -1:
                return "Op in " + str(idx + [0]) + " is a lop with n_args " \
                       + "== " + str(s[0].n_args) + " instead of -1 or " \
                       + "some N > 0."

            if s[0].n_args > 0 and s[0].n_args != len(s) - 1:
                return "Subeq in " + str(idx) + " has a lop which expects " \
                       + str(s[0].n_args) + " != " + str(len(s) - 1) \
                       + " parameters."

            # Non-applicable since GOP is the only non-user op.
            # if s[0] in NONUOPS and s[0].n_args != 1:
            #     return "Op in " + str(idx + [0]) + " is a non-user Op with " \
            #            + str(s[0].n_args) + " args."

            if s[0] in (PJUXT, TJUXT) and len(s) < 3:
                return "Subeq in " + str(idx) + " is a juxt-block which " \
                       + "only 1 juxted."

            # Recursive check.
            for ord in range(1, len(s)):
                msg = helper(s[ord], idx + [ord])
                if PASSED_MSG != msg:
                    return msg

        return PASSED_MSG

    return helper(bare_eq)


def checkidxstructure(idx):
    if not isinstance(idx, list):
        return "Index must be a list."
    if not all(isinstance(ele, int) for ele in idx):
        return "Not every element is an integer."
    if not all(ele >= 0 for ele in idx):
        return "Not every element is non-negative."
    try:
        first0pos = idx.index(0)
        if first0pos != len(idx) - 1:
            return "Non-last element is 0."
    except ValueError:
        pass
    return PASSED_MSG


def checksubeqexistence(idx, bare_eq, onlysubeqs=True):
    """Check that pointed subequation exists.

    If *onlysubeqs* is True, an index pointing to a lop is an error.

    .. note::
        Pointing to a lop is the last condition checked: if that is reported,
        the rest is OK.
    """
    if not idx:
        return PASSED_MSG

    eqref = bare_eq
    for lev, pos in enumerate(idx):
        if len(eqref) == 1:
            return "Subeq in " + str(idx[:lev]) \
                   + " is a symbol/0-args Op. It cannot be indexed."
        if pos > len(eqref) - 1:
            return "Subeq in " + str(idx[:lev]) \
                   + " has no position " + str(pos) + "."

        eqref = eqref[pos]

    # This must be the last condition
    if onlysubeqs and idx and not idx[-1]:
        return "Pointed element is a lop."

    return PASSED_MSG


def checkstructure(idx, bare_eq):
    """Check of integrity of a pair index-equation."""

    msg = checkidxstructure(idx)
    if msg != PASSED_MSG:
        return "Wrong index format: " + msg

    msg = checkeqstructure(bare_eq)
    if msg != PASSED_MSG:
        return "Wrong eq format: " + msg

    msg = checksubeqexistence(idx, bare_eq, onlysubeqs=True)
    if msg != PASSED_MSG:
        return "Wrong pointed subeq: " + msg

    return PASSED_MSG


def checkeqrules(eq: Subeq, sel_idx: Idx, dir: Dir):
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

    # Non-applicable
    # if NONUOPS != (utils.GOP,):
    #     return "Current implementation considers GOP, and only GOP, as " \
    #            "non-user op."

    s_sel = eq(sel_idx)
    if s_sel.is_tvoid() and dir is not Dir.O:
        return "A TVOID is selected and direction is not O."
    if s_sel.is_pvoid() and dir not in (Dir.O, Dir.V):
        return "A PVOID is selected and direction is not O nor V."
    if not s_sel.is_pvoid() and dir is Dir.V:
        return "A non-PVOID subeq is selected and direction is V."

    # Selectivity
    flag = eq.selectivity(sel_idx)
    if flag == 0:
        return "Selected subequation is not allowed to be selected. " \
               "In particular, it is a GOP-block which urepr is selectable."
    if flag == -1:
        return "Selected subequation is not allowed to be selected. " \
               "In particular, it is a GOP-block and GOP-par strict subeq."
    if flag == -2:
        return "Selected subequation is not allowed to be selected. " \
               "In particular, it is a usubeq and GOP-par strict subeq."

    def helper(index=None):
        idx = Idx(index)

        if len(idx) == 0:
            supsup = -2
            sup = -2
            s = eq
        elif len(idx) == 1:
            supsup = -2
            sup = eq
            s = sup[idx[-1]]
        else:
            supsup = eq(idx[:-2])
            sup = supsup[idx[-2]]
            s = sup[idx[-1]]

        # Non-applicable
        # Rules of faithful operators
        # if len(s) > 1 and not s.is_usubeq() and s[0].n_args != 1:
        #     return "Lop in " + str(idx + [0]) \
        #            + "is a non-user op and accepts "\
        #            + str(s[0].n_args) + " != 1 parameters."

        # GOP-nesting
        if supsup != -2 and supsup[0] == GOP and sup[0] == GOP:
            return "Subeq in " + str(idx) + " is a GOP-par which lop-block " \
                   + "is itself a GOP-par."

        # GOP-params
        if not s.isb() and sup != -2 and sup[0] == GOP:
            return "Subeq in " + str(idx) + " is a GOP-par and is a symbol."

        # TJUXTs
        if len(s) > 1 and s[0] == TJUXT:
            if sel_idx != idx:
                return "There exists a TJUXT-block which is not selected."

        # TVOIDs
        if s.is_tvoid():
            if sup == -2 or sup[0] != PJUXT or idx[-1] != len(sup) - 1:
                return "TVOID in " + str(idx) + " is not a last juxted " \
                       + "of a JUXT-block."
            if sel_idx != idx:
                return "There exists a TVOID which is not selected."

        # PVOIDs
        if s.is_pvoid() and sup != -2 and sup.is_jb():
            return "PVOID in " + str(idx) + " is a juxted."

        # End part of helper which recursively checks parameters
        if len(s) > 1:
            for ord in range(1, len(s)):
                msg = helper(idx + [ord])
                if PASSED_MSG != msg:
                    return msg

        return PASSED_MSG

    return helper(None)


def checkall(eq, sel_idx, dir):
    msg = checkstructure(sel_idx, eq)
    if msg != PASSED_MSG:
        return msg

    msg = checkeqrules(eq, sel_idx, dir)
    if msg != PASSED_MSG:
        return "Wrong implementation: " + msg

    return PASSED_MSG


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def debuginit(fun):
    """Decorator to debug a __init__ method."""

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        fun(self, *args, **kwargs)
        if not self.debug:
            return

        print(">>>>> Debugging started <<<<<")
        print(OKBLUE + "\neq: "  + ENDC + BOLD + str(self) + ENDC)
        print(OKBLUE + "\nidx: " + ENDC + BOLD + str(self.idx) + ENDC
              + OKBLUE + "\tdir: " + ENDC
              + BOLD + self.dir.name + ENDC)

        msg = checkall(self, self.idx, self.dir)
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
        msg = checkall(self.eq, self.idx, self.dir)
        if msg != PASSED_MSG:
            print("======>", msg)
            return -99
        else:
            print("Tests passed before call to "
                  + BOLD + fun.__name__ + ENDC + ". Executing now...")

        retval = fun(self, *args, **kwargs)
        print(OKBLUE + "\neq: "  + ENDC + BOLD + str(self) + ENDC)
        print(OKBLUE + "\nidx: " + ENDC + BOLD + str(self.idx) + ENDC
              + OKBLUE + "\tdir: " + ENDC
              + BOLD + self.dir.name + ENDC
              + ".\tReturn of " + BOLD + fun.__name__ + ENDC + ": "
              + WARNING + str(retval) + ENDC)

        msg = checkall(self, self.idx, self.dir)
        if msg != PASSED_MSG:
            print(FAIL + "ERROR " + ENDC + "------> " + BOLD + msg + ENDC)
            return -99
        else:
            print("\nTests passed after call. OK")

        return retval

    return wrapper
