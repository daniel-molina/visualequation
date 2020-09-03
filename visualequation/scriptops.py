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

from .subeqs import Subeq
from .idx import Idx
from .ops import Op, TVOID, PVOID
from .errors import ShowError

# Vertical script operators
UNDER = Op("under", r'\underset{{{1}}}{{{0}}}', 2, 'setscript')
OVER = Op("over", r'\overset{{{1}}}{{{0}}}', 2, 'setscript')
UNDEROVER = Op("underover", r'\overset{{{2}}}{{{\underset{{{1}}}{{{0}}}}}}', 3,
               'setscript')

# Standard script operators
LSUB = Op("lsub", r'\tensor*[_{{{1}}}]{{{0}}}{{}}', 2, 'script')
SUB = Op("sub", r'\tensor*{{{0}}}{{_{{{1}}}}}', 2, 'script')
LSUP = Op("lsup", r'\tensor*[^{{{1}}}]{{{0}}}{{}}', 2, 'script')
SUP = Op("sup", r'\tensor*{{{0}}}{{^{{{1}}}}}', 2, 'script')
LSUBSUB = Op("lsubsub", r'\tensor*[_{{{1}}}]{{{0}}}{{_{{{2}}}}}', 3, 'script')
LSUBLSUP = Op("lsublsup", r'\tensor*[_{{{1}}}^{{{2}}}]{{{0}}}{{}}', 3,
              'script')
LSUBSUP = Op("lsubsup", r'\tensor*[_{{{1}}}]{{{0}}}{{^{{{2}}}}}', 3, 'script')
SUBLSUP = Op("sublsup", r'\tensor*[^{{{2}}}]{{{0}}}{{_{{{1}}}}}', 3, 'script')
SUBSUP = Op("subsup", r'\tensor*{{{0}}}{{^{{{2}}}_{{{1}}}}}', 3, 'script')
LSUPSUP = Op("lsupsup", r'\tensor*[^{{{1}}}]{{{0}}}{{^{{{2}}}}}', 3, 'script')
LSUBSUBLSUP = Op("lsubsublsup",
                 r'\tensor*[_{{{1}}}^{{{3}}}]{{{0}}}{{_{{{2}}}}}', 4, 'script')
LSUBSUBSUP = Op("lsubsubsup", r'\tensor*[_{{{1}}}]{{{0}}}{{^{{{3}}}_{{{2}}}}}',
                4, 'script')
LSUBLSUPSUP = Op("lsublsupsup",
                 r'\tensor*[^{{{2}}}_{{{1}}}]{{{0}}}{{^{{{3}}}}}', 4, 'script')
SUBLSUPSUP = Op("sublsupsup", r'\tensor*[^{{{2}}}]{{{0}}}{{^{{{3}}}_{{{1}}}}}',
                4, 'script')
LSUBSUBLSUPSUP = Op("lsubsublsupsup",
                    r'\tensor*[_{{{1}}}^{{{3}}}]{{{0}}}{{_{{{2}}}^{{{4}}}}}',
                    5, 'script')

# Script for Large Operators. Valid only for variable-size, fun-args or
# anything defined with \mathop.
# It is necessary not to include brackets in the base when no \sideset is used
LOUNDER = Op("lounder", r'{0}_{{{1}}}', 2, 'loscript')
LOOVER = Op("loover", r'{0}^{{{1}}}', 2, 'loscript')
LOUNDEROVER = Op("lounderover", r'{0}_{{{1}}}^{{{2}}}', 3, 'loscript')

LOLSUB = Op("lolsub", r'\sideset{{_{{{1}}}}}{{}}{{{0}}}', 2, 'loscript')
LOSUB = Op("losub", r'\sideset{{}}{{_{{{1}}}}}{{{0}}}', 2, 'loscript')
LOLSUP = Op("lolsup", r'\sideset{{^{{{1}}}}}{{}}{{{0}}}', 2, 'loscript')
LOSUP = Op("losup", r'\sideset{{}}{{^{{{1}}}}}{{{0}}}', 2, 'loscript')
LOLSUBSUB = Op("lolsubsub", r'\sideset{{_{{{1}}}}}{{_{{{2}}}}}{{{0}}}', 3,
               'loscript')
LOLSUBLSUP = Op("lolsublsup", r'\sideset{{_{{{1}}}^{{{2}}}}}{{}}{{{0}}}', 3,
                'loscript')
LOLSUBSUP = Op("lolsubsup", r'\sideset{{_{{{1}}}}}{{^{{{2}}}}}{{{0}}}', 3,
               'loscript')
