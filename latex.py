import operators

def eqblock2latex(eq, index):
    def block2latex(index):
        """ Return latex code of the equation block starting at the given index
        and 1 + the index of the last element of the block in eq.
        A block is symbol or str, a unary operator with its first argument or
        a binary operator and their two arguments.
        Our equations should be a single block (with sub-blocks),
        usings as many Prod's at the begining as necessary.
        
        """
        if isinstance(eq[index], operators.BinaryOperator):
            # I have to find 2 independent blocks for this operator
            latex1, index1 = block2latex(index+1)
            latex2, index2 = block2latex(index1)
            return (eq[index](latex1, latex2), index2)
        elif isinstance(eq[index], operators.UnaryOperator):
            # I have to find 1 independent block for this operator
            latex1, index1 = block2latex(index+1)
            return (eq[index](latex1), index1)
        elif isinstance(eq[index], operators.Symbol):
            return (eq[index](), index+1)
        elif isinstance(eq[index], str):
            return (eq[index], index+1)
        else:
            raise ValueError('Unknown element in equation %s', eq)

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
    """ Given an equation an a selection index, it returns the latex code
    of the equation with the selection being boxed.
    """
    sel = list(eq)
    sel.insert(index, operators.Edit)
    return sel

def eq2sels_code(eq):
    """Given an equation, it returns a generator which return the latex code of all the possibles selections boxed.
    """
    return (eq2sel(eq, index) for index in range(len(eq)))

#def replace_block(eq, index_start, sub_eq):
#    _, index_end = eqblock2latex(eq, index_start)
#    eq[index_start:index_end] = sub_eq

def replace_by_symbol_or_str(eq, index, symb):
    """" Overwrite equation, inserting symbol in the place of the block
    of equation that starts in the given index.
    """
    _, index_end = eqblock2latex(eq, index)
    eq[index:index_end] = [symb]

def insert_unary_operator(eq, index, uop):
    """ Overwrite the equation, putting the unary operator in the place of
    the block pointed by the index and leaving the block as the argument of the    operator """
    eq.insert(index, uop)

def insert_binary_operator(eq, index_start, bop, arg2):
    """ Overwrite the equation, putting the binary operator in the block
    indicated by the given index. The block is left as the first argument of
    the operator and the given arg2 is used as second argument.
    arg2 is supplied as a symbol or str, not as a eq (a list)."""
    _, index_end_arg1 = eqblock2latex(eq, index_start)
    eq[index_start:index_end_arg1] = [bop] + eq[index_start:index_end_arg1] \
                                     + [arg2]
    return index_end_arg1+1

    
