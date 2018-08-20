from collections import namedtuple

nt = namedtuple

Frac = nt('Frac', 'num den')
Pow = nt('Pow', 'base exp')
Pi = nt('Pi', '')
Vec = nt('Vec', 'c')
Parenthesis = nt('Parenthesis', 'c') 

d = {
    Frac: r'\frac{%s}{%s}',
    Pow: r'{%s}^{%s}',
    Pi: r'\pi ',
    Vec: r'\vec{%s}',
    Parenthesis: r'\left(%s\right)',
}