LOSUBLSUP = Op("losublsup", r'\sideset{{^{{{2}}}}}{{_{{{1}}}}}{{{0}}}', 3,
               'loscript')
LOSUBSUP = Op("losubsup", r'\sideset{{}}{{_{{{1}}}^{{{2}}}}}{{{0}}}', 3,
              'loscript')
LOLSUPSUP = Op("lolsupsup", r'\sideset{{^{{{1}}}}}{{^{{{2}}}}}{{{0}}}', 3,
               'loscript')
LOLSUBSUBLSUP = Op("lolsubsublsup",
                   r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}}}{{{0}}}', 4,
                   'loscript')
LOLSUBSUBSUP = Op("lolsubsubsup",
                  r'\sideset{{_{{{1}}}}}{{^{{{3}}}_{{{2}}}}}{{{0}}}', 4,
                  'loscript')
LOLSUBLSUPSUP = Op("lolsublsupsup",
                   r'\sideset{{^{{{2}}}_{{{1}}}}}{{^{{{3}}}}}{{{0}}}', 4,
                   'loscript')
LOSUBLSUPSUP = Op("LOSUBLSUPSUP",
                  r'\sideset{{^{{{2}}}}}{{^{{{3}}}_{{{1}}}}}{{{0}}}', 4,
                  'loscript')
LOLSUBSUBLSUPSUP \
    = Op("lolsubsublsupsup",
         r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}^{{{4}}}}}{{{0}}}', 5,
         'loscript')
# +Under
LOLSUBUNDER = Op("lolsubunder", r'\sideset{{_{{{1}}}}}{{}}{{{0}}}_{{{2}}}', 3,
                 'loscript')
LOUNDERSUB = Op("loundersub", r'\sideset{{}}{{_{{{2}}}}}{{{0}}}_{{{1}}}', 3,
                'loscript')
LOUNDERLSUP = Op("lounderlsup", r'\sideset{{^{{{2}}}}}{{}}{{{0}}}_{{{1}}}', 3,
                 'loscript')
LOUNDERSUP = Op("loundersup", r'\sideset{{}}{{^{{{2}}}}}{{{0}}}_{{{1}}}', 3,
                'loscript')
LOLSUBUNDERSUB = Op("lolsubundersub",
                    r'\sideset{{_{{{1}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}', 4,
                    'loscript')
LOLSUBUNDERLSUP = Op("lolsubunderlsup",
                     r'\sideset{{_{{{1}}}^{{{3}}}}}{{}}{{{0}}}_{{{2}}}', 4,
                     'loscript')
LOLSUBUNDERSUP = Op("lolsubundersup",
                    r'\sideset{{_{{{1}}}}}{{^{{{3}}}}}{{{0}}}_{{{2}}}', 4,
                    'loscript')
LOUNDERSUBLSUP = Op("loundersublsup",
                    r'\sideset{{^{{{3}}}}}{{_{{{2}}}}}{{{0}}}_{{{1}}}', 4,
                    'loscript')
LOUNDERSUBSUP = Op("loundersubsup",
                   r'\sideset{{}}{{_{{{2}}}^{{{3}}}}}{{{0}}}_{{{1}}}', 4,
                   'loscript')
LOUNDERLSUPSUP = Op("lounderlsupsup",
                    r'\sideset{{^{{{2}}}}}{{^{{{3}}}}}{{{0}}}_{{{1}}}', 4,
                    'loscript')
LOLSUBUNDERSUBLSUP \
    = Op("lolsubundersublsup",
         r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}', 5,
         'loscript')
LOLSUBUNDERSUBSUP \
    = Op("lolsubundersubsup",
         r'\sideset{{_{{{1}}}}}{{^{{{4}}}_{{{3}}}}}{{{0}}}_{{{2}}}', 5,
         'loscript')
LOLSUBUNDERLSUPSUP \
    = Op("lolsubunderlsupsup",
         r'\sideset{{^{{{3}}}_{{{1}}}}}{{^{{{4}}}}}{{{0}}}_{{{2}}}', 5,
         'loscript')
LOUNDERSUBLSUPSUP \
    = Op("loundersublsupsup",
         r'\sideset{{^{{{3}}}}}{{^{{{4}}}_{{{2}}}}}{{{0}}}_{{{1}}}', 5,
         'loscript')
LOLSUBUNDERSUBLSUPSUP \
    = Op("lolsubundersublsupsup",
         r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}^{{{5}}}}}{{{0}}}_{{{2}}}', 6,
         'loscript')
