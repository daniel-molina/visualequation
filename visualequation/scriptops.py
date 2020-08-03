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

import copy

from . import eqqueries
from .symbols import utils
from .symbols.utils import Op, VOID
from .errors import ShowError

# Vertical script operators
UNDER = Op(2, r'\underset{{{1}}}{{{0}}}', 'setscript')
OVER = Op(2, r'\overset{{{1}}}{{{0}}}', 'setscript')
UNDEROVER = Op(2, r'\overset{{{2}}}{{{\underset{{{1}}}{{{0}}}}}}', 'setscript')

# Standard script operators
LSUB = Op(2, r'\tensor*[_{{{1}}}]{{{0}}}{{}}', 'script')
SUB = Op(2, r'\tensor*{{{0}}}{{_{{{1}}}}}', 'script')
LSUP = Op(2, r'\tensor*[^{{{1}}}]{{{0}}}{{}}', 'script')
SUP = Op(2, r'\tensor*{{{0}}}{{^{{{1}}}}}', 'script')
LSUBSUB = Op(3, r'\tensor*[_{{{1}}}]{{{0}}}{{_{{{2}}}}}', 'script')
LSUBLSUP = Op(3, r'\tensor*[_{{{1}}}^{{{2}}}]{{{0}}}{{}}', 'script')
LSUBSUP = Op(3, r'\tensor*[_{{{1}}}]{{{0}}}{{^{{{2}}}}}', 'script')
SUBLSUP = Op(3, r'\tensor*[^{{{2}}}]{{{0}}}{{_{{{1}}}}}', 'script')
SUBSUP = Op(3, r'\tensor*{{{0}}}{{^{{{2}}}_{{{1}}}}}', 'script')
LSUPSUP = Op(3, r'\tensor*[^{{{1}}}]{{{0}}}{{^{{{2}}}}}', 'script')
LSUBSUBLSUP = Op(4, r'\tensor*[_{{{1}}}^{{{3}}}]{{{0}}}{{_{{{2}}}}}', 'script')
LSUBSUBSUP = Op(4, r'\tensor*[_{{{1}}}]{{{0}}}{{^{{{3}}}_{{{2}}}}}', 'script')
LSUBLSUPSUP = Op(4, r'\tensor*[^{{{2}}}_{{{1}}}]{{{0}}}{{^{{{3}}}}}',
                 'script')
SUBLSUPSUP = Op(4, r'\tensor*[^{{{2}}}]{{{0}}}{{^{{{3}}}_{{{1}}}}}', 'script')
LSUBSUBLSUPSUP = Op(5,
                    r'\tensor*[_{{{1}}}^{{{3}}}]{{{0}}}{{_{{{2}}}^{{{4}}}}}',
                    'script')

# Script for Large Operators. Valid only for variable-size, fun-args or
# anything defined with \mathop.
# It is necessary not to include brackets in the base when no \sideset is used
LOUNDER = Op(2, r'{0}_{{{1}}}', 'loscript')
LOOVER = Op(2, r'{0}^{{{1}}}', 'loscript')
LOUNDEROVER = Op(2, r'{0}_{{{1}}}^{{{2}}}', 'loscript')

LOLSUB = Op(2, r'\sideset{{_{{{1}}}}}{{}}{{{0}}}', 'loscript')
LOSUB = Op(2, r'\sideset{{}}{{_{{{1}}}}}{{{0}}}', 'loscript')
LOLSUP = Op(2, r'\sideset{{^{{{1}}}}}{{}}{{{0}}}', 'loscript')
LOSUP = Op(2, r'\sideset{{}}{{^{{{1}}}}}{{{0}}}', 'loscript')
LOLSUBSUB = Op(3, r'\sideset{{_{{{1}}}}}{{_{{{2}}}}}{{{0}}}', 'loscript')
LOLSUBLSUP = Op(3, r'\sideset{{_{{{1}}}^{{{2}}}}}{{}}{{{0}}}', 'loscript')
LOLSUBSUP = Op(3, r'\sideset{{_{{{1}}}}}{{^{{{2}}}}}{{{0}}}', 'loscript')
LOSUBLSUP = Op(3, r'\sideset{{^{{{2}}}}}{{_{{{1}}}}}{{{0}}}', 'loscript')
LOSUBSUP = Op(3, r'\sideset{{}}{{_{{{1}}}^{{{2}}}}}{{{0}}}', 'loscript')
LOLSUPSUP = Op(3, r'\sideset{{^{{{1}}}}}{{^{{{2}}}}}{{{0}}}', 'loscript')
LOLSUBSUBLSUP = Op(4, r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}}}{{{0}}}',
                   'loscript')
