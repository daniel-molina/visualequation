from operators import *

#def eq2latex(eq):
#    if isinstance(eq, list):
#        if eq == []:
#            return r''
#        # At least list eq has one element
#        else:
#            return eq2latex(eq[0]) + eq2latex(eq[1:])
#    elif isinstance(eq, tuple):
#        return d[type(eq)] % tuple(eq2latex(e) for e in eq)
#    elif isinstance(eq, str):
#        return eq
#    else:
#        raise ValueError('Error while converting the equation to LaTeX:%s'
#                         % eq)

def eq2latex_code(eq):
    """Returns latex code of the block and
    1 + index of the last item in eq used"""
    def block2latex(index):
        if isinstance(eq[index], BinaryOperator):
            # I have to find 2 independent blocks for this operator
            latex1, index1 = block2latex(index+1)
            latex2, index2 = block2latex(index1)
            return (eq[index](latex1, latex2), index2)
        elif isinstance(eq[index], UnaryOperator):
            # I have to find 1 independent block for this operator
            latex1, index1 = block2latex(index+1)
            return (eq[index](latex1), index1)
        elif isinstance(eq[index], Symbol):
            return (eq[index](), index+1)
        elif isinstance(eq[index], str):
            return (eq[index], index+1)
        else:
            raise ValueError('Unknown element in equation %s', eq)

    index = 0
    latex = ''
    while index < len(eq):
        string, index = block2latex(index)
        latex += string

    return latex

def eq2sels_code(eq):
    """Given an equation, it returns a list with all possibles boxed
    selections.
    """
    def eq2sel(index):
        sel = list(eq)
        sel.insert(index, Edit)
        return sel

    return (eq2sel(index) for index, _ in enumerate(eq))
    
