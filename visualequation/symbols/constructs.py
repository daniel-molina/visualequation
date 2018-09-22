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
    LatexSymb('frac', Op(2, r'\frac{{{0}}}{{{1}}}'),
              r'\frac{\cdots}{\square}'),
    LatexSymb('sqrt', Op(1, r'\sqrt{{{0}}}'), r'\sqrt{\cdots}'),
    LatexSymb('nsqrt', Op(2, r'\sqrt[{1}]{{{0}}}'), r'\sqrt[\square]{\cdots}'),
    LatexSymb('overline', Op(1, r'\overline{{{0}}}'), r'\overline\cdots'),
    LatexSymb('underline', Op(1, r'\underline{{{0}}}'), r'\underline\cdots'),
    LatexSymb('widehat', Op(1, r'\widehat{{{0}}}'), r'\widehat\cdots'),
    LatexSymb('widetilde', Op(1, r'\widetilde{{{0}}}'), r'\widetilde\cdots'),
    LatexSymb('overrightarrow', Op(1, r'\overrightarrow{{{0}}}'),
              r'\overrightarrow\cdots'),
    LatexSymb('overleftarrow', Op(1, r'\overleftarrow{{{0}}}'),
              r'\overleftarrow\cdots'),
    LatexSymb('overleftrightarrow', Op(1, r'\overleftrightarrow{{{0}}}'),
              r'\overleftrightarrow\cdots'),
    LatexSymb('underrightarrow', Op(1, r'\underrightarrow{{{0}}}'),
              r'\underrightarrow\cdots'),
    LatexSymb('underleftarrow', Op(1, r'\underleftarrow{{{0}}}'),
              r'\underleftarrow\cdots'),
    LatexSymb('underleftrightarrow', Op(1, r'\underleftrightarrow{{{0}}}'),
              r'\underleftrightarrow\cdots'),
    LatexSymb('xrightarrow', Op(2, r'\xrightarrow[{0}]{{{1}}}'),
              r'\xrightarrow[\cdots]{{\square}}'),
    LatexSymb('xleftarrow', Op(2, r'\xleftarrow[{0}]{{{1}}}'),
              r'\xleftarrow[\cdots]{{\square}}'),
    LatexSymb('overbrace1', Op(1, r'\overbrace{{{0}}}'), r'\overbrace\cdots'),
    LatexSymb('underbrace1', Op(1, r'\underbrace{{{0}}}'),
              r'\underbrace\cdots'),
    LatexSymb('overbrace2', Op(2, r'\overbrace{{{0}}}^{{{1}}}'),
              r'\overbrace{\cdots}^\square'),
    LatexSymb('underbrace2', Op(2, r'\underbrace{{{0}}}_{{{1}}}'),
              r'\underbrace{\cdots}_\square'),
    LatexSymb('overset', Op(2, r'\overset{{{1}}}{{{0}}}'),
              r'\overset{{{\square}}}{{{\cdot}}}'),
    LatexSymb('underset', Op(2, r'\underset{{{1}}}{{{0}}}'),
              r'\underset{{{\square}}}{{{\cdot}}}'),
]