LOLSUBSUBSUP = Op(4, r'\sideset{{_{{{1}}}}}{{^{{{3}}}_{{{2}}}}}{{{0}}}',
                  'loscript')
LOLSUBLSUPSUP = Op(4, r'\sideset{{^{{{2}}}_{{{1}}}}}{{^{{{3}}}}}{{{0}}}',
                   'loscript')
LOSUBLSUPSUP = Op(4, r'\sideset{{^{{{2}}}}}{{^{{{3}}}_{{{1}}}}}{{{0}}}',
                  'loscript')
LOLSUBSUBLSUPSUP \
    = Op(5, r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}^{{{4}}}}}{{{0}}}',
         'loscript')
# +Under
LOLSUBUNDER = Op(3, r'\sideset{{_{{{1}}}}}{{}}{{{0}}}_{{{2}}}', 'loscript')
LOUNDERSUB = Op(3, r'\sideset{{}}{{_{{{2}}}}}{{{0}}}_{{{1}}}', 'loscript')
LOUNDERLSUP = Op(3, r'\sideset{{^{{{2}}}}}{{}}{{{0}}}_{{{1}}}', 'loscript')
LOUNDERSUP = Op(3, r'\sideset{{}}{{^{{{2}}}}}{{{0}}}_{{{1}}}', 'loscript')
LOLSUBUNDERSUB = Op(4, r'\sideset{{_{{{1}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}',
                    'loscript')
LOLSUBUNDERLSUP = Op(4, r'\sideset{{_{{{1}}}^{{{3}}}}}{{}}{{{0}}}_{{{2}}}',
                     'loscript')
LOLSUBUNDERSUP = Op(4, r'\sideset{{_{{{1}}}}}{{^{{{3}}}}}{{{0}}}_{{{2}}}',
                    'loscript')
LOUNDERSUBLSUP = Op(4, r'\sideset{{^{{{3}}}}}{{_{{{2}}}}}{{{0}}}_{{{1}}}',
                    'loscript')
LOUNDERSUBSUP = Op(4, r'\sideset{{}}{{_{{{2}}}^{{{3}}}}}{{{0}}}_{{{1}}}',
                   'loscript')
LOUNDERLSUPSUP = Op(4, r'\sideset{{^{{{2}}}}}{{^{{{3}}}}}{{{0}}}_{{{1}}}',
                    'loscript')
LOLSUBUNDERSUBLSUP \
    = Op(5, r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}',
         'loscript')
LOLSUBUNDERSUBSUP \
    = Op(5, r'\sideset{{_{{{1}}}}}{{^{{{4}}}_{{{3}}}}}{{{0}}}_{{{2}}}',
         'loscript')
LOLSUBUNDERLSUPSUP \
    = Op(5, r'\sideset{{^{{{3}}}_{{{1}}}}}{{^{{{4}}}}}{{{0}}}_{{{2}}}',
         'loscript')
LOUNDERSUBLSUPSUP \
    = Op(5, r'\sideset{{^{{{3}}}}}{{^{{{4}}}_{{{2}}}}}{{{0}}}_{{{1}}}',
         'loscript')
LOLSUBUNDERSUBLSUPSUP \
    = Op(6, r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}^{{{5}}}}}{{{0}}}_{{{2}}}',
         'loscript')
# +Over
LOLSUBOVER = Op(3, r'\sideset{{_{{{1}}}}}{{}}{{{0}}}^{{{2}}}', 'loscript')
LOSUBOVER = Op(3, r'\sideset{{}}{{_{{{1}}}}}{{{0}}}^{{{2}}}', 'loscript')
LOLSUPOVER = Op(3, r'\sideset{{^{{{1}}}}}{{}}{{{0}}}^{{{2}}}', 'loscript')
LOOVERSUP = Op(3, r'\sideset{{}}{{^{{{2}}}}}{{{0}}}^{{{1}}}', 'loscript')
LOLSUBSUBOVER = Op(4, r'\sideset{{_{{{1}}}}}{{_{{{2}}}}}{{{0}}}^{{{3}}}',
                   'loscript')
