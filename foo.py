#!/usr/bin/env python2
import unittest

from operators import *

# Equations are defined by a object or list of objects
#  eq = [Frac(['2', Pi()], 'x'), Pow('y','2')]
# such as strings, operators, and lists
#
def eq2latex(eq):
    if isinstance(eq, list):
        if eq == []:
            return r''
        # At least list eq has one element
        else:
            return eq2latex(eq[0]) + eq2latex(eq[1:])
    elif isinstance(eq, tuple):
        return d[type(eq)] % tuple(eq2latex(e) for e in eq)
    elif isinstance(eq, basestring):
        return eq
    else:
        raise ValueError('Error while converting the equation to LaTeX.')

class MyTest(unittest.TestCase):
        
    test_cases = (
        ('', r''),
        (' ', r' '),
        ('x', r'x'),
        ([], r''),
        (['x'], r'x'),
        ([Pi()], r'\pi '),
        ([Pow('y','2')], r'{y}^{2}'),
        ([Pow(Pi(),'2')], r'{\pi }^{2}'),
        ([Pow([Pi()],'2')], r'{\pi }^{2}'),
        ([Pow(Parenthesis(['4', Pi()]),'2')], r'{\left(4\pi \right)}^{2}'),
        ([Vec('i')], r'\vec{i}'),
        (['2', Pi()], r'2\pi '),
        (['2', Pi(), 'r'], r'2\pi r'),
        (['4', 'x', 'y', 'z', 't'], r'4xyzt'),
        ([Frac(['2', Pi()], 'x'), Pow('y','2')], r'\frac{2\pi }{x}{y}^{2}'),
    )

    def test_eq2latex(self):
        """ eq2latex should give known result with known output"""
        for eq,latex in self.test_cases:
            l = eq2latex(eq)
            self.assertEqual(l, latex)

unittest.main()
