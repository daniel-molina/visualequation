#  visualequation is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  visualequation is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

from visualequation.eqlib.ops import *


DICT = {
    'overline': (r'\overline{{{0}}}', 1),
    'underline': (r'\underline{{{0}}}', 1),
    'widehat': (r'\widehat{{{0}}}', 1),
    'widetilde': (r'\widetilde{{{0}}}', 1),
    'overrightarrow': (r'\overrightarrow{{{0}}}', 1),
    'overleftarrow': (r'\overleftarrow{{{0}}}', 1),
    'overleftrightarrow': (r'\overleftrightarrow{{{0}}}', 1),
    'underrightarrow': (r'\underrightarrow{{{0}}}', 1),
    'underleftarrow': (r'\underleftarrow{{{0}}}', 1),
    'underleftrightarrow': (r'\underleftrightarrow{{{0}}}', 1),
    'xrightarrow': (r'\xrightarrow[{{{1}}}]{{{0}}}', 2),
    'xleftarrow': (r'\xleftarrow[{{{1}}}]{{{0}}}', 2),
    'overbrace': (r'\overbrace{{{0}}}', 1),
    'underbrace': (r'\underbrace{{{0}}}', 1),
}


class MathConstruct(Op):
    def __init__(self, name, **kwargs):
        if not isinstance(name, str):
            raise TypeError("Parameter name must be a str.")
        if name not in DICT:
            raise ValueError("Parameter name not present in database.")

        latex, n_args = DICT[name]
        lo_base = name in ("overbrace", "underbrace")
        super().__init__(latex, n_args, lo_base=lo_base, **kwargs)
        self._vertical = name in ("xrightarrow", "xleftarrow")

    def rstep(self, arg_ord: Optional[int] = None):
        self._assert_valid_args(arg_ord)
        if arg_ord is None:
            return 1
        return None

    def lstep(self, arg_ord: Optional[int] = None):
        return self.rstep(arg_ord)

    def ustep(self, arg_ord: Optional[int], selmode: SelMode):
        self._assert_valid_args(arg_ord, selmode)
        if self._vertical and arg_ord == 2:
            return 1
        return None

    def dstep(self, arg_ord: Optional[int], selmode: SelMode):
        self._assert_valid_args(arg_ord, selmode)
        if self._vertical and arg_ord == 1:
            return 2
        return None

    @classmethod
    def from_json(cls, dct):
        return cls(dct["w"], pp=dct["pp"])

    def to_json(self):
        return dict(
            cls="MC", pp=self.pp.to_json(),
            w=next(k for k, v in DICT.items() if v[0] == self._latex_code))
