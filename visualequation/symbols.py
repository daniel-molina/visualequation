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
A module that contains the list of operators used in the menu.
"""
import os
from collections import namedtuple

import Tkinter

import dirs

class Op(object):
    """ Class for LaTeX operator (that has arguments)"""
    def __init__(self, n_args, latex_code):
        self.n_args = n_args
        self.latex_code = latex_code

    def __call__(self, *args):
        return self.latex_code.format(*args)

    def __eq__(self, other):
        if type(self) is type(other):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other 

    def __repr__(self):
        return "Op(" + repr(self.n_args) + ", " + repr(self.latex_code) + ")"

LatexSymb = namedtuple('LatexSymb', 'tag code expr')
MenuItemData = namedtuple('MenuItem', 'symb_l clickable_size dpi expr')

# Use these operators in the code, so it will be easy to change their value
# in next releases
SELARG = r'\cdots'
NEWARG = r'\square'
EDIT = Op(1, r'\boxed{{{0}}}')
#EDIT = Op(1, r'\left.\textcolor{{blue}}{{{0}}}\right|')
JUXT = Op(2, r'{0} {1}')
SUPERINDEX = Op(2, r'{0}^{{{1}}}')
SUBINDEX = Op(2, r'{0}_{{{1}}}')

MENUITEMSDATA = []
ADDITIONAL_LS = []

LOWER_GREEK = [
    LatexSymb('alpha', r'\alpha', r'\alpha'),
    LatexSymb('beta', r'\beta', r'\beta'),
    LatexSymb('gamma', r'\gamma', r'\gamma'),
    LatexSymb('digamma', r'\digamma', r'\digamma'),
    LatexSymb('delta', r'\delta', r'\delta'),
    LatexSymb('epsilon', r'\epsilon', r'\epsilon'),
    LatexSymb('zeta', r'\zeta', r'\zeta'),
    LatexSymb('eta', r'\eta', r'\eta'),
    LatexSymb('theta', r'\theta', r'\theta'),
    LatexSymb('iota', r'\iota', r'\iota'),
    LatexSymb('kappa', r'\kappa', r'\kappa'),
    LatexSymb('lambda', r'\lambda', r'\lambda'),
    LatexSymb('mu', r'\mu', r'\mu'),
    LatexSymb('nu', r'\nu', r'\nu'),
    LatexSymb('xi', r'\xi', r'\xi'),
    LatexSymb('pi', r'\pi', r'\pi'),
    LatexSymb('rho', r'\rho', r'\rho'),
    LatexSymb('sigma', r'\sigma', r'\sigma'),
    LatexSymb('tau', r'\tau', r'\tau'),
    LatexSymb('upsilon', r'\upsilon', r'\upsilon'),
    LatexSymb('phi', r'\phi', r'\phi'),
    LatexSymb('chi', r'\chi', r'\chi'),
    LatexSymb('psi', r'\psi', r'\psi'),
    LatexSymb('omega', r'\omega', r'\omega'),
]

UPPER_GREEK = [
    LatexSymb('uppergamma', r'\Gamma', r'\Gamma'),
    LatexSymb('upperdelta', r'\Delta', r'\Delta'),
    LatexSymb('uppertheta', r'\Theta', r'\Theta'),
    LatexSymb('upperlambda', r'\Lambda', r'\Lambda'),
    LatexSymb('upperxi', r'\Xi', r'\Xi'),
    LatexSymb('upperpi', r'\Pi', r'\Pi'),
    LatexSymb('uppersigma', r'\Sigma', r'\Sigma'),
    LatexSymb('upperupsilon', r'\Upsilon', r'\Upsilon'),
    LatexSymb('upperphi', r'\Phi', r'\Phi'),
    LatexSymb('upperpsi', r'\Psi', r'\Psi'),
    LatexSymb('upperomega', r'\Omega', r'\Omega'),
]

VAR_GREEK = [
    LatexSymb('varepsilon', r'\varepsilon', r'\varepsilon'),
    LatexSymb('vartheta', r'\vartheta', r'\vartheta'),
    LatexSymb('varkappa', r'\varkappa', r'\varkappa'),
    LatexSymb('varrho', r'\varrho', r'\varrho'),
    LatexSymb('varsigma', r'\varsigma', r'\varsigma'),
    LatexSymb('varphi', r'\varphi', r'\varphi'),
    LatexSymb('varpi', r'\varpi', r'\varpi'),
]

HEBREW = [
    LatexSymb('aleph', r'\aleph', r'\aleph'),
    LatexSymb('beth', r'\beth', r'\beth'),
    LatexSymb('daleth', r'\daleth', r'\daleth'),
    LatexSymb('gimel', r'\gimel', r'\gimel'),
]

SYMBOLS1 = [
    LatexSymb('infty', r'\infty', r'\infty'),
    LatexSymb('nabla', r'\nabla', r'\nabla'),
    LatexSymb('partial', r'\partial', r'\partial'),
    LatexSymb('times', r'\times', r'\times'),
    LatexSymb('cdot', r'\cdot', r'\cdot'),
    LatexSymb('div', r'\div', r'\div'),
]

MENUITEMSDATA.append(MenuItemData(
    symb_l=LOWER_GREEK + UPPER_GREEK + VAR_GREEK + HEBREW + SYMBOLS1,
    clickable_size=(30, 30), dpi=200,
    expr=r'\alpha\, \infty'))

MATHCONSTRUCTS = [
    LatexSymb('frac', Op(2, r'\frac{{{0}}}{{{1}}}'),
              r'\frac{\cdots}{\square}'),
    LatexSymb('sqrt', Op(1, r'\sqrt{{{0}}}'), r'\sqrt{\cdots}'),
    LatexSymb('nsqrt', Op(2, r'\sqrt[{1}]{{{0}}}'), r'\sqrt[\square]{\cdots}'),
    LatexSymb('overline', Op(1, r'\overline{{{0}}}'), r'\overline\cdots'),
    LatexSymb('underline', Op(1, r'\underline{{{0}}}'), r'\underline\cdots'),
    LatexSymb('widehat', Op(1, r'\widehat{{{0}}}'), r'\widehat\cdots'),
    LatexSymb('widetilde', Op(1, r'\widetilde{{{0}}}'), r'\widetilde\cdots'),
    LatexSymb('overrightarrow', Op(1, r'\overrightarrow{{{0}}}'),
              r'\overrightarrow\cdots'),
    LatexSymb('overleftarrow', Op(1, r'\overleftarrow{{{0}}}'),
              r'\overleftarrow\cdots'),
    LatexSymb('overbrace1', Op(1, r'\overbrace{{{0}}}'), r'\overbrace\cdots'),
    LatexSymb('underbrace1', Op(1, r'\underbrace{{{0}}}'),
              r'\underbrace\cdots'),
    LatexSymb('overbrace2', Op(2, r'\overbrace{{{0}}}^{{{1}}}'),
              r'\overbrace{\cdots}^\square'),
    LatexSymb('underbrace2', Op(2, r'\underbrace{{{0}}}_{{{1}}}'),
              r'\underbrace{\cdots}_\square'),
]

MENUITEMSDATA.append(MenuItemData(
    symb_l=MATHCONSTRUCTS,
    clickable_size=(55, 70), dpi=200,
    expr=r'\underbrace{{abc}}'))

SINGLEDELIMITERS = [
    LatexSymb('lparenthesis', '(', '('),
    LatexSymb('rparenthesis', ')', ')'),
    LatexSymb('vert', '|', '|'),
    LatexSymb('uppervert', r'\|', r'\|'),
    LatexSymb('lbracket', r'\{', r'\{'),
    LatexSymb('rbracket', r'\}', r'\}'),
    LatexSymb('langle', r'\langle', r'\langle'),
    LatexSymb('rangle', r'\rangle', r'\rangle'),
    LatexSymb('lfloor', r'\lfloor', r'\lfloor'),
    LatexSymb('rfloor', r'\rfloor', r'\rfloor'),
    LatexSymb('lceil', r'\lceil', r'\lceil'),
    LatexSymb('rceil', r'\rceil', r'\rceil'),
    LatexSymb('slash', '/', '/'),
    LatexSymb('backslash', r'\backslash', r'\backslash'),
    LatexSymb('lsqbracket', '[', '['),
    LatexSymb('rsqbracket', ']', ']'),
    LatexSymb('llcorner', r'\llcorner', r'\llcorner'),
    LatexSymb('lrcorner', r'\lrcorner', r'\lrcorner'),
    LatexSymb('ulcorner', r'\ulcorner', r'\ulcorner'),
    LatexSymb('urcorner', r'\urcorner', r'\urcorner'),
    LatexSymb('blankdelimiter', r'.', '\ '),
]

ADDITIONAL_LS += SINGLEDELIMITERS

def free_delimiters():
    def get_delimiter(delimiter):
        root = Tkinter.Tk()
        root.title(str(delimiter).capitalize() + " delimiter")
        Tkinter.Label(root, text='Choose ' + str(delimiter) + ' delimiter'
        ).pack(side=Tkinter.TOP)
        im_dict = {}
        for delim in SINGLEDELIMITERS:
            im_dict[delim.tag] = Tkinter.PhotoImage(
                file=os.path.join(dirs.SYMBOLS_DIR, delim.tag + '.png'))
            # Create the button with that image
            Tkinter.Button(
                # Trick to avoid the closure: var=var
                root,
                command=lambda root=root, delim_code=delim.code: delimiter.set(
                    root, delim_code),
                image=im_dict[delim.tag], width='30', height='40'
            ).pack(side=Tkinter.LEFT)

        def disable_event():
            pass
        root.protocol("WM_DELETE_WINDOW", disable_event)
        root.mainloop()

    class LatexCode(object):
        def __init__(self, part):
            self.part = part
            self.command = '\\' + part
        def set(self, root, delim_code):
            self.command += delim_code
            root.destroy()
        def get(self):
            return self.command
        def __str__(self):
            return self.part
    left = LatexCode('left')
    right = LatexCode('right')
    get_delimiter(left)
    get_delimiter(right)
    return Op(1, left.get() + r' {0} ' + right.get())

DELIMITERS = [
    LatexSymb('parenthesisb', Op(1, r'\left( {0} \right)'),
              r'\left(\cdots\right)'),
    LatexSymb('vertb', Op(1, r'\left| {0} \right|'),
              r'\left|\cdots\right|'),
    LatexSymb('uppervertb', Op(1, r'\left\| {0} \right\|'),
              r'\left\|\cdots\right\|'),
    LatexSymb('bracketsb', Op(1, r'\left\{{ {0} \right\}}'),
              r'\left\{\cdots\right\}'),
    LatexSymb('angleb', Op(1, r'\left\langle {0} \right\rangle'),
              r'\left\langle\cdots\right\rangle'),
    LatexSymb('floorb', Op(1, r'\left\lfloor {0} \right\rfloor'),
              r'\left\lfloor\cdots\right\rfloor'),
    LatexSymb('ceilb', Op(1, r'\left\lceil {0} \right\rceil'),
              r'\left\lceil\cdots\right\rceil'),
    LatexSymb('slashb', Op(1, r'\left/ {0} \right\backslash'),
              r'\left/\cdots\right\backslash'),
    LatexSymb('sqbracketsb', Op(1, r'\left[ {0} \right]'),
              r'\left[\cdots\right]'),
    LatexSymb('lcornerb', Op(1, r'\left\llcorner {0} \right\lrcorner'),
              r'\left\llcorner\cdots\right\lrcorner'),
    LatexSymb('ucornerb', Op(1, r'\left\ulcorner {0} \right\urcorner'),
              r'\left\ulcorner\cdots\right\urcorner'),
    LatexSymb('freedelimiters', free_delimiters, r'?_1\cdots ?_2'),
]

MENUITEMSDATA.append(MenuItemData(
    symb_l=DELIMITERS, clickable_size=(80, 50), dpi=200,
    expr=r'\left(ab\right)'))

FUNCTIONS = [
    LatexSymb('arccos', r'\arccos', r'\arccos'),
    LatexSymb('arcsin', r'\arcsin', r'\arcsin'),
    LatexSymb('arctan', r'\arctan', r'\arctan'),
    LatexSymb('arg', r'\arg', r'\arg'),
    LatexSymb('cos', r'\cos', r'\cos'),
    LatexSymb('cosh', r'\cosh', r'\cosh'),
    LatexSymb('coth', r'\coth', r'\coth'),
    LatexSymb('csc', r'\csc', r'\csc'),
    LatexSymb('deg', r'\deg', r'\deg'),
    LatexSymb('det', r'\det', r'\det'),
    LatexSymb('dim', r'\dim', r'\dim'),
    LatexSymb('exp', r'\exp', r'\exp'),
    LatexSymb('gcd', r'\gcd', r'\gcd'),
    LatexSymb('hom', r'\hom', r'\hom'),
    LatexSymb('inf', r'\inf', r'\inf'),
    LatexSymb('ker', r'\ker', r'\ker'),
    LatexSymb('lg', r'\lg', r'\lg'),
    LatexSymb('lim', r'\lim', r'\lim'),
    LatexSymb('liminf', r'\liminf', r'\liminf'),
    LatexSymb('limsup', r'\limsup', r'\limsup'),
    LatexSymb('ln', r'\ln', r'\ln'),
    LatexSymb('log', r'\log', r'\log'),
    LatexSymb('max', r'\max', r'\max'),
    LatexSymb('min', r'\min', r'\min'),
    LatexSymb('pr', r'\Pr', r'\Pr'),
    LatexSymb('sec', r'\sec', r'\sec'),
    LatexSymb('sin', r'\sin', r'\sin'),
    LatexSymb('sinh', r'\sinh', r'\sinh'),
    LatexSymb('sup', r'\sup', r'\sup'),
    LatexSymb('tan', r'\tan', r'\tan'),
    LatexSymb('tanh', r'\tanh', r'\tanh'),
    LatexSymb('upperre', r'\Re', r'\Re'),
    LatexSymb('upperim', r'\Im', r'\Im'),
    LatexSymb('wp', r'\wp', r'\wp'),
]

MENUITEMSDATA.append(MenuItemData(
    symb_l=FUNCTIONS, clickable_size=(100, 30), dpi=200,
    expr=r'f(x)'))

VARIABLESIZE = [
    LatexSymb('sum', r'\sum', r'\sum'),
    LatexSymb('prod', r'\prod', r'\prod'),
    LatexSymb('coprod', r'\coprod', r'\coprod'),
    LatexSymb('int', r'\int', r'\int'),
    LatexSymb('iint', r'\iint', r'\iint'),
    LatexSymb('iiint', r'\iiint', r'\iiint'),
    LatexSymb('oint', r'\oint', r'\oint'),
    LatexSymb('biguplus', r'\biguplus', r'\biguplus'),
    LatexSymb('bigcap', r'\bigcap', r'\bigcap'),
    LatexSymb('bigcup', r'\bigcup', r'\bigcup'),
    LatexSymb('bigoplus', r'\bigoplus', r'\bigoplus'),
    LatexSymb('bigotimes', r'\bigotimes', r'\bigotimes'),
    LatexSymb('bigodot', r'\bigodot', r'\bigodot'),
    LatexSymb('bigvee', r'\bigvee', r'\bigvee'),
    LatexSymb('bigwedge', r'\bigwedge', r'\bigwedge'),
    LatexSymb('bigsqcup', r'\bigsqcup', r'\bigsqcup'),
]

MENUITEMSDATA.append(MenuItemData(
    symb_l=VARIABLESIZE,
    clickable_size=(50, 60), dpi=150,
    expr=r'\sum'))

SOMEOPERATORS = [
    LatexSymb('circ', r'\circ', r'\circ'),
    LatexSymb('bullet', r'\bullet', r'\bullet'),
    LatexSymb('pm', r'\pm', r'\pm'),
    LatexSymb('mp', r'\mp', r'\mp'),
    LatexSymb('odot', r'\odot', r'\odot'),
    LatexSymb('ominus', r'\ominus', r'\ominus'),
    LatexSymb('oplus', r'\oplus', r'\oplus'),
    LatexSymb('oslash', r'\oslash', r'\oslash'),
    LatexSymb('otimes', r'\otimes', r'\otimes'),
    LatexSymb('cap', r'\cap', r'\cap'),
    LatexSymb('cup', r'\cup', r'\cup'),
    LatexSymb('wedge', r'\wedge', r'\wedge'),
    LatexSymb('vee', r'\vee', r'\vee'),
    LatexSymb('forall', r'\forall', r'\forall'),
    LatexSymb('exists', r'\exists', r'\exists'),
    LatexSymb('nexists', r'\nexists', r'\nexists'),
    LatexSymb('perp', r'\perp', r'\perp'),
    LatexSymb('parallel', r'\parallel', r'\parallel'),
    LatexSymb('equiv', r'\equiv', r'\equiv'),
    LatexSymb('less', r'<', r'<'),
    LatexSymb('greater', r'>', r'>'),
    LatexSymb('leq', r'\leq', r'\leq'),
    LatexSymb('geq', r'\geq', r'\geq'),
    LatexSymb('ll', r'\ll', r'\ll'),
    LatexSymb('gg', r'\gg', r'\gg'),
    LatexSymb('sim', r'\sim', r'\sim'),
    LatexSymb('cong', r'\cong', r'\cong'),
    LatexSymb('simeq', r'\simeq', r'\simeq'),
    LatexSymb('approx', r'\approx', r'\approx'),
    LatexSymb('asymp', r'\asymp', r'\asymp'),
    LatexSymb('doteq', r'\doteq', r'\doteq'),
    LatexSymb('propto', r'\propto', r'\propto'),
    LatexSymb('subset', r'\subset', r'\subset'),
    LatexSymb('supset', r'\supset', r'\supset'),
    LatexSymb('subseteq', r'\subseteq', r'\subseteq'),
    LatexSymb('supseteq', r'\supseteq', r'\supseteq'),
    LatexSymb('in', r'\in', r'\in'),
    LatexSymb('ni', r'\ni', r'\ni'),
    LatexSymb('notin', r'\notin', r'\notin'),
    LatexSymb('neq', r'\neq', r'\neq'),
    LatexSymb('neg', r'\neg', r'\neg'),
    LatexSymb('ncong', r'\ncong', r'\ncong'),
    LatexSymb('nparallel', r'\nparallel', r'\nparallel'),
    LatexSymb('notperp', r'\not\perp', r'\not\perp'),
    LatexSymb('nless', r'\nless', r'\nless'),
    LatexSymb('ngtr', r'\ngtr', r'\ngtr'),
    LatexSymb('nleq', r'\nleq', r'\nleq'),
    LatexSymb('ngeq', r'\ngeq', r'\ngeq'),
    LatexSymb('nsubseteq', r'\nsubseteq', r'\nsubseteq'),
    LatexSymb('nsupseteq', r'\nsupseteq', r'\nsupseteq'),
    LatexSymb('emptyset', r'\emptyset', r'\emptyset'),
    LatexSymb('varnothing', r'\varnothing', r'\varnothing'),
]

MENUITEMSDATA.append(MenuItemData(
    symb_l=SOMEOPERATORS,
    clickable_size=(30, 30), dpi=200,
    expr=r'\otimes \in'))

ARROWS = [
    LatexSymb('leftarrow', r'\leftarrow', r'\leftarrow'),
    LatexSymb('longleftarrow', r'\longleftarrow', r'\longleftarrow'),
    LatexSymb('upperleftarrow', r'\Leftarrow', r'\Leftarrow'),
    LatexSymb('upperlongleftarrow', r'\Longleftarrow', r'\Longleftarrow'),
    LatexSymb('rightarrow', r'\rightarrow', r'\rightarrow'),
    LatexSymb('longrightarrow', r'\longrightarrow', r'\longrightarrow'),
    LatexSymb('upperrightarrow', r'\Rightarrow', r'\Rightarrow'),
    LatexSymb('upperlongrightarrow', r'\Longrightarrow', r'\Longrightarrow'),
    LatexSymb('leftrightarrow', r'\leftrightarrow', r'\leftrightarrow'),
    LatexSymb('longleftrightarrow', r'\longleftrightarrow',
              r'\longleftrightarrow'),
    LatexSymb('upperleftrightarrow', r'\Leftrightarrow', r'\Leftrightarrow'),
    LatexSymb('upperlongleftrightarrow', r'\Longleftrightarrow',
              r'\Longleftrightarrow'),
    LatexSymb('uparrow', r'\uparrow', r'\uparrow'),
    LatexSymb('upperuparrow', r'\Uparrow', r'\Uparrow'),
    LatexSymb('downarrow', r'\downarrow', r'\downarrow'),
    LatexSymb('upperdownarrow', r'\Downarrow', r'\Downarrow'),
    LatexSymb('mapsto', r'\mapsto', r'\mapsto'),
    LatexSymb('nupperrightarrow', r'\nRightarrow', r'\nRightarrow'),
    LatexSymb('nupperleftarrow', r'\nLeftarrow', r'\nLeftarrow'),
    LatexSymb('nupperleftrightarrow', r'\nLeftrightarrow',
              r'\nLeftrightarrow'),
    LatexSymb('cdots', r'\cdots', r'\cdots'),
    LatexSymb('vdots', r'\vdots', r'\vdots'),
    LatexSymb('ldots', r'\ldots',
              r'\colorbox{white}{$\phantom{|}\ldots\phantom{|}$}'),
    LatexSymb('ddots', r'\ddots', r'\ddots'),
]

MENUITEMSDATA.append(MenuItemData(
    symb_l=ARROWS,
    clickable_size=(50, 40), dpi=200,
    expr=r'\rightarrow'))

def text():
    root = Tkinter.Tk()
    root.title("Text")
    text_tk = Tkinter.StringVar()
    Tkinter.Label(root, text='Text').grid(row=0)
    entry = Tkinter.Entry(root, textvariable=text_tk)
    entry.grid(row=0, column=1)
    entry.focus_set()
    def return_quit(event):
        root.quit()
    root.bind('<Return>', return_quit)
    Tkinter.Button(root, text="Accept", command=root.quit).grid(row=1,
                                                                column=1)
    # Avoid that the user does not introduce something
    def disable_event():
        pass
    root.protocol("WM_DELETE_WINDOW", disable_event)
    exit_cond = False
    while not exit_cond:
        root.mainloop()
        try:
            text_str = text_tk.get()
            # Check that characters are only ASCII
            text_str.decode('ascii')
            # Avoid problematic ACII characters
            assert '^' not in text_str
            assert '~' not in text_str
            assert '\\' not in text_str
            # Change ASCII with special sequencies
            # Be careful: do not include keys that are exactly equal to values
            latexdict = {
                '$':r'\$', '%':r'\%', '_':r'\_', '}':r'\}', '&':r'\&',
                '#':r'\#', '{':r'\{'}
            for key in latexdict:
                text_str = text_str.replace(key, latexdict[key])
            exit_cond = True
        except UnicodeEncodeError:
            pass
        except AssertionError:
            pass
    root.destroy()
    return r'\text{{' + text_str + '}}'

def special_format(latex_command, label_text, only_capital=False):
    def fun():
        root = Tkinter.Tk()
        root.title(label_text + " characters")
        text_tk = Tkinter.StringVar()
        Tkinter.Label(root, text=label_text).grid(row=0)
        entry = Tkinter.Entry(root, textvariable=text_tk)
        entry.grid(row=0, column=1)
        entry.focus_set()
        Tkinter.Button(root, text="Accept",
                       command=root.quit).grid(row=1, column=1)
        def return_quit(event):
            root.quit()
        root.bind('<Return>', return_quit)
        # Avoid that the user does not introduce something
        def disable_event():
            pass
        root.protocol("WM_DELETE_WINDOW", disable_event)
        exit_cond = False
        while not exit_cond:
            root.mainloop()
            text_str = text_tk.get()
            if only_capital:
                if text_str.isalpha():
                    text_str = text_str.upper()
                    exit_cond = True
            else:
                if text_str.isalnum():
                    exit_cond = True
        root.destroy()
        return latex_command + r'{' + text_str + '}'
    return fun

COLORS = [
    LatexSymb('black', 'black', r'\textcolor{black}{\text{black}}'),
    LatexSymb('blue', 'blue', r'\textcolor{blue}{\text{blue}}'),
    LatexSymb('brown', 'brown', r'\textcolor{brown}{\text{brown}}'),
    LatexSymb('cyan', 'cyan', r'\textcolor{cyan}{\text{cyan}}'),
    LatexSymb('darkgray', 'darkgray',
              r'\textcolor{darkgray}{\text{darkgray}}'),
    LatexSymb('gray', 'gray', r'\textcolor{gray}{\text{gray}}'),
    LatexSymb('green', 'green', r'\textcolor{green}{\text{green}}'),
    LatexSymb('lightgray', 'lightgray',
              r'\textcolor{lightgray}{\text{lightgray}}'),
    LatexSymb('lime', 'lime', r'\textcolor{lime}{\text{lime}}'),
    LatexSymb('magenta', 'magenta', r'\textcolor{magenta}{\text{magenta}}'),
    LatexSymb('olive', 'olive', r'\textcolor{olive}{\text{olive}}'),
    LatexSymb('orange', 'orange', r'\textcolor{orange}{\text{orange}}'),
    LatexSymb('pink', 'pink', r'\textcolor{pink}{\text{pink}}'),
    LatexSymb('purple', 'purple', r'\textcolor{purple}{\text{purple}}'),
    LatexSymb('red', 'red', r'\textcolor{red}{\text{red}}'),
    LatexSymb('teal', 'teal', r'\textcolor{teal}{\text{teal}}'),
    LatexSymb('violet', 'violet', r'\textcolor{violet}{\text{violet}}'),
    LatexSymb('white', 'white', r'\textcolor{white}{\text{white}}'),
    LatexSymb('yellow', 'yellow', r'\textcolor{yellow}{\text{yellow}}'),
]

ADDITIONAL_LS += COLORS

def color():
    class LatexCode(object):
        def set(self, root, color_code):
            self.color_code = color_code
            root.destroy()
        def get(self):
            return self.color_code
    code = LatexCode()
    root = Tkinter.Tk()
    root.title("Color")
    Tkinter.Label(root, text='Choose color').pack(side=Tkinter.TOP)
    im_dict = {}
    for color in COLORS:
        im_dict[color.tag] = Tkinter.PhotoImage(
            file=os.path.join(dirs.SYMBOLS_DIR, color.tag + '.png'))
        # Create the button with that image
        Tkinter.Button(
            # Trick to avoid the closure: var=var
            root,
            command=lambda root=root, color_code=color.code: code.set(
                root, color_code),
            image=im_dict[color.tag], width='140', height='30'
        ).pack(side=Tkinter.TOP)

    def disable_event():
        pass
    root.protocol("WM_DELETE_WINDOW", disable_event)
    root.mainloop()

    return Op(1, r'\begingroup\color{{' + code.get() + r'}}{0}\endgroup')

def colorbox():
    class LatexCode(object):
        def set(self, root, color_code):
            self.color_code = color_code
            root.destroy()
        def get(self):
            return self.color_code
    code = LatexCode()
    root = Tkinter.Tk()
    root.title("Color box")
    Tkinter.Label(root, text='Choose color').pack(side=Tkinter.TOP)
    im_dict = {}
    for color in COLORS:
        im_dict[color.tag] = Tkinter.PhotoImage(
            file=os.path.join(dirs.SYMBOLS_DIR, color.tag + '.png'))
        # Create the button with that image
        Tkinter.Button(
            # Trick to avoid the closure: var=var
            root,
            command=lambda root=root, color_code=color.code: code.set(
                root, color_code),
            image=im_dict[color.tag], width='140', height='30'
        ).pack(side=Tkinter.TOP)

    def disable_event():
        pass
    root.protocol("WM_DELETE_WINDOW", disable_event)
    root.mainloop()

    return Op(1, r'\colorbox{{' + code.get() + r'}}{{$\displaystyle {0}$}}')


TEXT = [
    LatexSymb('text', text, r"\text{Text}"),
    LatexSymb('mathcal', special_format(r'\mathcal', 'Caligraphic', True),
              r"\mathcal{ABC}"),
    LatexSymb('mathbb', special_format(r'\mathbb', 'Mathbb', True),
              r"\mathbb{ABC}"),
    LatexSymb('mathfrak', special_format(r'\mathfrak', 'Mathfrak'),
              r"\mathfrak{Ab1}"),
    LatexSymb('mathsf', special_format(r'\mathsf', 'Sans serif'),
              r"\mathsf{Ab1}"),
    LatexSymb('mathbf', special_format(r'\mathbf', 'Mathbf'),
              r"\mathbf{Ab1}"),
    LatexSymb('color', color, r'\textcolor{red}{C}\textcolor{blue}'
              + r'{o}\textcolor{olive}{|}\textcolor{pink}{0}'
              + r'\textcolor{purple}{r}'),
    LatexSymb('colorbox', colorbox, r'\colorbox{yellow}{$x^2$}/2'),
]

MENUITEMSDATA.append(MenuItemData(
    symb_l=TEXT,
    clickable_size=(80, 50), dpi=200,
    expr=r'\mathbb{R}\,\text{if}'))

def matrix(matrix_type):
    def fun():
        root = Tkinter.Tk()
        root.title(matrix_type.capitalize())
        n_rows_tk = Tkinter.StringVar()
        Tkinter.Label(root, text='Number of rows').grid(row=0)
        n_columns_tk = Tkinter.StringVar()
        Tkinter.Label(root, text='Number of columns').grid(row=1)
        entry1 = Tkinter.Entry(root, textvariable=n_rows_tk)
        entry2 = Tkinter.Entry(root, textvariable=n_columns_tk)
        entry1.grid(row=0, column=1)
        entry2.grid(row=1, column=1)
        entry1.focus_set()
        Tkinter.Button(root, text="Accept", command=root.quit).grid(row=2,
                                                                    column=1)
        def return_quit(event):
            root.quit()
        root.bind('<Return>', return_quit)
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
                assert n_rows > 0
                assert n_columns > 0
                exit_cond = True
            except ValueError:
                pass
            except AssertionError:
                pass
        root.destroy()
        row_code = r'{}' + r'&{}'*(n_columns-1) + r'\\'
        latex_code = r'\begin{{' + matrix_type + r'}}' + row_code*n_rows \
                         + r'\end{{' + matrix_type + r'}}'
        return Op(n_rows*n_columns, latex_code)
    return fun

def cases():
    root = Tkinter.Tk()
    root.title("Cases")
    n_cases_tk = Tkinter.StringVar()
    Tkinter.Label(root, text='Number of cases').grid(row=0)
    entry = Tkinter.Entry(root, textvariable=n_cases_tk)
    entry.grid(row=0, column=1)
    entry.focus_set()
    Tkinter.Button(root, text="Accept", command=root.quit).grid(row=1,
                                                                column=1)
    def return_quit(event):
        root.quit()
    root.bind('<Return>', return_quit)
    # Avoid that the user does not introduce something
    def disable_event():
        pass
    root.protocol("WM_DELETE_WINDOW", disable_event)
    exit_cond = False
    while not exit_cond:
        root.mainloop()
        try:
            n_cases = int(n_cases_tk.get())
            assert n_cases > 0
            exit_cond = True
        except ValueError:
            pass
        except AssertionError:
            pass
    root.destroy()
    case_code = r'{}&{}\\'
    latex_code = r'\begin{{cases}}' + case_code*n_cases + r'\end{{cases}}'
    return Op(n_cases*2, latex_code)

def equations_system():
    root = Tkinter.Tk()
    root.title("Equations system")
    n_cases_tk = Tkinter.StringVar()
    Tkinter.Label(root, text='Number of equations').grid(row=0)
    entry = Tkinter.Entry(root, textvariable=n_cases_tk)
    entry.grid(row=0, column=1)
    entry.focus_set()
    Tkinter.Button(root, text="Accept", command=root.quit).grid(row=1,
                                                                column=1)
    def return_quit(event):
        root.quit()
    root.bind('<Return>', return_quit)
    # Avoid that the user does not introduce something
    def disable_event():
        pass
    root.protocol("WM_DELETE_WINDOW", disable_event)
    exit_cond = False
    while not exit_cond:
        root.mainloop()
        try:
            n_cases = int(n_cases_tk.get())
            assert n_cases > 0
            exit_cond = True
        except ValueError:
            pass
        except AssertionError:
            pass
    root.destroy()
    case_code = r'{}\\'
    latex_code = r'\begin{{cases}}' + case_code*n_cases + r'\end{{cases}}'
    return Op(n_cases, latex_code)

MANYLINES = [
    LatexSymb('matrix', matrix('matrix'),
                r"\begin{matrix}\cdots&\square&\square\\" \
                 + r"\square&\square&\square\end{matrix}"),
    LatexSymb('pmatrix', matrix('pmatrix'),
                r"\begin{pmatrix}\cdots\\\square\end{pmatrix}"),
    LatexSymb('cases', cases,
            r'\begin{cases}a &\text{if }x>0\\b&\text{if }x<0\end{cases}'),
    LatexSymb('equations_system', equations_system,
                          r'\begin{cases}x+y=1\\x-y=8\end{cases}'),
]

MENUITEMSDATA.append(MenuItemData(
    symb_l=MANYLINES,
    clickable_size=(190, 90), dpi=200,
    expr=r'\begin{smallmatrix}a&b\\c&d\end{smallmatrix}'))

ACCENTS = [
    LatexSymb('acute', Op(1, r'\acute{{{0}}}'), r'\acute{{{\cdot}}}'),
    LatexSymb('breve', Op(1, r'\breve{{{0}}}'), r'\breve{{{\cdot}}}'),
    LatexSymb('ddot', Op(1, r'\ddot{{{0}}}'), r'\ddot{{{\cdot}}}'),
    LatexSymb('grave', Op(1, r'\grave{{{0}}}'), r'\grave{{{\cdot}}}'),
    LatexSymb('tilde', Op(1, r'\tilde{{{0}}}'), r'\tilde{{{\cdot}}}'),
    LatexSymb('bar', Op(1, r'\bar{{{0}}}'), r'\bar{{{\cdot}}}'),
    LatexSymb('check', Op(1, r'\check{{{0}}}'), r'\check{{{\cdot}}}'),
    LatexSymb('dot', Op(1, r'\dot{{{0}}}'), r'\dot{{{\cdot}}}'),
    LatexSymb('hat', Op(1, r'\hat{{{0}}}'), r'\hat{{{\cdot}}}'),
    LatexSymb('vec', Op(1, r'\vec{{{0}}}'), r'\vec{{{\cdot}}}'),
    LatexSymb('imath', r'\imath', r'\imath'),
    LatexSymb('jmath', r'\jmath', r'\jmath'),
    LatexSymb('ell', r'\ell', r'\ell'),
    LatexSymb('hbar', r'\hbar', r'\hbar'),
    LatexSymb('eth', r'\eth', r'\eth'),
]

MENUITEMSDATA.append(MenuItemData(
    symb_l=ACCENTS, clickable_size=(40, 30), dpi=200,
    expr=r'\acute{{a}}\;\tilde{{B}}'))

INDICES = [
    LatexSymb('super', SUPERINDEX, r'\cdot^{{\square}}'),
    LatexSymb('sub', SUBINDEX, r'\cdot_{{\square}}'),
    LatexSymb('lsuper', Op(2, r'{{}}^{{{1}}}{0}'), r'{{}}^{{\square}}\cdot'),
    LatexSymb('lsub', Op(2, r'{{}}_{{{1}}}{0}'), r'{{}}_{{\square}}\cdot'),
    LatexSymb('supersub', Op(3, r'{0}^{{{2}}}_{{{1}}}'),
                  r'\cdot^{{\square}}_{{\square}}'),
    LatexSymb('lsuperlsub', Op(3, r'{{}}^{{{2}}}_{{{1}}}{0}'),
                    r'{{}}^{{\square}}_{{\square}}\cdot'),
    LatexSymb('superlsuper', Op(3, r'{{}}^{{{1}}}{0}^{{{2}}}'),
                     r'{{}}^{{\square}}\cdot^{{\square}}'),
    LatexSymb('sublsub', Op(3, r'{{}}_{{{1}}}{0}_{{{2}}}'),
                     r'{{}}_{{\square}}\cdot_{{\square}}'),
    LatexSymb('supersublsuper', Op(4, r'{{}}^{{{1}}}{0}^{{{3}}}_{{{2}}}'),
                  r'{{}}^{{\square}}\cdot^{{\square}}_{{\square}}'),
    LatexSymb('supersublsub', Op(4, r'{{}}_{{{1}}}{0}^{{{3}}}_{{{2}}}'),
                  r'{{}}_{{\square}}\cdot^{{\square}}_{{\square}}'),
    LatexSymb('sublsublsuper', Op(4, r'{{}}_{{{1}}}^{{{3}}}{0}_{{{2}}}'),
                  r'{{}}_{{\square}}^{{\square}}\cdot_{{\square}}'),
    LatexSymb('superlsuperlsub', Op(4, r'{{}}^{{{1}}}_{{{2}}}{0}^{{{3}}}'),
                  r'{{}}^{{\square}}_{{\square}}\cdot^{{\square}}'),
    LatexSymb('supersublsuperlsub',
              Op(5, r'{{}}^{{{2}}}_{{{1}}}{0}^{{{4}}}_{{{3}}}'),
              r'{{}}^{{\square}}_{{\square}}\cdot^{{\square}}_{{\square}}'),
]

#    ('binomial', (Op(2, r'\binom{{{0}}}{{{1}}}'),
#     [r'\binom{{\cdot}}{{\square}}'])),

MENUITEMSDATA.append(MenuItemData(
    symb_l=INDICES, clickable_size=(60, 60), dpi=200, expr=r'a^b'))