# +Over
LOLSUBOVER = Op("lolsubover", r'\sideset{{_{{{1}}}}}{{}}{{{0}}}^{{{2}}}', 3,
                'loscript')
LOSUBOVER = Op("losubover", r'\sideset{{}}{{_{{{1}}}}}{{{0}}}^{{{2}}}', 3,
               'loscript')
LOLSUPOVER = Op("lolsupover", r'\sideset{{^{{{1}}}}}{{}}{{{0}}}^{{{2}}}', 3,
                'loscript')
LOOVERSUP = Op("looversup", r'\sideset{{}}{{^{{{2}}}}}{{{0}}}^{{{1}}}', 3,
               'loscript')
LOLSUBSUBOVER = Op("lolsubsubover",
                   r'\sideset{{_{{{1}}}}}{{_{{{2}}}}}{{{0}}}^{{{3}}}', 4,
                   'loscript')
LOLSUBLSUPOVER = Op("lolsublsupover",
                    r'\sideset{{_{{{1}}}^{{{2}}}}}{{}}{{{0}}}^{{{3}}}', 4,
                    'loscript')
LOLSUBOVERSUP = Op("lolsuboversup",
                   r'\sideset{{_{{{1}}}}}{{^{{{3}}}}}{{{0}}}^{{{2}}}', 4,
                   'loscript')
LOSUBLSUPOVER = Op("losublsupover",
                   r'\sideset{{^{{{2}}}}}{{_{{{1}}}}}{{{0}}}^{{{3}}}', 4,
                   'loscript')
LOSUBOVERSUP = Op("losuboversup",
                  r'\sideset{{}}{{_{{{1}}}^{{{3}}}}}{{{0}}}^{{{2}}}', 4,
                  'loscript')
LOLSUPOVERSUP = Op("lolsupoversup",
                   r'\sideset{{^{{{1}}}}}{{^{{{3}}}}}{{{0}}}^{{{2}}}', 4,
                   'loscript')
LOLSUBSUBLSUPOVER \
    = Op("lolsubsublsupover",
         r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}}}{{{0}}}^{{{4}}}', 5,
         'loscript')
LOLSUBSUBOVERSUP \
    = Op("lolsubsuboversup",
         r'\sideset{{_{{{1}}}}}{{^{{{4}}}_{{{2}}}}}{{{0}}}^{{{3}}}', 5,
         'loscript')
LOLSUBLSUPOVERSUP \
    = Op("lolsublsupoversup",
         r'\sideset{{^{{{2}}}_{{{1}}}}}{{^{{{4}}}}}{{{0}}}^{{{3}}}', 5,
         'loscript')
LOSUBLSUPOVERSUP \
    = Op("losublsupoversup",
         r'\sideset{{^{{{2}}}}}{{^{{{4}}}_{{{1}}}}}{{{0}}}^{{{3}}}', 5,
         'loscript')
LOLSUBSUBLSUPOVERSUP \
    = Op("lolsubsublsupoversup",
         r'\sideset{{_{{{1}}}^{{{3}}}}}{{_{{{2}}}^{{{5}}}}}{{{0}}}^{{{4}}}', 6,
         'loscript')
# +UnderOver
LOLSUBUNDEROVER = Op("lolsubunderover",
                     r'\sideset{{_{{{1}}}}}{{}}{{{0}}}_{{{2}}}^{{{3}}}', 4,
                     'loscript')
LOUNDERSUBOVER = Op("loundersubover",
                    r'\sideset{{}}{{_{{{2}}}}}{{{0}}}_{{{1}}}^{{{3}}}', 4,
                    'loscript')
LOUNDERLSUPOVER = Op("lounderlsupover",
                     r'\sideset{{^{{{2}}}}}{{}}{{{0}}}_{{{1}}}^{{{3}}}', 4,
                     'loscript')
LOUNDEROVERSUP = Op("lounderoversup",
                    r'\sideset{{}}{{^{{{3}}}}}{{{0}}}_{{{1}}}^{{{2}}}', 4,
                    'loscript')
LOLSUBUNDERSUBOVER \
    = Op("lolsubundersubover",
         r'\sideset{{_{{{1}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}^{{{4}}}', 5,
         'loscript')
LOLSUBUNDERLSUPOVER \
    = Op("lolsubunderlsupover",
         r'\sideset{{_{{{1}}}^{{{3}}}}}{{}}{{{0}}}_{{{2}}}^{{{4}}}', 5,
         'loscript')
