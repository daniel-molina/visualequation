import Tkinter
"""
A module that contains the list of operators used in the menu.
"""
from collections import namedtuple

class Op(object):
    """ Class for LaTeX operator (which has arguments)"""
    def __init__(self, n_args, latex_code):
        self.n_args = n_args
        self.latex_code = latex_code

    def __call__(self, *args):
        return self.latex_code.format(*args)

Ops = namedtuple('Ops', 'menuitem ops_l clickable_size dpi')

LOWER_LATIN = [
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
    ('d', 'd'),
    ('e', 'e'),
    ('f', 'f'),
    ('g', 'g'),
    ('h', 'h'),
    ('i', 'i'),
    ('j', 'j'),
    ('k', 'k'),
    ('l', 'l'),
    ('m', 'm'),
    ('n', 'n'),
    ('o', 'o'),
    ('p', 'p'),
    ('q', 'q'),
    ('r', 'r'),
    ('s', 's'),
    ('t', 't'),
    ('u', 'u'),
    ('v', 'v'),
    ('w', 'w'),
    ('x', 'x'),
    ('y', 'y'),
    ('z', 'z'),
]

UPPER_LATIN = [
    ('uppera', 'A'),
    ('upperb', 'B'),
    ('upperc', 'C'),
    ('upperd', 'D'),
    ('uppere', 'E'),
    ('upperf', 'F'),
    ('upperg', 'G'),
    ('upperh', 'H'),
    ('upperi', 'I'),
    ('upperj', 'J'),
    ('upperk', 'K'),
    ('upperl', 'L'),
    ('upperm', 'M'),
    ('uppern', 'N'),
    ('uppero', 'O'),
    ('upperp', 'P'),
    ('upperq', 'Q'),
    ('upperr', 'R'),
    ('uppers', 'S'),
    ('uppert', 'T'),
    ('upperu', 'U'),
    ('upperv', 'V'),
    ('upperw', 'W'),
    ('upperx', 'X'),
    ('uppery', 'Y'),
    ('upperz', 'Z'),
]

NUMBERS = [
    ('n0', '0'),
    ('n1', '1'),
    ('n2', '2'),
    ('n3', '3'),
    ('n4', '4'),
    ('n5', '5'),
    ('n6', '6'),
    ('n7', '7'),
    ('n8', '8'),
    ('n9', '9'),
]

COMMON_OPERATORS = [
    ('comma', (',', [r"\boxed{{\phantom{{|}},}}"])),
    ('period', ('.', [r"\boxed{{\phantom{{|}}.}}"])),
    ('sumation', '+'),
    ('negation', '-'),
    ('factorial', '!'),
    ('div', r'\div '),
    ('slash', r'/'),
    ('percent', r'\%'),
    ('times', r'\times '),
    ('equal', '=',),
    ('lparenthesis', '('),
    ('rparenthesis', ')'),
    ('lbracket', r'\{{'),
    ('rbracket', r'\}}'),
    ('lsqbracket', '['),
    ('rsqbracket', ']'),
]

MENUITEM_KEYBOARD = Ops(
    ops_l=LOWER_LATIN+UPPER_LATIN+NUMBERS+COMMON_OPERATORS,
    clickable_size=(30, 35), dpi=200, menuitem=[r'a\, 9'])

#Text = UnaryOperator(r'\text{%s}')

LOWER_GREEK = [
    ('alpha', r'\alpha '),
    ('beta', r'\beta '),
    ('gamma', r'\gamma '),
    ('digamma', r'\digamma '),
    ('delta', r'\delta '),
    ('epsilon', r'\epsilon '),
    ('zeta', r'\zeta '),
    ('eta', r'\eta '),
    ('theta', r'\theta '),
    ('iota', r'\iota '),
    ('kappa', r'\kappa '),
    ('lambda', r'\lambda '),
    ('mu', r'\mu '),
    ('nu', r'\nu '),
    ('xi', r'\xi '),
    ('pi', r'\pi '),
    ('rho', r'\rho '),
    ('sigma', r'\sigma '),
    ('tau', r'\tau '),
    ('upsilon', r'\upsilon '),
    ('phi', r'\phi '),
    ('chi', r'\chi '),
    ('psi', r'\psi '),
    ('omega', r'\omega '),
]

