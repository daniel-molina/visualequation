import ops

def eqblock2latex(eq, index):
    """ Return latex code of the equation block starting at the given index
    and 1 + the index of the last element of the block in eq.
    A block is symbol or str, a unary operator with its first argument or
    a binary operator and their two arguments.
    Our equations should be a single block (with sub-blocks),
    usings as many Prod's at the begining as necessary.        
    """
    def block2latex(index):
        if isinstance(eq[index], ops.Op):
            # I have to find n_arg independent blocks for this operator
            index_of_arg = index+1
            latex_args = ()
            for _ in range (eq[index].n_args):
                latex_arg, index_of_arg = block2latex(index_of_arg)
                latex_args += (latex_arg,)
            return (eq[index](*latex_args), index_of_arg)
        elif isinstance(eq[index], str):
            return (eq[index], index+1)
        else:
            raise ValueError('Unknown equation element %s', eq[index])

    return block2latex(index)


def eq2latex_code(eq):
    """ Returns latex code of the equation.
    """

    index = 0
    latex = ''
    while index < len(eq):
        string, index = eqblock2latex(eq, index)
        latex += string

    return latex

def eq2sel(eq, index):
    """ Given an equation and a selection index, it returns the latex code
    of the equation with the selection being boxed.
    """
    sel = list(eq)
    sel.insert(index, ops.Edit)
    return sel

def eq2sels_code(eq):
    """Given an equation, it returns a generator which return the latex code
    of all the possibles selections boxed.
    """
    return (eq2sel(eq, index) for index in range(len(eq)))

#def replace_block(eq, index_start, sub_eq):
#    _, index_end = eqblock2latex(eq, index_start)
#    eq[index_start:index_end] = sub_eq

def replace_by_str(eq, index, symb):
    """" Overwrite equation, inserting symbol in the place of the block
    of equation that starts in the given index.
    """
    _, index_end = eqblock2latex(eq, index)
    eq[index:index_end] = [symb]

def insert_unary_operator(eq, index, uop):
    """ Overwrite the equation, putting the unary operator in the place of
    the block pointed by the index and leaving the block as the argument of the    operator """
    eq.insert(index, uop)

def insert_multiple_operator(eq, index_start, op, arg):
    """ Overwrite the equation, putting the multiple operator in the block
    indicated by the given index. The block is left as the first argument of
    the operator and the given arg is used as second argument.
    arg2 is supplied as a str, not as a eq (a list)."""
    _, index_end_arg1 = eqblock2latex(eq, index_start)
    eq[index_start:index_end_arg1] = [op] + eq[index_start:index_end_arg1] \
                                     + [arg] * (op.n_args-1)
    return index_end_arg1+1

def is_arg_of_Juxt(eq, check_index):
    """
    Returns a tuple of three elements:
    The first element says whether check_index is an argument of a Juxt op.
    If it is, the 2nd element indicates the pos of that Juxt and the 3rd one
    the position of the other arg of Juxt.
    """
    start_index = 0
    try:
        while True:
            Juxt_index = eq.index(ops.Juxt, start_index)
            _, arg2index = eqblock2latex(eq, Juxt_index+1)
            if Juxt_index + 1 == check_index:
                return True, Juxt_index, arg2index
            elif arg2index == check_index:
                return True, Juxt_index, Juxt_index + 1
            else:
                start_index = Juxt_index + 1
    except ValueError:
        return False, None, None