LOLSUBUNDEROVERSUP \
    = Op("lolsubunderoversup",
         r'\sideset{{_{{{1}}}}}{{^{{{4}}}}}{{{0}}}_{{{2}}}^{{{3}}}', 5,
         'loscript')
LOUNDERSUBLSUPOVER \
    = Op("loundersublsupover",
         r'\sideset{{^{{{3}}}}}{{_{{{2}}}}}{{{0}}}_{{{1}}}^{{{4}}}', 5,
         'loscript')
LOUNDERSUBOVERSUP \
    = Op("loundersuboversup",
         r'\sideset{{}}{{_{{{2}}}^{{{4}}}}}{{{0}}}_{{{1}}}^{{{3}}}', 5,
         'loscript')
LOUNDERLSUPOVERSUP \
    = Op("lounderlsupoversup",
         r'\sideset{{^{{{2}}}}}{{^{{{4}}}}}{{{0}}}_{{{1}}}^{{{3}}}', 5,
         'loscript')
LOLSUBUNDERSUBLSUPOVER \
    = Op("lolsubundersublsupover",
         r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}}}{{{0}}}_{{{2}}}^{{{5}}}', 6,
         'loscript')
LOLSUBUNDERSUBOVERSUP \
    = Op("lolsubundersuboversup",
         r'\sideset{{_{{{1}}}}}{{^{{{5}}}_{{{3}}}}}{{{0}}}_{{{2}}}^{{{4}}}', 6,
         'loscript')
LOLSUBUNDERLSUPOVERSUP \
    = Op("lolsubunderlsupoversup",
         r'\sideset{{^{{{3}}}_{{{1}}}}}{{^{{{5}}}}}{{{0}}}_{{{2}}}^{{{4}}}', 6,
         'loscript')
LOUNDERSUBLSUPOVERSUP \
    = Op("loundersublsupoversup",
         r'\sideset{{^{{{3}}}}}{{^{{{5}}}_{{{2}}}}}{{{0}}}_{{{1}}}^{{{4}}}', 6,
         'loscript')
LOLSUBUNDERSUBLSUPOVERSUP \
    = Op("lolsubundersublsupoversup",
         r'\sideset{{_{{{1}}}^{{{4}}}}}{{_{{{3}}}^{{{6}}}}}{{{0}}}'
         r'_{{{2}}}^{{{5}}}', 7, 'loscript')

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
    LOLSUPOVER: (False, False, False, True, True, False),
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


def _init_script_pars(base, type_):
    """Return a pars list with certain base and no scripts."""
    basepar = [copy.deepcopy(base)]
    if type_ == "setscript":
        return basepar + [None] * 2
    if type_ == "script":
        return basepar + [None] * 4
    return basepar + [None] * 6


def _get_script_pos_in_pars(pars, scriptdir, is_superscript):
    """Return script position in a pars list. If script parameters are not
    compatible with pars, return -1.

    .. note::
        Only compatibility of referred script in provided *pars* is checked.
        In particular, it is NOT checked whether the base (pars[0]) is valid
        for the op associated to *pars*.

    Combinations which do not return -1:

        *   len(args) == 3 (setscript) and scriptdir == 0
        *   len(args) == 5 (script)    and scriptdir in (-1, 1)
        *   len(args) == 7 (loscript)  and scriptdir in (-1, 0, 1)

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


def _set_script_in_pars(pars, scriptdir, is_superscript, pspar):
    pars[_get_script_pos_in_pars(pars, scriptdir, is_superscript)] = pspar


def _get_script_in_pars(pars, scriptdir, is_superscript):
    """Get current script in pars according to parameters.

    If script is not compatible with passed pars, -1 is returned.
    """
    pos = _get_script_pos_in_pars(pars, scriptdir, is_superscript)
    return pars[pos] if pos > 0 else -1


def _scriptop_pars2loscript_pars(pars):
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


def _scriptop_pars2script_pars(pars):
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


def _scriptop_pars2setscript_pars(pars):
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


def _scriptop_pars2nonloscript_pars(pars):
    """Decide if setscript or script fit better certain pars and return the
    correspondent pars.

    .. note::
        This function only changes script positions being used, it does NOT
        check whether the base is valid at all.
    """
    if len(pars) != 7:
        return pars
    if pars[2] is None and pars[5] is None:
        # No subeqs are lost in this case
        return [pars[0], pars[1], pars[3], pars[4], pars[6]]
    else:
        # Some subeqs may be lost in this case
        return [pars[0], pars[2], pars[5]]


def do_require_loscript(base: Subeq):
    """Return whether a loscript operator is needed given its base."""
    # Valid for symbols/0-args ops and blocks.
    s = base[1] if base.is_gopb() else base
    return hasattr(s[0], 'type_') and s[0].type_ in LOSCRIPT_BASE_TYPES


def scriptop_type(op):
    """Return the type_ of a script operator.

    If it is not one of them, -1 is returned.
    """
    if hasattr(op, "type_") and op.type_ in SCRIPT_OP_TYPES:
        return op.type_
    return -1


def _scriptblock2pars(subeq, index=None):
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
            It is supposed that first parameter of *s* (the base) is not
            included in *opid*.

        :param opid: A tuple specifying the arguments used by the script
        operator, not considering the base.
        :param sub: A script-block (mandatory for this nested function).
        :return: The pars list of the script operator.
        """
        retv = [copy.deepcopy(sub[1])] + [None] * len(opid)
        par_pos = 2
        for i, valid in enumerate(opid):
            if valid:
                retv[i + 1] = copy.deepcopy(sub[par_pos])
                par_pos += 1
        return retv

    s = subeq(index)
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


