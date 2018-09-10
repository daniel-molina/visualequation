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
import symbols

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
        if isinstance(eq[index], symbols.Op):
            # I have to find n_arg independent blocks for this operator
            index_of_arg = index+1
            latex_args = ()
            for _ in range(eq[index].n_args):
                latex_arg, index_of_arg = block2latex(index_of_arg)
                latex_args += (latex_arg,)
            return (eq[index](*latex_args), index_of_arg)
        elif isinstance(eq[index], basestring):
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
        if isinstance(eq[index], symbols.Op):
            # I have to find n_arg independent blocks for this operator
            index_of_arg = index+1
            for _ in range(eq[index].n_args):
                index_of_arg = block2nextindex(index_of_arg)
            return index_of_arg
        elif isinstance(eq[index], basestring):
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

def sel_eq(eq, index):
    """ Given an equation and a selection index, it returns a new equation
    with the selection being boxed.
    """
    sel = list(eq)
    sel.insert(index, symbols.EDIT)
    return sel

def appendbyJUXT(eq, start_index, eqblock):
    """
    Append eqblock after the block which starts at start_index by using Juxt.
    Returns the begining index of inserted eqbox.
    """
    end_index = nextblockindex(eq, start_index)
    eq[start_index:end_index] = [symbols.JUXT] + eq[start_index:end_index] \
                                + eqblock
    return end_index+1

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
            Juxt_index = eq.index(symbols.JUXT, start_index)
            arg2index = nextblockindex(eq, Juxt_index+1)
            if Juxt_index + 1 == check_index:
                return True, Juxt_index, arg2index
            elif arg2index == check_index:
                return True, Juxt_index, Juxt_index + 1
            else:
                start_index = Juxt_index + 1
    except ValueError:
        return False, None, None
