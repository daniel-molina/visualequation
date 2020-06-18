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


def eqblock2latex(eq, index):
    """
    Return latex code of the equation block starting at the given index
    and 1 + the index of the last element of the block in eq.
    A block is symbol or str, a unary operator with its first argument or
    a binary operator and their two arguments.
    Our equations should be a single block (with sub-blocks),
    using as many Prod's at the beginning as necessary.
    """

    def block2latex(index):
        """ Incredible recursive function that DOES the real job"""
        if isinstance(eq[index], utils.Op):
            # I have to find n_arg independent blocks for this operator
            index_of_arg = index + 1
            latex_args = ()
            for ignored in range(eq[index].n_args):
                latex_arg, index_of_arg = block2latex(index_of_arg)
                latex_args += (latex_arg,)
            return (eq[index](*latex_args), index_of_arg)
        elif isinstance(eq[index], str):
            return (eq[index], index + 1)
        else:
            ShowError('Unknown equation element in block2latex: '
                      + repr(eq[index]), True)

    return block2latex(index)


def nextblockindex(eq, index):
    """
    It is a simplification of eqblock2latex that only returns the end index.
    This function was written because the previous one was called often
    just to calculate end of blocks.
    It returns the index after the end of the block,
    being a valid index or not (when it is passed the index of the start of
    an ending block of eq).
    """

    def block2nextindex(index):
        """ Simplification of the recursive nested function block2latex."""
        if isinstance(eq[index], utils.Op):
            # I have to find n_arg independent blocks for this operator
            index_of_arg = index + 1
            for ignored in range(eq[index].n_args):
                index_of_arg = block2nextindex(index_of_arg)
            return index_of_arg
        elif isinstance(eq[index], str):
            return index + 1
        else:
            ShowError('Unknown equation element in nextblockindex: '
                      + repr(eq[index]), True)

    return block2nextindex(index)


def eq2latex_code(eq):
    """
    Returns latex code of the equation.
    """

    index = 0
    latex = ''
    while index < len(eq):
        string, index = eqblock2latex(eq, index)
        latex += string

    return latex


def insertrbyjuxt(eq, start_index, eqblock):
    """
    Insert eqblock after the block which starts at start_index by using Juxt.
    Returns the index of the begining of inserted eqblock.
    """
    # If eqblock is the base of an index operator, consider the index operator
    # instead. It avoids a bit of caos in the equation structure.
    # if hasattr(eq[start_index - 1], 'type_') \
    #   and eq[start_index - 1].type_ in ('index', 'opindex'):
    #    start_index -= 1
    end_index = nextblockindex(eq, start_index)
    eq[start_index:end_index] = [utils.JUXT] + eq[start_index:end_index] \
                                + eqblock
    return end_index + 1


def insertlbyjuxt(eq, start_index, eqblock):
    """
    Insert eqblock before the block which starts at start_index by using Juxt.
    Returns the index of the inserted block.
    """
    # If eqblock is the base of an index operator, consider the index operator
    # instead. It avoids a bit of chaos in the equation structure.
    # if hasattr(eq[start_index - 1], 'type_') \
    #   and eq[start_index - 1].type_ in ('index', 'opindex'):
    #    start_index -= 1
    end_index = nextblockindex(eq, start_index)
    eq[start_index:end_index] = [utils.JUXT] + eqblock \
                                + eq[start_index:end_index]
    return start_index + 1


def replaceby(eq, start_index, eqblock):
    """
    Replace block starting at start_index by eqblock.
    Returns the index of the next element (if any) after inserted eqblock
    """
    end_index = nextblockindex(eq, start_index)
    eq[start_index:end_index] = eqblock
    return start_index + len(eqblock) + 1


def is_arg_of_juxt(eq, check_index):
    """
    Returns a tuple of three elements:
    The first element says whether check_index is an argument of a Juxt op.
    If it is, the 2nd element indicates the pos of that Juxt and the 3rd one
    the position of the other arg of Juxt.
    Note: If it is not an argument of a Juxt, that means that check_index
    points to the beginning of a block (an argument of any non-JUXT operator or
    the whole equation).
    """
    start_index = 0
    try:
        while True:
            juxt_index = eq.index(utils.JUXT, start_index)
            arg2index = nextblockindex(eq, juxt_index + 1)
            if juxt_index + 1 == check_index:
                return True, juxt_index, arg2index
            elif arg2index == check_index:
                return True, juxt_index, juxt_index + 1
            else:
                start_index = juxt_index + 1
    except ValueError:
        return False, None, None