UPPER_GREEK = [
    ('uppergamma', r'\Gamma '),
    ('upperdelta', r'\Delta '),
    ('uppertheta', r'\Theta '),
    ('upperlambda', r'\Lambda '),
    ('upperxi', r'\Xi '),
    ('upperpi', r'\Pi '),
    ('uppersigma', r'\Sigma '),
    ('upperupsilon', r'\Upsilon '),
    ('upperphi', r'\Phi '),
    ('upperpsi', r'\Psi '),
    ('upperomega', r'\Omega '),
]

VAR_GREEK = [
    ('varepsilon', r'\varepsilon '),
    ('vartheta', r'\vartheta '),
    ('varkappa', r'\varkappa '),
    ('varrho', r'\varrho '),
    ('varsigma', r'\varsigma '),
    ('varphi', r'\varphi '),
    ('varpi', r'\varpi '),
]

HEBREW = [
    ('aleph', r'\aleph '),
    ('beth', r'\beth '),
    ('daleth', r'\daleth '),
    ('gimel', r'\gimel '),
]

SYMBOLS1 = [
    ('infty', r'\infty '),
    ('nabla', r'\nabla '),
    ('partial', r'\partial '),
    ('times', r'\times '),
    ('cdot', r'\cdot '),
    ('div', r'\div '),
]

MENUITEM_GREEK_HEBREW_SYMBOLS1 = Ops(
    ops_l=LOWER_GREEK + UPPER_GREEK + VAR_GREEK + HEBREW + SYMBOLS1,
    clickable_size=(30, 30), dpi=200,
    menuitem=[r'\alpha\, \infty'])

ACCENTS = [
    ('acute', (Op(1, r'\acute{{{0}}}'), [r'\acute{{{\cdot}}}'])),
    ('breve', (Op(1, r'\breve{{{0}}}'), [r'\breve{{{\cdot}}}'])),
    ('ddot', (Op(1, r'\ddot{{{0}}}'), [r'\ddot{{{\cdot}}}'])),
    ('grave', (Op(1, r'\grave{{{0}}}'), [r'\grave{{{\cdot}}}'])),
    ('tilde', (Op(1, r'\tilde{{{0}}}'), [r'\tilde{{{\cdot}}}'])),
    ('bar', (Op(1, r'\bar{{{0}}}'), [r'\bar{{{\cdot}}}'])),
    ('check', (Op(1, r'\check{{{0}}}'), [r'\check{{{\cdot}}}'])),
    ('dot', (Op(1, r'\dot{{{0}}}'), [r'\dot{{{\cdot}}}'])),
    ('hat', (Op(1, r'\hat{{{0}}}'), [r'\hat{{{\cdot}}}'])),
    ('vec', (Op(1, r'\vec{{{0}}}'), [r'\vec{{{\cdot}}}'])),
    ('imath', r'\imath '),
    ('jmath', r'\jmath '),
    ('ell', r'\ell '),
    ('hbar', r'\hbar '),
    ('eth', r'\eth '),
    ('wp', r'\wp '),
]

MENUITEM_ACCENTS = Ops(
    ops_l=ACCENTS,
    clickable_size=(50, 50), dpi=300,
    menuitem=[r'\acute{{a}}\;\tilde{{B}}'])