def _valid_pars_pos(pars, flat_pos):
    """Return the position of the n-th non-None par in pars.

    .. note::

        flat_pos == 0 would mean the base in the pars of a script-block.
    """
    valid_pars_found = 0
    for pars_pos, pars_arg in enumerate(pars):
        if pars_arg is not None:
            if valid_pars_found == flat_pos:
                return pars_pos
            else:
                valid_pars_found += 1


def par_ord_from_pars_pos(pars, par_pos):
    """Return the ordinal of a parameter of an operator given the pars
    representation of its block and the position in pars of the parameter.

    .. note::

        A *par_pos* refers to the base of a script-block it will be returned
        value 1.

    :param pars: A pars list.
    :param par_pos: The position of the par in *pars* (first par pos is 0).
    :return: The parameter ordinal associted to *par_pos*.
    """
    # Take into account the leading op, which is not included in args
    ordinal = 1
    if pars[par_pos] is None:
        raise ValueError("Asked parameter is None in the pars representation")
    for i in range(par_pos):
        if pars[i] is not None:
            ordinal += 1
    return ordinal


def _pars2scriptop(pars):
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


def _pars2scriptblock(pars):
    """Return a script block associated to certain pars list of any script op.

    .. note::
        If every argument, except possibly the base, is None, -1 is returned.
    """
    op = _pars2scriptop(pars)
    if op is None:
        return -1
    else:
        return Subeq([op] + [item for item in pars if item is not None])


def is_scriptop(elem, index=None):
    """Return whether an operator is an script op."""
    op = elem if index is None else elem(index)
    return hasattr(op, "type_") and op.type_ in SCRIPT_OP_TYPES