def start_of_smallest_block(eq, idx):
    """
    Return the index of the first element of a block.
    (The index of any previous operator except intermediate JUXTs)
    """
    wrong_idx = True
    while wrong_idx:
        retidx = idx
        wrong_idx, idx, ignored = is_arg_of_juxt(eq, retidx)
    return retidx


def is_first_element_of_block(eq, idx):
    """
    1st output indicates if element with index idx is the start of a block.
    2nd argument is the index of the start of the smallest block which contains
    element pointed by idx.
    """
    block_start = start_of_smallest_block(eq, idx)
    return block_start == idx, block_start


def prev_block_start(eq, idx):
    """
    Similar to start_of_smallest_block but if idx is already the solution,
    return the index of the previous block.

    If idx is a negative number, 0 is returned. Useful to avoid checking
    output value before a call with idx equal to that previous output
    minus 1.

    Properties of output:
        * If idx is not the start of a block, block starting at output
          contains idx.
        * If idx is the start of a block, the block does not always contains
          idx.
    """
    if idx <= 0:
        return 0
    is_first, idx_first = is_first_element_of_block(eq, idx)
    return idx_first if not is_first else start_of_smallest_block(eq, idx-1)


def surrounding_block_start(eq, idx):
    """
    Similar to start_of_smallest_block but, if idx is already the solution,
    return the index of the next smallest block containing index idx.

    If idx is a negative number, 0 is returned. Useful to avoid checking
    output value before a call with idx equal to that previous output
    minus 1.
    """
    # prev_block_start manages case idx < 0
    candidate_idx = prev_block_start(eq, idx)
    if candidate_idx == 0:
        return 0
    while idx >= nextblockindex(eq, candidate_idx):
        candidate_idx = prev_block_start(eq, candidate_idx-1)
        if candidate_idx <= 0:
            return 0
    return candidate_idx


def first_arg_of_juxt_seq(eq, juxt_index):
    """
    It returns the index of the first argument of the first JUXT with
    first argument different than JUXT in a group of JUXTs.
    """
    assert eq[juxt_index] == utils.JUXT
    while True:
        arg1_start = juxt_index + 1
        if eq[arg1_start] == utils.JUXT:
            juxt_index = arg1_start
        else:
            return arg1_start


def last_arg_of_juxt_seq(eq, juxt_index):
    """
    It returns the index of the second argument of the last JUXT in a group of
    JUXTs.
    """
    if eq[juxt_index] != utils.JUXT:
        ShowError('No JUXT passed to last_arg_of_juxt_seq function', True)

    arg2index = nextblockindex(eq, juxt_index + 1)
    while True:
        if eq[arg2index] == utils.JUXT:
            juxt_index = arg2index
            arg2index = nextblockindex(eq, juxt_index + 1)
        else:
            return arg2index


def is_intermediate_juxt(eq, index):
    """
    Check whether index points to a JUXT that is the argument of
    other JUXT.
    """
    if eq[index] == utils.JUXT:
        cond, ignored1, ignored2 = is_arg_of_juxt(eq, index)
        if cond:
            return True
    return False


def is_last_element_of_block(eq, idx_element, start=None):
    """
    * 1st output indicates whether idx_element points to last element
      of a block. Note that intermediate JUXTs are not considered as blocks.
    * If it does, 2nd output value is the index of the closest operator
      such that its last element is pointed by idx_element.
    * If start is not None, do not consider operators which start in that
      position or after that. If it is negative, False is returned (handy if
       you are calculating it from previous output and not checking that it
       out of range). It must be smaller than idx_element and len(eq).
      -> As a consequence, 2nd output value - 1 of a previous successful call
       (1st output value == True) is a valid value to look for a next
       closest operator.
    """
    if start is not None:
        assert start < idx_element
        assert start < len(eq)
    assert 0 <= idx_element < len(eq)

    candidate = idx_element - 1 if start is None else start
    while candidate >= 0:
        while not isinstance(eq[candidate], utils.Op) or \
                is_intermediate_juxt(eq, candidate):
            candidate -= 1
            if candidate < 0:
                return False, None
        index_after_block = nextblockindex(eq, candidate)
        if index_after_block == idx_element + 1:
            return True, candidate
        # Skip some iterations
        elif index_after_block > idx_element + 1:
            return False, None
        else:
            candidate -= 1
    return False, None


