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
    LatexSymb('boxdot', r'\boxdot', r'\boxdot'),
    LatexSymb('boxminus', r'\boxminus', r'\boxminus'),
    LatexSymb('boxplus', r'\boxplus', r'\boxplus'),
    LatexSymb('boxtimes', r'\boxtimes', r'\boxtimes'),
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
