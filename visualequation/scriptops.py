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

from . import eqqueries
from .symbols.utils import Op, NEWARG
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
SUBSUP = Op(3, r'\tensor*{{{0}}}{{^{{{3}}}_{{{2}}}}}', 'script')
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


def init_script_args(base, type_):
    "Return an args list with certain base and no scripts."
    if type_ == "setscript":
        return [base] + [None]*2
    if type_ == "script":
        return [base] + [None]*4
    return [base] + [None]*6


def get_script_pos_in_args(args, dir, is_superscript):
    """Return script position in an args list. If script parameters are not
    compatible with args, return -1.

    .. note::
        Only compatibility of referred script in provided *args* is checked.
        In particular, it is NOT checked whether the base (args[0]) is valid
        for the op associated to *args*.

    Combinations which do not return -1:

        *   len(args) == 3 and dir == 0
        *   len(args) == 5 and dir in (-1, 1)
        *   len(args) == 7 and dir in (-1, 0, 1)

    :param args: An args list of a script operator.
    :param dir: 0 for under/over, -1 for lsub/lsup and 1 for sub/sup.
    :param is_superscript: True for over, lsup and sup. Ow, False.
    :return: script position in args (from 1 to len(args)-1 since base is not a
    script) or -1.
    """
    if len(args) == 3:
        if dir != 0:
            return -1
        return 2 if is_superscript else 1
    elif len(args) == 5:
        if dir not in (-1, 1):
            return -1
        if dir == -1:
            return 3 if is_superscript else 1
        else:
            return 4 if is_superscript else 2
    else:
        if dir == -1:
            return 4 if is_superscript else 1
        elif dir == 0:
            return 5 if is_superscript else 2
        elif dir == 1:
            return 6 if is_superscript else 3
        else:
            return -1


def set_script_in_args(args, dir, is_superscript, psarg):
    args[get_script_pos_in_args(args, dir, is_superscript)] = psarg


def get_script_in_args(args, dir, is_superscript):
    """Get current script in args according to parameters.

    If script is not compatible with passed args, -1 is returned.
    """
    pos = get_script_pos_in_args(args, dir, is_superscript)
    return args[pos] if pos > 0 else -1


def scriptop_args2loscript_args(args):
    """Transform, if needed, args to match the best loscript op.

    .. note::
        This function only changes script positions being used, it does NOT
        check whether the base is valid for certain type_. It does not care
        about valid bases.
    """
    if len(args) == 3:
        return [args[0], None, args[1], None, None, args[2], None]
    elif len(args) == 5:
        return [args[0], args[1], None, args[2], args[3], None, args[4]]
    else:
        return args


def scriptop_args2script_args(args):
    """Transform, if needed, args to match the best script op.

    .. note::
        This function only changes script positions being used, it does NOT
        check whether the base is valid for certain type_. It does not care
        about valid bases.

    Consider scriptop_args2nonloscript_args function if you do not want to
    impose script on setscript.
    """
    if len(args) == 3:
        return [args[0], None, args[1], None, args[2]]
    elif len(args) == 5:
        return args
    elif args[2] is None and args[5] is None:
        return [args[0], args[1], args[3], args[4], args[6]]
    else:
        return [args[0], None, args[2], None, args[5]]


def scriptop_args2setscript_args(args):
    """Transform, if needed, args to match the best setscript op.

    .. note::
        This function only changes script positions being used, it does NOT
        check whether the base is valid for certain type_. It does not care
        about valid bases.

    Consider scriptop_args2nonloscript_args function if you do not want to
    impose setscript on script.
    """
    if len(args) == 3:
        return args
    elif len(args) == 5:
        return [args[0], args[2], args[4]]
    elif args[2] is None and args[5] is None:
        return [args[0], args[3], args[6]]
    else:
        return [args[0], args[2], args[5]]


def scriptop_args2nonloscript_args(args):
    """Decide if setscript or script fit better certain args and return the
    correspondent args.

    .. note::
        This function only changes script positions being used, it does NOT
        check whether the base is valid for certain type_. It does not care
        about valid bases.
    """
    if len(args) != 7:
        return args
    if args[2] is None and args[5] is None:
        return [args[0], args[1], args[3], args[4], args[6]]
    else:
        return [args[0], args[2], args[5]]


def do_require_loscript(base_pelem):
    """Return if a loscript operator is needed given the first primitive of
    the base.

    :param base_pelem: symbol or leading operator of the base.
    :return: A boolean.
    """
    if hasattr(base_pelem, 'type_') \
            and base_pelem.type_ in LOSCRIPT_BASE_TYPES:
        return True
    else:
        return False