def remove_script(index, eq):
    """Remove pointed script from equation. Intentionally not accepting
    stricts subeqs of an equation because its supeq may need to be modified.

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
    idx = Idx(index)
    supeq = eq.supeq(idx)
    pars = _scriptblock2pars(supeq)
    # Remove script.
    # Note: Subtracting 1 since indexing starts from 0 and real pars from 1
    pars[_valid_pars_pos(pars, idx[-1] - 1)] = None
    new_block = _pars2scriptblock(pars)

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
    supeqsupeq = eq(idx[:-2])
    if not is_scriptop(supeqsupeq[0]):
        return idx[:-1]

    # Subcase: Adapt external script op if internal script was loscript
    ext_op_idx = supeqsupeq[0]
    # It is OK to call the following function even if the base would require
    # an operator of type_ loscript.
    temp_ext_op_args = _scriptblock2pars(supeqsupeq)
    new_ext_op_args = _scriptop_pars2loscript_pars(temp_ext_op_args)
    supeqsupeq[:] = _pars2scriptblock(new_ext_op_args)

    return idx[:-2]


# Dictionaries providing a map between positions of pars before a change of
# script-block and after it. SET_SCR means that the setscript is more external.
SCR2SET_DICT = {0: 0, 2: 1, 4: 2}
SCR2LO_DICT = {0: 0, 1: 1, 2: 3, 3: 4, 4: 6}
SCR2SCR_SET_DICT = {0: (0, 0), 1: (1,), 2: (2,), 3: (3,), 4: (4,)}
SCR2SET_SCR_DICT = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (0, 3), 4: (0, 4)}
SCR_SET2SET_SCR_DICT = {(0, 0): (0, 0),
                   (1,): (0, 1), (0, 1): (1,), (2,): (0, 2),
                   (3,): (0, 3), (0, 2): (2,), (4,): (0, 4)}
SET2LO_DICT = {0: 0, 1: 2, 2: 5}
SET2SCR_SET_DICT = {0: (0, 0), 1: (0, 1), 2: (0, 2)}
SET2SET_SCR_DICT = {0: (0, 0), 1: (1, ), 2: (2, )}
SCR_SET2LO_DICT = {
    (0, 0): 0, (1,): 1, (0, 1): 2, (2,): 3, (3,): 4, (0, 2): 5, (4,): 6}
SET_SCR2LO_DICT = {
    (0, 0): 0, (0, 1): 1, (1,): 2, (0, 2): 3, (0, 3): 4, (2,): 5, (0, 4): 6}

SET2SCR_DICT = {v: k for k, v in SCR2SET_DICT.items()}
LO2SCR_DICT = {v: k for k, v in SCR2LO_DICT.items()}
SCR_SET2SCR_DICT = {v: k for k, v in SCR2SCR_SET_DICT.items()}
SET_SCR2SCR_DICT = {v: k for k, v in SCR2SET_SCR_DICT.items()}
SET_SCR2SCR_SET_DICT = {v: k for k, v in SCR_SET2SET_SCR_DICT.items()}
LO2SET_DICT = {v: k for k, v in SET2LO_DICT.items()}
SCR_SET2SET_DICT = {v: k for k, v in SET2SCR_SET_DICT.items()}
SET_SCR2SET_DICT = {v: k for k, v in SET2SET_SCR_DICT.items()}
LO2SCR_SET_DICT = {v: k for k, v in SCR_SET2LO_DICT.items()}
LO2SET_SCR_DICT = {v: k for k, v in SET_SCR2LO_DICT.items()}


def _map_refindex(sb_index, ref_index, ext_prev_pars, prev_pars, ext_next_pars,
                  next_pars):
    """Return the equivalent index of a subequation after a modification of a
    script-block or a external-internal script-block.

    Requirements:

        This function is very flexible. The only requirement is that
        *ref_index* must point to a real subeq before the operation.

    In case that *ref_index* points to a script involved in the operation and
    it does not exist after it, -1 is returned.

    *sb_index* must be the index od the script-block that was effectively
    updated. In the case of being two of them, the most external one.

    *ext_\*_pars* and/or *ext_\*_pars* must be set to None if there are
    external script block.
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
        prev_pos_key = _valid_pars_pos(prev_pars, tail.pop(0) - 1)
    elif tail == [1] and ext_next_pars is None:
        return start
    elif tail == [1]:
        return start + [1]
    elif tail[0] == 1:
        prev_pos_key = (0, _valid_pars_pos(prev_pars, tail[1] - 1))
        del tail[0:2]
    else:
        prev_pos_key = (_valid_pars_pos(ext_prev_pars, tail.pop(0) - 1),)

    def next_pos_value2l(next_pos_val):
        # It can raise ValueError, which will be handled by the caller (below)
        if ext_next_pars is None:
            # This case assures that value is not a tuple
            return [par_ord_from_pars_pos(next_pars, next_pos_val)]
        elif len(next_pos_val) == 1:
            return [par_ord_from_pars_pos(ext_next_pars, next_pos_val[0])]
        else:
            return [1, par_ord_from_pars_pos(next_pars, next_pos_val[1])]

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
            return prev_pos_key2idx(SET2SCR_DICT)
        if len(prev_pars) == 3 and len(next_pars) == 7:
            return prev_pos_key2idx(SET2LO_DICT)
        if len(prev_pars) == 5 and len(next_pars) == 3:
            return prev_pos_key2idx(SCR2SET_DICT)
        if len(prev_pars) == 5 and len(next_pars) == 7:
            return prev_pos_key2idx(SCR2LO_DICT)
        if len(prev_pars) == 7 and len(next_pars) == 3:
            return prev_pos_key2idx(LO2SET_DICT)
        if len(prev_pars) == 7 and len(next_pars) == 5:
            return prev_pos_key2idx(LO2SCR_DICT)

    if ext_prev_pars and ext_next_pars is None:
        if len(ext_prev_pars) == 3 and len(next_pars) == 3:
            return prev_pos_key2idx(SET_SCR2SET_DICT)
        if len(ext_prev_pars) == 3 and len(next_pars) == 5:
            return prev_pos_key2idx(SET_SCR2SCR_DICT)
        if len(ext_prev_pars) == 3 and len(next_pars) == 7:
            return prev_pos_key2idx(SET_SCR2LO_DICT)
        if len(ext_prev_pars) == 5 and len(next_pars) == 3:
            return prev_pos_key2idx(SCR_SET2SET_DICT)
        if len(ext_prev_pars) == 5 and len(next_pars) == 5:
            return prev_pos_key2idx(SCR_SET2SCR_DICT)
        if len(ext_prev_pars) == 5 and len(next_pars) == 7:
            return prev_pos_key2idx(SCR_SET2LO_DICT)

    if ext_prev_pars is None and ext_next_pars:
        if len(prev_pars) == 3 and len(ext_next_pars) == 3:
            return prev_pos_key2idx(SET2SET_SCR_DICT)
        if len(prev_pars) == 3 and len(ext_next_pars) == 5:
            return prev_pos_key2idx(SET2SCR_SET_DICT)
        if len(prev_pars) == 5 and len(ext_next_pars) == 3:
            return prev_pos_key2idx(SCR2SET_SCR_DICT)
        if len(prev_pars) == 5 and len(ext_next_pars) == 5:
            return prev_pos_key2idx(SCR2SCR_SET_DICT)
        if len(prev_pars) == 7 and len(ext_next_pars) == 3:
            return prev_pos_key2idx(LO2SET_SCR_DICT)
        if len(prev_pars) == 7 and len(ext_next_pars) == 5:
            return prev_pos_key2idx(LO2SCR_SET_DICT)

    if len(ext_prev_pars) == len(ext_next_pars):
        return prev_pos_key2idx()
    if len(ext_prev_pars) == 3 and len(ext_next_pars) == 5:
        return prev_pos_key2idx(SET_SCR2SCR_SET_DICT)
    return prev_pos_key2idx(SCR_SET2SET_SCR_DICT)


