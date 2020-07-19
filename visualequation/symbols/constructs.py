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

MATHCONSTRUCTS = [
    PanelIcon('frac', Op(2, r'\frac{{{0}}}{{{1}}}')),
    PanelIcon('sqrt', Op(1, r'\sqrt{{{0}}}')),
    PanelIcon('nsqrt', Op(2, r'\sqrt[{{{1}}}]{{{0}}}')),
    PanelIcon('overline', Op(1, r'\overline{{{0}}}')),
    PanelIcon('underline', Op(1, r'\underline{{{0}}}')),
    PanelIcon('widehat', Op(1, r'\widehat{{{0}}}')),
    PanelIcon('widetilde', Op(1, r'\widetilde{{{0}}}')),
    PanelIcon('overrightarrow', Op(1, r'\overrightarrow{{{0}}}')),
    PanelIcon('overleftarrow', Op(1, r'\overleftarrow{{{0}}}')),
    PanelIcon('overleftrightarrow', Op(1, r'\overleftrightarrow{{{0}}}')),
    PanelIcon('underrightarrow', Op(1, r'\underrightarrow{{{0}}}')),
    PanelIcon('underleftarrow', Op(1, r'\underleftarrow{{{0}}}')),
    PanelIcon('underleftrightarrow', Op(1, r'\underleftrightarrow{{{0}}}')),
    PanelIcon('xrightarrow', Op(2, r'\xrightarrow[{{{0}}}]{{{1}}}')),
    PanelIcon('xleftarrow', Op(2, r'\xleftarrow[{{{0}}}]{{{1}}}')),
    PanelIcon('overbrace', Op(1, r'\overbrace{{{0}}}', 'opconstruct')),
    PanelIcon('underbrace', Op(1, r'\underbrace{{{0}}}', 'opconstruct')),
]
