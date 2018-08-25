class BinaryOperator:
    def __init__(self, latex_code):
        self.latex_code = latex_code

    def __call__(self, s1, s2):
        return self.latex_code % (s1, s2)

class UnaryOperator:
    def __init__(self, latex_code):
        self.latex_code = latex_code

    def __call__(self, s1):
        return self.latex_code % (s1,)

class Symbol:
    def __init__(self, latex_code):
        self.latex_code = latex_code

    def __call__(self):
        return self.latex_code

Frac = BinaryOperator(r'\frac{%s}{%s}')
Pow = BinaryOperator(r'{%s}^{%s}')
Prod = BinaryOperator(r'%s %s')

Parenthesis = UnaryOperator(r'\left(%s\right)')
Vec = UnaryOperator(r'\vec{%s}')
Edit = UnaryOperator(r'\boxed{%s}')

Pi = Symbol(r'\pi ')
Bullet = Symbol(r'\bullet ')
Cdot = Symbol(r'\cdot ')
Square = Symbol(r'\square ')

# Use these operators in the code, so it will be easy to change their value
# in next releases
SelArg = Cdot
NewArg = Square