def scriptblock2args(eq, idx):
    """Return a list of arguments of the script-block pointed by *idx*.

    The list has the format [base, lsub_arg, ..., sup_arg].
    The arguments not available will be set to None.

    If *idx* does not point to a script operator, -1 will be returned.

    .. note::
        It is OK if the script block pointed by *idx* does not have a valid
        base according to do_require_loscript (probably because you are
        modificating *eq*). What decides the args returned is the script op.

    :param eq: An equation.
    :param idx: Index of a script operator in *eq*.
    :return: The args list of the script block or -1.
    """

    def args(opid):
        """Return the args list provided a tuple from any script operator
        dictionary.

        .. note::
            In this nested function, parameter *idx* MUST point to a script
            operator. It is supposed that first argument (the base) is not
            included in *opid*.

        :param eq: An equation.
        :param idx: The index of a script operator in *eq*.
        :param opid: A tuple specifying the arguments used by the script
        operator, not considering the base.
        :return: The args list of the script operator.
        """
        arg_idx = idx + 1
        arg_end = eqqueries.nextsubeq(eq, arg_idx)
        retv = [eq[arg_idx:arg_end]] + [None] * len(opid)
        for i, valid in enumerate(opid):
            if valid:
                arg_idx, arg_end = arg_end, eqqueries.nextsubeq(eq, arg_idx)
                retv[i+1] = eq[arg_idx:arg_end]
        return retv

    op = eq[idx]  # it can be an index operator, but not necessarily
    if not hasattr(op, 'type_') or op.type_ not in SCRIPT_OP_TYPES:
        return -1

    if op.type_ == "setscript":
        return args(SETSCRIPT_OP2ID_DICT[op])
    elif op.type_ == "script":
        return args(SCRIPT_OP2ID_DICT[op])
    else:
        return args(LOSCRIPT_OP2ID_DICT[op])


def flat_args(args):
    """Flat an args list without including elements equal to None.

    .. note::
        Example: [[JUXT, 2, 3], None, [8]] -> [JUXT, 2, 3, 8]
    """
    new_args = []
    for arg in args:
        if arg is not None:
            for symb in arg:
                new_args.append(symb)
    return new_args


def valid_args_pos(args, flat_pos):
    """Return the position of the n-th non-None arg in args."""
    valid_args_found = 0
    for args_pos, args_arg in enumerate(args):
        if args_arg is not None:
            if valid_args_found == flat_pos:
                return args_pos
            else:
                valid_args_found += 1


def ublock_arg_idx_given_its_args(args, arg_pos):
    """Return the index of an argument in a block given its args
    representation and the position in args of the argument.

    :param args: An args list.
    :param arg_pos: The position of the arg in *args* (first arg pos is 0).
    :return: The index in the ublock. Operator (which is not present in *args*)
    would have index 0.
    """
    # Include the first pelem (the leading op) which is not included in args
    pelems = 1
    for i in range(arg_pos):
        if args[i] is not None:
            pelems += len(args[i])
    return pelems


def args2scriptop(args):
    """Return the operator associated to an arglist.

    .. note::
        If every argument, except possibly the base, is None, None is returned.
    """
    key = tuple(bool(arg) for arg in args[1:])
    try:
        if len(key) == 2:
            return ID2SETSCRIPT_OP_DICT[key]
        elif len(key) == 4:
            return ID2SCRIPT_OP_DICT[key]
        elif len(key) == 6:
            return ID2LOSCRIPT_OP_DICT[key]
        else:
            ShowError('Wrong number of arguments in arg list processed by '
                      'args2scriptop: ' + repr(args), True)
    except KeyError:
        ShowError('Wrong arg list in args2scriptop: ' + repr(args), True)


def args2scriptblock(args):
    """Return a script block associated to certain args of any script op.

    .. note::
        If every argument, except possibly the base, is None, -1 is returned.
    """
    op = args2scriptop(args)
    if op is None:
        return -1
    else:
        return [op] + flat_args(args)


def which_script(eq, idx):
    """Return information about scripts arguments.

    Returns a tuple of two elements:

        *   If idx points to an argument (base included) of an script
            operator in *eq*, the 1st element indicates the index in *eq* of
            the associated script operator. Else, it is -1.
        *   The 2nd element indicates which argument of the script operator is
            being pointed by *idx*, 0 if it is the base.
    """
    return eqqueries.whosearg_filter_type(eq, idx, SCRIPT_OP_TYPES)


def is_scriptop(eq, idx):
    return hasattr(eq[idx], 'type_') and eq[idx].type_ in SCRIPT_OP_TYPES


def is_base(eq, idx):
    return idx != 0 and is_scriptop(eq, idx-1)


