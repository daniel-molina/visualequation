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
Module to transform equations to latex code and getting information from or
replacing equation blocks.
"""
from .symbols import utils
from .errors import ShowError


def subeq2latex(eq, idx):
    """
    1st output is the latex code of the subequation which starts at idx.
    2nd output is the idx idx_end AFTER the last element of the subeq such
    that eq[idx:idx_end] defines the subequation.
    """

    def subeq2latex_helper(index):
        """Amazing recursive function that DOES the real job."""
        if isinstance(eq[index], utils.Op):
            # Find n_args independent subeqs for this operator
            arg_index = index + 1
            latex_args = ()
            for ignored in range(eq[index].n_args):
                latex_arg, arg_index = subeq2latex_helper(arg_index)
                latex_args += (latex_arg,)
            return eq[index](*latex_args), arg_index
        elif isinstance(eq[index], str):
            return eq[index], index + 1
        else:
            ShowError('Unknown equation element in subeq2latex_helper: '
                      + repr(eq[index]), True)

    return subeq2latex_helper(idx)


def nextsubeq(eq, idx):
    """
    It is a simplification of subeq2latex that only returns the end idx
    that defines the subequation as eq[idx:end_idx].
    This function was written because the previous one was called often
    just to calculate end of blocks.
    Returned idx is not necessarily a valid idx of eq, but it is when
    another subequation can be found after subequation starting at idx. In
    that case, it is equal to its first element.
    """

    def nextsubeqindex_helper(index):
        """ Simplification of subeq2latex_helper."""
        if isinstance(eq[index], utils.Op):
            # I have to find n_arg independent blocks for this operator
            arg_index = index + 1
            for ignored in range(eq[index].n_args):
                arg_index = nextsubeqindex_helper(arg_index)
            return arg_index
        elif isinstance(eq[index], str):
            return index + 1
        else:
            ShowError('Unknown equation element in nextsubeq: '
                      + repr(eq[index]), True)

    return nextsubeqindex_helper(idx)


def which_arg_is(eq, maybe_arg_idx, op_idx):
    """
    *Low level function (no correction checkings)*

    Requirement: op_idx must be smaller than maybe_arg_idx.

    Rules:

        *   If op_idx points to a symbol or no argument of the operator starts
            in maybe_arg_idx, return -1.
        *   Else, return the ordinal of the argument starting in maybe_arg_idx
            of operator in op_idx. That is, if it is its first argument,
            1 is returned; if it is the second, 2 is returned, and so on.
    """
    if isinstance(eq[op_idx], str) or eq[op_idx].n_args == 0:
        return -1
    arg_idx = op_idx + 1
    if arg_idx == maybe_arg_idx:
        return 1
    for argminus2 in range(eq[op_idx].n_args - 1):
        arg_idx = nextsubeq(eq, arg_idx)
        if arg_idx == maybe_arg_idx:
            return argminus2 + 2
    return -1


def eq2latex_code(eq):
    """
    Returns latex code of the equation.
    """

    index = 0
    latex = ''
    while index < len(eq):
        string, index = subeq2latex(eq, index)
        latex += string

    return latex


def whosearg(eq, idx):
    """
    Theory:

        *   Every index in an equation is mapped naturally with the subequation
            starting at that index.
        *   A subequation is always the whole equation or an argument of some
            operator.

    Rules:
        *   If :idx: is 0, return (-1, None).
        *   Else:

            *   1st output value is the index of the operator which has an
                argument starting at :idx:.
            *   2nd output value is the ordinal of operator's argument which
                starts at :idx:.
    """
    if idx == 0:
        return -1, None
    start_idx = idx - 1
    while True:
        ordinal = which_arg_is(eq, idx, start_idx)
        if ordinal > 0:
            return start_idx, ordinal
        start_idx -= 1


def prev_arg(eq, idx, surpass_op=False):
    """Return index of the previous argument.

    Warning:

        This is a very low-level function. It will return indices of descendant
        JUXTs, for example, if that is right solution.

    Consider the operator that has an argument at index :idx:.
        *   If :idx: == 0, -2 is returned.
        *   Elif argument at :idx: is not the first argument of the operator,
            return the index of the previous argument of the operator.
        *   Elif surpass_op == False, return -1.
        *   Else, return the index of the operator.
    """
    op_idx, ordinal = whosearg(eq, idx)
    if op_idx < 0:
        return -2
    if ordinal == 1:
        if surpass_op:
            return op_idx
        else:
            return -1
    prev_arg_idx = op_idx + 1
    for ignored in range(ordinal - 2):
        prev_arg_idx = nextsubeq(eq, prev_arg_idx)
    return prev_arg_idx


def next_arg(eq, idx, surpass_op=False):
    """Return the index of the next argument.

    Warning:

        This is a very low-level function. It can return indices of
        descendant JUXTs if appropriated, for example.

    Consider the operator that has an argument at index :idx:.

        *   If :idx: == 0, return -2.
        *   If :idx: == len(:eq:)-1, return -3.
        *   Elif :idx: does not point to the last argument of the operator,
            return the index of the next argument.
        *   Elif surpass_op == False, return -1.
        *   Else, return the index after last element of argument pointed by
            :idx:.
    """
    if not idx:
        return -2
    if idx == len(eq) - 1:
        return -3
    op_idx, ordinal = whosearg(eq, idx)
    if ordinal == eq[op_idx].n_args and not surpass_op:
        return -1
    # 2 cases: Ordinary and next index after last element of last argument.
    return nextsubeq(eq, idx)


def supeq(eq, idx):
    """Return index of smallest supeq of a subequation.

    If idx <= 0, -1 is returned.
    """
    if idx <= 0:
        return -1
    while idx > 0:
        current_arg_idx = idx
        idx = prev_arg(eq, current_arg_idx)
    return current_arg_idx - 1


def other_juxt_arg(eq, idx, start_idx=None):
    """Find if it is an arg of JUXT and, in that case, where is the other arg.

    Return a tuple of two elements:

    *   1st output value indicates the index of the JUXT which has one argument
        starting at :idx:. If that JUXT does not exist, it is -1.
    *   If the first output value is not -1, 2nd output value is the index
        of the other arg of the JUXT. Else, it is None.

    If you know in advance that, in the case of being an argument of JUXT,
    that JUXT cannot have an index bigger than certain value, you can specify
    it with :start_idx: parameter.

    Properties:

        *   As expected, if :idx: points to a descendant JUXT or a citizen,
            a non-negative 1st output value is returned.
        *   If -1 is returned, that means that :idx: points to the whole
            equation or to an uarg.
    """
    if idx == 0:
        return -1, None

    # Case 1: idx points to first argument of JUXT
    if eq[idx - 1] == utils.JUXT:
        arg2_idx = nextsubeq(eq, idx)
        return idx - 1, arg2_idx

    # Case 2: idx points to second argument of JUXT
    lookidx = idx - 2 if start_idx is None else start_idx
    while lookidx >= 0:
        if eq[lookidx] == utils.JUXT:
            arg2_idx = nextsubeq(eq, lookidx + 1)
            if arg2_idx == idx:
                return lookidx, lookidx + 1
            elif arg2_idx > idx:
                return -1, None
        lookidx -= 1
    return -1, None


def is_juxt_arg(eq, idx):
    """Return whether a subequation is an arg of JUXT.

    A simplification of other_juxt_arg which only returns a boolean indicating
    whether :idx: points to the argument of a JUXT.
    """
    juxt_idx, ignored = other_juxt_arg(eq, idx)
    return juxt_idx >= 0


def is_terminal_juxt(eq, idx):
    """Return if subequation if element is a terminal JUXT.

    Marginal cases:

        *   If it is the unique JUXT of a JUXT-ublock, it returns True.
        *   If it is not a JUXT, it returns False.
    """
    # If idx points to a JUXT, it is guaranteed that nextsubeq(eq, idx+1)
    # points to a valid element of the equation.
    return eq[idx] == utils.JUXT and nextsubeq(eq, idx + 1) != utils.JUXT


def is_last_citizen(eq, idx):
    juxt_idx, arg2_idx = other_juxt_arg(eq, idx)
    return juxt_idx >= 0 and arg2_idx < idx


def is_parent_juxt(eq, idx):
    """Return whether an element is the parent JUXT of a JUXT-ublock.

    Marginal cases:
        *   Of course, if it is the unique JUXT of a JUXT-ublock, it returns
            True.
        *   If it is not a JUXT, it returns False.
    """
    return eq[idx] == utils.JUXT and not is_juxt_arg(eq, idx)


def is_first_citizen(eq, idx):
    return is_parent_juxt(eq, idx - 1)


def is_descendant_juxt(eq, idx):
    return eq[idx] == utils.JUXT and is_juxt_arg(eq, idx)


def is_ublock(eq, idx):
    return isinstance(eq[idx], utils.Op) and not is_descendant_juxt(eq, idx)


def is_usubeq(eq, idx):
    return not is_descendant_juxt(eq, idx)


def is_uarg(eq, idx):
    return not idx and not is_juxt_arg(eq, idx)


def is_citizen(eq, idx):
    return eq[idx] != utils.JUXT and is_juxt_arg(eq, idx)


def whoami(eq, idx):
    """
    Return 0 if idx points to the whole equation.
    Return 1 if idx points to an uarg.
    Return 2 if idx points to a citizen.
    Return -1 if idx points to a descendant JUXT.
    It is guaranteed that any :idx: point uniquely to one of those subeqs.
    """
    if idx == 0:
        return 0
    op_idx, ignored = whosearg(eq, idx)
    if eq[op_idx] != utils.JUXT:
        return 1
    elif eq[idx] != utils.JUXT:
        return 2
    else:
        return -1


def cocitizen(eq, idx, forward=True):
    """Return the index of the co-citizen to the right of a citizen.

    If :forward: is False, then return the index of the co-citizen to the left
        instead.
    If :idx: does not point to a citizen, -1 is returned.
    If the asked co-citizen does not exist, -2 is returned.

    Properties:
        * If -1 is returned, :idx: points to an uarg, descendant JUXT or is 0.
        * If -2 is returned, :idx: points to:

            a) If :forward: is True, the last citizen of a JUXT-ublock.
        or,
            b) If :forward: is False, the first citizen of a JUXT-ublock.
    """
    # Discard DJUXT-blocks (also JUXT-ublocks)
    if eq[idx] == utils.JUXT:
        return -1

    # Discard the whole equation and every uarg
    juxt_idx, otherarg_idx = other_juxt_arg(eq, idx)
    if juxt_idx < 0:
        return -1

    # From this point, it is sure that we are dealing with a citizen
    if otherarg_idx < idx:
        # Forward/Backward subcases: idx is the 2nd arg of terminal JUXT
        return -2 if forward else otherarg_idx
    elif forward:
        # Forward subcases: idx is 1st arg of (terminal / non-terminal JUXT)
        return otherarg_idx if eq[otherarg_idx] != utils.JUXT \
            else otherarg_idx + 1
    elif is_parent_juxt(eq, juxt_idx):
        # Backward subcase: no co-citizen to the left
        return -2
    # If juxt_idx is not parent JUXT, then juxt_idx -2 > 0
    elif eq[juxt_idx - 2] == utils.JUXT:
        # Backward subcase: symbol co-citizen to the left of the JUXT
        return juxt_idx - 1
    else:
        # Backward subcase: block co-citizen to the left of the JUXT
        ignored, citizen = other_juxt_arg(eq, juxt_idx)
        return citizen


def parent_juxt(eq, idx):
    """Return the parent JUXT of a JUXT-ublock.

    If idx does not point to a JUXT or a citizen, -1 is returned.

    :eq: A valid equation.
    :idx: index of a citizen or a JUXT of the JUXT-ublock.
    :return: The index of the parent JUXT or -1.
    """
    juxt_idx, ignored = other_juxt_arg(eq, idx)
    if juxt_idx < 0:
        if eq[idx] != utils.JUXT:
            return -1
        else:
            return idx

    while True:
        idx = juxt_idx
        juxt_idx, ignored = other_juxt_arg(eq, idx)
        if juxt_idx < 0:
            return idx


def first_cocitizen(eq, idx):
    """Return the first citizen of a JUXT-ublock.

    If idx does not point to a JUXT or a citizen, -1 is returned.

    :eq: A valid equation.
    :idx: index of a citizen or a JUXT of the JUXT-ublock.
    :return: The index of the first citizen of the JUXT-ublock or -1.
    """
    juxtublock_idx = parent_juxt(eq, idx)
    return juxtublock_idx + 1 if juxtublock_idx >= 0 else -1


def last_citizen(eq, idx):
    """Returns the last citizen of a JUXT-ublock.

    If idx does not point to a citizen or JUXT, -1 is returned.

    :eq: A valid equation.
    :idx: index of a citizen or a JUXT of the JUXT-ublock.
    :return: The index of the last citizen of the JUXT-ublock or -1.
    """
    if eq[idx] == utils.JUXT:
        idx += 1

    nextidx = cocitizen(eq, idx)
    if nextidx == -1:
        return -1
    while nextidx > 0:
        idx = nextidx
        nextidx = cocitizen(eq, idx)
    return idx


def prev_neighbour(eq, idx):
    """Return the index of the previous neighbour.

    If returned value is negative, there is no such neighbour.
    """
    flag = whoami(eq, idx)
    if not flag:
        return -2
    if flag == 1:
        return prev_arg(eq, idx, surpass_op=False)
    if flag == 2:
        return cocitizen(eq, idx, forward=False)
    return -1


def next_neighbour(eq, idx):
    """Return the index of the next neighbour.

    If returned value is negative, there is no such neighbour.
    """
    flag = whoami(eq, idx)
    if not flag:
        return -2
    if flag == 1:
        return next_arg(eq, idx, surpass_op=False)
    if flag == 2:
        return cocitizen(eq, idx, forward=True)
    return -1


def usupeq(eq, idx):
    """Return the index of the smallest usupeq of a subequation.

    :eq: A valid equation.
    :idx: The index in :eq: of a subequation.

    Marginal cases:
        * If len(eq) == 1, return -2.
        * Elif idx == 0, return -1.
    """
    if len(eq) == 1:
        return -2
    if idx == 0:
        return -1

    op_idx = supeq(eq, idx)
    if eq[op_idx] != utils.JUXT:
        return op_idx
    else:
        # Can return op_idx if it points to a parent JUXT.
        return parent_juxt(eq, op_idx)


def supeq_finishing_at(eq, end_idx, subeq_idx=None):
    """Return index of smallest supeq of  finishing at certain index.

    Return -1 if such usubeq does not exist.

    If :start_idx: is not None, do not consider usubeqs which index starts
    after that value.

    :start_idx: must be smaller than :idx_element: and len(:eq:).

    Properties:

        *   returned value of a previous successful call is a valid
            value to look for a next bigger usubeq.
    """
    if subeq_idx is not None:
        assert subeq_idx < end_idx
        assert subeq_idx < len(eq)
    assert 0 <= end_idx < len(eq)

    if subeq_idx is None:
        subeq_idx = end_idx

    # Loop iterated more than once only if start_idx is passed and it points to
    # an usubeq that does not include end_idx
    while True:
        subeq_idx = usupeq(eq, subeq_idx)
        idx_after_usubeq = nextsubeq(eq, subeq_idx)
        if idx_after_usubeq - 1 == end_idx:
            return subeq_idx
        if idx_after_usubeq - 1 > end_idx:
            return -1


def indexop2arglist(eq, sel_idx):
    """
    Convert the block of indices pointed by sel_index to a list of arguments.
    The list has the format [base, lsub_arg, sub_arg, sup_arg, lsup_arg].
    The arguments not available will be replaced by None.
    If sel_index does not point to an script operator at all, base will be the
    pointed usubeq and the rest will be set to None.
    """
    op = eq[sel_idx]  # it can be an idx operator or not, as explained above
    if not hasattr(op, 'type_') or op.type_ not in ('script', 'opindex'):
        end_block = nextsubeq(eq, sel_idx)
        return [eq[sel_idx:end_block], None, None, None, None]
    start_arg1 = sel_idx + 1
    start_arg2 = nextsubeq(eq, start_arg1)
    if op in (utils.LSUB, utils.OPLSUB):
        end_arg2 = nextsubeq(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None, None, None]
    elif op in (utils.SUB, utils.OPSUB):
        end_arg2 = nextsubeq(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2], None, None]
    elif op in (utils.SUP, utils.OPSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                None, None, eq[start_arg2:end_arg2], None]
    elif op in (utils.LSUP, utils.OPLSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                None, None, None, eq[start_arg2:end_arg2]]
    elif op in (utils.LSUBSUB, utils.OPLSUBSUB):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3], None, None]
    elif op in (utils.SUBSUP, utils.OPSUBSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2], eq[end_arg2:end_arg3], None]
    elif op in (utils.SUPLSUP, utils.OPSUPLSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                None, None, eq[start_arg2:end_arg2], eq[end_arg2:end_arg3]]
    elif op in (utils.LSUBLSUP, utils.OPLSUBLSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None, None, eq[end_arg2:end_arg3]]
    elif op in (utils.LSUBSUP, utils.OPLSUBSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None, eq[end_arg2:end_arg3], None]
    elif op in (utils.SUBLSUP, utils.OPSUBLSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2], None, eq[end_arg2:end_arg3]]
    elif op in (utils.LSUBSUBSUP, utils.OPLSUBSUBSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        end_arg4 = nextsubeq(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3],
                eq[end_arg3:end_arg4], None]
    elif op in (utils.LSUBSUBLSUP, utils.OPLSUBSUBLSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        end_arg4 = nextsubeq(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3],
                None, eq[end_arg3:end_arg4]]
    elif op in (utils.LSUBSUPLSUP, utils.OPLSUBSUPLSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        end_arg4 = nextsubeq(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None,
                eq[end_arg2:end_arg3], eq[end_arg3:end_arg4]]
    elif op in (utils.SUBSUPLSUP, utils.OPSUBSUPLSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        end_arg4 = nextsubeq(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2],
                eq[end_arg2:end_arg3], eq[end_arg3:end_arg4]]
    elif op in (utils.LSUBSUBSUPLSUP, utils.OPLSUBSUBSUPLSUP):
        end_arg2 = nextsubeq(eq, start_arg2)
        end_arg3 = nextsubeq(eq, end_arg2)
        end_arg4 = nextsubeq(eq, end_arg3)
        end_arg5 = nextsubeq(eq, end_arg4)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3],
                eq[end_arg3:end_arg4], eq[end_arg4:end_arg5]]
    else:
        ShowError("Equation element not recognised in indexop2arglist: "
                  + repr(op), True)


def flat_arglist(args):
    """
    Flat the list of list args without including elements equal to None.
    """
    new_args = []
    for arg in args:
        if arg is not None:
            for symb in arg:
                new_args.append(symb)
    return new_args


def arglist2indexop(args):
    index_dict = {
        (True, False, False, False, False): None,
        (True, True, False, False, False): utils.LSUB,
        (True, False, True, False, False): utils.SUB,
        (True, False, False, True, False): utils.SUP,
        (True, False, False, False, True): utils.LSUP,
        (True, True, True, False, False): utils.LSUBSUB,
        (True, False, True, True, False): utils.SUBSUP,
        (True, False, False, True, True): utils.SUPLSUP,
        (True, True, False, False, True): utils.LSUBLSUP,
        (True, True, False, True, False): utils.LSUBSUP,
        (True, False, True, False, True): utils.SUBLSUP,
        (True, True, True, True, False): utils.LSUBSUBSUP,
        (True, True, True, False, True): utils.LSUBSUBLSUP,
        (True, True, False, True, True): utils.LSUBSUPLSUP,
        (True, False, True, True, True): utils.SUBSUPLSUP,
        (True, True, True, True, True): utils.LSUBSUBSUPLSUP,
    }
    opindex_dict = {
        (True, False, False, False, False): None,
        (True, True, False, False, False): utils.OPLSUB,
        (True, False, True, False, False): utils.OPSUB,
        (True, False, False, True, False): utils.OPSUP,
        (True, False, False, False, True): utils.OPLSUP,
        (True, True, True, False, False): utils.OPLSUBSUB,
        (True, False, True, True, False): utils.OPSUBSUP,
        (True, False, False, True, True): utils.OPSUPLSUP,
        (True, True, False, False, True): utils.OPLSUBLSUP,
        (True, True, False, True, False): utils.OPLSUBSUP,
        (True, False, True, False, True): utils.OPSUBLSUP,
        (True, True, True, True, False): utils.OPLSUBSUBSUP,
        (True, True, True, False, True): utils.OPLSUBSUBLSUP,
        (True, True, False, True, True): utils.OPLSUBSUPLSUP,
        (True, False, True, True, True): utils.OPSUBSUPLSUP,
        (True, True, True, True, True): utils.OPLSUBSUBSUPLSUP,
    }
    try:
        if hasattr(args[0][0], 'type_') \
                and args[0][0].type_ in utils.OPINDEX_ARG_LIST:
            return opindex_dict[tuple(bool(arg) for arg in args)]
        else:
            return index_dict[tuple(bool(arg) for arg in args)]
    except KeyError:
        ShowError('Bad argument list in arglist2indexop: '
                  + repr(args), True)


def is_script(eq, sel_index):
    """
    Returns a tuple of three elements:
    The 1st element indicates if the element pointed by sel_index is a script.
    If it is or if it is the base, the 2nd element indicates the pos of the
    associated idx operator.
    The 3rd element indicates which argument of the idx operator is being
    pointed by sel_index, or 0 if it is the base.
    """
    g = ((index, op) for index, op in enumerate(eq) if hasattr(op, 'type_')
         and op.type_ in ('opindex', 'script'))
    for op_index, op in g:
        arg_i_index = op_index + 1
        if arg_i_index == sel_index:
            return False, op_index, 0
        for arg_i in range(1, op.n_args):
            arg_i_index = nextsubeq(eq, arg_i_index)
            if arg_i_index == sel_index:
                return True, op_index, arg_i
    else:
        return False, None, None