INDICES = [
    ('super', (Op(2, r'{0}^{{{1}}}'), [r'\cdot^{{\square}}'])),
    ('sub', (Op(2, r'{0}_{{{1}}}'), [r'\cdot_{{\square}}'])),
    ('lsuper', (Op(2, r'{{}}^{{{1}}}{0}'), [r'{{}}^{{\square}}\cdot'])),
    ('lsub', (Op(2, r'{{}}_{{{1}}}{0}'), [r'{{}}_{{\square}}\cdot'])),
    ('supersub', (Op(3, r'{0}^{{{1}}}_{{{2}}}'),
                  [r'\cdot^{{\square}}_{{\square}}'])),
    ('lsuperlsub', (Op(3, r'{{}}^{{{2}}}_{{{1}}}{0}'),
                    [r'{{}}^{{\square}}_{{\square}}\cdot'])),
    ('superlsuper', (Op(3, r'{{}}^{{{1}}}{0}^{{{2}}}'),
                     [r'{{}}^{{\square}}\cdot^{{\square}}'])),
    ('sublsub', (Op(3, r'{{}}_{{{1}}}{0}_{{{2}}}'),
                     [r'{{}}_{{\square}}\cdot_{{\square}}'])),
    ('supersublsuper', (Op(4, r'{{}}^{{{1}}}{0}^{{{3}}}_{{{2}}}'),
                  [r'{{}}^{{\square}}\cdot^{{\square}}_{{\square}}'])),
    ('supersublsub', (Op(4, r'{{}}_{{{1}}}{0}^{{{3}}}_{{{2}}}'),
                  [r'{{}}_{{\square}}\cdot^{{\square}}_{{\square}}'])),
    ('sublsublsuper', (Op(4, r'{{}}_{{{1}}}^{{{2}}}{0}_{{{3}}}'),
                  [r'{{}}_{{\square}}^{{\square}}\cdot_{{\square}}'])),
    ('superlsuperlsub', (Op(4, r'{{}}^{{{1}}}_{{{2}}}{0}^{{{3}}}'),
                  [r'{{}}^{{\square}}_{{\square}}\cdot^{{\square}}'])),
    ('supersublsuperlsub',
     (Op(5, r'{{}}^{{{2}}}_{{{1}}}{0}^{{{4}}}_{{{3}}}'),
      [r'{{}}^{{\square}}_{{\square}}\cdot^{{\square}}_{{\square}}'])),
]

#    ('binomial', (Op(2, r'\binom{{{0}}}{{{1}}}'),
#     [r'\binom{{\cdot}}{{\square}}'])),

MENUITEM_INDICES = Ops(
    ops_l=INDICES,
    clickable_size=(60, 70), dpi=200,
    menuitem=[r'a^b'])

MATHCONSTRUCTS = [
    ('frac', Op(2, r'\frac{{{0}}}{{{1}}}')),
    ('prime', (r"'", [r"\boxed{{\phantom{{|}}'}}"])),
    ('sqrt', Op(1, r'\sqrt{{{0}}}')),
    ('nsqrt', Op(2, r'\sqrt[{1}]{{{0}}}')),
    ('overline', Op(1, r'\overline{{{0}}}')),
    ('underline', Op(1, r'\underline{{{0}}}')),
    ('widehat', Op(1, r'\widehat{{{0}}}')),
    ('widetilde', Op(1, r'\widetilde{{{0}}}')),
    ('overrightarrow', Op(1, r'\overrightarrow{{{0}}}')),
    ('overleftarrow', Op(1, r'\overleftarrow{{{0}}}')),
    ('overbrace1', Op(1, r'\overbrace{{{0}}}')),
    ('underbrace1', Op(1, r'\underbrace{{{0}}}')),
    ('overbrace2', Op(2, r'\overbrace{{{0}}}^{{{1}}}')),
    ('underbrace2', Op(2, r'\underbrace{{{0}}}_{{{1}}}')),
]

MENUITEM_MATHCONSTRUCTS = Ops(
    ops_l=MATHCONSTRUCTS,
    clickable_size=(55, 70), dpi=200,
    menuitem=[r'\underbrace{{abc}}'])

