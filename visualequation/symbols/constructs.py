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
    LatexSymb('frac', Op(2, r'\frac{{{0}}}{{{1}}}')),
    LatexSymb('sqrt', Op(1, r'\sqrt{{{0}}}')),
    LatexSymb('nsqrt', Op(2, r'\sqrt[{{{1}}}]{{{0}}}')),
    LatexSymb('overline', Op(1, r'\overline{{{0}}}')),
    LatexSymb('underline', Op(1, r'\underline{{{0}}}')),
    LatexSymb('widehat', Op(1, r'\widehat{{{0}}}')),
    LatexSymb('widetilde', Op(1, r'\widetilde{{{0}}}')),
    LatexSymb('overrightarrow', Op(1, r'\overrightarrow{{{0}}}')),
    LatexSymb('overleftarrow', Op(1, r'\overleftarrow{{{0}}}')),
    LatexSymb('overleftrightarrow', Op(1, r'\overleftrightarrow{{{0}}}')),
    LatexSymb('underrightarrow', Op(1, r'\underrightarrow{{{0}}}')),
    LatexSymb('underleftarrow', Op(1, r'\underleftarrow{{{0}}}')),
    LatexSymb('underleftrightarrow', Op(1, r'\underleftrightarrow{{{0}}}')),
    LatexSymb('xrightarrow', Op(2, r'\xrightarrow[{{{0}}}]{{{1}}}')),
    LatexSymb('xleftarrow', Op(2, r'\xleftarrow[{{{0}}}]{{{1}}}')),
    LatexSymb('overbrace1', Op(1, r'\overbrace{{{0}}}', 'opconstruct')),
    LatexSymb('underbrace1', Op(1, r'\underbrace{{{0}}}', 'opconstruct')),
    LatexSymb('overbrace2',
              Op(2, r'\overbrace{{{0}}}^{{{1}}}', 'opconstruct')),
    LatexSymb('underbrace2',
              Op(2, r'\underbrace{{{0}}}_{{{1}}}', 'opconstruct')),
    LatexSymb('overset', Op(2, r'\overset{{{1}}}{{{0}}}')),
    LatexSymb('underset', Op(2, r'\underset{{{1}}}{{{0}}}')),
]