LOLSUBLSUPOVER = Op(4, r'\sideset{{_{{{1}}}^{{{2}}}}}{{}}{{{0}}}^{{{3}}}',
                    'loscript')
LOLSUBOVERSUP = Op(4, r'\sideset{{_{{{1}}}}}{{^{{{3}}}}}{{{0}}}^{{{2}}}',
                   'loscript')
LOSUBLSUPOVER = Op(4, r'\sideset{{^{{{2}}}}}{{_{{{1}}}}}{{{0}}}^{{{3}}}',
                   'loscript')
LOSUBOVERSUP = Op(4, r'\sideset{{}}{{_{{{1}}}^{{{3}}}}}{{{0}}}^{{{2}}}',
                  'loscript')
LOLSUPOVERSUP = Op(4, r'\sideset{{^{{{1}}}}}{{^{{{3}}}}}{{{0}}}^{{{2}}}',
                   'loscript')
LOLSUBSUBLSUPOVER \
    = Op(5, r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}}}{{{0}}}^{{{4}}}',
         'loscript')
LOLSUBSUBOVERSUP \
    = Op(5, r'\sideset{{_{{{1}}}}}{{^{{{4}}}_{{{2}}}}}{{{0}}}^{{{3}}}',
         'loscript')
LOLSUBLSUPOVERSUP \
    = Op(5, r'\sideset{{^{{{2}}}_{{{1}}}}}{{^{{{4}}}}}{{{0}}}^{{{3}}}',
         'loscript')
LOSUBLSUPOVERSUP \
    = Op(5, r'\sideset{{^{{{2}}}}}{{^{{{4}}}_{{{1}}}}}{{{0}}}^{{{3}}}',
         'loscript')
LOLSUBSUBLSUPOVERSUP \
    = Op(6, r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}^{{{5}}}}}{{{0}}}^{{{4}}}',
         'loscript')
# +UnderOver
LOLSUBUNDEROVER = Op(4, r'\sideset{{_{{{1}}}}}{{}}{{{0}}}_{{{2}}}^{{{3}}}',
                     'loscript')
LOUNDERSUBOVER = Op(4, r'\sideset{{}}{{_{{{2}}}}}{{{0}}}_{{{1}}}^{{{3}}}',
                    'loscript')
LOUNDERLSUPOVER = Op(4, r'\sideset{{^{{{2}}}}}{{}}{{{0}}}_{{{1}}}^{{{3}}}',
                     'loscript')
LOUNDEROVERSUP = Op(4, r'\sideset{{}}{{^{{{3}}}}}{{{0}}}_{{{1}}}^{{{2}}}',
                    'loscript')
LOLSUBUNDERSUBOVER \
    = Op(5, r'\sideset{{_{{{1}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}^{{{4}}}',
         'loscript')
LOLSUBUNDERLSUPOVER \
    = Op(5, r'\sideset{{_{{{1}}}^{{{3}}}}}{{}}{{{0}}}_{{{2}}}^{{{4}}}',
         'loscript')
LOLSUBUNDEROVERSUP \
    = Op(5, r'\sideset{{_{{{1}}}}}{{^{{{4}}}}}{{{0}}}_{{{2}}}^{{{3}}}',
         'loscript')
LOUNDERSUBLSUPOVER \
    = Op(5, r'\sideset{{^{{{3}}}}}{{_{{{2}}}}}{{{0}}}_{{{1}}}^{{{4}}}',
         'loscript')
LOUNDERSUBOVERSUP \
    = Op(5, r'\sideset{{}}{{_{{{2}}}^{{{4}}}}}{{{0}}}_{{{1}}}^{{{3}}}',
         'loscript')
LOUNDERLSUPOVERSUP \
    = Op(5, r'\sideset{{^{{{2}}}}}{{^{{{4}}}}}{{{0}}}_{{{1}}}^{{{3}}}',
         'loscript')
LOLSUBUNDERSUBLSUPOVER \
    = Op(6, r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}^{{{5}}}',
         'loscript')
