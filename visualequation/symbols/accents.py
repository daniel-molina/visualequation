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
    PanelIcon('dot', Op(1, r'\dot{{{0}}}')),
    PanelIcon('ddot', Op(1, r'\ddot{{{0}}}')),
    PanelIcon('dddot', Op(1, r'\dddot{{{0}}}')),
    PanelIcon('acute', Op(1, r'\acute{{{0}}}')),
    PanelIcon('breve', Op(1, r'\breve{{{0}}}')),
    PanelIcon('grave', Op(1, r'\grave{{{0}}}')),
    PanelIcon('tilde', Op(1, r'\tilde{{{0}}}')),
    PanelIcon('bar', Op(1, r'\bar{{{0}}}')),
    PanelIcon('check', Op(1, r'\check{{{0}}}')),
    PanelIcon('hat', Op(1, r'\hat{{{0}}}')),
    PanelIcon('vec', Op(1, r'\vec{{{0}}}')),
    PanelIcon('imath', r'\imath'),
    PanelIcon('jmath', r'\jmath'),
    PanelIcon('ell', r'\ell'),
    PanelIcon('hbar', r'\hbar'),
    PanelIcon('eth', r'\eth'),
]