def _change2loscriptblock(eq: Subeq, index, refindex=None):
    """Internal function.

    eq(index) must be a real \*script-block.

    If pointed subeq is a script/setscript-block, it checks whether the 1-level
    supeq is a setscript/script-block so their scripts can be included in
    the new loscriptblock.
    """
    idx = Idx(index)
    refidx = Idx(refindex)
    sb = eq(idx)
    op_type = scriptop_type(sb[0])
    if op_type == "loscript":
        return refidx

    inner_pars = _scriptblock2pars(sb)
    sup = eq.supeq(index)
    ext_pars = None
    if sup != -2:
        # Not including loscript type: it cannot have a \*script-block as base
        if scriptop_type(sup[0]) not in (-1, op_type):
            ext_pars = _scriptblock2pars(sup)
            del idx[-1]

    if op_type == "script":
        # Subcases:
        #   [script, ...] -> [loscript, ...]
        #   [setscript, [script, ...], ...] -> [loscript, ...]
        new_pars = [inner_pars[0], inner_pars[1], None, inner_pars[2],
                    inner_pars[3], None, inner_pars[4]]
        if ext_pars:
            new_pars[2] = ext_pars[1]
            new_pars[5] = ext_pars[2]
    elif not ext_pars:
        # Subcase: [setscript, ...] -> [loscript, ...]
        new_pars = [inner_pars[0], None, inner_pars[1], None, None,
                    inner_pars[2], None]
    else:
        # Subcase: [script, [setscript, ...], ...] -> [loscript, ...]
        new_pars = [inner_pars[0], ext_pars[1], inner_pars[1], ext_pars[2],
                    ext_pars[3], inner_pars[2], ext_pars[4]]

    # Note: idx has previously been corrected if needed
    eq(idx)[:] = _pars2scriptblock(new_pars)
    return _map_refindex(idx, refidx, ext_pars, inner_pars, None, new_pars)