LOLSUBUNDERSUBOVERSUP \
    = Op(6, r'\sideset{{_{{{1}}}}}{{^{{{5}}}_{{{3}}}}}{{{0}}}_{{{2}}}^{{{4}}}',
         'loscript')
LOLSUBUNDERLSUPOVERSUP \
    = Op(6, r'\sideset{{^{{{3}}}_{{{1}}}}}{{^{{{5}}}}}{{{0}}}_{{{2}}}^{{{4}}}',
         'loscript')
LOUNDERSUBLSUPOVERSUP \
    = Op(6, r'\sideset{{^{{{3}}}}}{{^{{{5}}}_{{{2}}}}}{{{0}}}_{{{1}}}^{{{4}}}',
         'loscript')
LOLSUBUNDERSUBLSUPOVERSUP \
    = Op(7, r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}^{{{6}}}}}{{{0}}}'
            r'_{{{2}}}^{{{5}}}', 'loscript')

SCRIPT_OP_TYPES = ('setscript', 'script', 'loscript')

LOSCRIPT_BASE_TYPES = ('vs', 'fun_args', 'opconstruct')

SETSCRIPT_OP2ID_DICT = {
    None: (False, False),
    UNDER: (True, False),
    OVER: (False, True),
    UNDEROVER: (True, True)
}

ID2SETSCRIPT_OP_DICT = {v: k for k, v in SETSCRIPT_OP2ID_DICT.items()}

SCRIPT_OP2ID_DICT = {
    None: (False, False, False, False),
    LSUB: (True, False, False, False),
    SUB: (False, True, False, False),
    LSUP: (False, False, True, False),
    SUP: (False, False, False, True),
    LSUBSUB: (True, True, False, False),
    LSUBLSUP: (True, False, True, False),
    LSUBSUP: (True, False, False, True),
    SUBLSUP: (False, True, True, False),
    SUBSUP: (False, True, False, True),
    LSUPSUP: (False, False, True, True),
    LSUBSUBLSUP: (True, True, True, False),
    LSUBSUBSUP: (True, True, False, True),
    LSUBLSUPSUP: (True, False, True, True),
    SUBLSUPSUP: (False, True, True, True),
    LSUBSUBLSUPSUP: (True, True, True, True)
}

ID2SCRIPT_OP_DICT = {v: k for k, v in SCRIPT_OP2ID_DICT.items()}