def indexop2arglist(eq, sel_index):
    """
    Convert the block of indices pointed by sel_index to a list of arguments.
    The list has the format [base, lsub_arg, sub_arg, sup_arg, lsup_arg].
    The arguments not available will be replaced by None.
    If sel_index does not point to an operator index at all, base will be the
    pointed block and the rest will be set to None.
    """
    op = eq[sel_index]  # it can be index operator or not, as explained above
    if not hasattr(op, 'type_') or op.type_ not in ('index', 'opindex'):
        end_block = nextblockindex(eq, sel_index)
        return [eq[sel_index:end_block], None, None, None, None]
    start_arg1 = sel_index + 1
    start_arg2 = nextblockindex(eq, start_arg1)
    if op in (utils.LSUB, utils.OPLSUB):
        end_arg2 = nextblockindex(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None, None, None]
    elif op in (utils.SUB, utils.OPSUB):
        end_arg2 = nextblockindex(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2], None, None]
    elif op in (utils.SUP, utils.OPSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                None, None, eq[start_arg2:end_arg2], None]
    elif op in (utils.LSUP, utils.OPLSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                None, None, None, eq[start_arg2:end_arg2]]
    elif op in (utils.LSUBSUB, utils.OPLSUBSUB):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3], None, None]
    elif op in (utils.SUBSUP, utils.OPSUBSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2], eq[end_arg2:end_arg3], None]
    elif op in (utils.SUPLSUP, utils.OPSUPLSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                None, None, eq[start_arg2:end_arg2], eq[end_arg2:end_arg3]]
    elif op in (utils.LSUBLSUP, utils.OPLSUBLSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None, None, eq[end_arg2:end_arg3]]
    elif op in (utils.LSUBSUP, utils.OPLSUBSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None, eq[end_arg2:end_arg3], None]
    elif op in (utils.SUBLSUP, utils.OPSUBLSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2], None, eq[end_arg2:end_arg3]]
    elif op in (utils.LSUBSUBSUP, utils.OPLSUBSUBSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        end_arg4 = nextblockindex(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3],
                eq[end_arg3:end_arg4], None]
    elif op in (utils.LSUBSUBLSUP, utils.OPLSUBSUBLSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        end_arg4 = nextblockindex(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3],
                None, eq[end_arg3:end_arg4]]
    elif op in (utils.LSUBSUPLSUP, utils.OPLSUBSUPLSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        end_arg4 = nextblockindex(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None,
                eq[end_arg2:end_arg3], eq[end_arg3:end_arg4]]
    elif op in (utils.SUBSUPLSUP, utils.OPSUBSUPLSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        end_arg4 = nextblockindex(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2],
                eq[end_arg2:end_arg3], eq[end_arg3:end_arg4]]
    elif op in (utils.LSUBSUBSUPLSUP, utils.OPLSUBSUBSUPLSUP):
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        end_arg4 = nextblockindex(eq, end_arg3)
        end_arg5 = nextblockindex(eq, end_arg4)
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
    associated index operator.
    The 3rd element indicates which argument of the index operator is being
    pointed by sel_index, or 0 if it is the base.
    """
    g = ((index, op) for index, op in enumerate(eq) if hasattr(op, 'type_')
         and op.type_ in ('opindex', 'index'))
    for op_index, op in g:
        arg_i_index = op_index + 1
        if arg_i_index == sel_index:
            return False, op_index, 0
        for arg_i in range(1, op.n_args):
            arg_i_index = nextblockindex(eq, arg_i_index)
            if arg_i_index == sel_index:
                return True, op_index, arg_i
    else:
        return False, None, None
