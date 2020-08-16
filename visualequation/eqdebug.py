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

from . import eqqueries
from .symbols import utils


DEBUG_PASSED_MESSAGE = "OK!"


def eqstr(elem):
    if not isinstance(elem, list):
        return str(elem)
    s_str = "[" + eqstr(elem[0])
    for e in elem[1:]:
        s_str += ", " + eqstr(e)
    return s_str + "]"


def checkeqstructure(eq):
    """Check validity of an eq according strictly to the formalism of an
    equation."""

    def helper(s, aux_idx=None):
        idx = aux_idx[:] if aux_idx is not None else []

        if not isinstance(s, list):
            return "Subeq in " + str(idx) + " is not a list."

        if len(s) == 1:
            if not (isinstance(s[0], str) or isinstance(s[0], utils.Op)):
                return "Subeq in " + str(idx) \
                        + " has length 1 and content is not a str or op."

            if isinstance(s[0], utils.Op) and s[0].n_args:
                return "Subeq in " + str(idx) + " has length 1 and content " \
                    + "is Op with n_args == " + str(s[0].n_args) + " != 0."

        if len(s) > 1:
            if not isinstance(s[0], utils.Op):
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

            if s[0] in utils.NONUOPS and s[0].n_args != 1:
                return "Op in " + str(idx + [0]) + " is a non-user Op with " \
                       + str(s[0].n_args) + " args."

            if s[0] in (utils.JUXT, utils.TJUXT) and len(s) < 3:
                return "Subeq in " + str(idx) + " is a juxt-block which " \
                       + "only 1 juxted."

            # Recursive check.
            for ord in range(1, len(s)):
                msg = helper(s[ord], idx + [ord])
                if DEBUG_PASSED_MESSAGE != msg:
                    return msg

        return DEBUG_PASSED_MESSAGE

    return helper(eq)


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
    return DEBUG_PASSED_MESSAGE


def checksubeqexistence(idx, eq, onlysubeqs=True):
    """Check that pointed subequation exists.

    If *onlysubeqs* is True, an index pointing to a lop is an error.
    That is the last condition checked: if that is reported, the rest is OK.
    """
    if not idx:
        return DEBUG_PASSED_MESSAGE

    eqref = eq
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

    return DEBUG_PASSED_MESSAGE


def checkstructure(idx, eq):
    """Check of integrity of a pair index-equation.

    """

    msg = checkidxstructure(idx)
    if msg != DEBUG_PASSED_MESSAGE:
        return "Wrong index format: " + msg

    msg = checkeqstructure(eq)
    if msg != DEBUG_PASSED_MESSAGE:
        return "Wrong eq format: " + msg

    msg = checksubeqexistence(idx, eq, onlysubeqs=True)
    if msg != DEBUG_PASSED_MESSAGE:
        return "Wrong pointed subeq: " + msg

    return DEBUG_PASSED_MESSAGE