LOSCRIPT_OP2ID_DICT = {
    None: (False, False, False, False, False, False),
    LOUNDER: (False, True, False, False, False, False),
    LOOVER: (False, False, False, False, True, False),
    LOUNDEROVER: (False, True, False, False, True, False),
    LOLSUB: (True, False, False, False, False, False),
    LOSUB: (False, False, True, False, False, False),
    LOLSUP: (False, False, False, True, False, False),
    LOSUP: (False, False, False, False, False, True),
    LOLSUBSUB: (True, False, True, False, False, False),
    LOLSUBLSUP: (True, False, False, True, False, False),
    LOLSUBSUP: (True, False, False, False, False, True),
    LOSUBLSUP: (False, False, True, True, False, False),
    LOSUBSUP: (False, False, True, False, False, True),
    LOLSUPSUP: (False, False, False, True, False, True),
    LOLSUBSUBLSUP: (True, False, True, True, False, False),
    LOLSUBSUBSUP: (True, False, True, False, False, True),
    LOLSUBLSUPSUP: (True, False, False, True, False, True),
    LOSUBLSUPSUP: (False, False, True, True, False, True),
    LOLSUBSUBLSUPSUP: (True, False, True, True, False, True),
    # +Under
    LOLSUBUNDER: (True, True, False, False, False, False),
    LOUNDERSUB: (False, True, True, False, False, False),
    LOUNDERLSUP: (False, True, False, True, False, False),
    LOUNDERSUP: (False, True, False, False, False, True),
    LOLSUBUNDERSUB: (True, True, True, False, False, False),
    LOLSUBUNDERLSUP: (True, True, False, True, False, False),
    LOLSUBUNDERSUP: (True, True, False, False, False, True),
    LOUNDERSUBLSUP: (False, True, True, True, False, False),
    LOUNDERSUBSUP: (False, True, True, False, False, True),
    LOUNDERLSUPSUP: (False, True, False, True, False, True),
    LOLSUBUNDERSUBLSUP: (True, True, True, True, False, False),
    LOLSUBUNDERSUBSUP: (True, True, True, False, False, True),
    LOLSUBUNDERLSUPSUP: (True, True, False, True, False, True),
    LOUNDERSUBLSUPSUP: (False, True, True, True, False, True),
    LOLSUBUNDERSUBLSUPSUP: (True, True, True, True, False, True),
    # +Over
    LOLSUBOVER: (True, False, False, False, True, False),
    LOSUBOVER: (False, False, True, False, True, False),
    LOLSUPOVER: (False, False, False, True, False, True),
    LOOVERSUP: (False, False, False, False, True, True),
    LOLSUBSUBOVER: (True, False, True, False, True, False),
    LOLSUBLSUPOVER: (True, False, False, True, True, False),
    LOLSUBOVERSUP: (True, False, False, False, True, True),
    LOSUBLSUPOVER: (False, False, True, True, True, False),
    LOSUBOVERSUP: (False, False, True, False, True, True),
    LOLSUPOVERSUP: (False, False, False, True, True, True),
    LOLSUBSUBLSUPOVER: (True, False, True, True, True, False),
    LOLSUBSUBOVERSUP: (True, False, True, False, True, True),
    LOLSUBLSUPOVERSUP: (True, False, False, True, True, True),
    LOSUBLSUPOVERSUP: (False, False, True, True, True, True),
    LOLSUBSUBLSUPOVERSUP: (True, False, True, True, True, True),
    # +UnderOver
    LOLSUBUNDEROVER: (True, True, False, False, True, False),
    LOUNDERSUBOVER: (False, True, True, False, True, False),
    LOUNDERLSUPOVER: (False, True, False, True, True, False),
    LOUNDEROVERSUP: (False, True, False, False, True, True),
    LOLSUBUNDERSUBOVER: (True, True, True, False, True, False),
    LOLSUBUNDERLSUPOVER: (True, True, False, True, True, False),
    LOLSUBUNDEROVERSUP: (True, True, False, False, True, True),
    LOUNDERSUBLSUPOVER: (False, True, True, True, True, False),
    LOUNDERSUBOVERSUP: (False, True, True, False, True, True),
    LOUNDERLSUPOVERSUP: (False, True, False, True, True, True),
    LOLSUBUNDERSUBLSUPOVER: (True, True, True, True, True, False),
    LOLSUBUNDERSUBOVERSUP: (True, True, True, False, True, True),
    LOLSUBUNDERLSUPOVERSUP: (True, True, False, True, True, True),
    LOUNDERSUBLSUPOVERSUP: (False, True, True, True, True, True),
    LOLSUBUNDERSUBLSUPOVERSUP: (True, True, True, True, True, True)
}

ID2LOSCRIPT_OP_DICT = {v: k for k, v in LOSCRIPT_OP2ID_DICT.items()}


def init_script_pars(base, type_):
    "Return an pars list with certain base and no scripts."
    basepar = [copy.deepcopy(base)]
    if type_ == "setscript":
        return basepar + [None]*2
    if type_ == "script":
        return basepar + [None]*4
    return basepar + [None]*6


def get_script_pos_in_pars(pars, scriptdir, is_superscript):
    """Return script position in a pars list. If script parameters are not
    compatible with pars, return -1.

    .. note::
        Only compatibility of referred script in provided *pars* is checked.
        In particular, it is NOT checked whether the base (pars[0]) is valid
        for the op associated to *pars*.

    Combinations which do not return -1:

        *   len(args) == 3 and dir == 0
        *   len(args) == 5 and dir in (-1, 1)
        *   len(args) == 7 and dir in (-1, 0, 1)

    :param pars: A pars list of a script operator.
    :param scriptdir: 0 for under/over, -1 for lsub/lsup and 1 for sub/sup.
    :param is_superscript: True for over, lsup and sup. Ow, False.
    :return: script position in pars (from 1 to len(pars)-1 since base is not a
    script) or -1.
    """
    if len(pars) == 3:
        if scriptdir != 0:
            return -1
        return 2 if is_superscript else 1
    elif len(pars) == 5:
        if scriptdir not in (-1, 1):
            return -1
        if scriptdir == -1:
            return 3 if is_superscript else 1
        else:
            return 4 if is_superscript else 2
    else:
        if scriptdir == -1:
            return 4 if is_superscript else 1
        elif scriptdir == 0:
            return 5 if is_superscript else 2
        elif scriptdir == 1:
            return 6 if is_superscript else 3
        else:
            return -1


