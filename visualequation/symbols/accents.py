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
from visualequation.eqlib.ops import *

ACCENTS = [
    PanelIcon('dot', Op(r'\dot{{{0}}}', 1)),
    PanelIcon('ddot', Op(r'\ddot{{{0}}}', 1)),
    PanelIcon('dddot', Op(r'\dddot{{{0}}}', 1)),
    PanelIcon('acute', Op(r'\acute{{{0}}}', 1)),
    PanelIcon('breve', Op(r'\breve{{{0}}}', 1)),
    PanelIcon('grave', Op(r'\grave{{{0}}}', 1)),
    PanelIcon('tilde', Op(r'\tilde{{{0}}}', 1)),
    PanelIcon('bar', Op(r'\bar{{{0}}}', 1)),
    PanelIcon('check', Op(r'\check{{{0}}}', 1)),
    PanelIcon('hat', Op(r'\hat{{{0}}}', 1)),
    PanelIcon('vec', Op(r'\vec{{{0}}}', 1)),
    PanelIcon('imath', r'\imath'),
    PanelIcon('jmath', r'\jmath'),
    PanelIcon('ell', r'\ell'),
    PanelIcon('hbar', r'\hbar'),
    PanelIcon('eth', r'\eth'),
]
