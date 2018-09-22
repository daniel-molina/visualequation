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

def eqblock2latex(eq, index):
    """ Return latex code of the equation block starting at the given index
    and 1 + the index of the last element of the block in eq.
    A block is symbol or str, a unary operator with its first argument or
    a binary operator and their two arguments.
    Our equations should be a single block (with sub-blocks),
    usings as many Prod's at the begining as necessary.
    """
    def block2latex(index):
        """ Incredible recursive function that DOES the real job"""
        if isinstance(eq[index], utils.Op):
            # I have to find n_arg independent blocks for this operator
            index_of_arg = index+1
            latex_args = ()
            for _ in range(eq[index].n_args):
                latex_arg, index_of_arg = block2latex(index_of_arg)
                latex_args += (latex_arg,)
            return (eq[index](*latex_args), index_of_arg)
        elif isinstance(eq[index], str):
            return (eq[index], index+1)
        else:
            raise ValueError('Unknown equation element %s', eq[index])

    return block2latex(index)

def nextblockindex(eq, index):
    """
    It is a simplification of eqblock2latex that only returns the end index.
    This function was written because the previous one was called often
    just to calculate end of blocks.
    It returns the index after the end of the block,
    being a valid index or not (when it is passed an ending block of eq).
    """
    def block2nextindex(index):
        """ Simplification of the recursive nested function block2latex."""
        if isinstance(eq[index], utils.Op):
            # I have to find n_arg independent blocks for this operator
            index_of_arg = index+1
            for _ in range(eq[index].n_args):
                index_of_arg = block2nextindex(index_of_arg)
            return index_of_arg
        elif isinstance(eq[index], str):
            return index+1
        else:
            raise ValueError('Unknown equation element %s', eq[index])

    return block2nextindex(index)

def eq2latex_code(eq):
    """ Returns latex code of the equation.
    """

    index = 0
    latex = ''
    while index < len(eq):
        string, index = eqblock2latex(eq, index)
        latex += string

    return latex

def sel_eq(eq, index, right_sel):
    """ Given an equation and a selection index, it returns a new equation
    with the selection being boxed.
    """
    sel = list(eq)
    if right_sel:
        sel.insert(index, utils.REDIT)
    else:
        sel.insert(index, utils.LEDIT)
    return sel

def insertrbyJUXT(eq, start_index, eqblock):
    """
    Insert eqblock after the block which starts at start_index by using Juxt.
    Returns the index of the begining of inserted eqblock.
    """
    # If eqblock is the base of an index operator, consider the index operator
    # instead. It avoids a bit of caos in the equation structure.
    if eq[start_index-1] in utils.INDEX_OPS:
        start_index -= 1
    end_index = nextblockindex(eq, start_index)
    eq[start_index:end_index] = [utils.JUXT] + eq[start_index:end_index] \
                                + eqblock
    return end_index+1

def insertlbyJUXT(eq, start_index, eqblock):
    """
    Insert eqblock before the block which starts at start_index by using Juxt.
    Returns the index of the insert block.
    """
    # If eqblock is the base of an index operator, consider the index operator
    # instead. It avoids a bit of caos in the equation structure.
    if eq[start_index-1] in utils.INDEX_OPS:
        start_index -= 1
    end_index = nextblockindex(eq, start_index)
    eq[start_index:end_index] = [utils.JUXT] + eqblock \
                                + eq[start_index:end_index]
    return start_index+1

def replaceby(eq, start_index, eqblock):
    """
    Replace block starting at start_index by eqblock.
    Returns the index of the next element (if any) after inserted eqblock
    """
    end_index = nextblockindex(eq, start_index)
    eq[start_index:end_index] = eqblock
    return start_index + len(eqblock) + 1

def is_arg_of_JUXT(eq, check_index):
    """
    Returns a tuple of three elements:
    The first element says whether check_index is an argument of a Juxt op.
    If it is, the 2nd element indicates the pos of that Juxt and the 3rd one
    the position of the other arg of Juxt.
    """
    start_index = 0
    try:
        while True:
            Juxt_index = eq.index(utils.JUXT, start_index)
            arg2index = nextblockindex(eq, Juxt_index+1)
            if Juxt_index + 1 == check_index:
                return True, Juxt_index, arg2index
            elif arg2index == check_index:
                return True, Juxt_index, Juxt_index + 1
            else:
                start_index = Juxt_index + 1
    except ValueError:
        return False, None, None