DELIMITERS = [
    ('parenthesisb', Op(1, r'\left({0}\right)')),
    ('vertb', Op(1, r'\left|{0}\right|')),
    ('uppervertb', Op(1, r'\left\|{0}\right\|')),
    ('bracketsb', Op(1, r'\left\{{{0}\right\}}')),
    ('angleb', Op(1, r'\left\langle{0}\right\rangle')),
    ('floorb', Op(1, r'\left\lfloor{0}\right\rfloor')),
    ('ceilb', Op(1, r'\left\lceil{0}\right\rceil')),
    ('slashb', Op(1, r'\left/{0}\right\backslash')),
    ('sqbracketsb', Op(1, r'\left[{0}\right]')),
    ('lcornerb', Op(1, r'\left\llcorner{0}\right\lrcorner')),
    ('ucornerb', Op(1, r'\left\ulcorner{0}\right\urcorner')),
]

MENUITEM_DELIMITERS = Ops(
    ops_l=DELIMITERS,
    clickable_size=(70, 50), dpi=200,
    menuitem=[r'\left(ab\right)'])

FUNCTIONS = [
    ('arccos', r'\arccos '),
    ('arcsin', r'\arcsin '),
    ('arctan', r'\arctan '),
    ('arg', r'\arg '),
    ('cos', r'\cos '),
    ('cosh', r'\cosh '),
    ('coth', r'\coth '),
    ('csc', r'\csc '),
    ('deg', r'\deg '),
    ('det', r'\det '),
    ('dim', r'\dim '),
    ('exp', r'\exp '),
    ('gcd', r'\gcd '),
    ('hom', r'\hom '),
    ('inf', r'\inf '),
    ('ker', r'\ker '),
    ('lg', r'\lg '),
    ('ln', r'\ln '),
    ('log', r'\log '),
    ('max', r'\max '),
    ('min', r'\min '),
    ('pr', r'\Pr '),
    ('sec', r'\sec '),
    ('sin', r'\sin '),
    ('sinh', r'\sinh '),
    ('sup', r'\sup '),
    ('tan', r'\tan '),
    ('tanh', r'\tanh '),
    ('upperre', r'\Re '),
    ('upperim', r'\Im '),
]

#lim = Symbol(r'\lim ')
#liminf = Symbol(r'\liminf ')
#limsup = Symbol(r'\limsup ')

MENUITEM_FUNCTIONS = Ops(
    ops_l=FUNCTIONS,
    clickable_size=(80, 30), dpi=200,
    menuitem=[r'f(x)'])

VARIABLESIZE = [
    ('sum', r'\sum'),
    ('prod', r'\prod'),
    ('coprod', r'\coprod'),
    ('int', r'\int'),
    ('iint', r'\iint'),
    ('iiint', r'\iiint'),
    ('oint', r'\oint'),
    ('biguplus', r'\biguplus'),
    ('bigcap', r'\bigcap'),
    ('bigcup', r'\bigcup'),
    ('bigoplus', r'\bigoplus'),
    ('bigotimes', r'\bigotimes'),
    ('bigodot', r'\bigodot'),
    ('bigvee', r'\bigvee'),
    ('bigwedge', r'\bigwedge'),
    ('bigsqcup', r'\bigsqcup'),
]

MENUITEM_VARIABLESIZE = Ops(
    ops_l=VARIABLESIZE,
    clickable_size=(50, 60), dpi=150,
    menuitem=[r'\sum'])