def set_script_in_pars(pars, scriptdir, is_superscript, pspar):
    pars[get_script_pos_in_pars(pars, scriptdir, is_superscript)] = pspar


def get_script_in_pars(pars, scriptdir, is_superscript):
    """Get current script in pars according to parameters.

    If script is not compatible with passed pars, -1 is returned.
    """
    pos = get_script_pos_in_pars(pars, scriptdir, is_superscript)
    return pars[pos] if pos > 0 else -1


def scriptop_pars2loscript_pars(pars):
    """Transform, if needed, pars to match the best loscript op.

    .. note::
        This function only changes script positions being used, it does NOT
        check whether the base is valid for certain type_. It does not care
        about valid bases.
    """
    if len(pars) == 3:
        return [pars[0], None, pars[1], None, None, pars[2], None]
    elif len(pars) == 5:
        return [pars[0], pars[1], None, pars[2], pars[3], None, pars[4]]
    else:
        return pars


def scriptop_pars2script_pars(pars):
    """Transform, if needed, pars to match the best script op.

    .. note::
        This function only changes script positions being used, it does NOT
        check whether the base is valid for certain type_. It does not care
        about valid bases.

    Consider scriptop_pars2nonloscript_pars function if you do not want to
    impose script on setscript.
    """
    if len(pars) == 3:
        return [pars[0], None, pars[1], None, pars[2]]
    elif len(pars) == 5:
        return pars
    elif pars[2] is None and pars[5] is None:
        return [pars[0], pars[1], pars[3], pars[4], pars[6]]
    else:
        return [pars[0], None, pars[2], None, pars[5]]


def scriptop_pars2setscript_pars(pars):
    """Transform, if needed, pars to match the best setscript op.

    .. note::
        This function only changes script positions being used, it does NOT
        check whether the base is valid for certain type_. It does not care
        about valid bases.

    Consider scriptop_pars2nonloscript_pars function if you do not want to
    impose setscript on script.
    """
    if len(pars) == 3:
        return pars
    elif len(pars) == 5:
        return [pars[0], pars[2], pars[4]]
    elif pars[2] is None and pars[5] is None:
        return [pars[0], pars[3], pars[6]]
    else:
        return [pars[0], pars[2], pars[5]]


def scriptop_pars2nonloscript_pars(pars):
    """Decide if setscript or script fit better certain pars and return the
    correspondent pars.

    .. note::
        This function only changes script positions being used, it does NOT
        check whether the base is valid for certain type_. It does not care
        about valid bases.
    """
    if len(pars) != 7:
        return pars
    if pars[2] is None and pars[5] is None:
        return [pars[0], pars[1], pars[3], pars[4], pars[6]]
    else:
        return [pars[0], pars[2], pars[5]]


def do_require_loscript(base):
    """Return whether a loscript operator is needed given its base."""
    # Valid for symbols/0-args ops and blocks.
    if hasattr(base[0], 'type_') and base[0].type_ in LOSCRIPT_BASE_TYPES:
        return True
    else:
        return False


def scriptblock2pars(subeq, idx=None):
    """Return a list of arguments of the passed script-block.

    The list will have the format [base, lsub_arg, ..., sup_arg].
    The parameters not available will be set to None.

    If lop-block is not a script operator, -1 will be returned.

    .. note::
        It is OK if the script-block does not have a valid base according to
        do_require_loscript (probably because you are modificating the eq).
        What decides the pars returned is the script op.
    """

    def pars(opid, sub):
        """Return the args list provided a tuple from any script operator
        dictionary.

        .. note::
            It is supposed that first argument of *s* (the base) is not
            included in *opid*.

        :param opid: A tuple specifying the arguments used by the script
        operator, not considering the base.
        :param sub: A script-block (mandatory for this nested function).
        :return: The args list of the script operator.
        """
        retv = [copy.deepcopy(sub[1])] + [None] * len(opid)
        par_pos = 2
        for i, valid in enumerate(opid):
            if valid:
                retv[i+1] = copy.deepcopy(sub[par_pos])
                par_pos += 1
        return retv

    s = subeq if idx is None else eqqueries.get(idx, subeq)
    op = s[0]
    # Check that it is effectively a script-block
    if not hasattr(op, 'type_') or op.type_ not in SCRIPT_OP_TYPES:
        return -1

    if op.type_ == "setscript":
        return pars(SETSCRIPT_OP2ID_DICT[op], s)
    elif op.type_ == "script":
        return pars(SCRIPT_OP2ID_DICT[op], s)
    else:
        return pars(LOSCRIPT_OP2ID_DICT[op], s)