def is_intermediate_JUXT(eq, index):
    """
    Check whether if index points to a JUXT that is the argument of
    other JUXT.
    """
    if eq[index] == utils.JUXT:
        cond, _, _ = is_arg_of_JUXT(eq, index)
        if cond:
            return True
    return False


def indexop2arglist(eq, sel_index):
    """
    Convert the block of indices pointed by sel_index to a list of arguments.
    The list has the format [base, lsub_arg, sub_arg, sup_arg, lsup_arg].
    The arguments not available will be replaced by None.
    If sel_index does not point to an operator index at all, base will be the
    pointed block and the rest will be set to None.
    """
    op = eq[sel_index] # it can be index operator but not necessarily (!)
    if op not in utils.INDEX_OPS:
        end_block = nextblockindex(eq, sel_index)    
        return [eq[sel_index:end_block], None, None, None, None]
    start_arg1 = sel_index + 1
    start_arg2 = nextblockindex(eq, start_arg1)
    if op == utils.LSUB:
        end_arg2 = nextblockindex(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None, None, None]
    elif op == utils.SUB:
        end_arg2 = nextblockindex(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2], None, None]
    elif op == utils.SUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                None, None, eq[start_arg2:end_arg2], None]
    elif op == utils.LSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        return [eq[start_arg1:start_arg2],
                None, None, None, eq[start_arg2:end_arg2]]
    elif op == utils.LSUBSUB:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3], None, None]
    elif op == utils.SUBSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2], eq[end_arg2:end_arg3], None]
    elif op == utils.SUPLSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                None, None, eq[start_arg2:end_arg2], eq[end_arg2:end_arg3]]
    elif op == utils.LSUBLSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None, None, eq[end_arg2:end_arg3]]
    elif op == utils.LSUBSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None, eq[end_arg2:end_arg3], None]
    elif op == utils.SUBLSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2], None, eq[end_arg2:end_arg3]]
    elif op == utils.LSUBSUBSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        end_arg4 = nextblockindex(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3],
                eq[end_arg3:end_arg4], None]
    elif op == utils.LSUBSUBLSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        end_arg4 = nextblockindex(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3],
                None, eq[end_arg3:end_arg4]]
    elif op == utils.LSUBSUPLSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        end_arg4 = nextblockindex(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], None,
                eq[end_arg2:end_arg3], eq[end_arg3:end_arg4]]
    elif op == utils.SUBSUPLSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        end_arg4 = nextblockindex(eq, end_arg3)
        return [eq[start_arg1:start_arg2],
                None, eq[start_arg2:end_arg2],
                eq[end_arg2:end_arg3], eq[end_arg3:end_arg4]]
    elif op == utils.LSUBSUBSUPLSUP:
        end_arg2 = nextblockindex(eq, start_arg2)
        end_arg3 = nextblockindex(eq, end_arg2)
        end_arg4 = nextblockindex(eq, end_arg3)
        end_arg5 = nextblockindex(eq, end_arg4)
        return [eq[start_arg1:start_arg2],
                eq[start_arg2:end_arg2], eq[end_arg2:end_arg3],
                eq[end_arg3:end_arg4], eq[end_arg4:end_arg5]]

def flat_arglist(args):
    # Flat the list of args
    new_args = []
    for arg in args:
        if arg != None:
            for symb in arg:
                new_args.append(symb)
    return new_args

def arglist2indexop(args):
    indexops_dict = {
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
    try:
        return indexops_dict[tuple(bool(arg) for arg in args)]
    except KeyError:
        raise SystemExit('Internal error:'
                         + ' Bad argument list of index operator.')

def is_script(eq, sel_index):
    """
    Returns a tuple of three elements:
    The first element says whether element pointed by sel_index is a script.
    If it is or if it is the base, the 2nd element indicates the pos of the
    associated index operator.
    The 3rd element indicates which argument of the index operator is being
    pointed by sel_index, or 0 if it is the base.
    """
    for op in utils.INDEX_OPS:
        try:
            start_index = 0
            while True:
                op_index = eq.index(op, start_index)
                # Check if some of the args is pointed by sel_index
                arg_i_index = op_index + 1
                if arg_i_index == sel_index:
                    return False, op_index, 0
                for arg_i in range(1, op.n_args):
                    arg_i_index = nextblockindex(eq, arg_i_index)
                    if arg_i_index == sel_index:
                        return True, op_index, arg_i
                # Next operator can be inside the args, do not skip them
                start_index = op_index + 1
        except ValueError:
            continue
    return False, None, None