def remove_script(eq, idx):
    """Remove a script.

     It can downgrade the script op or remove it, depending whether other
     scripts remain or not.

    .. note::
        *idx* MUST point to an argument of a script operator DIFFERENT than
        the base.

    .. note::
        In the typical case in which the script operator will be updated but
        not removed, the updated operator will be in the same position than the
        original.
        If operator is removed, the base is placed in the same position in
        which the operator was except in the case:


    Special rule:

        If:

            *   The only script of a script operator is requested to be
                removed, and
            *   Script operator had type_ == "loscript", and
            *   Script operator was the leading op of the base of a more
                external script operator (setscript or script),

        then, the internal script operator is removed and the external script
        operator is changed to the equivalent one of type_ "loscript".

    :param eq: An equation.
    :param idx: The index in *eq* of the script.
    :return: Position of script operator whose script is going to be removed.
    (It will be there a new script operator or the base, if there was only one
    script),
    """
    op_idx, arg_ord = eqqueries.whosearg_filter_type(eq, idx)
    end_block = eqqueries.nextsubeq(eq, op_idx)
    args = scriptblock2args(eq, op_idx)
    # Remove script.
    # Note: Subtracting 1 since indexing starts from 0 and ordinals from 1
    args[valid_args_pos(args, arg_ord - 1)] = None
    new_block = args2scriptblock(args)

    if new_block != -1:
        eq[op_idx:end_block] = new_block
    else:
        eq[op_idx:end_block] = args[0]
        if eq[op_idx].type_ == "loscript" and is_base(eq, op_idx):
            # Special subcase mentioned in docstring
            ext_op_idx = op_idx-1
            # It is OK to call this function even if the base would require
            # an operator of type_ loscript.
            temp_ext_op_args = scriptblock2args(eq, ext_op_idx)
            new_ext_op_args = scriptop_args2loscript_args(temp_ext_op_args)
            end_ext_block = eqqueries.nextsubeq(eq, ext_op_idx)
            eq[ext_op_idx:end_ext_block] = args2scriptblock(new_ext_op_args)

    return op_idx


def update_scriptblock(eq, op_idx, pelem):
    """Update a script block if needed by providing the new first primitive
    element of the base.

    .. note::
        The script operator is updated independently of which is its current
        base. That means that you are free to set the new base before or after
        calling this function.

    :param eq: An equation.
    :param op_idx: Index of the script op.
    :param pelem: First primitive element of the new base.
    """
    end_block = eqqueries.nextsubeq(eq, op_idx)
    args = scriptblock2args(eq, op_idx)
    if do_require_loscript(pelem):
        new_args = scriptop_args2loscript_args(args)
    else:
        new_args = scriptop_args2nonloscript_args(args)
    eq[op_idx:end_block] = args2scriptblock(new_args)


def _insert_initial_script(eq, idx, dir, is_superscript, subeq):
    """Insert a script to a block which is (currently) not a base or requested
    script is not compatible with operator script of base pointed.

    Return script index in eq.
    """
    end = eqqueries.nextsubeq(eq, idx)
    if do_require_loscript(eq[idx]):
        type_ = "loscript"
    elif dir == 0:
        type_ = "setscript"
    else:
        type_ = "script"
    args = init_script_args(eq[idx:end], type_)
    # referred script is guaranteed to be valid in args because we
    # constructed args with that intention
    set_script_in_args(args, dir, is_superscript, subeq)
    eq[idx:end] = args2scriptblock(args)
    return end + 1


def insert_script(eq, idx, dir, is_superscript, subeq=None):
    """Insert a script and return its index in the equation.

    Rules:

        *   If *idx* does not point to a current base, a script operator will
            be added, being the base the subeq pointed by *idx*.
            The index of the script in *eq* will be returned.
        *   Elif *idx* points to a current base and requested script does not
            exist and the script is compatible with the script operator, script
            operator is upgraded and the index of the new script is returned.
        *   Elif *idx* points to a current base, requested script does not
            exist and the script is not compatible with the script operator,
            a new script block containing the requested script will be the
            base of the current script operator. In detail:

                *   The new script operator will have as base the base of the
                    old script operator
                *   The new script operator will have only one script,
                    the requested one.
            The index of the new script in *eq* is returned.
        *   Else (*idx* points to a current base and requested script exists),
            *eq* is not modified and minus the index of the script is returned.

    :param eq: An equation.
    :param idx: The index of the subeq which will be the base of the script.
    :param dir: Direction in which to include the script. 0 means vscript.
    :param is_superscript: Boolean indicating whether it is a superscript.
    If False, a subscript is inserted.
    :param subeq: A subeq with which to initialize the script.
    If it is None, a NEWARG is inserted instead.
    :return: The index of inserted script in *eq*. If it already existed,
    the index of the script is returned but negative.
    """
    if subeq is None:
        subeq = [NEWARG]

    if not is_base(eq, idx):
        # Case: idx does not point to a base
        return _insert_initial_script(eq, idx, dir, is_superscript, subeq)

    scriptop_idx = idx-1
    args = scriptblock2args(eq, scriptop_idx)
    script_pos = get_script_pos_in_args(args, dir, is_superscript)
    if script_pos == -1:
        # Case: Requested script is not compatible with current operator
        return _insert_initial_script(eq, idx, dir, is_superscript, subeq)

    if args[script_pos] is not None:
        # Case: Requested script already exists
        return -(scriptop_idx
                 + ublock_arg_idx_given_its_args(args, script_pos))

    # Case: Requested script is compatible with current script op type_ and
    # script is not present
    args[script_pos] = subeq
    end_current_scriptop = eqqueries.nextsubeq(eq, scriptop_idx)
    eq[scriptop_idx:end_current_scriptop] = args2scriptblock(args)
    return scriptop_idx + ublock_arg_idx_given_its_args(args, script_pos)
