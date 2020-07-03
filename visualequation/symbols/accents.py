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
    Symbol('dot', Op(1, r'\dot{{{0}}}')),
    Symbol('ddot', Op(1, r'\ddot{{{0}}}')),
    Symbol('dddot', Op(1, r'\dddot{{{0}}}')),
    Symbol('acute', Op(1, r'\acute{{{0}}}')),
    Symbol('breve', Op(1, r'\breve{{{0}}}')),
    Symbol('grave', Op(1, r'\grave{{{0}}}')),
    Symbol('tilde', Op(1, r'\tilde{{{0}}}')),
    Symbol('bar', Op(1, r'\bar{{{0}}}')),
    Symbol('check', Op(1, r'\check{{{0}}}')),
    Symbol('hat', Op(1, r'\hat{{{0}}}')),
    Symbol('vec', Op(1, r'\vec{{{0}}}')),
    Symbol('imath', r'\imath'),
    Symbol('jmath', r'\jmath'),
    Symbol('ell', r'\ell'),
    Symbol('hbar', r'\hbar'),
    Symbol('eth', r'\eth'),
]