SOMEOPERATORS = [
    ('circ', r'\circ '),
    ('bullet', r'\bullet '),
    ('pm', r'\pm '),
    ('mp', r'\mp '),
    ('odot', r'\odot '),
    ('ominus', r'\ominus '),
    ('oplus', r'\oplus '),
    ('oslash', r'\oslash '),
    ('otimes', r'\otimes '),
    ('cap', r'\cap '),
    ('cup', r'\cup '),
    ('wedge', r'\wedge'),
    ('vee', r'\vee '),
    ('forall', r'\forall '),
    ('exists', r'\exists '),
    ('nexists', r'\nexists '),
    ('perp', r'\perp '),
    ('parallel', r'\parallel '),
    ('equiv', r'\equiv '),
    ('less', r'<'),
    ('greater', r'>'),
    ('leq', r'\leq '),
    ('geq', r'\geq '),
    ('ll', r'\ll '),
    ('gg', r'\gg '),
    ('sim', r'\sim '),
    ('cong', r'\cong '),
    ('simeq', r'\simeq '),
    ('approx', r'\approx '),
    ('asymp', r'\asymp '),
    ('doteq', r'\doteq '),
    ('propto', r'\propto '),
    ('subset', r'\subset '),
    ('supset', r'\supset '),
    ('subseteq', r'\subseteq '),
    ('supseteq', r'\supseteq '),
    ('in', r'\in '),
    ('ni', r'\ni '),
    ('notin', r'\notin '),
    ('neq', r'\neq '),
    ('neg', r'\neg '),
    ('ncong', r'\ncong '),
    ('nparallel', r'\nparallel '),
    ('notperp', r'\not\perp '),
    ('nless', r'\nless '),
    ('ngtr', r'\ngtr '),
    ('nleq', r'\nleq '),
    ('ngeq', r'\ngeq '),
    ('nsubseteq', r'\nsubseteq '),
    ('nsupseteq', r'\nsupseteq '),
    ('emptyset', r'\emptyset '),
    ('varnothing', r'\varnothing '),
]

MENUITEM_SOMEOPERATORS = Ops(
    ops_l=SOMEOPERATORS,
    clickable_size=(30, 30), dpi=200,
    menuitem=[r'\otimes \in'])

ARROWS = [
    ('leftarrow', r'\leftarrow '),
    ('longleftarrow', r'\longleftarrow '),
    ('upperleftarrow', r'\Leftarrow '),
    ('upperlongleftarrow', r'\Longleftarrow'),
    ('rightarrow', r'\rightarrow '),
    ('longrightarrow', r'\longrightarrow '),
    ('upperrightarrow', r'\Rightarrow '),
    ('upperlongrightarrow', r'\Longrightarrow '),
    ('leftrightarrow', r'\leftrightarrow '),
    ('longleftrightarrow', r'\longleftrightarrow '),
    ('upperleftrightarrow', r'\Leftrightarrow '),
    ('upperlongleftrightarrow', r'\Longleftrightarrow'),
    ('uparrow', r'\uparrow '),
    ('upperuparrow', r'\Uparrow'),
    ('downarrow', r'\downarrow '),
    ('upperdownarrow', r'\Downarrow'),
    ('mapsto', r'\mapsto '),
    ('nupperrightarrow', r'\nRightarrow '),
    ('nupperleftarrow', r'\nLeftarrow '),
    ('nupperleftrightarrow', r'\nLeftrightarrow '),
]

MENUITEM_ARROWS = Ops(
    ops_l=ARROWS,
    clickable_size=(40, 30), dpi=200,
    menuitem=[r'\rightarrow'])

# Use these operators in the code, so it will be easy to change their value
# in next releases
SELARG = r'\cdots '
NEWARG = r'\square '
EDIT = Op(1, r'\boxed{{{0}}}')
#EDIT = Op(1, r'\left.\textcolor{{blue}}{{{0}}}\right|')
JUXT = Op(2, r'{0} {1}')

