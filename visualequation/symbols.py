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
A module that contains lists of operators and symbols used in the symbolstab.
"""
import os
from collections import namedtuple

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import dirs

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
MenuItemData = namedtuple('MenuItem', 'tag symb_l clickable_size dpi expr')

# Use these operators in the code, so it will be easy to change their value
# in next releases
SELARG = r'\cdots'
NEWARG = r'\square'
#EDIT = Op(1, r'\boxed{{{0}}}')
#EDIT = Op(1, r'\left.\textcolor{{blue}}{{{0}}}\right|')
REDIT = Op(1, r'\left\lmoustache{{{0}}}\right\rgroup')
LEDIT = Op(1, r'\left\lgroup{{{0}}}\right\rmoustache')
#REDIT = Op(1, r'\left\rgroup{{{0}}}\right\rgroup')
#LEDIT = Op(1, r'\left\lgroup{{{0}}}\right\lgroup')
JUXT = Op(2, r'{0} {1}')

MENUITEMSDATA = []
ADDITIONAL_LS = []

# It does NOT include ' ', '^', '\\' and '~'
# so it is valid for both text and math environments
ASCII_LATEX_TRANSLATION = {
    '|': r'|',
    '!': r'!',
    '$': r'\$',
    '%': r'\%',
    '&': r'\&',
    '/': r'/',
    '(': r'(',
    ')': r')',
    '=': r'=',
    '?': r'?',
    "'": r"'",
    '@': r'@',
    '#': r'\#',
    '[': r'[',
    ']': r']',
    '{': r'\{',
    '}': r'\}',
    '*': r'*',
    '+': r'+',
    '-': r'-',
    '<': r'<',
    '>': r'>',
    ',': r',',
    '.': r'.',
    ';': r';',
    ':': r':',
    '_': r'\_',
}

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
    LatexSymb('emptyset', r'\emptyset', r'\emptyset'),
    LatexSymb('varnothing', r'\varnothing', r'\varnothing'),
    LatexSymb('dagger', r'\dagger', r'\dagger'),
    LatexSymb('ddagger', r'\ddagger', r'\ddagger'),
    LatexSymb('wr', r'\wr', r'\wr'),
    LatexSymb('clubsuit', r'\clubsuit', r'\clubsuit'),
    LatexSymb('diamondsuit', r'\diamondsuit', r'\diamondsuit'),
    LatexSymb('heartsuit', r'\heartsuit', r'\heartsuit'),
    LatexSymb('spadesuit', r'\spadesuit', r'\spadesuit'),
    LatexSymb('pounds', r'\pounds', r'\pounds'),
    LatexSymb('upperp', r'\P', r'\P'),
    LatexSymb('uppers', r'\S', r'\S'),
]

MENUITEMSDATA.append(MenuItemData(
    tag="tab_greek_hebrew_symb1",
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
    LatexSymb('overleftrightarrow', Op(1, r'\overleftrightarrow{{{0}}}'),
              r'\overleftrightarrow\cdots'),
    LatexSymb('underrightarrow', Op(1, r'\underrightarrow{{{0}}}'),
              r'\underrightarrow\cdots'),
    LatexSymb('underleftarrow', Op(1, r'\underleftarrow{{{0}}}'),
              r'\underleftarrow\cdots'),
    LatexSymb('underleftrightarrow', Op(1, r'\underleftrightarrow{{{0}}}'),
              r'\underleftrightarrow\cdots'),
    LatexSymb('xrightarrow', Op(2, r'\xrightarrow[{0}]{{{1}}}'),
              r'\xrightarrow[\cdots]{{\square}}'),
    LatexSymb('xleftarrow', Op(2, r'\xleftarrow[{0}]{{{1}}}'),
              r'\xleftarrow[\cdots]{{\square}}'),
    LatexSymb('overbrace1', Op(1, r'\overbrace{{{0}}}'), r'\overbrace\cdots'),
    LatexSymb('underbrace1', Op(1, r'\underbrace{{{0}}}'),
              r'\underbrace\cdots'),
    LatexSymb('overbrace2', Op(2, r'\overbrace{{{0}}}^{{{1}}}'),
              r'\overbrace{\cdots}^\square'),
    LatexSymb('underbrace2', Op(2, r'\underbrace{{{0}}}_{{{1}}}'),
              r'\underbrace{\cdots}_\square'),
    LatexSymb('overset', Op(2, r'\overset{{{1}}}{{{0}}}'),
              r'\overset{{{\square}}}{{{\cdot}}}'),
    LatexSymb('underset', Op(2, r'\underset{{{1}}}{{{0}}}'),
              r'\underset{{{\square}}}{{{\cdot}}}'),
]

MENUITEMSDATA.append(MenuItemData(
    tag="tab_mathconstructs",
    symb_l=MATHCONSTRUCTS,
    clickable_size=(55, 70), dpi=200,
    expr=r'\underbrace{{abc}}'))

SINGLEDELIMITERS = [
    LatexSymb('lparenthesis', '(', '('),
    LatexSymb('rparenthesis', ')', ')'),
    LatexSymb('vert', '|', '|'),
    LatexSymb('uppervert', r'\|', r'\|'),
<<<<<<< HEAD
    LatexSymb('lbracket', r'\{{', r'\{'), # {{: It will be part of an operator
    LatexSymb('rbracket', r'\}}', r'\}'), # }}: Idem
=======
    LatexSymb('lbracket', r'\{{', r'\{'), # They will be part of an operator:
    LatexSymb('rbracket', r'\}}', r'\}'), # so double brackets
>>>>>>> 39eab88460aade6ee82d7c5322e84a07ba24cde5
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
    LatexSymb('blankdelimiter', r'.', r'\text{No delimiter}'),
]

ADDITIONAL_LS += SINGLEDELIMITERS

def free_delimiters(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Free delimiters')
            label_l = QLabel('Left delimiter:')
            self.combo_l = QComboBox()
            self.combo_l.setIconSize(self.combo_l.minimumSizeHint())
            for delim in SINGLEDELIMITERS:
                self.combo_l.addItem(QIcon(os.path.join(dirs.SYMBOLS_DIR,
                                                        delim.tag + '.png')),
                                     '')
            label_r = QLabel('Right delimiter:')
            self.combo_r = QComboBox()
            self.combo_r.setIconSize(self.combo_r.minimumSizeHint())
            for delim in SINGLEDELIMITERS:
                self.combo_r.addItem(QIcon(os.path.join(dirs.SYMBOLS_DIR,
                                                        delim.tag + '.png')),
                                     '')
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label_l)
            vbox.addWidget(self.combo_l)
            vbox.addWidget(label_r)
            vbox.addWidget(self.combo_r)
            vbox.addWidget(self.buttons)

            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        @staticmethod
        def get_delimiter(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return ((SINGLEDELIMITERS[dialog.combo_l.currentIndex()].code,
                         SINGLEDELIMITERS[dialog.combo_r.currentIndex()].code),
                        True)
            else:
                return ((None, None), False)
            
    (delim_l, delim_r), ok = Dialog.get_delimiter(parent)
    if ok:
        return Op(1, r'\left' + delim_l + r' {0} ' + r'\right' +  delim_r)
    else:
        return None

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
    tag="tab_delimiters",
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
    tag="tab_functions",
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
    tag="tab_variablesize",
    symb_l=VARIABLESIZE,
    clickable_size=(50, 60), dpi=150,
    expr=r'\sum'))

SOMEOPERATORS = [
    LatexSymb('nabla', r'\nabla', r'\nabla'),
    LatexSymb('partial', r'\partial', r'\partial'),
    LatexSymb('times', r'\times', r'\times'),
    LatexSymb('cdot', r'\cdot', r'\cdot'),
    LatexSymb('div', r'\div', r'\div'),
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
    LatexSymb('uplus', r'\uplus', r'\uplus'),
    LatexSymb('sqcap', r'\sqcap', r'\sqcap'),
    LatexSymb('sqcup', r'\sqcup', r'\sqcup'),    
    LatexSymb('wedge', r'\wedge', r'\wedge'),
    LatexSymb('vee', r'\vee', r'\vee'),
    LatexSymb('forall', r'\forall', r'\forall'),
    LatexSymb('exists', r'\exists', r'\exists'),
    LatexSymb('nexists', r'\nexists', r'\nexists'),
]

MENUITEMSDATA.append(MenuItemData(
    tag="tab_someoperators",
    symb_l=SOMEOPERATORS,
    clickable_size=(30, 30), dpi=200,
    expr=r'\otimes'))

RELATIONS = [
    LatexSymb('perp', r'\perp', r'\perp'),
    LatexSymb('parallel', r'\parallel', r'\parallel'),
    LatexSymb('equiv', r'\equiv', r'\equiv'),
    LatexSymb('less', r'<', r'<'),
    LatexSymb('greater', r'>', r'>'),
    LatexSymb('leq', r'\leq', r'\leq'),
    LatexSymb('geq', r'\geq', r'\geq'),
    LatexSymb('ll', r'\ll', r'\ll'),
    LatexSymb('gg', r'\gg', r'\gg'),
    LatexSymb('prec', r'\prec', r'\prec'),
    LatexSymb('succ', r'\succ', r'\succ'),
    LatexSymb('preceq', r'\preceq', r'\preceq'),
    LatexSymb('succeq', r'\succeq', r'\succeq'),
    LatexSymb('sim', r'\sim', r'\sim'),
    LatexSymb('cong', r'\cong', r'\cong'),
    LatexSymb('simeq', r'\simeq', r'\simeq'),
    LatexSymb('approx', r'\approx', r'\approx'),
    LatexSymb('asymp', r'\asymp', r'\asymp'),
    LatexSymb('lll', r'\lll', r'\lll'),
    LatexSymb('ggg', r'\ggg', r'\ggg'),
    LatexSymb('doteq', r'\doteq', r'\doteq'),
    LatexSymb('triangleq', r'\triangleq', r'\triangleq'),
    LatexSymb('circeq', r'\circeq', r'\circeq'),
    LatexSymb('propto', r'\propto', r'\propto'),
    LatexSymb('subset', r'\subset', r'\subset'),
    LatexSymb('supset', r'\supset', r'\supset'),
    LatexSymb('subseteq', r'\subseteq', r'\subseteq'),
    LatexSymb('supseteq', r'\supseteq', r'\supseteq'),
    LatexSymb('sqsubset', r'\sqsubset', r'\sqsubset'),
    LatexSymb('sqsupset', r'\sqsupset', r'\sqsupset'),
    LatexSymb('sqsubseteq', r'\sqsubseteq', r'\sqsubseteq'),
    LatexSymb('sqsupseteq', r'\sqsupseteq', r'\sqsupseteq'),
    LatexSymb('dashv', r'\dashv', r'\dashv'),
    LatexSymb('vdash', r'\vdash', r'\vdash'),
    LatexSymb('models', r'\models', r'\models'),
    LatexSymb('smile', r'\smile', r'\smile'),
    LatexSymb('frown', r'\frown', r'\frown'),
    LatexSymb('in', r'\in', r'\in'),
    LatexSymb('ni', r'\ni', r'\ni'),
    LatexSymb('notin', r'\notin', r'\notin'),
    LatexSymb('neq', r'\neq', r'\neq'),
    LatexSymb('neg', r'\neg', r'\neg'),
    LatexSymb('ncong', r'\ncong', r'\ncong'),
    LatexSymb('nsim', r'\nsim', r'\nsim'),
    LatexSymb('nparallel', r'\nparallel', r'\nparallel'),
    LatexSymb('notperp', r'\not\perp', r'\not\perp'),
    LatexSymb('nless', r'\nless', r'\nless'),
    LatexSymb('ngtr', r'\ngtr', r'\ngtr'),
    LatexSymb('nleq', r'\nleq', r'\nleq'),
    LatexSymb('ngeq', r'\ngeq', r'\ngeq'),
    LatexSymb('lneq', r'\lneq', r'\lneq'),
    LatexSymb('gneq', r'\gneq', r'\gneq'),
    LatexSymb('nsubseteq', r'\nsubseteq', r'\nsubseteq'),
    LatexSymb('nsupseteq', r'\nsupseteq', r'\nsupseteq'),
    LatexSymb('subsetneq', r'\subsetneq', r'\subsetneq'),
    LatexSymb('supsetneq', r'\supsetneq', r'\supsetneq'),
    LatexSymb('nprec', r'\nprec', r'\nprec'),
    LatexSymb('nsucc', r'\nsucc', r'\nsucc'),
    LatexSymb('npreceq', r'\npreceq', r'\npreceq'),
    LatexSymb('nsucceq', r'\nsucceq', r'\nsucceq'),
]

MENUITEMSDATA.append(MenuItemData(
    tag="tab_relations",
    symb_l=RELATIONS,
    clickable_size=(30, 30), dpi=200,
    expr=r'< \in'))

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
    LatexSymb('updownarrow', r'\updownarrow', r'\updownarrow'),
    LatexSymb('upperupdownarrow', r'\Updownarrow', r'\Updownarrow'),
    LatexSymb('mapsto', r'\mapsto', r'\mapsto'),
    LatexSymb('longmapsto', r'\longmapsto', '\longmapsto'),
    LatexSymb('nupperrightarrow', r'\nRightarrow', r'\nRightarrow'),
    LatexSymb('nupperleftarrow', r'\nLeftarrow', r'\nLeftarrow'),
    LatexSymb('nupperleftrightarrow', r'\nLeftrightarrow',
              r'\nLeftrightarrow'),
    LatexSymb('nleftarrow', r'\nleftarrow', r'\nleftarrow'),
    LatexSymb('nrightarrow', r'\nrightarrow', r'\nrightarrow'),
    LatexSymb('nleftrightarrow', r'\nleftrightarrow', r'\nleftrightarrow'),
    LatexSymb('nearrow', r'\nearrow', r'\nearrow'),
    LatexSymb('searrow', r'\searrow', r'\searrow'),
    LatexSymb('swarrow', r'\swarrow', r'\swarrow'),
    LatexSymb('nwarrow', r'\nwarrow', r'\nwarrow'),
    LatexSymb('diagup', r'\diagup', r'\diagup'),
    LatexSymb('diagdown', r'\diagdown', r'\diagdown'),
    LatexSymb('cdots', r'\cdots', r'\cdots'),
    LatexSymb('vdots', r'\vdots', r'\vdots'),
    LatexSymb('ldots', r'\ldots', r'\ldots'),
    LatexSymb('ddots', r'\ddots', r'\ddots'),
]

MENUITEMSDATA.append(MenuItemData(
    tag="tab_arrows",
    symb_l=ARROWS,
    clickable_size=(50, 40), dpi=200,
    expr=r'\rightarrow'))

def text(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Text')
            label = QLabel('Text:')
            self.ledit = QLineEdit()
            regexp = QRegExp("^[a-zA-Z\d\s|!\\$%&/()=?'@#\\[\\]{}*+-<>,.;:_]+$")
            self.validator = QRegExpValidator(regexp)
            self.ledit.setValidator(self.validator)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label)
            vbox.addWidget(self.ledit)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit.setFocus()

            self.ledit.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        def check_state(self, *args, **kargs):
            state = self.validator.validate(self.ledit.text(), 0)[0]
            if state == QValidator.Acceptable:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)

        @staticmethod
        def get_text(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (dialog.ledit.text(), True)
            else:
                return (None, False)
            
    text, ok = Dialog.get_text(parent)
    if ok:
        # Correct string
        for key in ASCII_LATEX_TRANSLATION:
            text = text.replace(key, ASCII_LATEX_TRANSLATION[key])
        return r'\text{{' + text + '}}'
    else:
        return None

def special_format(latex_command, label_text, only_capital=False):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle(label_text + " characters")
            label = QLabel(label_text + ':')
            self.ledit = QLineEdit()
            if only_capital:
                regexp = QRegExp("^[A-Z]+$")
            else:
                regexp = QRegExp("^[a-zA-Z\d]+$")
            self.validator = QRegExpValidator(regexp)
            self.ledit.setValidator(self.validator)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label)
            vbox.addWidget(self.ledit)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit.setFocus()

            self.ledit.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        def check_state(self, *args, **kargs):
            state = self.validator.validate(self.ledit.text(), 0)[0]
            if state == QValidator.Acceptable:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)

        @staticmethod
        def get_text(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (dialog.ledit.text(), True)
            else:
                return (None, False)

    def fun(parent):
        text, ok = Dialog.get_text(parent)
        if ok:
            return latex_command + text + '}'
        else:
            return None

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

def color(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Color')
            label = QLabel('Color:')
            self.combo = QComboBox()
            self.combo.setIconSize(self.combo.minimumSizeHint())
            for color in COLORS:
                self.combo.addItem(QIcon(os.path.join(dirs.SYMBOLS_DIR,
                                                      color.tag + '.png')), '')
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label)
            vbox.addWidget(self.combo)
            vbox.addWidget(self.buttons)

            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        @staticmethod
        def get_color(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (COLORS[dialog.combo.currentIndex()].code, True)
            else:
                return (None, False)
            
    color, ok = Dialog.get_color(parent)
    if ok:
        return Op(1, r'\begingroup\color{{' + color + r'}}{0}\endgroup')
    else:
        return None

def colorbox(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Color Box')
            label = QLabel('Color:')
            self.combo = QComboBox()
            self.combo.setIconSize(self.combo.minimumSizeHint())
            for color in COLORS:
                self.combo.addItem(QIcon(os.path.join(dirs.SYMBOLS_DIR,
                                                      color.tag + '.png')), '')
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label)
            vbox.addWidget(self.combo)
            vbox.addWidget(self.buttons)

            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        @staticmethod
        def get_color(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (COLORS[dialog.combo.currentIndex()].code, True)
            else:
                return (None, False)
            
    color, ok = Dialog.get_color(parent)
    if ok:
        return Op(1, r'\colorbox{{' + color
                  + r'}}{{$\displaystyle {0}$}}')
    else:
        return None

TEXT = [
    LatexSymb('text', text, r"\text{Text}"),
    LatexSymb('mathcal', special_format(r'\mathcal{', 'Caligraphic', True),
              r"\mathcal{ABC}"),
    LatexSymb('mathbb', special_format(r'\mathbb{', 'Mathbb', True),
              r"\mathbb{ABC}"),
    LatexSymb('mathfrak', special_format(r'\mathfrak{', 'Fraktur'),
              r"\mathfrak{Ab1}"),
    LatexSymb('mathsf', special_format(r'\mathsf{', 'Sans serif'),
              r"\mathsf{Ab1}"),
    LatexSymb('mathbf', special_format(r'\mathbf{', 'Bold'),
              r"\mathbf{Ab1}"),
    LatexSymb('textbfem', special_format(r'\textbf{\em ', 'Bold Italic'),
              r"\textbf{\em Ab1}"),
    LatexSymb('color', color, r'\textcolor{red}{C}\textcolor{blue}'
              + r'{o}\textcolor{olive}{|}\textcolor{pink}{0}'
              + r'\textcolor{purple}{r}'),
    LatexSymb('colorbox', colorbox, r'\colorbox{yellow}{$x^2$}/2'),
]

MENUITEMSDATA.append(MenuItemData(
    tag="tab_text",
    symb_l=TEXT,
    clickable_size=(80, 50), dpi=200,
    expr=r'\mathbb{R}\,\text{if}'))

MATRIXTYPES = [
    LatexSymb('pmatrix', 'pmatrix', r'\begin{pmatrix}\square\end{pmatrix}'),
    LatexSymb('vmatrix', 'vmatrix', r'\begin{vmatrix}\square\end{vmatrix}'),
    LatexSymb('Vmatrix', 'Vmatrix', r'\begin{Vmatrix}\square\end{Vmatrix}'),
    LatexSymb('bmatrix', 'bmatrix', r'\begin{bmatrix}\square\end{bmatrix}'),
    LatexSymb('Bmatrix', 'Bmatrix', r'\begin{Bmatrix}\square\end{Bmatrix}'),
    LatexSymb('matrix', 'matrix', r'\begin{matrix}\square\end{matrix}'),
]

ADDITIONAL_LS += MATRIXTYPES

def matrix_type(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Matrix')
            label_rows = QLabel('Number of rows:')
            self.ledit_rows = QLineEdit()
            label_cols = QLabel('Number of columns:')
            self.ledit_cols = QLineEdit()
            regexp = QRegExp('^[1-9]$')
            self.validator = QRegExpValidator(regexp)
            self.ledit_rows.setValidator(self.validator)
            self.ledit_cols.setValidator(self.validator)
            label_combo = QLabel('Matrix type:')
            self.combo = QComboBox()
            for mtype in MATRIXTYPES:
                self.combo.addItem(QIcon(os.path.join(dirs.SYMBOLS_DIR,
                                                      mtype.tag + '.png')), '')
            self.combo.setIconSize(self.combo.minimumSizeHint())
            #self.combo.setSizePolicy(QSizePolicy.Expanding,
            #                         QSizePolicy.Maximum)
            #self.combo.setSizeAdjustPolicy(0) 
            #self.combo.setMinimumHeight(50)
            #self.combo.SizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
            #self.combo.setView(QListView())
            #self.combo.setStyleSheet('''
            #QComboBox QAbstractItemView::item { min-height: 50px;}
            #''')
            
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label_rows)
            vbox.addWidget(self.ledit_rows)
            vbox.addWidget(label_cols)
            vbox.addWidget(self.ledit_cols)
            vbox.addWidget(label_combo)
            vbox.addWidget(self.combo)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit_rows.setFocus()

            self.ledit_rows.textChanged.connect(self.check_state)
            self.ledit_cols.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        def check_state(self, *args, **kargs):
            state1 = self.validator.validate(self.ledit_rows.text(), 0)[0]
            state2 = self.validator.validate(self.ledit_cols.text(), 0)[0]
            if state1 == state2 == QValidator.Acceptable:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)

        @staticmethod
        def get_matrix_def(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return ((int(dialog.ledit_rows.text()),
                         int(dialog.ledit_cols.text()),
                         MATRIXTYPES[dialog.combo.currentIndex()].code),
                        True)
            else:
                return ((None, None, None), False)

    (n_rows, n_cols, mtype), ok = Dialog.get_matrix_def(parent)
    if ok:
        row_code = r'{}' + r'&{}'*(n_cols-1) + r'\\'
        latex_code = r'\begin{{' + mtype + r'}}' + row_code*n_rows \
                     + r'\end{{' + mtype + r'}}'
        return Op(n_rows*n_cols, latex_code)
    else:
        return None

def cases(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Cases')
            label = QLabel('Number of cases:')
            self.ledit = QLineEdit()
            regexp = QRegExp('^[1-9]$')
            self.validator = QRegExpValidator(regexp)
            self.ledit.setValidator(self.validator)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label)
            vbox.addWidget(self.ledit)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit.setFocus()

            self.ledit.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        def check_state(self, *args, **kargs):
            state = self.validator.validate(self.ledit.text(), 0)[0]
            if state == QValidator.Acceptable:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)

        @staticmethod
        def get_n_cases(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (int(dialog.ledit.text()), True)
            else:
                return (None, False)
            
    n_cases, ok = Dialog.get_n_cases(parent)
    if ok:
        case_code = r'{}&{}\\'
        latex_code = r'\begin{{cases}}' + case_code*n_cases + r'\end{{cases}}'
        return Op(n_cases*2, latex_code)
    else:
        return None

def equation_system(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('Equation system')
            label = QLabel('Number of equations:')
            self.ledit = QLineEdit()
            regexp = QRegExp('^[1-9]$')
            self.validator = QRegExpValidator(regexp)
            self.ledit.setValidator(self.validator)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label)
            vbox.addWidget(self.ledit)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit.setFocus()

            self.ledit.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        def check_state(self, *args, **kargs):
            state = self.validator.validate(self.ledit.text(), 0)[0]
            if state == QValidator.Acceptable:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)

        @staticmethod
        def get_n_equations(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return (int(dialog.ledit.text()), True)
            else:
                return (None, False)
            
    n_equations, ok = Dialog.get_n_equations(parent)
    if ok:
        case_code = r'{}\\'
        latex_code = r'\begin{{cases}}' + case_code*n_equations \
                     + r'\end{{cases}}'
        return Op(n_equations, latex_code)
    else:
        return None

def array(parent):
    class Dialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setWindowTitle('General Array')
            label_rows = QLabel('Number of rows:')
            self.ledit_rows = QLineEdit()
            label_cols = QLabel('Number of columns:')
            self.ledit_cols = QLineEdit()
            regexp = QRegExp('^[1-9]$')
            self.validator = QRegExpValidator(regexp)
            self.ledit_rows.setValidator(self.validator)
            self.ledit_cols.setValidator(self.validator)
            label_align = QLabel('Alignment of columns (eg. lc|r):\n'+
                                 '(l: left, c: center, r: right, |: v. line)')
            self.ledit_align = QLineEdit()
            label_l = QLabel('Left delimiter:')
            self.combo_l = QComboBox()
            self.combo_l.setIconSize(self.combo_l.minimumSizeHint())
            for delim in SINGLEDELIMITERS:
                self.combo_l.addItem(QIcon(os.path.join(dirs.SYMBOLS_DIR,
                                                        delim.tag + '.png')),
                                     '')
            label_r = QLabel('Right delimiter:')
            self.combo_r = QComboBox()
            self.combo_r.setIconSize(self.combo_l.minimumSizeHint())
            for delim in SINGLEDELIMITERS:
                self.combo_r.addItem(QIcon(os.path.join(dirs.SYMBOLS_DIR,
                                                        delim.tag + '.png')),
                                     '')
            self.combo_r.setCurrentIndex(1)
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            vbox = QVBoxLayout(self)
            vbox.addWidget(label_rows)
            vbox.addWidget(self.ledit_rows)
            vbox.addWidget(label_cols)
            vbox.addWidget(self.ledit_cols)
            vbox.addWidget(label_align)
            vbox.addWidget(self.ledit_align)
            vbox.addWidget(label_l)
            vbox.addWidget(self.combo_l)
            vbox.addWidget(label_r)
            vbox.addWidget(self.combo_r)
            vbox.addWidget(self.buttons)
            self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)
            self.ledit_align.setDisabled(True)
            self.ledit_rows.setFocus()

            self.ledit_rows.textChanged.connect(self.check_state)
            self.ledit_cols.textChanged.connect(self.check_state)
            self.ledit_align.textChanged.connect(self.check_state)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

        def check_state(self, *args, **kargs):
            state1 = self.validator.validate(self.ledit_rows.text(), 0)[0]
            state2 = self.validator.validate(self.ledit_cols.text(), 0)[0]
            if state2 == QValidator.Acceptable:
                self.ledit_align.setEnabled(True)
                n_cols = self.ledit_cols.text()
                regexp = QRegExp("^" + "(\\|*[lcr]\\|*){" + n_cols + '}' + "$")
                val_align = QRegExpValidator(regexp)
                self.ledit_align.setValidator(val_align)
                state3 = val_align.validate(self.ledit_align.text(), 0)[0]
            else:
                self.ledit_align.setDisabled(True)
                state3 = QValidator.Invalid
            if state1 == state2 == state3 == QValidator.Acceptable:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(True)

        @staticmethod
        def get_array(parent=None):
            dialog = Dialog(parent)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                return ((int(dialog.ledit_rows.text()),
                         int(dialog.ledit_cols.text()),
                         SINGLEDELIMITERS[dialog.combo_l.currentIndex()].code,
                         SINGLEDELIMITERS[dialog.combo_r.currentIndex()].code,
                         dialog.ledit_align.text()),
                        True)
            else:
                return ((None, None, None, None, None), False)

    (n_rows, n_cols, delim_l, delim_r, align), ok = Dialog.get_array(parent)
    if ok:
        row_code = r'{}' + r'&{}'*(n_cols-1) + r'\\'
        latex_code = r'\left' + delim_l \
                     + r'\begin{{array}}' \
                     + '{{' + align + '}}' \
                     + row_code*n_rows \
                     + r'\end{{array}}' \
                     + r'\right' + delim_r
        return Op(n_rows*n_cols, latex_code)
    else:
        return None
   

MANYLINES = [
    LatexSymb('matrix_type', matrix_type,
                r"\begin{pmatrix}\cdots&\square\\\square&\square\end{pmatrix}"),
    LatexSymb('cases', cases,
              r'\begin{cases}\cdots &\text{if }x>0\\b&\text{ow.}\end{cases}'),
    LatexSymb('equations_system', equation_system,
                          r'\begin{cases}\cdots\\x-y=8\end{cases}'),
    LatexSymb('array', array,
              r'\left(\begin{array}{l|r}\cdots&\square\\\square&\square\end{array}\right]')
]

MENUITEMSDATA.append(MenuItemData(
    tag="tab_manylines",
    symb_l=MANYLINES,
    clickable_size=(190, 90), dpi=200,
    expr=r'\begin{smallmatrix}a&b\\c&d\end{smallmatrix}'))

ACCENTS = [
    LatexSymb('dot', Op(1, r'\dot{{{0}}}'), r'\dot{{{\cdot}}}'),
    LatexSymb('ddot', Op(1, r'\ddot{{{0}}}'), r'\ddot{{{\cdot}}}'),
    LatexSymb('dddot', Op(1, r'\dddot{{{0}}}'), r'\dddot{{{\cdot}}}'),
    LatexSymb('acute', Op(1, r'\acute{{{0}}}'), r'\acute{{{\cdot}}}'),
    LatexSymb('breve', Op(1, r'\breve{{{0}}}'), r'\breve{{{\cdot}}}'),
    LatexSymb('grave', Op(1, r'\grave{{{0}}}'), r'\grave{{{\cdot}}}'),
    LatexSymb('tilde', Op(1, r'\tilde{{{0}}}'), r'\tilde{{{\cdot}}}'),
    LatexSymb('bar', Op(1, r'\bar{{{0}}}'), r'\bar{{{\cdot}}}'),
    LatexSymb('check', Op(1, r'\check{{{0}}}'), r'\check{{{\cdot}}}'),
    LatexSymb('hat', Op(1, r'\hat{{{0}}}'), r'\hat{{{\cdot}}}'),
    LatexSymb('vec', Op(1, r'\vec{{{0}}}'), r'\vec{{{\cdot}}}'),
    LatexSymb('imath', r'\imath', r'\imath'),
    LatexSymb('jmath', r'\jmath', r'\jmath'),
    LatexSymb('ell', r'\ell', r'\ell'),
    LatexSymb('hbar', r'\hbar', r'\hbar'),
    LatexSymb('eth', r'\eth', r'\eth'),
]

MENUITEMSDATA.append(MenuItemData(
    tag="tab_accents",
    symb_l=ACCENTS, clickable_size=(40, 30), dpi=200,
    expr=r'\acute{{a}}\;\tilde{{B}}'))

LSUB = Op(2, r'{{}}_{{{1}}}{0}')
SUB = Op(2, r'{0}_{{{1}}}')
SUP = Op(2, r'{0}^{{{1}}}')
LSUP = Op(2, r'{{}}^{{{1}}}{0}')
LSUBSUB = Op(3, r'{{}}_{{{1}}}{0}_{{{2}}}')
SUBSUP = Op(3, r'{0}_{{{1}}}^{{{2}}}')
SUPLSUP = Op(3, r'{{}}^{{{2}}}{0}^{{{1}}}')
LSUBLSUP = Op(3, r'{{}}_{{{1}}}^{{{2}}}{0}')
LSUBSUP = Op(3, r'{{}}_{{{1}}}{0}^{{{2}}}')
SUBLSUP = Op(3, r'{{}}^{{{2}}}{0}_{{{1}}}')
LSUBSUBSUP = Op(4, r'{{}}_{{{1}}}{0}^{{{3}}}_{{{2}}}')
LSUBSUBLSUP = Op(4, r'{{}}_{{{1}}}^{{{3}}}{0}_{{{2}}}')
LSUBSUPLSUP = Op(4, r'{{}}^{{{3}}}_{{{1}}}{0}^{{{2}}}')
SUBSUPLSUP = Op(4, r'{{}}^{{{3}}}{0}^{{{2}}}_{{{1}}}')
LSUBSUBSUPLSUP = Op(5, r'{{}}_{{{1}}}^{{{4}}}{0}_{{{2}}}^{{{3}}}')

# First elements are the most common
INDEX_OPS = [
    SUP, SUB, SUBSUP, LSUP, LSUB,
    LSUBSUB, SUPLSUP, LSUBLSUP, LSUBSUP, SUBLSUP,
    LSUBSUBSUP, LSUBSUBLSUP, LSUBSUPLSUP, SUBSUPLSUP,
    LSUBSUBSUPLSUP,
]

#INDICES = [
#    LatexSymb('lsub', LSUB, r'{{}}_{{\square}}\cdot'),
#    LatexSymb('sub', SUB, r'\cdot_{{\square}}'),
#    LatexSymb('super', SUP, r'\cdot^{{\square}}'),
#    LatexSymb('lsup', LSUP, r'{{}}^{{\square}}\cdot'),
#    LatexSymb('lsubsub', LSUBSUB, r'{{}}_{{\square}}\cdot_{{\square}}'),
#    LatexSymb('subsup', SUBSUP, r'\cdot^{{\square}}_{{\square}}'),
#    LatexSymb('suplsup', SUPLSUP, r'{{}}^{{\square}}\cdot^{{\square}}'),
#    LatexSymb('lsublsup', LSUBLSUP, r'{{}}^{{\square}}_{{\square}}\cdot'),
#    LatexSymb('lsubsup', LSUBSUP, r'{{}}_{{\square}}\cdot^{{\square}}'),
#    LatexSymb('sublsup', SUBLSUP, r'{{}}^{{\square}}\cdot_{{\square}}'),
#    LatexSymb('lsubsubsup', LSUBSUBSUP,
#              r'{{}}_{{\square}}\cdot^{{\square}}_{{\square}}'),
#    LatexSymb('lsubsublsup', LSUBSUBLSUP,
#              r'{{}}_{{\square}}^{{\square}}\cdot_{{\square}}'),
#    LatexSymb('lsubsuplsup', LSUBSUPLSUP,
#              r'{{}}^{{\square}}_{{\square}}\cdot^{{\square}}'),
#    LatexSymb('subsuplsup', SUBSUPLSUP,
#              r'{{}}^{{\square}}\cdot^{{\square}}_{{\square}}'),
#    LatexSymb('lsubsubsuplsup', LSUBSUBSUPLSUP,
#              r'{{}}^{{\square}}_{{\square}}\cdot^{{\square}}_{{\square}}'),
#]

#    ('binomial', (Op(2, r'\binom{{{0}}}{{{1}}}'),
#     [r'\binom{{\cdot}}{{\square}}'])),

#MENUITEMSDATA.append(MenuItemData(
#    tag="tab_indices",
#    symb_l=INDICES, clickable_size=(60, 60), dpi=200, expr=r'a^b'))
