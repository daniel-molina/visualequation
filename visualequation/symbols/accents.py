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

ACCENTS = [
    LatexSymb('dot', Op(1, r'\dot{{{0}}}')),
    LatexSymb('ddot', Op(1, r'\ddot{{{0}}}')),
    LatexSymb('dddot', Op(1, r'\dddot{{{0}}}')),
    LatexSymb('acute', Op(1, r'\acute{{{0}}}')),
    LatexSymb('breve', Op(1, r'\breve{{{0}}}')),
    LatexSymb('grave', Op(1, r'\grave{{{0}}}')),
    LatexSymb('tilde', Op(1, r'\tilde{{{0}}}')),
    LatexSymb('bar', Op(1, r'\bar{{{0}}}')),
    LatexSymb('check', Op(1, r'\check{{{0}}}')),
    LatexSymb('hat', Op(1, r'\hat{{{0}}}')),
    LatexSymb('vec', Op(1, r'\vec{{{0}}}')),
    LatexSymb('imath', r'\imath'),
    LatexSymb('jmath', r'\jmath'),
    LatexSymb('ell', r'\ell'),
    LatexSymb('hbar', r'\hbar'),
    LatexSymb('eth', r'\eth'),
]
