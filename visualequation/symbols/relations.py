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

from .utils import *

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
