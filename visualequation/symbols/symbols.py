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