def matrix():
    root = Tkinter.Tk()
    n_rows_tk = Tkinter.StringVar()
    label1 = Tkinter.Label(root, text='Number of rows').grid(row=0)
    n_columns_tk = Tkinter.StringVar()
    label2 = Tkinter.Label(root, text='Number of columns').grid(row=1)
    entry1 = Tkinter.Entry(root, textvariable=n_rows_tk)
    entry2 = Tkinter.Entry(root, textvariable=n_columns_tk)
    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)
    entry1.focus_set()
    Tkinter.Button(root, text="Accept", command=root.quit).grid(row=3,
                                                                column=1)
    # Avoid that the user does not introduce something
    def disable_event():
        pass
    root.protocol("WM_DELETE_WINDOW", disable_event)
    exit_cond = False
    while not exit_cond:
        root.mainloop()
        try:
            n_rows = int(n_rows_tk.get())
            n_columns = int(n_columns_tk.get())
            assert(n_rows>0)
            assert(n_columns>0)
            exit_cond = True
        except ValueError:
            pass
        except AssertionError:
            pass

    root.destroy()
    n_args = n_rows*n_columns
    row_code = r'{}' + r'&{}'*(n_columns-1) + r'\\'
    latex_code = r'\begin{{matrix}}' + row_code*n_rows + r'\end{{matrix}}'
    return Op(n_args, latex_code)

def text():
    root = Tkinter.Tk()
    text_tk = Tkinter.StringVar()
    label = Tkinter.Label(root, text='Text').grid(row=0)
    entry = Tkinter.Entry(root, textvariable=text_tk)
    entry.grid(row=0, column=1)
    entry.focus_set()
    Tkinter.Button(root, text="Accept", command=root.destroy).grid(row=2,
                                                                   column=1)
    # Avoid that the user does not introduce something
    def disable_event():
        pass
    root.protocol("WM_DELETE_WINDOW", disable_event)
    root.mainloop()
    return r'\text{{' + text_tk.get() + '}}'


def special_format(latex_command, label_text, only_capital=False):
    def fun():
        root = Tkinter.Tk()
        text_tk = Tkinter.StringVar()
        label = Tkinter.Label(root, text=label_text).grid(row=0)
        entry = Tkinter.Entry(root, textvariable=text_tk)
        entry.grid(row=0, column=1)
        entry.focus_set()
        Tkinter.Button(root, text="Accept",
                       command=root.quit).grid(row=2, column=1)
        # Avoid that the user does not introduce something
        def disable_event():
            pass
        root.protocol("WM_DELETE_WINDOW", disable_event)
        exit_cond = False
        while not exit_cond:
            root.mainloop()
            text = text_tk.get()
            if(only_capital):
                if text.isalpha():
                    text = text.upper()
                    exit_cond = True
            else:
                if text.isalnum():
                    exit_cond = True

        root.destroy()
        return latex_command + r'{{' + text + '}}'

    return fun
    

USERINPUT = [
    ('matrix', (matrix, 
                [r"\begin{smallmatrix}\cdots&\square&\square\\" \
                 + r"\square&\square&\square\end{smallmatrix}"])),
    ('text', (text, [r"\text{Text}"])),
    ('mathcal', (special_format(r'\mathcal', 'Caligraphic', True),
                 [r"\mathcal{ABC}"])),
    ('mathbb', (special_format(r'\mathbb', 'Mathbb', True),
                 [r"\mathbb{ABC}"])),
    ('mathfrak', (special_format(r'\mathfrak', 'Mathfrak'),
                  [r"\mathfrak{Ab1}"])),
    ('mathsf', (special_format(r'\mathst', 'Sans serif'),
                 [r"\mathsf{Ab1}"])),
    ('mathbf', (special_format(r'\mathbf', 'Mathbf'),
                 [r"\mathbf{Ab1}"])),

]

MENUITEM_USERINPUT = Ops(
    ops_l=USERINPUT,
    clickable_size=(80, 50), dpi=200,
    menuitem=[r'\begin{smallmatrix}a&b\\c&d\end{smallmatrix}'])

MENUITEMS = [
    MENUITEM_GREEK_HEBREW_SYMBOLS1,
    MENUITEM_ACCENTS,
    MENUITEM_INDICES,
    MENUITEM_MATHCONSTRUCTS,
    MENUITEM_DELIMITERS,
    MENUITEM_FUNCTIONS,
    MENUITEM_VARIABLESIZE,
    MENUITEM_SOMEOPERATORS,
    MENUITEM_ARROWS,
    MENUITEM_USERINPUT,
]