def valid_pars_pos(pars, flat_pos):
    """Return the position of the n-th non-None par in pars."""
    valid_pars_found = 0
    for pars_pos, pars_arg in enumerate(pars):
        if pars_arg is not None:
            if valid_pars_found == flat_pos:
                return pars_pos
            else:
                valid_pars_found += 1


def par_ord_from_pars_pos(pars, par_pos):
    """Return the ordinal of a parameter of a operator given the pars
    representation of its block and the position in pars of the parameter.

    :param pars: A pars list.
    :param par_pos: The position of the par in *pars* (first par pos is 0).
    :return: The parameter ordinal associted to *par_pos*.
    """
    # Take into account the the leading op, which is not included in args
    ordinal = 1
    for i in range(par_pos):
        if pars[i] is not None:
            ordinal += 1
    return ordinal


def pars2scriptop(pars):
    """Return the operator associated to a pars list.

    .. note::
        If every argument, except possibly the base, is None, None is returned.
    """
    key = tuple(bool(par) for par in pars[1:])
    try:
        if len(key) == 2:
            return ID2SETSCRIPT_OP_DICT[key]
        elif len(key) == 4:
            return ID2SCRIPT_OP_DICT[key]
        elif len(key) == 6:
            return ID2LOSCRIPT_OP_DICT[key]
        else:
            ShowError('Wrong number of parameters in pars list processed by '
                      'pars2scriptop: ' + repr(pars), True)
    except KeyError:
        ShowError('Wrong pars list in pars2scriptop: ' + repr(pars), True)


def pars2scriptblock(pars):
    """Return a script block associated to certain pars list of any script op.

    .. note::
        If every argument, except possibly the base, is None, -1 is returned.
    """
    op = pars2scriptop(pars)
    if op is None:
        return -1
    else:
        return [op] + [item for item in pars if item is not None]


def is_scriptop(elem, idx=None):
    """Return whether an operator is an script op."""
    op = elem if idx is None else eqqueries.get(idx, elem)
    return op.type_ in SCRIPT_OP_TYPES


def remove_script(idx, eq):
    """Remove pointed script from equation. Intentionally not accepting subeqs
    because its supeq may need to be modified.

     Downgrade script op or remove it, depending on whether other scripts
     remain. It may modify a script-supeq of the script-block.

    .. note::
        *idx* MUST point to an argument of a script operator DIFFERENT than
        the base.

    .. note::
        If script op is removed, the base is placed in the same position in
        which the script op-block was except in the case detailed below:

    Special rule:

        If:

            *   The only script of a script operator is requested to be
                removed, and
            *   Script op had type_ == "loscript", and
            *   Script-block was the base of another more external script
                operator (setscript or script),

        then, the internal script operator is removed and the external script
        operator is changed to the equivalent one of type_ "loscript".

    :param eq: An equation.
    :param idx: The index in *eq* of the script.
    :return: Position of a script block or bare base. Useful because it points
    to the external script op in the special case.
    """
    supeq = eqqueries.supeq(idx, eq, True)
    pars = scriptblock2pars(supeq)
    # Remove script.
    # Note: Subtracting 1 since indexing starts from 0 and real pars from 1
    pars[valid_pars_pos(pars, idx[-1] - 1)] = None
    new_block = pars2scriptblock(pars)

    old_scriptop_type = supeq[0].type_
    if new_block != -1:
        # Case: Downgrade script op
        supeq[:] = new_block
        return idx[:-1]

    # Case: Remove op
    supeq[:] = pars[0]

    # Was script-block a loscript-block and base of another script-block?
    if old_scriptop_type != "loscript" or len(idx) < 2 or idx[-2] != 1:
        return idx[:-1]
    supeqsupeq = eqqueries.get(idx[:-2], eq)
    if not is_scriptop(supeqsupeq[0]):
        return idx[:-1]

    # Subcase: Adapt external script op if internal script was loscript
    ext_op_idx = supeqsupeq[0]
    # It is OK to call the following function even if the base would require
    # an operator of type_ loscript.
    temp_ext_op_args = scriptblock2pars(supeqsupeq)
    new_ext_op_args = scriptop_pars2loscript_pars(temp_ext_op_args)
    supeqsupeq[:] = pars2scriptblock(new_ext_op_args)

    return idx[:-2]


