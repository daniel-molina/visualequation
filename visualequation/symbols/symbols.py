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
    Symbol('alpha', r'\alpha'),
    Symbol('beta', r'\beta'),
    Symbol('gamma', r'\gamma'),
    Symbol('digamma', r'\digamma'),
    Symbol('delta', r'\delta'),
    Symbol('epsilon', r'\epsilon'),
    Symbol('zeta', r'\zeta'),
    Symbol('eta', r'\eta'),
    Symbol('theta', r'\theta'),
    Symbol('iota', r'\iota'),
    Symbol('kappa', r'\kappa'),
    Symbol('lambda', r'\lambda'),
    Symbol('mu', r'\mu'),
    Symbol('nu', r'\nu'),
    Symbol('xi', r'\xi'),
    Symbol('pi', r'\pi'),
    Symbol('rho', r'\rho'),
    Symbol('sigma', r'\sigma'),
    Symbol('tau', r'\tau'),
    Symbol('upsilon', r'\upsilon'),
    Symbol('phi', r'\phi'),
    Symbol('chi', r'\chi'),
    Symbol('psi', r'\psi'),
    Symbol('omega', r'\omega'),
]

UPPER_GREEK = [
    Symbol('uppergamma', r'\Gamma'),
    Symbol('upperdelta', r'\Delta'),
    Symbol('uppertheta', r'\Theta'),
    Symbol('upperlambda', r'\Lambda'),
    Symbol('upperxi', r'\Xi'),
    Symbol('upperpi', r'\Pi'),
    Symbol('uppersigma', r'\Sigma'),
    Symbol('upperupsilon', r'\Upsilon'),
    Symbol('upperphi', r'\Phi'),
    Symbol('upperpsi', r'\Psi'),
    Symbol('upperomega', r'\Omega'),
]

VAR_GREEK = [
    Symbol('varepsilon', r'\varepsilon'),
    Symbol('vartheta', r'\vartheta'),
    Symbol('varkappa', r'\varkappa'),
    Symbol('varrho', r'\varrho'),
    Symbol('varsigma', r'\varsigma'),
    Symbol('varphi', r'\varphi'),
    Symbol('varpi', r'\varpi'),
]

HEBREW = [
    Symbol('aleph', r'\aleph'),
    Symbol('beth', r'\beth'),
    Symbol('daleth', r'\daleth'),
    Symbol('gimel', r'\gimel'),
]

SYMBOLS1 = [
    Symbol('infty', r'\infty'),
    Symbol('emptyset', r'\emptyset'),
    Symbol('varnothing', r'\varnothing'),
    Symbol('dagger', r'\dagger'),
    Symbol('ddagger', r'\ddagger'),
    Symbol('wr', r'\wr'),
    Symbol('clubsuit', r'\clubsuit'),
    Symbol('diamondsuit', r'\diamondsuit'),
    Symbol('heartsuit', r'\heartsuit'),
    Symbol('spadesuit', r'\spadesuit'),
    Symbol('pounds', r'\pounds'),
    Symbol('upperp', r'\P'),
    Symbol('uppers', r'\S'),
]