def checkeqrules(eq, sel_idx=None, dir=None):
    """Check that an equation satisfy the conditions of current implementation
    of an equation in Visual Equation.

    If *sel_idx* is not None, it is checked that a valid subeq is selected.

    If *dir* is not None, it is checked that a valid direction is being used.

    It checks:

        *   Building rules.
        *   Selectivity rules.
        *   Direction rules.
        *   Other assumptions of Visual Equation.

    .. note::
        This function intentionally does not check *sel_idx* nor *eq*
        structures. checkstructure function should be called before calling
        this function.
    """
    if utils.NONUOPS != (utils.GOP,):
        return "Current implementation considers GOP, and only GOP, as " \
               "non-user op."

    if dir is not None:
        s_sel = eqqueries.get(sel_idx, eq)
        if s_sel == utils.void(temp=True) and dir != utils.ODIR:
            return "A TVOID is selected and direction is not ODIR."
        if s_sel == utils.void() and dir not in (utils.ODIR, utils.VDIR):
            return "A VOID is selected and direction is not ODIR nor VDIR."
        if s_sel != utils.void() and dir == utils.VDIR:
            return "A non-VOID is selected and direction is VDIR."

    # Selectivity
    sel_flag = eqqueries.selectivity(sel_idx, eq)
    if sel_flag == 0:
        return "Selected subequation is not allowed to be selected. " \
               "In particular, it is a GOP-block strict subeq which is not " \
               "its urepr."
    if sel_flag == -1:
        return "Selected subequation is not allowed to be selected. " \
               "In particular, it is not an usubeq."

    # It is interesting to count TVOIDs and TJUXT-blocks in case that no
    # sel_idx is passed.
    # (If sel_idx is passed an error would be reported even without counting
    # them)
    n_tjuxts = 0
    n_tvoids = 0

    def helper(idx_aux=None):
        idx = [] if idx_aux is None else idx_aux[:]

        if len(idx) == 0:
            supsup = -2
            sup = -2
            s = eq
        elif len(idx) == 1:
            supsup = -2
            sup = eq
            s = sup[idx[-1]]
        else:
            supsup = eqqueries.get(idx[:-2], eq)
            sup = supsup[idx[-2]]
            s = sup[idx[-1]]

        # Rules of faithful operators
        if len(s) > 1 and s[0] in utils.NONUOPS and s[0].n_args != 1:
            return "Lop in " + str(idx + [0]) \
                   + "is a non-user op and accepts "\
                   + str(s[0].n_args) + " != 1 parameters."

        # GOP-nesting
        if supsup != -2 and supsup[0] == utils.GOP and sup[0] == utils.GOP:
            return "Subeq in " + str(idx) + " is a GOP-par which lop-block " \
                   + "is itself a GOP-par."

        # TJUXTs
        nonlocal n_tjuxts
        if len(s) > 1 and s[0] == utils.TJUXT:
            n_tjuxts += 1
            if n_tjuxts > 1:
                return "There is more than 1 TJUXT."
            if sel_idx is not None and sel_idx != idx:
                return "There exists a TJUXT-block which is not selected."

        # TVOIDs
        nonlocal n_tvoids
        if s == utils.void(temp=True):
            n_tvoids += 1
            if n_tvoids > 1:
                return "There is more than 1 TVOID."
            if sup == -2 or sup[0] != utils.JUXT or idx[-1] != len(sup) - 1:
                return "TVOID in " + str(idx) + " is not a last juxted " \
                       + "of a JUXT-block."
            if sel_idx is not None and sel_idx != idx:
                return "There exists a TVOID which is not selected."

        # VOIDs
        if s == utils.void() and sup != -2 \
                and sup[0] in (utils.TJUXT, utils.JUXT):
            return "VOID in " + str(idx) + " is a juxted."

        # End part of helper which recursively checks parameters
        if len(s) > 1:
            for ord in range(1, len(s)):
                msg = helper(idx + [ord])
                if DEBUG_PASSED_MESSAGE != msg:
                    return msg

        return DEBUG_PASSED_MESSAGE

    return helper(None)


def checkall(eq, sel_idx, dir):
    msg = checkstructure(sel_idx, eq)
    if msg != DEBUG_PASSED_MESSAGE:
        return msg

    msg = checkeqrules(eq, sel_idx, dir)
    if msg != DEBUG_PASSED_MESSAGE:
        return "Wrong implementation: " + msg

    return DEBUG_PASSED_MESSAGE


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
        print("**** START DEBUGGING (Initial object) ****")

        fun(self, *args, **kwargs)
        print(OKBLUE + "\neq: "  + ENDC + BOLD + eqstr(self.eq)  + ENDC)
        print(OKBLUE + "\nidx: " + ENDC + BOLD + str(self.idx) + ENDC
              + OKBLUE + "\tdir: " + ENDC
              + BOLD + utils.DIR2NAME[self.dir] + ENDC)

        msg = checkall(self.eq, self.idx, self.dir)
        if msg != DEBUG_PASSED_MESSAGE:
            print(FAIL + "ERROR." + ENDC + "=======> " + BOLD + msg + ENDC)
            return -99
        else:
            print("\nOK. Tests passed.")
        #print("**** END DEBUGGING ****")

    return wrapper


PATTERN_START = re.compile(r"^.*\.")
PATTERN_END = re.compile(r"\sat.*$")


def debug(fun):
    """Decorator to debug a regular method."""

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        #print("**** START DEBUGGING ****")
        fun_str = str(fun)
        fun_str = PATTERN_START.sub("", fun_str)
        fun_str = PATTERN_END.sub("", fun_str)
        # Debugging eq and idx
        msg = checkall(self.eq, self.idx, self.dir)
        if msg != DEBUG_PASSED_MESSAGE:
            print("======>", msg)
            return -99
        else:
            print("OK. Tests passed before call to "
                  + BOLD + fun_str + ENDC + ". Executing now...")

        retval = fun(self, *args, **kwargs)
        print(OKBLUE + "\neq: "  + ENDC + BOLD + eqstr(self.eq)  + ENDC)
        print(OKBLUE + "\nidx: " + ENDC + BOLD + str(self.idx) + ENDC
              + OKBLUE + "\tdir: " + ENDC
              + BOLD + utils.DIR2NAME[self.dir] + ENDC
              + ".\tReturn of " + BOLD + fun_str + ENDC + ": "
              + WARNING + str(retval) + ENDC)

        msg = checkall(self.eq, self.idx, self.dir)
        if msg != DEBUG_PASSED_MESSAGE:
            print(FAIL + "ERROR. " + ENDC + "------> " + BOLD + msg + ENDC)
            return -99
        else:
            print("\nOK. Tests passed after call.")

        #print("**** END DEBUGGING ****")
        return retval

    return wrapper