def update_scriptblock(nextbase, subeq, idx=None):
    """Update a script op if needed by providing the next base it will have.

    It must be passed the script block or its index.

    .. note::
        The script operator is updated independently of which is its current
        base. That means that you are free to set the new base before or after
        calling this function.
    """
    scriptblock = subeq if idx is None else eqqueries.get(idx, subeq)
    args = scriptblock2pars(scriptblock)
    if do_require_loscript(nextbase):
        new_args = scriptop_pars2loscript_pars(args)
    else:
        new_args = scriptop_pars2nonloscript_pars(args)
    scriptblock[:] = pars2scriptblock(new_args)


def _insert_initial_script(baseref, scriptdir, is_superscript, newscript):
    """Insert a script to a block which is (currently) not a base or requested
    script is not compatible with operator script of base pointed.

    Index of the script will be index of *baseref* plus [2]
    """
    if do_require_loscript(baseref):
        type_ = "loscript"
    elif scriptdir == 0:
        type_ = "setscript"
    else:
        type_ = "script"
    pars = init_script_pars(baseref, type_)
    # referred script is guaranteed to be valid in pars list because we
    # constructed pars with the correct type_
    set_script_in_pars(pars, scriptdir, is_superscript, newscript)
    baseref[:] = pars2scriptblock(pars)


def insert_script(idx, eq, scriptdir, is_superscript, newscript=None):
    """Insert a script and return its index.

    Rules:

        *   If *idx* does not point to a current base, a script operator will
            be added, being the base the subeq pointed by *idx*.
            The index of the script will be returned.
        *   Elif *idx* points to a current base, requested script does not
            exist and the script is compatible with the script operator, script
            operator is upgraded and the index of the new script is returned.
        *   Elif *idx* points to a current base, requested script does not
            exist and the script is not compatible with the script operator,
            the simplest script block including the requested script will
            be the base of the current script operator.
            The index of the new script in *eq* is returned.
        *   Else (*idx* points to a current base and requested script exists),
            *eq* is not modified and index of the script is returned with
            last value multiplied by -1.

    :param idx: The index of the subeq which will be the base of the script.
    :param eq: An equation.
    :param scriptdir: Direction in which to include the script. 0 means
    vscript.
    :param is_superscript: Boolean indicating whether it is a superscript.
    If False, a subscript is inserted.
    :param newscript: A subeq with which to initialize the script.
    If it is None, a VOID is inserted instead.
    :return: The index of inserted script in *eq*. If it already existed,
    the last value of the index will be negative.
    """
    if newscript is None:
        newscript = utils.void()

    supeq = eqqueries.supeq(idx, eq, True)
    if supeq == -2 or not is_scriptop(supeq[0]):
        # Case: idx does not point to a base
        baseref = eq if supeq == -2 else supeq[idx[-1]]
        _insert_initial_script(baseref, scriptdir, is_superscript, newscript)
        return idx + [2]

    pars = scriptblock2pars(supeq)
    script_pos = get_script_pos_in_pars(pars, scriptdir, is_superscript)
    if script_pos == -1:
        # Case: Requested script is not compatible with current operator
        return _insert_initial_script(eq, idx, scriptdir, is_superscript,
                                      newscript)

    if pars[script_pos] is not None:
        # Case: Requested script already exists
        return idx[:-1] + [-par_ord_from_pars_pos(pars, script_pos)]

    # Case: Requested script is compatible with current script op type_ and
    # script is not present
    pars[script_pos] = newscript
    supeq[:] = pars2scriptblock(pars)
    return idx[:-1] + [par_ord_from_pars_pos(pars, script_pos)]