def _change2nonloscriptblock(eq: Subeq, index, refindex=None):
    """Internal function.

    It does not check any supeq, so they are never combined with the new
    scriptop. However, to avoid loosing scripts a loscript-block will be
    converted in a script-block which base is a setscript-block if necesary.

    Implementation note:

        [loscript, ...] -> [script, [setscript, ...], ....]
    """
    idx = Idx(index)
    refidx = Idx(refindex)
    sb = eq(idx)
    op_type = scriptop_type(sb[0])
    if op_type != "loscript":
        return refidx

    pars = _scriptblock2pars(sb)
    new_ext_pars = None
    if pars[2] is None and pars[5] is None:
        new_inner_pars = [pars[0], pars[1], pars[3], pars[4], pars[6]]
        new_pars = new_inner_pars
    elif [pars[1], pars[3], pars[4], pars[6]].count(None) == 4:
        new_inner_pars = [pars[0], pars[2], pars[5]]
        new_pars = new_inner_pars
    else:
        # Two script ops are needed to avoid missing any script
        # -> Use the setscript op externally and script op internally
        new_inner_pars = [pars[0], pars[2], pars[5]]
        inner_sb = _pars2scriptblock(new_inner_pars)
        new_ext_pars = [inner_sb, pars[1], pars[3], pars[4], pars[6]]
        new_pars = new_ext_pars

    sb[:] = _pars2scriptblock(new_pars)
    return _map_refindex(idx, refidx, None, pars, new_ext_pars, new_inner_pars)


def equivalent_op(op: Op, ext_op: Op = None):
    """Return equivalent op, or op-pair, which is equivalent to passed
    script op but of different script type: lo <-> nonlo.

    A pair is returned. If only one script op is needed for the equivalence,
    the second element is set to to None. Else, the first one is the internal
    script op.

    By the moment this function is used only for testing.

    .. note::
        The order is unusual for the arguments and output: firstly internal op,
        secondly external op.
    """
    s = Subeq([op] + [["x"]] * op.n_args)
    if op.type_ == "loscript":
        _change2nonloscriptblock(s, [])
        if is_scriptop(s[1][0]):
            return s[1][0], s[0]
        return s[0], None

    if ext_op is None:
        _change2loscriptblock(s, [])
        return s[0], None

    s = Subeq([ext_op] + [s] + [["x"]] * ext_op.n_args)
    # Refer to the internal script-block, not the external
    _change2loscriptblock(s, [1])
    return s[0], None


def update_scriptblock(nextbase, eq: Subeq, index=None, refindex=None):
    """Update a script op if needed by providing the next base it will have.
    Pointed subeq must be the script block which base is being modified.

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
    op_type = scriptop_type(scriptblock[0])
    if op_type == -1:
        return refidx
    if op_type == "loscript":
        if do_require_loscript(Subeq(nextbase)):
            return refidx
        else:
            # setscript/script (or a combination of both) -> loscript
            return _change2nonloscriptblock(eq, index, refindex)
    elif not do_require_loscript(Subeq(nextbase)):
        return refidx
    return _change2loscriptblock(eq, index, refindex)


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
    pars = _init_script_pars(baseref, type_)
    # referred script is guaranteed to be valid in pars list because we
    # constructed pars with the correct type_
    _set_script_in_pars(pars, scriptdir, is_superscript, newscript)
    baseref[:] = _pars2scriptblock(pars)


def insert_script(index, eq: Subeq, scriptdir, is_superscript, newscript=None):
    """Insert a script and return its index.

    If pointed subeq is a TVOID without a script, it is replaced by VOID
    before inserting the script.

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
    :param scriptdir: Dir in which to include the script. 0 means vscript.
    :param is_superscript: Boolean indicating whether it is a superscript.
    :param newscript: A subeq with which to initialize script. None means VOID.
    :return: The index of inserted script. If it already existed, a flag.
    """
    if newscript is None:
        newscript = Subeq(None)

    idx = Idx(index)
    supeq = eq.supeq(idx)
    if supeq == -2 or not is_scriptop(supeq[0]):
        # Case: idx does not point to a base
        baseref = eq if supeq == -2 else supeq[idx[-1]]
        if baseref == [TVOID]:
            # TVOID -> PVOID
            baseref[:] = [PVOID]
        _insert_initial_script(baseref, scriptdir, is_superscript, newscript)
        return idx[:] + [2]

    pars = _scriptblock2pars(supeq)
    script_pos = _get_script_pos_in_pars(pars, scriptdir, is_superscript)
    if script_pos == -1:
        # Case: Requested script is not compatible with current operator
        baseref = supeq[idx[-1]]
        _insert_initial_script(baseref, scriptdir, is_superscript, newscript)
        return idx[:] + [2]

    if pars[script_pos] is not None:
        # Case: Requested script already exists
        return idx[:-1] + [-par_ord_from_pars_pos(pars, script_pos)]

    # Case: Requested script is compatible with current script op type_ and
    # script is not present
    pars[script_pos] = newscript
    supeq[:] = _pars2scriptblock(pars)
    return idx[:-1] + [par_ord_from_pars_pos(pars, script_pos)]
